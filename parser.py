from urllib.request import urlopen
from bs4 import BeautifulSoup
import re



def get_cars(model='', page_count=30):
	model = get_link_part(model)
	cars = []
	for page_num in range(1, page_count + 1):
		# ссылка для авто с мотором ...л, ценой до ...
		link = "https://www.avito.ru/ekaterinburg/avtomobili/{}mehanika/levyy_rul?p={}&pmax=6000000&pmin=0&radius=1000".format(model, page_num)
		print('downloadind page {} of {} ...'.format(page_num, model))
		try:
			cars_textparts = get_cars_textparts(get_page_code(link))
		except:
			print('something has gone wrong; stop downloadind')
			break
		
		for text_part in cars_textparts:
			m = extract_car(text_part)
			try:
				cars.append(get_car(m))
			except(Exception):
				continue
	cars.sort(key=lambda x: x.year, reverse=False)
	print('cars count:', len(cars))
	# for car in cars:
	# 	print(car.mark, car.model, car.year, car.price)
	return cars

def get_page_code(link):
	with urlopen(link) as page:
		return page.read()

def get_textparts(page_code):
	# возвр текстовые фрагменты 
	soup = BeautifulSoup(page_code, "html5lib")
	# car_ads = soup.find_all('table', 'standartTable')
	car_ads = soup.find_all('tr', 'clickableRow')
	# return car_ads # если бы возвр soup объекты
	return [str(x) for x in car_ads]

def extract_car(text_part):
	# возвр match_obj для get car
	# print('-------\n{}\n-------'.format(text_part))
	reg_href = r'href="(.+?)" '
	reg_title = r'title="(.+?)"'
	reg_price = r'.*?class="price">\n (.*?)<span class=.*?'
	reg_descr = r'class="specific-params specific-params_block">\s*(.*?) </div>'
	reg_place = r''
	reg_date = r''

	regexpr = re.compile(reg_href + reg_title + reg_price + reg_descr, re.DOTALL)
	m = re.search(regexpr, text_part)
	return m



class Parser:
	link = 'https://heavens-above.com/IridiumFlares.aspx?lat=0&lng=0&loc=Unspecified&alt=0&tz=UCT'
	def get_iridium_flares():
		pass


if __name__ == '__main__':
	page_code = get_page_code('https://heavens-above.com/IridiumFlares.aspx?lat=0&lng=0&loc=Unspecified&alt=0&tz=UCT')
	print(get_textparts(page_code))



