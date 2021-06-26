import scrapy


class Category(scrapy.Item):
    category_id = scrapy.Field()
    category_name = scrapy.Field()
    created_by = scrapy.Field()
    created_on = scrapy.Field()
    modified_by = scrapy.Field()
    modified_on = scrapy.Field()
    is_deleted = scrapy.Field()
