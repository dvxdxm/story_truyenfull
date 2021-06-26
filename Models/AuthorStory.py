import scrapy


class AuthorStory(scrapy.Item):
    story_id = scrapy.Field()
    author_id = scrapy.Field()
    percent = scrapy.Field()
    created_by = scrapy.Field()
    created_on = scrapy.Field()
    modified_by = scrapy.Field()
    modified_on = scrapy.Field()
    is_deleted = scrapy.Field()