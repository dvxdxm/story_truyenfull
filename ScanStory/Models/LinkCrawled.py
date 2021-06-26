import scrapy


class LinkCrawl(scrapy.Item):
    story_name = scrapy.Field()
    link = scrapy.Field()
    crawled = scrapy.Field()
    created_on = scrapy.Field()
    created_by = scrapy.Field()
    modified_on = scrapy.Field()
    modified_by = scrapy.Field()
    is_deleted = scrapy.Field()
    hidden = scrapy.Field()
    collection_name = scrapy.Field()
