import pygame

class Land(pygame.sprite.Sprite):
	def __init__(self, level, *groups):
		super(Land, self).__init__(*groups)
		#the game level
		self.level = level
		#base image
		self.level.animator.set_Img(0,5)
		self.image = self.level.animator.get_Img().convert()
		self.secretimage = self.level.animator.get_Img().convert()
		self.image.set_colorkey((255,0,0))
		self.revealed = False
		#location
		self.firstflag = True
		self.mapx = 0 
		self.mapy = 0 
		self.scrnx = 0
		self.scrny = 0
		
		#type
		self.flavor_saver = ["Void", "Grassland", "Grass and Trees", "Light Woods", "Medium Woods", "Dense Woods", "Hills", "Scrub", "Dunes",\
			"Gravel", "Mountain", "Extinct Volcano", "Active Volcano", "Water", "Ocean", "Whirlpool"]
		self.flavor = "Void"

	def spawn(self,x,y):
		if self.firstflag:
			self.mapx = x
			self.mapy = y
			firstflag = False
		self.scrnx = x
		self.scrny = y
		self.rect = pygame.rect.Rect((x * self.level.tilex, y * self.level.tiley), self.image.get_size())
		
	def reveal(self):
		self.image = self.secretimage
		self.revealed = True
		
	def set_type(self, land):
		self.flavor = self.flavor_saver[land]
		if land == 0:
			xind = 0
			yind = 5
		if land == 1:
			xind = 0
			yind = 0
		if land == 2:
			xind = 0
			yind = 2
		if land == 3:
			xind = 4
			yind = 0
		if land == 4:
			xind = 4
			yind = 1
		if land == 5:
			xind = 4
			yind = 2
		if land == 6:
			xind = 0
			yind = 1
		if land == 7:
			xind = 1
			yind = 0
		if land == 8:
			xind = 1
			yind = 1
		if land == 9:
			xind = 2
			yind = 0
		if land == 10:
			xind = 2
			yind = 1
		if land == 11:
			xind = 2
			yind = 2
		if land == 12:
			xind = 2
			yind = 3
		if land == 13:
			xind = 3
			yind = 0
		if land == 14:
			xind = 3
			yind = 1
		if land == 15:
			xind = 3
			yind = 2
		self.level.animator.set_Img(xind,yind)
		self.secretimage = self.level.animator.get_Img().convert()
		
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
