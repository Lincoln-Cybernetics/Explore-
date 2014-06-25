import pygame

class Land(pygame.sprite.Sprite):
	def __init__(self, level, *groups):
		super(Land, self).__init__(*groups)
		#the game level
		self.level = level
		#base image
		self.level.animator.set_Img(0,5)
		self.image = self.level.animator.get_Img().convert()
		
		#self.revealed = False
		#location
		self.mapx = 0 
		self.mapy = 0 
		self.scrnx = 0
		self.scrny = 0
		
		#harvestable
		self.woodpoints = 0
		
		#type
		self.flavor_saver = ["Void", "Grassland", "Grass and Trees", "Light Woods", "Medium Woods", "Dense Woods", "Hills", "Scrub", "Dunes",\
			"Gravel", "Mountain", "Extinct Volcano", "Active Volcano", "Water", "Ocean", "Whirlpool","Oasis"]
		
		self.AP_markup = {"Void":0, "Grassland":0, "Grass and Trees":0, "Light Woods":1, "Medium Woods":2, "Dense Woods":3, "Hills":1, "Scrub":1, "Dunes":2,\
			"Gravel":1, "Mountain":2, "Extinct Volcano":3, "Active Volcano":2, "Water":2, "Ocean":3, "Whirlpool":2, "Oasis":2}	
		
		self.AP_cost = 0
		self.flavor = "Void"
		self.flavnum = 0

	def spawn(self,x,y):
		self.mapx = x
		self.mapy = y
		self.scrnx = x
		self.scrny = y
		self.rect = pygame.rect.Rect((x * self.level.tilex, y * self.level.tiley), self.image.get_size())
		
	
		
	def set_type(self, land):
		self.flavor = self.flavor_saver[land]
		self.flavnum = land
		#Void
		if land == 0:
			xind = 0
			yind = 5
		#Grassland
		if land == 1:
			xind = 0
			yind = 0
		#Grassland and Trees
		if land == 2:
			xind = 0
			yind = 2
			self.woodpoints = 1
		#Light Woods
		if land == 3:
			xind = 4
			yind = 0
			self.woodpoints = 2
		#Medium Woods
		if land == 4:
			xind = 4
			yind = 1
			self.woodpoints = 3
		#Dense Woods
		if land == 5:
			xind = 4
			yind = 2
			self.woodpoints = 4
		#Hills
		if land == 6:
			xind = 0
			yind = 1
		#Scrub
		if land == 7:
			xind = 1
			yind = 0
		#Dunes
		if land == 8:
			xind = 1
			yind = 1
		#Gravel
		if land == 9:
			xind = 2
			yind = 0
		#Mountain
		if land == 10:
			xind = 2
			yind = 1
		#Extinct Volcano
		if land == 11:
			xind = 2
			yind = 2
		#Active Volcano
		if land == 12:
			xind = 2
			yind = 3
		#Water
		if land == 13:
			xind = 3
			yind = 0
		#Ocean
		if land == 14:
			xind = 3
			yind = 1
		#Whirlpool
		if land == 15:
			xind = 3
			yind = 2
		#Oasis
		if land == 16:
			xind = 1
			yind = 2
		self.level.animator.set_Img(xind,yind)
		self.image = self.level.animator.get_Img().convert()
		self.AP_cost = self.AP_markup[self.flavor]
		
	def fade(self):
		self.level.animator.set_Img(0,5)
		fadeimg = self.level.animator.get_Img().convert()
		fadeimg.set_alpha(128)
		self.image.blit(fadeimg, (0,0))
		
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
