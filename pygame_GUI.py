import pygame, sys
from pygame.locals import *
from drawer import *
from stars import *


class PyGameApp:
	def __init__(self):
		self.window_size = 1000
		pygame.init()
		self.FPS = 5 # frames per second setting
		self.fpsClock = pygame.time.Clock()
		pygame.display.set_caption('Stars')

		# set up the window
		self.screen = pygame.display.set_mode((self.window_size, self.window_size), 0, 32)

		catImg = pygame.image.load('cat.png')
		catx = 10
		caty = 10
		direction = 'right'

		self.stars = PyGameApp.get_stars()
		# self.create_buttons()

	def Start(self):
		while True: # the main game loop
			self.screen.fill(Color.black)

			highlight_cons = ''
			pos = pygame.mouse.get_pos()
			for s in self.stars:
				if abs(s.x - pos[0]) < 5 and abs(s.y - pos[1]) < 5:
					highlight_cons = s.const_name
					print(highlight_cons)
					continue

			for s in self.stars:
				pygame.draw.circle(self.screen, Color.grey, [s.x, s.y], s.radius)
				if highlight_cons and s.const_name == highlight_cons:
					pygame.draw.circle(self.screen, s.color, [s.x, s.y], s.radius)


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


	def get_stars():
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

	def get_all_stars00(self):
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



