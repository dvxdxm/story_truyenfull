import scrapy


class Author(scrapy.Item):
    author_id = scrapy.Field()
    user_id = scrapy.Field()
    author_name = scrapy.Field()
    author_nickname = scrapy.Field()
    avatar = scrapy.Field()
    dob = scrapy.Field()
    dead_year = scrapy.Field()
    created_by = scrapy.Field()
    created_on = scrapy.Field()
    modified_by = scrapy.Field()
    modified_on = scrapy.Field()
    is_deleted = scrapy.Field()
