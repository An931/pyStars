import re
import os
from stars import *
from geometry import *
from GUI import *


class Drawer:

	def get_color(star):
		main_colors = dict(
			M = 'red',  # '#ff8f8f'
			K = 'orange',  # '#ffc78a'
			G = 'yellow',  # '#ffe899'
			F = 'cream',  # '#e6e3c6'
			A = 'white',  # '#f3f1f1'
			B = 'light-blue',  # '#d3ebf3'
			O = 'blue',  # '#c4f1ff'
			S = 'orange',  # '#ffc78a'
			C = 'red',  # '#ff8f8f'
			)
		clas = re.search(r'[MKGFABOSC]', star.sp_class).group(0)
		return main_colors[clas]


	def get_radius(star, im_size=1000):
		# c = im_size / 10000
		# r = 2 * c
		r = 1
		if star.mag < 2:
			r = 5
		elif star.mag < 4:
			r = 4
		elif star.mag < 5:
			r = 2
		return r

