import sys
import requests
import lxml.html
import logging

urls = [
	'http://www.comicbus.com/html/103.html',		# One piece
	'http://www.comicbus.com/html/10818.html',		# Kakegurui
]

def to_int(raw):
	try:
		num = int(raw)
		return num
	except ValueError as e:
		raise e

if __name__ == '__main__':

	# load the last episode
	for url in urls:

		retry = 10
		while retry > 0:
			try:
				r = requests.get(url)
				r.raise_for_status()
				break
			except requests.exceptions.Timeout:
				# Maybe set up for a retry, or continue in a retry loop
				retry -= 1
				logging.info('retry ...')
			except requests.exceptions.TooManyRedirects:
				# Tell the user their url was bad and try a different one
				logging.warning('bad url')
			except requests.exceptions.RequestException as e:
				# catastrophic error. bail.
				logging.error('request exception encountred, exit directly')
				sys.exit(1)

		root = lxml.html.fromstring(r.content)
		texts = root.xpath(
				'//body/table[5]//table[2]//table[1]//table[1]//a/font/b/text()'
		)

		if texts:
			# the first string represents current episodes of manga in a form
			# of '1-NUM'
			tokens = texts[0].split('-')
			if len(tokens) > 1:
				try:
					latest = to_int(tokens[1])
				except ValueError as ex:
					logging.warning('invalid raw string for conversion')
					continue
				print(latest)

