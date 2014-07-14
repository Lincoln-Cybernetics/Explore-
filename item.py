import pygame

class Item(pygame.sprite.Sprite):
	def __init__(self, level, *groups):
		super(Item, self).__init__(*groups)
		#the game level
		self.level = level
		#base image
		self.level.animator.set_Img(6,0)
		self.level.animator.set_colorkey((255,0,0))
		self.image = self.level.animator.get_Img().convert()
		
		
		#type
		self.flavor_saver = ['gem', 'axe', 'sammich', 'telescope', 'canteen']
		self.flavor = 'gem'
		#location
		self.firstflag = True
		self.scrnx = 0
		self.scrny = 0
		self.mapx = 0
		self.mapy = 0
		
	def spawn(self,x,y):
		self.mapx = x
		self.mapy = y
		self.level.mymap[self.mapx][self.mapy].set_type(self.level.get_passable())
		self.level.player1.unpassable.remove(self.level.mymap[self.mapx][self.mapy])
		
	def position(self,x,y):
		self.scrnx = x
		self.scrny = y
		self.rect = pygame.rect.Rect((self.scrnx*self.level.tilex, self.scrny*self.level.tiley), self.image.get_size())
	
	def set_type(self, itype):
		self.flavor = self.flavor_saver[itype]
		if itype == 0:
			xind = 6
			yind = 0
		if itype == 1:
			xind = 6
			yind = 5
		if itype == 2:
			xind = 6
			yind = 4
		if itype == 3:
			xind = 6
			yind = 3
		if itype == 4:
			xind = 4
			yind = 4
			
		self.level.animator.set_Img(xind,yind)
		self.level.animator.set_colorkey(True,(255,0,0))
		self.image = self.level.animator.get_Img().convert()
	


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
		
	def draw(self):
		self.level.screen.blit(self.image, (self.rect.x,self.rect.y))
