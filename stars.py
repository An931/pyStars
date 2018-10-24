
import re

class Star:
	def __init__(self, str, constellation):
		# if str == '': 
		# 	return
		# print(str)
		r_crds1 = r'([\+-]{0,1}[ \d]{1,2}:[ \d]{1,2}:[ \d\.]+)'
		r_crds2 = r'([\+-]{0,1}[ \d]{1,2}:[ \d]{1,2}:[ \d]{2})'
		r_smth = r'[\d\.]+\s+-*[\d\.]+[\sA-Z]+'
		r_m_sp = r'([\-\d\.]+)\s+([^\s]+\s{0,1}[^\s]*)'
		r_smth2 = r'\s+[\+-]{0,1}[\d\.]+\s+[\+-]{0,1}[\d\.]+[\sD\d]+[\+-]\d{3}\s+\d+'
		m = re.search(r_crds1+r'\s+'+r_crds2+r'\s+'+r_smth+r_m_sp+r_smth2+r'\s+\d*([A-Za-z]*)', str)

		self.line = str

		self.ra = RightAscension(m.group(1))
		self.dec = Declination(m.group(2))
		self.mag = float(m.group(3))
		self.sp_class = m.group(4).strip()
		self.label = m.group(5)

		# self.constellation = constellation


class Constellation000:
	def __init__(self, text, name):
		self.name = name
		lines = text.splitlines()
		self.stars = []
		for l in lines:
			star = Star(l, self)
			# if star.label:
			self.logic_stars.append(star)
			# self.stars.append(QtStars(star))


class RightAscension:
	def __init__(self, str):
		measures = str.split(':')
		self.hours = int(measures[0])
		self.minutes = int(measures[1])
		self.seconds = float(measures[2])
		if self.hours > 24 or self.minutes > 60 or self.seconds > 60:
			raise Exception()
		self._full_sec = self.hours*3600 + self.minutes*60 + self.seconds

	@property
	def full_sec(self):
		return self._full_sec

	@full_sec.setter
	def full_sec(self, value):
		self._full_sec = value % (24 * 60 * 60 + 0)

	def __str__(self):
		return '{}:{}:{}'.format(self.hours, self.minutes, self.seconds)


class Declination:
	def __init__(self, str):
		if str[0] == '-':
			self.sign = -1
		else:
			self.sign = 1
		if str[0] == '-' or str[0] == '+':
			str = str[1:]
		measures = str.split(':')
		self.degrees = int(measures[0])
		self.minutes = int(measures[1])
		self.seconds = float(measures[2])		
		if self.degrees > 90 or self.minutes > 60 or self.seconds > 60:
			raise Exception()
		self._full_sec = self.sign * (self.degrees*3600 + self.minutes*60 + self.seconds)

	@property
	def full_sec(self):
		return self._full_sec

	@full_sec.setter
	def full_sec(self, value):
		half_round = 90 * 60 * 60
		if value <= half_round and value >= -half_round:
			self._full_sec = value
		if value > half_round:
			self._full_sec = -half_round + (value - half_round)
		if value < -half_round:
			self._full_sec = half_round + (value + half_round)
		# self._full_sec = value


	def __str__(self):
		sign = '+' if self.sign == 1 else '-'
		return '{}{}:{}:{}'.format(sign, self.degrees, self.minutes, self.seconds)
