from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from satellites import Satellite

class Parser:
	def get_satellites():
		link = 'https://heavens-above.com/AllSats.aspx?lat=0&lng=0&loc=Unspecified&alt=0&tz=UCT'
		page_code = Parser.get_page_code(link)
		rows = Parser.get_rows(page_code)
		lists_info = [Parser.get_satellite_info(r) for r in rows]
		satellites = [Satellite(info) for info in lists_info]
		return satellites

	def get_page_code(link):
		# with urlopen(link) as page:
		# 	return page.read()
		# 	FROM FILE: !!!!!
		with open('page_code.txt') as file:
			return file.read()

	def get_rows(page_code):
		soup = BeautifulSoup(page_code, "html5lib")
		table_info = soup.find_all('tr', 'clickableRow')
		return table_info

	def get_satellite_info(row):
		info = row.find_all('td')
		info = [i.text.strip() for i in info]
		# print(info)
		return info


if __name__ == '__main__':
	page_code = Parser.get_page_code('https://heavens-above.com/AllSats.aspx?lat=0&lng=0&loc=Unspecified&alt=0&tz=UCT')
	# print(page_code)
	blocks = Parser.get_rows(page_code)
	for b in blocks:
		c = Parser.get_satellite_info(b)
		print(c)




