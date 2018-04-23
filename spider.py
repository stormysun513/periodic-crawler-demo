import scrapy

class MangaUpdateSpider(scrapy.Spider):

	# define static variables here
	name = 'manga_update_spider'
	start_urls = [
		'http://www.comicbus.com/html/103.html',	# One piece
		'http://www.comicbus.com/html/10818.html',	# Kakegurui
	]

	# implement the parse function to handle collected data
	def parse(self, resp):
		hxs = scrapy.Selector(resp)
		selector = hxs.xpath('//body/table[5]//table[2]//table[1]//table[1]//a/font/b/text()')

		print('dir: ', [attr for attr in dir(scrapy.Spider) if callable(getattr(scrapy.Spider, attr))])
		print('URL: ', resp.request.url)

		# extract the latest episode index from text
		text = selector.extract_first()
