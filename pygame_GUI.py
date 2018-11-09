import pygame, sys
from pygame.locals import *
from drawer import *
from stars import *


class PyGameApp:
	def __init__(self):
		self.window_size = 1000
		pygame.init()
		self.FPS = 30
		self.fpsClock = pygame.time.Clock()

		pygame.display.set_caption('Stars')
		self.screen = pygame.display.set_mode((self.window_size+60, self.window_size+60), 0, 32)
		self.indent = 30 # отступ сверху и слева

		self.stars = PyGameApp.get_stars(self.window_size)
		self.create_buttons()

		self._view_coef = 1

	@property
	def view_coef(self):
		return self._view_coef

	@view_coef.setter
	def view_coef(self, value):
		if value < 1 or value > 5:
			return
		self._view_coef = value

	def get_stars(window_size):
		stars = []
		path = './data/'
		txt_files = [x for x in os.listdir(path) if x.endswith('.txt')]
		for name in txt_files:
			with open(path + name) as f:
				lines = f.readlines()
				for l in lines:
					s = Star(l, name[:-4])
					s.x, s.y = Geom.get_int_image_coords(s, window_size, 30, 30)
					s.color = Drawer.get_color_for_pygame(s)
					s.radius = Drawer.get_radius_for_pygame(s)
					stars.append(s)
		return stars

	def create_buttons(self):
		# pygame.draw.rect(screen, BLACK, [150, 10, 50, 20])
		# self.right_btn = pygame.image.load('btn.png')
		btn_path = './buttons/template.png'
		btn_onclick_path = './buttons/template(onclick).png'
		self.up = ChangeVieweButton(btn_path, btn_onclick_path, 100, 10, self, 'up', 1, 1)
		self.down = ChangeVieweButton(btn_path, btn_onclick_path, 100, 50, self, 'down', 1, 1)
		self.right = ChangeVieweButton(btn_path, btn_onclick_path, 120, 30, self, 'right', 1, 1)
		self.left = ChangeVieweButton(btn_path, btn_onclick_path, 80, 30, self, 'left', 1, 1)

		self.zoom_plus = ChangeVieweButton(btn_path, btn_onclick_path, 170, 20, self, 'left', 0, 1.01)
		self.zoom_minus = ChangeVieweButton(btn_path, btn_onclick_path, 170, 50, self, 'left', 0, 0.99)

		self.buttons = [self.up, self.down, self.right, self.left, self.zoom_plus, self.zoom_minus]

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
				self.draw_star(s, Color.grey)
				if highlight_cons and s.const_name == highlight_cons:
					self.draw_star(s, s.color)

			for b in self.buttons:
				# self.screen.blit(b.get_img(), (b.x, b.y))
				self.screen.blit(b.update(), (b.x, b.y))

			for event in pygame.event.get():
					if event.type == QUIT:
							pygame.quit()
							sys.exit()
					if event.type == pygame.MOUSEBUTTONDOWN:
						pass #when would only one turn on one click
						for b in self.buttons:
							self.screen.blit(b.update(), (b.x, b.y))

			print('day:', self.right.click_count-self.left.click_count)

			pygame.display.update()
			self.fpsClock.tick(self.FPS)

	def draw_star(self, star, color):
		# print(star.x, star.y)
		if abs(star.x)>self.window_size*2 or abs(star.y)>self.window_size*2:
			return # костыль с увеличением координат ra 
		if star.x < self.indent or star.y < self.indent:
			return
		if star.radius == 1:
			pygame.draw.line(self.screen, color, [star.x, star.y], [star.x+1, star.y], 2)
		else:
			pygame.draw.circle(self.screen, color, [star.x, star.y], star.radius)

	def draw_toolTip(self, text):
		font = pygame.font.SysFont('Arial', 18)
		# self.screen.blit(font.render(text, True, Color.white), (750, 100)) # в одном и том же углу 
		pos = pygame.mouse.get_pos()
		# pygame.draw.rect(self.screen, Color.white, [pos[0], pos[1], 20, 10])
		self.screen.blit(font.render(text, True, Color.white), [pos[0]+5, pos[1]+5])

	def create_observer_pos(self):
		self.observer_lat = 0 # Latitude (-180, 180)
		self.observer_long = 0 # Longitude (-90, 90)

	def turn(self, side, angle=1, view_coef=1):
		self.view_coef *= view_coef
		ra_angle = (24*60*60)/360
		dec_angle = (60*60*180)/360
		if side == 'right':
				delta = (angle*ra_angle, 0)
		elif side == 'left':
				delta = (-angle*ra_angle, 0)
		elif side == 'up':
				delta = (0, -angle*dec_angle)
		elif side == 'down':
				delta = (0, angle*dec_angle)
		else:
			raise Exception()
		self.change_view(*delta, self.view_coef)

	def change_view(self, delta_ra, delta_dec, view_coef=1):
		for s in self.stars:
			s.ra.full_sec += delta_ra
			s.dec.full_sec += delta_dec
			coords = Geom.get_int_image_coords(s, self.window_size, self.indent, self.indent)
			s.x, s.y = coords[0], coords[1]
			new_coords = Geom.get_resize_int_image_coords((s.x, s.y), SIZE, view_coef)
			s.x, s.y = new_coords[0], new_coords[1]
			# s.move(*new_coords)

	def init_time(self):
		self.month = 0
		self.day = 0
		self.hour = 0
		self.minute = 0

	def update_time_information(self):
		pass


class ChangeVieweButton:
	def __init__(self, img, img_light, x1, y1, parent, direction, angle, view_coef):
		self.img = img
		self.img_onclick = img_light
		self.x = x1
		self.y = y1
		pic = pygame.image.load(self.img)
		self.x2 = pic.get_rect().size[0] + x1
		self.y2 = pic.get_rect().size[1] + y1
		self.parent = parent
		self.direction = direction
		self.angle = angle
		self.view_coef = view_coef

		self.click_count = 0

	def check_on_click000(self, mouse_pos, mouse_pressed):
		if not mouse_pressed[0]:
			return False
		return (mouse_pos[0] > self.x1 and mouse_pos[0] < self.x2
			and mouse_pos[1] > self.y1 and mouse_pos[1] < self.y2)

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
			self.parent.turn(self.direction, self.angle, self.view_coef)
			return pygame.image.load(self.img_onclick)
		return pygame.image.load(self.img)




	def draw(self):
		pass


class DatePanel:
	pass

class Color:
	white = (255, 255, 255)
	black = (0, 0, 0)
	grey = (70, 70, 70)


if __name__ == '__main__':
	app = PyGameApp()
	app.Start()



