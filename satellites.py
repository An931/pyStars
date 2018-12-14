from datetime import time, datetime, timedelta
# import datetime
import math

class Satellite:
	def __init__(self, info):
		if not isinstance(info, list) or len(info) != 11:
			raise Exception('! info should be list of 11 elements')
		self.name = info[0]
		# self.mag = float(info[1])
		self.mag = float('.'.join(info[1].split(',')))
		self.start_info = Satellite_info(info[2], info[3], info[4])
		self.highest_info = Satellite_info(info[5], info[6], info[7])
		self.end_info = Satellite_info(info[8], info[9], info[10])


	def get_alt_and_azimith(self, time):
		return self.end_info.alt, self.end_info.azim


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
		if time < self.start_info.time or time > self.end_info.time:
			return
		alt, azim = self.get_alt_and_azimith(time)
		angle = (azim + 90) % 360
		x = math.cos(math.radians(angle))
		y = math.sin(math.radians(angle))
		v = (90 - alt)/90 # посчитать длину вектора (в завис от высоты)
		x, y = x * v, y * v
		# print(x, y)
		return (x, y)

	def get_image_coords(self, time, im_size, x_shift, y_shift):
		if time < self.start_info.time or time > self.end_info.time:
			return
		x, y = self.get_pos_on_standart_coords(time)
		x += 1
		y += 1
		return im_size - x * im_size / 2 + x_shift, im_size - y * im_size / 2 + y_shift

	def get_start_pos_on_standart_coords000(self):
		angle = (self.start_info.azim + 90) % 360
		x = math.cos(math.radians(angle))
		y = math.sin(math.radians(angle))
		v = (90-self.start_info.alt)/90 # посчитать длину вектора (в завис от высоты)
		x, y = x * v, y * v
		print(x, y)
		return (x, y)

	def get_start_image_coords000(self, im_size, x_shift, y_shift):
		x, y = self.get_start_pos_on_standart_coords()
		x += 1
		y += 1
		# if x>2 or y>2:
		# 	print(im_size - x * im_size / 2 + x_shift, im_size - y * im_size / 2 + y_shift)
		# # return abs(im_size - x * im_size / 2 + x_shift), abs(im_size - y * im_size / 2 + y_shift)
		return im_size - x * im_size / 2 + x_shift, im_size - y * im_size / 2 + y_shift

	def get_int_image_coords(self, time, im_size, x_shift=0, y_shift=0):
		# основной метод, который вызывается извне
		if time < self.start_info.time or time > self.end_info.time:
			print(self.start_info.time, time, self.end_info.time)
			return
		coords = self.get_image_coords(time, im_size, x_shift, y_shift)
		return int(coords[0]), int(coords[1])


class Satellite_info:
	rus_azimuths = {'С':0, 'ССЗ':22.5, 'СЗ':45, 'ЗСЗ':67.5,
										'З':90, 'ЗЮЗ':112.5, 'ЮЗ':135, 'ЮЮЗ':157.5,
										'Ю':180, 'ЮЮВ':202.5, 'ЮВ':225, 'ВЮВ':247.5,
										'В':270, 'ВСВ':292.5, 'СВ':315, 'ССВ':337.5 }
		# смотри вики стороны света

	def __init__(self, time, altitude, azimuth):
		# !!!!! works only with current day (later get day from page code)
		time_str = '2018-14-12 ' + time
		self.time = datetime.strptime(time_str, '%Y-%d-%m %H:%M:%S')
		self.alt = int(altitude[:-1])
		self.azim = Satellite_info.rus_azimuths[azimuth]



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
