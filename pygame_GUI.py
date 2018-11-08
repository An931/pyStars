import pygame, sys
from pygame.locals import *
from drawer import *
from stars import *


class PyGameApp:
	def __init__(self):
		self.window_size = 1000
		pygame.init()
		self.FPS = 30 # frames per second setting
		self.fpsClock = pygame.time.Clock()
		pygame.display.set_caption('Stars')

		# set up the window
		self.screen = pygame.display.set_mode((self.window_size, self.window_size), 0, 32)

		catImg = pygame.image.load('cat.png')
		catx = 10
		caty = 10
		direction = 'right'



		self.constellations = Constellation.get_constellations()
		self.stars = self.get_all_stars()
		Drawer.add_draw_parametrs_for_pygame(self.stars, self.window_size)
		# self.create_buttons()

	def Start(self):
		while True: # the main game loop
			self.screen.fill(Color.black)

			pos = pygame.mouse.get_pos()
			# print(pos)
			# pygame.draw.line(self.screen, (  0, 255,   0), [0, 0], pos, 5)
			# pygame.draw.circle(self.screen, (  255,  0, 0), pos, 6)

			for s in self.stars:
				pygame.draw.circle(self.screen, Color.grey, [s.x, s.y], s.radius)
				if abs(s.x - pos[0]) < 3 and abs(s.y - pos[1]) < 3:
					print(pos)
					const = s.const_name
					# pygame.draw.rect(screen, BLACK, [150, 10, 50, 20])
					for s1 in self.stars:
						if s1.const_name == const:
							# pygame.draw.circle(self.screen, (  255,   0, 0), [s1.x, s1.y], 2)
							pygame.draw.circle(self.screen, s1.color, [s1.x, s1.y], s1.radius)
						else:
							pass
							# pygame.draw.circle(self.screen, s1.color, [s1.x, s1.y], 2)
							pygame.draw.circle(self.screen, Color.grey, [s1.x, s1.y], s1.radius)

			# self.screen.blit(catImg, (catx, caty))

			for event in pygame.event.get():
					if event.type == QUIT:
							pygame.quit()
							sys.exit()
			pygame.display.update()
			self.fpsClock.tick(self.FPS)

	def draw_star(self):
			pass

	def create_buttons():
		# pygame.draw.rect(screen, BLACK, [150, 10, 50, 20])
		self.right_btn = ()


	def get_stars00():
			stars = []
			path = './data/'
			txt_files = [x for x in os.listdir(path) if x.endswith('.txt')]
			for name in txt_files:
					with open(path + name) as f:
							lines = f.readlines()
							for l in lines:
									s = Star(l, name)
									s.x, s.y = Geom.get_int_image_coords(s, 1000)
									s.color = Drawer.get_color_for_pygame(s)
									s.radius = Drawer.get_radius_for_pygame(s)
									stars.append(s)
			return stars

	def get_all_stars(self):
		stars = []
		for cons in self.constellations:
			for s in cons.stars:
				stars.append(s)
		return stars


class PyGameButton00:
	def __init__(self):
		pass

	def draw(self):
		pass


class Color:
	white = (255, 255, 255)
	black = (0, 0, 0)
	grey = (70, 70, 70)

if __name__ == '__main__':
	app = PyGameApp()
	app.Start()



