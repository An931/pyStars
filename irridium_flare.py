from urllib.request import urlopen
from stars import *

class IridiumFlare:
	def __init__(self):
		pass


class Parser:
	def get_page_text(lat=0, lng=0):
		link = 'https://heavens-above.com/IridiumFlares.aspx?lat={}&lng={}'.format(lat, lng)
		with urlopen(link) as page:
		return page.read()
