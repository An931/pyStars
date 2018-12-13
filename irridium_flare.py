from datetime import time, datetime
# import datetime
import math

class IridiumFlare():
	def __init__(self, info):
		if not isinstance(info, list) or len(info) != 8:
			raise Exception('! info is list of 8 elements')
		self.datetime = Parser.get_date(info[0])
		self.mag = int(info[1])
		self.alt = int(info[2][:-1])
		self.azim = int(info[3].split()[0][:-1])
		self.name = info[0]


	def get_date(info):
		# дек 21 08:23:34
		months = { 'янв' : 01, 'фев' : 02, 'дек' : 12, 'ноя' : 11 }
		FMT = '%Y-%m-%d %H:%M:%S'
		info = info.split()
		# ! год не учитывается
		s = '2018-{}-{} {}'.format(months[info[0]], info[1], info[2])
		dt = datetime.strptime(s, FMT)
		return dt

	def get_current_pos(self, time, size):
		# возвр (x, y)
		if time < self.start_info.time or time > self.end_info.time:
			return
		pass

	def get_pos_on_standart_coords(self, time):
		# возвр координаты на единичном круге с центром в 0, 0
		pass

	def get_start_pos_on_standart_coords(self):
		x = math.cos(self.start_info.azim)
		x = math.cos(self.start_info.azim)
		v = v # посчитать длину вектора (в завис от высоты)
		x, y = x * v, y * v
		return (x, y)

	def get_image_coords(self, time, size):
		pass


if __name__ == '__main__':
	time = '2018-03-21 8:23:34'
	time2 = '8:25:34'
	# =======================
	# FMT = '%H:%M:%S'
	# dt = datetime.strptime(time2, FMT)

	FMT = '%Y-%m-%d %H:%M:%S'
	dt = datetime.strptime(time, FMT)


	print(dt)