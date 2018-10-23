from PIL import Image, ImageDraw
import re
import os
from stars import *
from geometry import *


class Drawer:
	def draw_star(star, im, x, y):
		# if star.label not in ['Alp', 'Bet', 'Gam', 'Del', 'Eps']:
		# 	return
		color = Drawer.get_color(star)
		r = Drawer.get_radius(star, im.size[0])
		# r = Drawer.get_radius(star, 1000)

		draw = ImageDraw.Draw(im)
		draw.ellipse((x-r, y-r, x+r, y+r), fill=color)


	def get_color(star):
		main_colors = dict(
			M = '#ff8f8f',
			K = '#ffc78a',
			G = '#ffe899',
			F = '#e6e3c6',
			A = '#f3f1f1',
			B = '#d3ebf3',
			O = '#c4f1ff',
			S = '#ffc78a',
			C = '#ff8f8f')
		clas = re.search(r'[MKGFABOSC]', star.sp_class).group(0)
		return main_colors[clas]


	def get_radius(star, im_size):
		# c = im_size / 10000
		# r = 2 * c
		r = 1
		if star.mag < 2:
			r = 5
		elif star.mag < 4:
			r = 4
		elif star.mag < 5:
			r = 2
		return r/2


	def draw_stars(stars, im):
		for star in stars:
			x, y = Geom.get_image_coords(star, im.size[0])
			# x, y = Geom.get_image_coords(star, 1000)

			Drawer.draw_star(star, im, x, y)


class PictureCreator:
	def create_lv(new_pic_name, coords=(0, 0), angle=360):
		path = './data/'
		txt_files = [x for x in os.listdir(path) if x.endswith('.txt')]
		# im_size = 10000
		#im_size = 1000
		im_size = 1100
		im = Image.new('RGBA', (im_size, im_size), color='#000000')
		for name in txt_files:
			# if name != 'cas.txt':
			# 	continue
			file = open(path + name)
			constellation = Constellation(file.read())
			for star in constellation.stars:
				star.ra.full_sec += coords[0]
				star.dec.full_sec += coords[1]
			Drawer.draw_stars(constellation.stars, im)
		im.save(new_pic_name)


class StarsGetter:
	def get_stars():
		path = './data/'
		txt_files = [x for x in os.listdir(path) if x.endswith('.txt')]
		# im_size = 10000
		#im_size = 1000

		# stars = []
		for name in txt_files:
			with open(path + name) as f:
				constellation = Constellation(f.read())
				for s in constellation.stars:
					# stars.append(s)
					yield s
			# return stars



if __name__ == '__main__':
	pass
	# if not os.path.exists('./shifts'):
	# 	os.mkdir('shifts')
	# for h in range(25):
	# 		for d in range(19):
	# 			new_path = './shifts/{}ra_{}dec.png'.format(h*3600, d*10*3600)
	# 			print(new_path)
	# 			PictureCreator.create_lv(new_path, (3600*h, 3600*10*d))
