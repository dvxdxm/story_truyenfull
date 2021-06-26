import scrapy


class Chapter(scrapy.Item):
    chapter_id = scrapy.Field()
    story_id = scrapy.Field()
    author_id = scrapy.Field()
    translator_id = scrapy.Field()
    cost = scrapy.Field()
    chapter_no = scrapy.Field()
    chapter_title = scrapy.Field()
    content = scrapy.Field()
    origin_chapter_id = scrapy.Field()
    status = scrapy.Field()
    created_by = scrapy.Field()
    created_on = scrapy.Field()
    modified_by = scrapy.Field()
    modified_on = scrapy.Field()
    is_deleted = scrapy.Field()
    collection_name = scrapy.Field()
    story_name = scrapy.Field()
    sort_number = scrapy.Field()
    dealer_id = scrapy.Field()
    slug = scrapy.Field()