import datetime
import scrapy
from ScanStory.Models.Story import Story
from ScanStory.Models.Chapter import Chapter
from slugify import slugify


def download_image_to_link(link):
    yield scrapy.Request(link)


def response_list_chapters(response, story_name, sort):
    list_urls_chapter = response.xpath('//ul[contains(@class, "list-chapter")]//a/@href').getall()
    if len(list_urls_chapter) > 0:

        for link_url in list_urls_chapter:
            sort += 1
            # print(f"Count item: {sort}")
            yield request_get_content_of_chapter(link_url, story_name, sort)


def request_get_content_story(link):
    request = scrapy.Request(link, callback=get_content_story_to_url, cb_kwargs=dict(link=link))
    return request


def request_get_content_of_chapter(link, story_name, sort):

    request = scrapy.Request(link, callback=get_content_chapter, cb_kwargs=dict(story_name=story_name, sort=sort))
    return request


def get_content_chapter(response, story_name, sort):
    item = Chapter()
    content = response.xpath('//div[@id="chapter-c" and not(contains(@class, "ads-network"))]').get()

    chapter_title = response.xpath('//a[contains(@class, "chapter-title")]/@title').get()
    text_replace = story_name + " - "
    text_after_replace = chapter_title.replace(f"{text_replace}", "")
    index_number_chapter = text_after_replace.index(":", 0)
    # print(f"Index : {index_number_chapter}")
    page_title_sort = text_after_replace[:index_number_chapter]
    # print(f"Chương : {page_title_sort}")
    sort_new_value = page_title_sort.replace('Chương ', '')
    # print(f"Count Item: {sort_new_value}")
    # if sort_new_value is None:
    #     sort_new_value
    item['content'] = content
    item["collection_name"] = 'chapter'
    item["chapter_title"] = text_after_replace
    item["story_name"] = story_name
    item['created_by'] = "admin"
    item['created_on'] = datetime.datetime.now()
    item['modified_on'] = datetime.datetime.now()
    item['modified_by'] = "admin"
    item['story_id'] = ""
    item['sort_number'] = int(sort_new_value)
    item["slug"] = slugify(text_after_replace).lower()
    item["dealer_id"] = '08d92f17-4e75-4be2-84ba-522e9cc87468'
    yield item


def get_content_story_to_url(response, link):
    item = Story()
    avatarPath = response.xpath('//div[contains(@class,"book")]//img/@src').get()
    story_name = response.xpath('//h3[contains(@class,"title")]/text()').get()
    description = response.xpath('//div[contains(@class, "desc-text desc-text-full") or contains(@class, "desc-text")]').get()
    source = response.xpath('//span[contains(@class, "source")]/text()').get()
    status = response.xpath('//span[contains(@class, "text-primary")]/text()').get()
    author = response.xpath('//div[contains(@class, "info")]//a[contains(@itemprop, "author")]/text()').get()
    genre = response.xpath('//div[contains(@class, "info")]//a[contains(@itemprop, "genre")]/text()').getall()
    keywords = response.xpath('//meta[contains(@name, "keywords")]/@content').get()
    description_seo = response.xpath('//meta[contains(@name, "description")]/@content').get()
    # get cac chapter o page 1 theo title
    # list_chapter = response.xpath('//ul[contains(@class, "list-chapter")]//a/@title').getall()
    # get cac chapter o page 1
    list_urls_chapter = response.xpath('//ul[contains(@class, "list-chapter")]//a/@href').getall()
    # check story co nhieu chapters hay khoong?
    last_page_text = response.xpath('//ul[contains(@class, "pagination")]//li[not(contains(@class,"active"))]//a[text('
                                    ')="Cuối "]/@title').get()
    sort_index = 0

    if len(list_urls_chapter) > 0:
        for link_url in list_urls_chapter:
            sort_index = sort_index + 1
            yield request_get_content_of_chapter(link_url, story_name, sort_index)

    if last_page_text:
        text_replace_page = story_name + " - Trang "
        replace_last_page_text = last_page_text.replace(text_replace_page, "")
        if int(replace_last_page_text) > 0:
            for index in range(int(replace_last_page_text)):
                link_to_page = link + "trang-" + str(index+1)
                sort = 50*index
                print(f"sort item: {sort}")
                yield scrapy.Request(link_to_page, callback=response_list_chapters, cb_kwargs=dict(story_name=story_name, sort=sort))

    else:
        list_pages = response.xpath('//ul[contains(@class, "pagination")]//li[not(contains(@class,"active"))]//a[not('
                                    'span)]/text()').getall()
        if len(list_pages) > 0:
            number_index_pages = list_pages[len(list_pages) - 1]
            for index in range(int(number_index_pages)):
                link_to_page = link + "trang-" + str(index + 1)
                sort = 50*index
                yield scrapy.Request(link_to_page, callback=response_list_chapters, cb_kwargs=dict(story_name=story_name, sort=sort))

    # item save db
    item['story_name'] = story_name
    item['avatar_path'] = avatarPath
    item['description'] = description
    item['status'] = status
    item['source'] = source
    item['author'] = author
    item['genre'] = genre
    item['created_by'] = "admin"
    item['created_on'] = datetime.datetime.now()
    item['modified_on'] = datetime.datetime.now()
    item['modified_by'] = "admin"
    item["is_deleted"] = 0
    item["hidden"] = 1
    item["collection_name"] = 'story'
    item["keywords"] = keywords
    item["description_seo"] = description_seo
    item["slug"] = slugify(story_name).lower()
    item["dealer_id"] = '08d92f17-4e75-4be2-84ba-522e9cc87468'
    yield item


def get_list_genre(response):
    get_links = response.xpath('//h3[@class="truyen-title"]//a/@href').getall()

    if len(get_links) > 0:
        for link in get_links:
            yield request_get_content_story(link)


class TienHiep(scrapy.Spider):
    name = 'tienhiep'
    allowed_domains = ['truyenfull.vn']
    start_urls = ['https://truyenfull.vn/the-loai/tien-hiep/']
    the_loai = 'Tiên Hiệp'

    def parse(self, response):
        last_page_text = response.xpath(
            '//ul[contains(@class, "pagination")]//li[not(contains(@class,"active"))]//a[text('
            ')="Cuối "]/@title').get()
        if last_page_text:
            text_replace_page = self.the_loai + " - Trang "
            replace_last_page_text = last_page_text.replace(text_replace_page, "")
            if int(replace_last_page_text) > 0:
                for index in range(int(replace_last_page_text)):
                    link_to_page = self.start_urls[0] + "trang-" + str(index)
                    yield scrapy.Request(link_to_page, callback=get_list_genre)
