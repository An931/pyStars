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

		# to compute coef
		# # промежутки между началом и высшей точкой
		self.start_coords = self.get_pos_on_standart_coords_depends_on_altazim(self.start_info.time)
		self.height_coords = self.get_pos_on_standart_coords_depends_on_altazim(self.highest_info.time)
		self.end_coords = self.get_pos_on_standart_coords_depends_on_altazim(self.end_info.time)
		print('coords ', self.start_coords, self.height_coords, self.end_coords)


		self.first_part_timedelta = (self.highest_info.time - self.start_info.time).seconds
		self.first_part_delta_x = self.height_coords[0] - self.start_coords[0]
		self.first_part_delta_y = self.height_coords[1] - self.start_coords[1]
		self.second_part_timedelta = (self.end_info.time - self.highest_info.time).seconds
		self.second_part_delta_x = self.end_coords[0] - self.height_coords[0]
		self.second_part_delta_y = self.end_coords[1] - self.height_coords[1]
		print('first part ', self.first_part_delta_x, self.first_part_delta_y )
		print('sec part ', self.second_part_delta_x, self.second_part_delta_y )


	def get_alt_and_azimith(self, time):
		# return self.highest_info.alt, self.highest_info.azim
		# возвр предположительные выс и азим в момент времени
		# if time <= self.start_info.time or time >= self.end_info.time:
		# 	return

		# return self.start_info.alt, self.start_info.azim
		# return self.highest_info.alt, self.highest_info.azim
		# return self.end_info.alt, self.end_info.azim

		if time < self.highest_info.time:
			part_timedelta = self.first_part_timedelta
			part_delta_alt = self.first_part_delta_alt
			part_delta_azim = self.first_part_delta_azim
			current_time_delta = (time - self.start_info.time).seconds
			coef = current_time_delta / part_timedelta
			delta_alt = coef * part_delta_alt
			delta_azim = coef * part_delta_azim 
			alt = self.start_info.alt + delta_alt
			# azim =  delta_azim
			azim = self.start_info.azim + delta_azim
			# print('timedelta ', current_time_delta)
			# print('coef ', coef)
			# print('delta_alt ', delta_alt)
			# print('delta_azim ', delta_azim)
			# print(alt, azim)

		else:
			part_timedelta = self.second_part_timedelta
			part_delta_alt = self.second_part_delta_alt
			part_delta_azim = self.second_part_delta_azim
			current_time_delta = (time - self.highest_info.time).seconds
			coef = current_time_delta / part_timedelta
			delta_alt =  coef * part_delta_alt 
			delta_azim = coef * part_delta_azim
			alt = self.highest_info.alt + delta_alt
			azim = self.highest_info.azim + delta_azim
			# azim = self.end_info.azim #+ delta_azim

		# print(self.start_info. alt, azim)
		return (alt, azim)

	def get_pos_on_standart_coords_depends_on_altazim(self, time):

		# if time < self.start_info.time or time > self.end_info.time:
		# 	return
		if time == self.start_info.time:
			alt, azim = self.start_info.alt, self.start_info.azim
		elif time == self.highest_info.time:
			alt, azim = self.highest_info.alt, self.highest_info.azim
		elif time == self.end_info.time:
			alt, azim = self.end_info.alt, self.end_info.azim
		angle = (azim + 90)
		x = math.cos(math.radians(angle))
		y = math.sin(math.radians(angle))
		v = (90 - alt)/90 # посчитать длину вектора (в завис от высоты)
		x, y = x * v, y * v
		# print(x, y)
		return (x, y)

	def get_pos_on_standart_coords_OLD(self, time):
		# if time < self.start_info.time or time > self.end_info.time:
		# 	return
		alt, azim = self.get_alt_and_azimith(time)
		angle = (azim + 90)
		x = math.cos(math.radians(angle))
		y = math.sin(math.radians(angle))
		v = (90 - alt)/90 # посчитать длину вектора (в завис от высоты)
		x, y = x * v, y * v
		# print(x, y)
		return (x, y)

	def get_pos_on_standart_coords(self, time):

		# if time < self.start_info.time or time > self.end_info.time:
		# 	return

		if time < self.highest_info.time:
			part_timedelta = self.first_part_timedelta
			part_delta_x = self.first_part_delta_x
			part_delta_y = self.first_part_delta_y
			current_time_delta = (time - self.start_info.time).seconds
			coef = current_time_delta / part_timedelta
			delta_x = coef * part_delta_x
			delta_y = coef * part_delta_y
			x = self.start_coords[0] + delta_x
			# azim =  delta_azim
			y = self.start_coords[1] + delta_y
			# print('timedelta ', current_time_delta)
			# print('coef ', coef)
			# print('delta_alt ', delta_alt)
			# print('delta_azim ', delta_azim)
			# print(alt, azim)

		else:
			part_timedelta = self.second_part_timedelta
			part_delta_x = self.second_part_delta_x
			part_delta_y = self.second_part_delta_y
			current_time_delta = (time - self.highest_info.time).seconds
			coef = current_time_delta / part_timedelta
			delta_x =  coef * part_delta_x
			delta_y = coef * part_delta_y
			x = self.height_coords[0] + delta_x
			y = self.height_coords[1] + delta_y
			# azim = self.end_info.azim #+ delta_azim

		# print(self.start_info. alt, azim)
		# return (alt, azim)
		# alt, azim = self.get_alt_and_azimith(time)
		# angle = (azim + 90)
		# x = math.cos(math.radians(angle))
		# y = math.sin(math.radians(angle))
		# v = (90 - alt)/90 # посчитать длину вектора (в завис от высоты)
		# x, y = x * v, y * v
		# print(x, y)
		return (x, y)


	def get_image_coords(self, time, im_size, x_shift, y_shift):
		# if time < self.start_info.time or time > self.end_info.time:
		# 	return
		x, y = self.get_pos_on_standart_coords(time)
		# print(x, y)
		x += 1
		y += 1
		# print(x * im_size / 2, im_size - y * im_size / 2)
		return x * im_size / 2 + x_shift, im_size - y * im_size / 2 + y_shift
		# return im_size - x * im_size / 2 + x_shift, im_size - y * im_size / 2 + y_shift

	def get_start_pos_on_standart_coords000(self):
		angle = (self.start_info.azim - 90) % 360
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
		print(im_size - x * im_size / 2, im_size - y * im_size / 2)
		return im_size - x * im_size / 2 + x_shift, im_size - y * im_size / 2 + y_shift

	def get_int_image_coords(self, time, im_size, x_shift=0, y_shift=0):
		
		# основной метод, который вызывается извне
		if time <= self.start_info.time or time >= self.end_info.time:
			# print(self.start_info.time, time, self.end_info.time)
			return
		if (time - self.start_info.time).seconds == 0 or (self.end_info.time - time).seconds == 0:
			return
		print(self.name)
		coords = self.get_image_coords(time, im_size, x_shift, y_shift)
		return int(coords[0]), int(coords[1])


class Satellite_info:
	rus_azimuths = {'С':0, 'ССВ':22.5, 'СВ':45, 'ВСВ':67.5,
										'В':90, 'ВЮВ':112.5, 'ЮВ':135, 'ЮЮВ':157.5,
										'Ю':180, 'ЮЮЗ':202.5, 'ЮЗ':225, 'ЗЮЗ':247.5,
										'З':270, 'ЗСЗ':292.5, 'СЗ':315, 'ССЗ':337.5 }
		# смотри вики стороны света ! восток и запад строго наоборот

	def __init__(self, time, altitude, azimuth):
		# !!!!! works only with current day (later get day from page code)
		time_str = '2018-20-12 ' + time
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
