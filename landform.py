import pygame
import ss

class Acre(pygame.sprite.Sprite):
	def __init__(self, level, *groups):
		super(Acre, self).__init__(*groups)
		self.sheet = pygame.image.load('exp100.png').convert()
		self.animator = ss.Cutout(self.sheet, 100, 100)
		self.animator.set_Img(0,0)
		self.image = self.animator.get_Img().convert()
		self.rect = pygame.rect.Rect((0,0), self.image.get_size())
		self.level = level
		self.x = 0
		self.y = 0
		self.flavor = 'Plain'
		self.flavor_saver = [ 'Plain', 'Plain with Trees', 'Hill', 'Scrub', 'Dunes', 'Gravel', 'Mountain',\
			'Extinct Volcano', 'Active Volcano', 'Shallows', 'Ocean', 'Whirlpool',  'Light Woods', 'Medium Woods',\
			'Dense Woods']
		
	def set_Biome(self, land):
		self.flavor = self.flavor_saver[land]
		land = self.flavor
		if land == 'Plain':
			xind = 0
			yind = 0
		elif land == 'Plain with Trees':
			xind = 0
			yind = 2
		elif land == 'Hill':
			xind = 0
			yind = 1
		elif land == 'Scrub':
			xind = 1
			yind = 0
		elif land == 'Dunes':
			xind = 1
			yind = 1
		elif land == 'Gravel':
			xind = 2
			yind = 0
		elif land == 'Mountain':
			xind = 2
			yind = 1
		elif land == 'Extinct Volcano':
			xind = 2
			yind = 2
		elif land == 'Active Volcano':
			xind = 2
			yind = 3
		elif land == 'Shallows':
			xind = 3
			yind = 0
		elif land == 'Ocean':
			xind = 3
			yind = 1
		elif land == 'Whirlpool':
			xind = 3
			yind = 2
		elif land == 'Light Woods':
			xind = 4
			yind = 0
		elif land == 'Medium Woods':
			xind = 4
			yind = 1
		elif land == 'Dense Woods':
			xind = 4
			yind = 2
		else:
			xind = 0
			yind = 0
		self.animator.set_Img(xind, yind)
		self.image = self.animator.get_Img().convert()
		
		
	def set_Index(self, x, y):
		self.x = x
		self.rect.x = x*100
		self.y = y
		self.rect.y = y*100 
		
	def get_Index(self, axis):
		if axis == 'X':
			return self.x
		if axis == 'Y':
			return self.y
		return -1

	def update(self):
		pass
		
