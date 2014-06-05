import pygame


class Item(pygame.sprite.Sprite):
	def __init__(self, level, *groups):
		super(Item, self).__init__(*groups)
		self.image = pygame.image.load('gem.png')
		self.level = level
		self.rect = pygame.rect.Rect((100,100), self.image.get_size())
		self.flavor = 'gem'
		self.x = 0
		self.y = 0
		


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
