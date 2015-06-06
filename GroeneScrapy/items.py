import scrapy

class GroeneNummer(scrapy.Item):
    weeknummer = scrapy.Field()
    jaar = scrapy.Field()
