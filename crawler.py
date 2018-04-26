import os
import sys
import requests
import lxml.html
import logging

LOG_FILE = '/tmp/mycrawler.log'
URL_TEMPLATE = 'http://www.comicbus.com/html/{}.html'
PAGE_TEMPLATE = 'http://v.comicbus.com/online/comic-{}.html?ch={}'

targets = {
	'103': 'One Piece',
	# '10818': 'Kakegurui',
	# '653': 'Detective Conan',
}

def macos_notif(title, content):
    os.system("""
			osascript -e 'display notification "{}" with title "{}"'
			""".format(content, title))

if __name__ == '__main__':

	mangas = {}
	# load the last record
	try:
		with open(LOG_FILE,'r') as f:
			for line in f:
				tokens = list(map(str.strip, line.split(',')))
				mangas[tokens[0]] = tokens[1] if tokens[0] in targets else 'none'
	except IOError as e:
		# ignore file not exists exception
		pass

	# create log file if not exists
	f = open(LOG_FILE, 'w+')

	for index, name in targets.items():
		retry = 10
		while retry > 0:
			try:
				r = requests.get(URL_TEMPLATE.format(index))
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

		# the first string represents current episodes of manga should be
		# in a form of '1-NUM'
		tokens = list(map(str.strip, texts[0].split('-'))) if texts else None
		if len(tokens) > 1:
			try:
				latest = int(tokens[1])
			except ValueError as ex:
				logging.warning('invalid raw string for conversion')
				continue
			f.write('{},{}\n'.format(index, latest))
			link = PAGE_TEMPLATE.format(index, latest)
			if str(latest) != mangas[index]:
				logging.error('new episode found')
				macos_notif(name + ' has new episode!', link)

	f.close()

