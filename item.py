import pygame

class Item(pygame.sprite.Sprite):
	def __init__(self, level, *groups):
		super(Item, self).__init__(*groups)
		#the game level
		self.level = level
		#base image
		self.level.animator.set_Img(6,0)
		self.image = self.level.animator.get_Img().convert()
		self.image.set_colorkey((255,0,0))
		
		#type
		self.flavor_saver = ['gem', 'axe']
		self.flavor = 'gem'
		#location
		self.firstflag = True
		self.scrnx = 0
		self.scrny = 0
		self.mapx = 0
		self.mapy = 0
		
	def spawn(self,x,y):
		self.scrnx = x
		self.scrny = y
		if self.firstflag:
			self.mapx = x
			self.mapy = y
			self.firstflag = False
		self.rect = pygame.rect.Rect((x * self.level.tilex, y * self.level.tiley), self.image.get_size())
	
	def set_type(self, itype):
		self.flavor = self.flavor_saver[itype]
		if itype == 0:
			xind = 6
			yind = 0
		if itype == 1:
			xind = 6
			yind = 5
			
		self.level.animator.set_Img(xind,yind)
		self.image = self.level.animator.get_Img().convert()
		self.image.set_colorkey((255,0,0))

	def set_Index(self, x, y):
		self.scrnx = x
		self.rect.x = x*self.level.tilex
		self.scrny = y
		self.rect.y = y*self.level.tiley
		
	def get_Index(self, axis):
		if axis == 'X':
			return self.scrnx
		if axis == 'Y':
			return self.scrny
		return -1
