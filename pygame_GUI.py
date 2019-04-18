import pygame, sys
from pygame.locals import *
from drawer import *
from stars import *
# from iridium_flare import *
# from satellites import *
# from parser import *
from h_a_site_parser import *
from datetime import time, datetime, timedelta



class PyGameApp:
	def __init__(self):
		self.window_size = 800
		pygame.init()
		self.FPS = 30
		self.fpsClock = pygame.time.Clock()

		pygame.display.set_caption('Stars')
		self.screen = pygame.display.set_mode((self.window_size+60, self.window_size+60), 0, 32)
		self.indent = 30 # отступ сверху и слева

		self.stars = self.get_stars()
		# info = ['ATLAS 3B R/B', '2,9', '18:15:06', '10°', 'ЮЮЗ', '18:22:26', '76°', 'ВЮВ', '18:29:31', '10°', 'ССВ']
		# info = ['OAO 3 Rocket', '3,2', '19:10:38', '10°', 'ЗСЗ', '19:15:27', '78°', 'ЮЗ', '19:19:46', '12°', 'ЮВ']
		# info = ['Ariane V96 H10-3', '3,1', '18:27:08', '10°', 'З', '18:29:49', '85°', 'Ю', '18:38:15', '10°', 'В']
		# info = ['GPS 2-04 Rocket1', '3,2', '18:26:42', '10°', 'ССЗ', '18:30:40', '41°', 'СВ', '18:34:41', '10°', 'ВЮВ']

		# self.satellites = [Satellite(info)]
		self.satellites = Parser.get_satellites()
		# self.satellites = Parser.get_satellites()[:1]
		self.create_buttons()
		self.datePanel = DatePanel(self)

		self.delta_sec = 0
		self._view_coef = 1
		self.main_stars_button = MainStarsButton('./buttons/template.png', './buttons/template(onclick).png', 0, 0, self)
		self.main_stars_flag = False

	@property
	def view_coef(self):
		return self._view_coef

	@view_coef.setter
	def view_coef(self, value):
		if value < 1 or value > 5:
			return
		self._view_coef = value

	def get_stars(self):
		stars = []
		path = './data/'
		txt_files = [x for x in os.listdir(path) if x.endswith('.txt')]
		for name in txt_files:
			with open(path + name) as f:
				lines = f.readlines()
				for l in lines:
					s = Star(l, name[:-4])
					s.x, s.y = Geom.get_int_image_coords(s, 0, self.window_size, self.indent, self.indent)
					s.color = Drawer.get_color_for_pygame(s)
					s.radius = Drawer.get_radius_for_pygame(s)
					stars.append(s)
		return stars

	def create_buttons(self):
		# pygame.draw.rect(screen, BLACK, [150, 10, 50, 20])
		# self.right_btn = pygame.image.load('btn.png')
		btn_path = './buttons/template.png'
		btn_onclick_path = './buttons/template(onclick).png'
		# self.up = ChangeVieweButton(btn_path, btn_onclick_path, 100, 10, self, 'up', 1, 1)
		# self.down = ChangeVieweButton(btn_path, btn_onclick_path, 100, 50, self, 'down', 1, 1)
		self.right = ChangeVieweButton(btn_path, btn_onclick_path, 120, 30, self, 5*60, 1)
		self.left = ChangeVieweButton(btn_path, btn_onclick_path, 80, 30, self, -5*60, 1)

		self.zoom_plus = ChangeVieweButton(btn_path, btn_onclick_path, 170, 20, self, 0, 1.01)
		self.zoom_minus = ChangeVieweButton(btn_path, btn_onclick_path, 170, 50, self, 0, 0.99)
		self.buttons = [self.right, self.left, self.zoom_plus, self.zoom_minus]
		# self.buttons = [self.up, self.down, self.right, self.left, self.zoom_plus, self.zoom_minus]

	def create_time_info00(self):
		self.month = 0
		self.day = 0
		self.hour = 0
		self.minute = 0

	def create_datePanel(self):
		pass

	def Start(self):
		while True:
			self.screen.fill(Color.black)

			pressed = pygame.mouse.get_pressed()
			pos = pygame.mouse.get_pos()

			highlight_cons = ''
			for s in self.stars:
				if abs(s.x - pos[0]) < 5 and abs(s.y - pos[1]) < 5:
					highlight_cons = s.const_name
					# print(highlight_cons)
					self.draw_toolTip(highlight_cons)
					break

			for s in self.stars:
				if self.main_stars_flag and not s.label:
					continue # when draw only main stars
				self.draw_star(s, Color.grey)
				if highlight_cons and s.const_name == highlight_cons:
					self.draw_star(s, s.color)

			for sat in self.satellites:
				self.draw_satellite(sat)

			for b in self.buttons:
				# self.screen.blit(b.get_img(), (b.x, b.y))
				# update вызывает turn и возвращает картинку кнопки
				self.screen.blit(b.update(), (b.x, b.y))

			self.datePanel.second += 1
			self.datePanel.draw_on_screen(self.screen, self.indent, self.window_size+self.indent-150, False)


			for event in pygame.event.get():
					if event.type == QUIT:
							pygame.quit()
							sys.exit()
					if event.type == pygame.MOUSEBUTTONDOWN:
						#when would only one turn on one click
						if self.main_stars_button.on_click():
							self.main_stars_flag = not self.main_stars_flag
						# for b in self.buttons:
						# 	self.screen.blit(b.update(), (b.x, b.y))
						self.datePanel.draw_on_screen(self.screen, self.indent, self.window_size+self.indent-150, True)

			self.screen.blit(self.main_stars_button.get_img(), (self.main_stars_button.x, self.main_stars_button.y))
			pygame.display.update()
			self.fpsClock.tick(self.FPS)

	def draw_satellite(self, satellite):
		coords = satellite.get_int_image_coords(self.datePanel.time, self.window_size, self.indent, self.indent)
		if coords:

			pygame.draw.circle(self.screen, Color.red, coords, 5)
			font = pygame.font.SysFont('Georgia', 15)
			self.screen.blit(font.render(satellite.name, True, Color.red), coords)

	def draw_star(self, star, color):
		# print(star.x, star.y)
		# if abs(star.x)>self.window_size*2 or abs(star.y)>self.window_size*2:
		# 	return # костыль с увеличением координат ra 
		if star.x < self.indent or star.y < self.indent:
			return
		if star.radius == 1:
			pygame.draw.line(self.screen, color, [star.x, star.y], [star.x+1, star.y], 2)
		else:
			pygame.draw.circle(self.screen, color, [star.x, star.y], star.radius)

	def draw_toolTip(self, text):
		font = pygame.font.SysFont('Georgia', 15)
		# self.screen.blit(font.render(text, True, Color.white), (750, 100)) # в одном и том же углу 
		pos = pygame.mouse.get_pos()
		# pygame.draw.rect(self.screen, Color.white, [pos[0], pos[1], 20, 10])
		self.screen.blit(font.render(text, True, Color.white), [pos[0]+5, pos[1]+5])

	def create_observer_pos000(self):
		self.observer_lat = 0 # Latitude (-180, 180)
		self.observer_long = 0 # Longitude (-90, 90)

	def turn(self, delta_sec, view_coef=1):
		self.view_coef *= view_coef
		self.delta_sec += delta_sec
		# ra_angle = (24*60*60)/360
		# if side == 'right':
		# 		delta = seconds
		# elif side == 'left':
		# 		delta = -seconds
		# else:
		# 	return
		# 	raise Exception()
		self.change_view(self.delta_sec, self.view_coef)

	def change_view(self, delta_time, view_coef=1):
		for s in self.stars:
			# s.ra.full_sec += delta_ra
			# s.dec.full_sec += delta_dec
			coords = Geom.get_int_image_coords(s, delta_time, self.window_size, self.indent, self.indent)
			s.x, s.y = coords[0], coords[1]
			new_coords = Geom.get_resize_int_image_coords((s.x, s.y), self.window_size, view_coef)
			s.x, s.y = new_coords[0], new_coords[1]
			# s.move(*new_coords)

