# encoding: utf-8

import sys
from HTMLParser import HTMLParser
from workflow import Workflow, ICON_WEB, web

BASE_URL = 'https://sdkdocs.roku.com'
htmlParser = HTMLParser()

def main(wf):
	matches = wf.cached_data('search_' + sys.argv[1], searchQuery, max_age = 3600)
	addListsOfResults(wf, matches)
	wf.send_feedback()


def searchQuery():
	searchUrl = 'https://sdkdocs.roku.com/rest/quicknav/1/search?query=' + sys.argv[1]
	r = web.get(searchUrl)
	r.raise_for_status()
	return r.json()['contentNameMatches']


def addListsOfResults(wf, lists):
	for li in lists:
		for item in li:
			url = BASE_URL + item['href']
			wf.add_item(
				title = htmlParser.unescape(item['name']),
				subtitle = url,
				arg = url,
				valid = True,
				icon = ICON_WEB
			)


if __name__ == u"__main__":
	wf = Workflow()
	sys.exit(wf.run(main))
