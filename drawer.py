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

	def get_color_for_pygame(star):
		main_colors = dict(
			M = (255, 120, 120), # 'red',  # '#ff8f8f'
			K = (251, 190, 138), # 'orange',  # '#ffc78a'
			G = (255, 250, 157), # 'yellow',  # '#ffe899'
			F = (254, 239, 220), # 'cream',  # '#e6e3c6'
			A = (255, 255, 255), # 'white',  # '#f3f1f1'
			B = (216, 254, 254), # 'light-blue',  # '#d3ebf3'
			O = (197, 231, 254), # 'blue',  # '#c4f1ff'
			S = (251, 190, 138), # 'orange',  # '#ffc78a'
			C = (255, 120, 120) # 'red',  # '#ff8f8f'
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

	def get_radius_for_pygame(star, im_size=1000):
		# c = im_size / 10000
		# r = 2 * c
		r = 1
		if star.mag < 2:
			r = 4
		elif star.mag < 4:
			r = 3
		elif star.mag < 5:
			r = 2
		return r

	def add_draw_parametrs_for_pygame00(stars, window_size):
		for s in stars:
			s.x, s.y = Geom.get_int_image_coords(s, window_size)
			s.color = Drawer.get_color_for_pygame(s)
			s.radius = Drawer.get_radius_for_pygame(s)