class ChangeVieweButton:
	def __init__(self, img, img_light, x1, y1, parent, delta_sec, view_coef):
		self.img = img
		self.img_onclick = img_light
		self.x = x1
		self.y = y1
		pic = pygame.image.load(self.img)
		self.x2 = pic.get_rect().size[0] + x1
		self.y2 = pic.get_rect().size[1] + y1
		self.parent = parent
		# self.direction = direction
		# self.angle = angle
		self.delta_sec = delta_sec
		self.view_coef = view_coef

		self.click_count = 0

	def on_click(self):
		mouse_pos = pygame.mouse.get_pos()
		mouse_pressed = pygame.mouse.get_pressed()
		if not mouse_pressed[0]:
			return False
		return (mouse_pos[0] > self.x and mouse_pos[0] < self.x2
			and mouse_pos[1] > self.y and mouse_pos[1] < self.y2)

	def on_enter(self):
		mouse_pos = pygame.mouse.get_pos()
		return (mouse_pos[0] > self.x and mouse_pos[0] < self.x2
			and mouse_pos[1] > self.y and mouse_pos[1] < self.y2)


	def get_img(self):
		if self.on_enter():
			return pygame.image.load(self.img_onclick)
		return pygame.image.load(self.img)

	def update(self):
		if self.on_click():
			self.click_count += 1
			self.parent.turn(self.delta_sec, self.view_coef)
			return pygame.image.load(self.img_onclick)
		return pygame.image.load(self.img)

	def draw(self):
		pass

