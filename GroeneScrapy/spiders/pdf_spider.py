import scrapy
import os

import GroeneScrapy.settings as settings
from GroeneScrapy.items import GroeneNummer

class PdfSpider(scrapy.Spider):
    name = "pdfspider"
    allowed_domains = ["www.groene.nl"]
    start_urls = ["https://www.groene.nl/home"]
    
    def parse(self, response):
        return scrapy.FormRequest.from_response(
            response,
            url="https://www.groene.nl/gebruiker/inloggen",
            method="post",
            formdata={
                      'user[email]': settings.GROENE_USERNAME, 
                      'user[password]': settings.GROENE_PASSWORD
                     },
            callback=self.after_login
        )

    def after_login(self, response):
        if "E-mailadres en/of wachtwoord is onjuist." in response.body:
            print "ERROR: Login failed"
            return
        for sel in response.xpath("/html/body/div[@id='loggedin-tooltip']/ul/li[a='Download pdf']/a/@href"):
            item = GroeneNummer()
            relUrl = sel.extract()
            item['jaar'] = relUrl.split('/')[1]
            item['weeknummer'] = relUrl.split('/')[2].split('.')[0]
            pdfRequest = scrapy.Request("https://www.groene.nl" + relUrl, callback = self.download_pdf)
            pdfRequest.meta['item'] = item
            yield pdfRequest
    
    def download_pdf(self, response):
        item = response.meta['item']
        with open(os.path.join(settings.GROENE_PDF_PATH, item['jaar'] + "-" + item['weeknummer'] + ".pdf"), 'w') as f:
            f.write(response.body)
