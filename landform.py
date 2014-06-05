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
		
	def set_Biome(self, land):
		if land == 'Plain':
			xind = 0
			yind = 0
		if land == 'Hill':
			xind = 0
			yind = 1
		if land == 'Scrub':
			xind = 1
			yind = 0
		if land == 'Dunes':
			xind = 1
			yind = 1
		if land == 'Gravel':
			xind = 2
			yind = 0
		if land == 'Mountain':
			xind = 2
			yind = 1
		if land == 'Extinct Volcano':
			xind = 2
			yind = 2
		if land == 'Active Volcano':
			xind = 2
			yind = 3
		if land == 'Shallows':
			xind = 3
			yind = 0
		if land == 'Ocean':
			xind = 3
			yind = 1
		if land == 'Whirlpool':
			xind = 3
			yind = 2
		if land == 'Light Woods':
			xind = 4
			yind = 0
		if land == 'Med Woods':
			xind = 4
			yind = 1
		if land == 'Dense Woods':
			xind = 4
			yind = 2
		self.animator.set_Img(xind, yind)
		self.image = self.animator.get_Img().convert()
		
	def populate(self, img):
		self.image.blit(img, (0,0), pygame.rect(0,0,100,100)).convert()
		
	def unpopulate(self):
		self.image = animator.get_Img().convert()
		
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
