from datetime import time, datetime, timedelta
# import datetime
import math

class Satellite:
	def __init__(self, info):
		if not isinstance(info, list) or len(info) != 11:
			raise Exception('! info is list of 11 elements')
		self.name = info[0]
		# self.mag = float(info[1])
		self.mag = float('.'.join(info[1].split(',')))
		self.start_info = Satellite_info(info[2], info[3], info[4])
		self.highest_info = Satellite_info(info[5], info[6], info[7])
		self.end_info = Satellite_info(info[8], info[9], info[10])

	def get_current_pos(self, time, size):
		# возвр (x, y)
		alt, azim = self.get_alt_and_azimith(time)


	def get_alt_and_azimith(self, time):
		# возвр предположительные выс и азим в момент времени
		if time < self.start_info.time or time > self.end_info.time:
			return
		if time < self.highest_info:
			# можно (нужно) считать в ините. дельта времени старт-выс, дельта высоты, дельта азимута
			half_delta_time = (self.highest_info.time - self.start_info.time).seconds
			half_delta_alt = math.abs(self.highest_info.alt - self.start_info.alt)
			half_delta_azim = math.abs(self.highest_info.azim - self.start_info.azim)
			# !!! смотреть что там по знакам!
			time_delta = (self.start_info.time - time).seconds
			coef = half_delta_time / time_delta
			delta_alt = coef * half_delta_alt
			delta_azim = coef * half_delta_azim
			alt = self.start_info.alt + delta_alt
			azim = self.start_info.azim + delta_azim
		else:
			# можно (нужно) считать в ините. дельта времени старт-выс, дельта высоты, дельта азимута
			half_delta_time = (self.end_info.time - self.highest_info.time).seconds
			half_delta_alt = math.abs(self.end_info.alt - self.highest_info.alt)
			half_delta_azim = math.abs(self.end_info.azim - self.highest_info.azim)
			# !!! смотреть что там по знакам!
			time_delta = (self.end_info.time - time).seconds
			coef = half_delta_time / time_delta
			delta_alt = coef * half_delta_alt
			delta_azim = coef * half_delta_azim
			alt = self.highest_info.alt + delta_alt
			azim = self.highest_info.azim + delta_azim

		return (alt, azim)



	def get_pos_on_standart_coords(self, time):
		# возвр координаты на единичном круге с центром в 0, 0
		pass

	def get_start_pos_on_standart_coords(self):
		x = math.cos(self.start_info.azim)
		x = math.cos(self.start_info.azim)
		v = v # посчитать длину вектора (в завис от высоты)
		x, y = x * v, y * v
		return (x, y)

	def get_image_coords(self, sky_coords, size):
		alt, azim = sky_coords
		# координаты для системы от -1 до 1
		x = 0 # cos(azim ) * alt * (1/90) ? -- см знаки азимута и коэф для высоты (длины вектора)

	def get_int_image_coords(self, time, size, x_shift=0, y_shift=0):
		# основной метод, который вызывается извне
		if time < self.start_info.time or time > self.end_info.time:
			print(self.start_info.time, time, self.end_info.time)
			return
		return (100, 200)


	# def get_all():
	# 	import parser
	# 	return parser.Parser.get_satellites()


class Satellite_info:
	rus_azimuths = {'С':0, 'Ю':180, 'З':270, 'В':90,
										'С':0, 'Ю':180, 'З':270, 'В':90,
										'С':0, 'Ю':180, 'З':270, 'В':90 }
		# смотри вики стороны света

	def __init__(self, time, altitude, azimuth):
		# !!!!! works only with current day (later get day from page code)
		time_str = '2018-14-12 ' + time
		self.time = datetime.strptime(time_str, '%Y-%d-%m %H:%M:%S')
		self.alt = int(altitude[:-1])
		# self.azim = Satellite_info.rus_azimuths[azimuth]
		# !!!!!!!!!!!!!!!!!!!!!!!11
		self.azim = 0


# мб прописать соответствия рус-англ азимут 

if __name__ == '__main__':
	# print(Satellite.get_all())

	time = '8:23:34'
	time2 = '8:25:34'
	# t = datetime.time(5, 7, 9)
	# t = datetime.time(*[int(x) for x in time.split(':')])
	# t2 = datetime.time(*[int(x) for x in time2.split(':')])
	# print(t)
	# =======================
	FMT = '%H:%M:%S'
	d1 = datetime.strptime(time, FMT)
	d2 = datetime.strptime(time2, FMT)
	print((d2-d1).seconds)
	print((datetime.strptime(time2, FMT) > datetime.strptime(time, FMT)))
