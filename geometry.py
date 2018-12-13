from stars import *
from numpy import sqrt


class Geom:

	def get_resize_image_coords(coords, im_size, coef, x_shift=0, y_shift=0):
		center_coords = coords[0] - im_size/2, coords[1] - im_size/2
		changed_center_coords = center_coords[0] * coef, center_coords[1] * coef
		a = changed_center_coords[0] + im_size/2, changed_center_coords[1] + im_size/2
		return changed_center_coords[0] + im_size/2, changed_center_coords[1] + im_size/2

	def get_resize_int_image_coords(coords, im_size, coef, x_shift=0, y_shift=0):
		coords = Geom.get_resize_image_coords(coords, im_size, coef, x_shift, y_shift)
		return int(coords[0]), int(coords[1])


	def get_int_image_coords(star, time_delta, im_size, x_shift, y_shift):
		coords = Geom.get_image_coords(star, time_delta, im_size, x_shift, y_shift)
		return int(coords[0]), int(coords[1])

	def get_image_coords(star, time_delta, im_size, x_shift=0, y_shift=0):
		x, y = Geom.get_coords(star, time_delta)
		if not x or not y:
			return im_size, im_size
		x += 1
		y += 1
		if x>2 or y>2:
			print(im_size - x * im_size / 2 + x_shift, im_size - y * im_size / 2 + y_shift)
		# return abs(im_size - x * im_size / 2 + x_shift), abs(im_size - y * im_size / 2 + y_shift)
		return im_size - x * im_size / 2 + x_shift, im_size - y * im_size / 2 + y_shift

	def get_coords00(star):
		def get_half_chord(dec):
			return sqrt(abs(1 - dec * dec))
		ra = Geom.get_ra_coords(star.ra)
		dec = Geom.get_dec_coords(star.dec)
		if not ra: # invisible stars on other halph sphere (6-18 hours)
			return None, None
		def get_dec_coef(ra):
			return sqrt(ra**2 + 1)
		dec_coef = get_dec_coef(ra)
		if dec*dec_coef > 1:
			# it means that star is out of picture bounds
			print(star.ra, star.dec, dec*dec_coef)
		# return (ra * get_half_chord(dec), dec)
		return (ra * get_half_chord(dec*dec_coef), dec * dec_coef)
		# return (ra * get_half_chord(dec*dec_coef), min(1, dec * dec_coef))

	def get_ra_coords(ra, delta):
		all_sec = 12*60*60/2
		# delta = delta % (60*60*24)
		ra_full_sec = (ra.full_sec + delta) % (60*60*24)
		# print(ra_full_sec)
		# ra_full_sec = ra.full_sec
		if ra_full_sec>6*60*60 and ra_full_sec<18*60*60:
			return None # to draw only half sphere
		if ra_full_sec < all_sec:
			return ra_full_sec / all_sec
		return (ra_full_sec - all_sec * 4) / all_sec

	def get_ra_coords24(ra, delta):
		all_sec = 12*60*60
		if ra.full_sec < all_sec:
			return ra.full_sec / all_sec
		return (ra.full_sec - all_sec * 2) / all_sec

	def get_dec_coords(dec):
		all_sec = 90*60*60
		return dec.full_sec / all_sec

	def get_coords(star, time_delta):
		# replace star depends on time only (delta - in secconds)
		# return coords where 0,0 = 0,0; 0,90 = 0,1; 6*60*60,0 = -1,0
		def get_half_chord(dec):
			# return sqrt(1 - dec * dec)
			return sqrt(abs(1 - dec * dec))
		def get_dec_coef(ra):
			return sqrt(ra**2 + 1)
		ra = Geom.get_ra_coords(star.ra, time_delta)
		dec = Geom.get_dec_coords(star.dec)
		if not ra: # invisible stars on other halph sphere (6-18 hours)
			return None, None
		dec_coef = get_dec_coef(ra)
		# прямые горизонтальн линии
		# return (ra * get_half_chord(dec), dec)
		# эллипсы
		return (ra * get_half_chord(dec*dec_coef), dec * dec_coef)



