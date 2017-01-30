import scrapy
import os

import GroeneScrapy.settings as settings
from GroeneScrapy.items import GroeneNummer

class PdfSpider(scrapy.Spider):
    name = "pdfspider"
    allowed_domains = ["www.groene.nl"]
    start_urls = ["https://www.groene.nl/accounts/inloggen"]
    
    def parse(self, response):
        return scrapy.FormRequest.from_response(
            response,
            formnumber = 1,
            method="post",
            formdata={
                      'customer[email]': settings.GROENE_USERNAME,
                      'customer[password]': settings.GROENE_PASSWORD
                     },
            callback=self.after_login
        )

    def after_login(self, response):
        if "Ongeldig e-mailadres of wachtwoord." in response.body:
            print "ERROR: Login failed"
            return
        editionPageRequest = scrapy.Request("https://www.groene.nl/nieuwste-editie", callback = self.edition_page)
        yield editionPageRequest

    def edition_page(self, response):
        for sel in response.xpath("//a[.='Download pdf']/@href"):
            item = GroeneNummer()
            relUrl = response.url
            item['jaar'] = relUrl.split('/')[-2]
            item['weeknummer']  = relUrl.split('/')[-1]
            pdfRequest = scrapy.Request("https://www.groene.nl" + sel.extract(), callback = self.download_pdf)
            pdfRequest.meta['item'] = item
            yield pdfRequest

    def download_pdf(self, response):
        item = response.meta['item']
        with open(os.path.join(settings.GROENE_PDF_PATH, item['jaar'] + "-" + item['weeknummer'].zfill(2) + ".pdf"), 'w') as f:
            f.write(response.body)
