from datetime import time, datetime
# import datetime
import math

class Satellite():
	def __init__(self, info):
		if not isinstance(info, list) or len(info) != 11:
			raise Exception('! info is list of 11 elements')
		self.name = info[0]
		self.mag = int(info[1])
		self.start_info = Satellite_info(info[2], info[3], info[4])
		self.highest_info = Satellite_info(info[5], info[6], info[7])
		self.end_info = Satellite_info(info[8], info[9], info[10])

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




class Satellite_info:
	def __init__(self, time, altitude, azimuth):
		self.time_str = time
		self.time = datetime.strptime(time, '%H:%M:%S')
		self.alt = int(altitude[-1])
		self.azim = azimuth


# мб прописать соответствия рус-англ азимут 

if __name__ == '__main__':
	time = '8:23:34'
	time2 = '8:25:34'
	# t = datetime.time(5, 7, 9)
	# t = datetime.time(*[int(x) for x in time.split(':')])
	# t2 = datetime.time(*[int(x) for x in time2.split(':')])
	# print(t)
	# =======================
	FMT = '%H:%M:%S'
	print(datetime.strptime(time2, FMT) - datetime.strptime(time, FMT))
	print((datetime.strptime(time2, FMT) > datetime.strptime(time, FMT)))