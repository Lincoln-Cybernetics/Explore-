import pygame
import ss


class Item(pygame.sprite.Sprite):
	def __init__(self, level, flav, *groups):
		super(Item, self).__init__(*groups)
		#self.image = pygame.image.load('gem.png')
		self.sheet = pygame.image.load('exp100.png').convert()
		self.animator = ss.Cutout(self.sheet, 100, 100)
		#self.animator.set_Img(6,0)
		#self.image = self.animator.get_Img().convert()
		#self.image.set_colorkey((255,0,0))
		self.level = level
		
		#self.flavor = 'default'
		self.flavor_saver = ['gem', 'axe']
		self.x = 0
		self.y = 0
		self.set_type(flav)
		#0 = gem
		#1 = axe
		
	def set_type(self, item):
		self.flavor = self.flavor_saver[item]
		if item == 0:
			xind = 6
			yind = 0
			self.flavor = 'gem'
		elif item == 1:
			xind = 6
			yind = 5
			self.flavor = 'axe'
		else:
			xind = 6
			yind = 0
			self.flavor = 'default'
		self.animator.set_Img(xind, yind)
		self.image = self.animator.get_Img().convert()
		self.image.set_colorkey((255,0,0))
		self.rect = pygame.rect.Rect((100,100), self.image.get_size())

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