class MainStarsButton:
	def __init__(self, img, img_light, x1, y1, parent):
		self.img = img
		self.img_onclick = img_light
		self.x = x1
		self.y = y1
		pic = pygame.image.load(self.img)
		self.x2 = pic.get_rect().size[0] + x1
		self.y2 = pic.get_rect().size[1] + y1
		self.parent = parent

	def on_click(self):
		mouse_pos = pygame.mouse.get_pos()
		mouse_pressed = pygame.mouse.get_pressed()
		if not mouse_pressed[0]:
			return False
		return (mouse_pos[0] > self.x and mouse_pos[0] < self.x2
			and mouse_pos[1] > self.y and mouse_pos[1] < self.y2)

	def on_enter(self):
		mouse_pos = pygame.mouse.get_pos()
		return (mouse_pos[0] > self.x and mouse_pos[0] < self.x2
			and mouse_pos[1] > self.y and mouse_pos[1] < self.y2)

	def get_img(self):
		if self.on_enter() or self.parent.main_stars_flag:
			return pygame.image.load(self.img_onclick)
		return pygame.image.load(self.img)

	def update(self):
		if self.on_click():
			return pygame.image.load(self.img_onclick)
		return pygame.image.load(self.img)

class DatePanel:
	def __init__(self, parent):
		self.heigh = 40
		self.width = parent.window_size
		self.parent = parent

		self.time = datetime.now() - timedelta(hours=5)
		# self._month = 1
		# self._day = 1
		# self._hour = 0
		# self._minute = 0
		# self._seconds = 0
		self.create_buttons()

	def create_buttons(self):
		full_round = 60*60*24
		self.btn_month = ChangeTimeButton(100, 100, self, full_round/12, 'month')
		self.btn_day = ChangeTimeButton(150, 100, self, full_round//365, 'day')
		self.btn_hour = ChangeTimeButton(200, 100, self, full_round/24, 'hour')
		self.btn_minute = ChangeTimeButton(250, 100, self, full_round/(24*60), 'minute')

		self.buttons = [self.btn_month, self.btn_day, self.btn_hour, self.btn_minute]

	def draw_on_screen(self, screen, x, y, mouse_pressed):
		font = pygame.font.SysFont('Georgia', 15)

		pygame.draw.rect(screen, Color.black, [x, y, self.width, self.heigh])
		y_text = y + self.heigh/2 - 10
		screen.blit(font.render('month: ', True, Color.white), [x+4, y_text])
		screen.blit(font.render(str(self.month), True, Color.white), [x+60, y_text])
		screen.blit(self.btn_month.update([x+80, y], mouse_pressed), [x+80, y])

		screen.blit(font.render('day: ', True, Color.white), [x+120, y_text])
		screen.blit(font.render(str(self.day), True, Color.white), [x+160, y_text])
		screen.blit(self.btn_day.update([x+180, y], mouse_pressed), [x+180, y])

		screen.blit(font.render('hour: ', True, Color.white), [x+210, y_text])
		screen.blit(font.render(str(self.hour), True, Color.white), [x+250, y_text])
		screen.blit(self.btn_hour.update([x+270, y], mouse_pressed), [x+270, y])

		screen.blit(font.render('minute: ', True, Color.white), [x+300, y_text])
		screen.blit(font.render(str(self.minute), True, Color.white), [x+360, y_text])
		screen.blit(self.btn_minute.update([x+380, y], mouse_pressed), [x+380, y])

		screen.blit(font.render('second: ', True, Color.white), [x+410, y_text])
		screen.blit(font.render(str(self.second), True, Color.white), [x+470, y_text])

		# screen.blit(b.update(), (b.x, b.y))

	# !! all setters works only for add 1
	@property
	def month(self):
		return self.time.month
	@month.setter
	def month(self, value):
		self.time = self.time + timedelta(months = value - self.month)
	@property
	def day(self):
		return self.time.day
	@day.setter
	def day(self, value):
		self.time = self.time + timedelta(days = value - self.day)
	@property
	def hour(self):
		return self.time.hour
	@hour.setter
	def hour(self, value):
		self.time = self.time + timedelta(hours = value - self.hour)
	@property
	def minute(self):
		return self.time.minute
	@minute.setter
	def minute(self, value):
		self.time = self.time + timedelta(minutes = value - self.minute)
	@property
	def second(self):
		return self.time.second
	@second.setter
	def second(self, value):
		self.parent.turn(-(value - self.second))
		self.time = self.time + timedelta(seconds = value - self.second)


class ChangeTimeButton:
	def __init__(self, x1, y1, panel, delta_sec, fieldname_to_change):
		self.img = './buttons/plus-minus.png'
		self.img_plus_onclick = './buttons/plus_onclick.png'
		self.img_minus_onclick = './buttons/minus_onclick.png'
		# self.x = x1
		# self.y = y1
		pic = pygame.image.load(self.img)
		self.heigh, self.width = pic.get_rect().size[1], pic.get_rect().size[0]
		# self.x2 = pic.get_rect().size[0] + x1
		# self.y2 = pic.get_rect().size[1] + y1
		self.panel = panel
		self.delta_sec = delta_sec
		self.field = fieldname_to_change

	def on_plus_click(self, btn_pos):
		mouse_pos = pygame.mouse.get_pos()
		mouse_pressed = pygame.mouse.get_pressed()
		x, y = btn_pos
		if not mouse_pressed[0]:
			return False
		return (mouse_pos[0] > x and mouse_pos[0] < x+self.width
			and mouse_pos[1] > y and mouse_pos[1] < y+self.heigh/2)

	def on_minus_click(self, btn_pos):
		mouse_pos = pygame.mouse.get_pos()
		mouse_pressed = pygame.mouse.get_pressed()
		x, y = btn_pos
		if not mouse_pressed[0]:
			return False
		return (mouse_pos[0] > x and mouse_pos[0] < x+self.width
			and mouse_pos[1] > y+self.heigh/2 and mouse_pos[1] < y+self.heigh)

	def on_plus_enter(self, btn_pos):
		mouse_pos = pygame.mouse.get_pos()
		x, y = btn_pos
		return (mouse_pos[0] > x and mouse_pos[0] < x+self.width
			and mouse_pos[1] > y and mouse_pos[1] < y+self.heigh/2)

	def on_minus_enter(self, btn_pos):
		mouse_pos = pygame.mouse.get_pos()
		x, y = btn_pos
		return (mouse_pos[0] > x and mouse_pos[0] < x+self.width
			and mouse_pos[1] > y+self.heigh/2 and mouse_pos[1] < y+self.heigh)

	def get_img(self):
		if self.on_enter():
			return pygame.image.load(self.img_onclick)
		return pygame.image.load(self.img)

	def update(self, btn_pos, mouse_pressed):
		if mouse_pressed:
			was = getattr(self.panel, self.field)
			if self.on_plus_click(btn_pos):
				setattr(self.panel, self.field, was+1)
				self.panel.parent.turn(-self.delta_sec, 1)
				return pygame.image.load(self.img_plus_onclick)
			if self.on_minus_click(btn_pos):
				setattr(self.panel, self.field, was-1)
				self.panel.parent.turn(self.delta_sec, 1)
				return pygame.image.load(self.img_minus_onclick)
		if self.on_plus_enter(btn_pos):
			return pygame.image.load(self.img_plus_onclick)
		if self.on_minus_enter(btn_pos):
			return pygame.image.load(self.img_minus_onclick)
		return pygame.image.load(self.img)

	def draw(self):
		pass


class Color:
	white = (255, 255, 255)
	black = (0, 0, 0)
	grey = (70, 70, 70)
	red = (130, 0, 0)


if __name__ == '__main__':
	app = PyGameApp()
	app.Start()



