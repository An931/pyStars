from stars import *
from numpy import sqrt


class Geom:
	def get_image_coords(star, im_size):
		x, y = Geom.get_coords(star)
		x += 1
		y += 1
		return im_size - x * im_size / 2, im_size - y * im_size / 2

	def get_image_coords000(star, im_size, x_shift=0, y_shift=0):
		x, y = Geom.get_coords(star)
		x += 1
		y += 1
		return im_size - x * im_size / 2 + x_shift, im_size - y * im_size / 2 + y_shift


	def get_coords(star):
		def get_half_chord(dec):
			return sqrt(1 - dec * dec)
		ra = Geom.get_ra_coords(star.ra)
		dec = Geom.get_dec_coords(star.dec)
		return (ra * get_half_chord(dec), dec)

	def get_ra_coords(ra):
		all_sec = 12*60*60
		if ra.full_sec < all_sec:
			return ra.full_sec / all_sec
		return (ra.full_sec - all_sec * 2) / all_sec

	def get_dec_coords(dec):
		all_sec = 90*60*60
		return dec.full_sec / all_sec


