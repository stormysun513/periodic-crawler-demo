import scrapy

class MangaUpdateSpider(scrapy.Spider):

	name = 'manga_update_spider'
	start_urls = ['http://www.comicbus.com']
