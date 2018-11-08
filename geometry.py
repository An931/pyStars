from stars import *
from numpy import sqrt


class Geom:

	def get_resize_image_coords(coords, im_size, coef):
		center_coords = coords[0] - im_size/2, coords[1] - im_size/2
		changed_center_coords = center_coords[0] * coef, center_coords[1] * coef
		a = changed_center_coords[0] + im_size/2, changed_center_coords[1] + im_size/2
		return changed_center_coords[0] + im_size/2, changed_center_coords[1] + im_size/2

	def get_resize_int_image_coords(coords, im_size, coef):
		coords = Geom.get_resize_image_coords(coords, im_size, coef)
		return int(coords[0]), int(coords[1])


	def get_int_image_coords(star, im_size, x_shift=0, y_shift=0):
		coords = Geom.get_image_coords(star, im_size, x_shift, y_shift)
		return int(coords[0]), int(coords[1])

	def get_image_coords(star, im_size, x_shift=0, y_shift=0):
		x, y = Geom.get_coords(star)
		x += 1
		y += 1
		return im_size - x * im_size / 2 + x_shift, im_size - y * im_size / 2 + y_shift


	def get_coords(star):
		def get_half_chord(dec):
			return sqrt(1 - dec * dec)
		# def get_half_chord2(ra):
		# 	return sqrt(1 - ra * ra)
		# def get_half_ellipse(ra):
		# 	return (1/2)*3.14159265*(ra+90*60*60)
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


