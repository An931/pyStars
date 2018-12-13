from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import satellites

class Parser:
	link = 'https://heavens-above.com/AllSats.aspx?lat=0&lng=0&loc=Unspecified&alt=0&tz=UCT'

	def get_satellites():
		page_code = Parser.get_page_code(link)
		rows = Parser.get_rows(page_code)
		lists_info = [Parser.get_satellites_info(r) for r in row]
		satellites = [Sattellite(info) for info in lists_info]
		return satellites

	def get_page_code(link):
		with urlopen(link) as page:
			return page.read()

	def get_rows(page_code):
		soup = BeautifulSoup(page_code, "html5lib")
		satellites_info = soup.find_all('tr', 'clickableRow')
		return satellites_info

	def get_satellites_info(row):
		info = row.find_all('td')
		info = [i.text.strip() for i in info]
		# print(info)
		return info


if __name__ == '__main__':
	page_code = Parser.get_page_code('https://heavens-above.com/AllSats.aspx?lat=0&lng=0&loc=Unspecified&alt=0&tz=UCT')
	blocks = Parser.get_rows(page_code)
	for b in blocks:
		c = Parser.get_satellites_info(b)

		# print(c)
		# print(b.attr)
		# print(type(b))
		# print(b)




