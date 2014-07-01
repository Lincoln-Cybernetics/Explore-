import pygame


class Land(pygame.sprite.Sprite):
	def __init__(self, level, *groups):
		super(Land, self).__init__(*groups)
		#the game level
		self.level = level
		#base image
		self.level.animator.set_Img(0,5)
		self.image = self.level.animator.get_Img().convert()
		
		
		#spritegroups
		self.neighbors = pygame.sprite.Group()
		
		#location
		self.mapx = 0 
		self.mapy = 0 
		self.scrnx = 0
		self.scrny = 0
		
		#harvestable
		self.wood_level = 0
		
		#desertification
		self.desert_level = 0
		self.desert_points = 0
		
		#type
		self.flavor_saver = ["Void", "Grassland", "Grass and Trees", "Light Woods", "Medium Woods", "Dense Woods", "Hills", "Scrub", "Dunes",\
			"Gravel", "Mountain", "Extinct Volcano", "Active Volcano", "Water", "Ocean", "Whirlpool","Oasis"]
		
	
		
		self.AP_cost = 0
		self.flavor = "Void"
		self.flavnum = 0

	def spawn(self,x,y):
		self.mapx = x
		self.mapy = y
		self.scrnx = x
		self.scrny = y
		self.rect = pygame.rect.Rect((x * self.level.tilex, y * self.level.tiley), self.image.get_size())
		
	
		
	def set_type(self, land, reset= False):
		self.flavor = self.flavor_saver[land]
		self.flavnum = land
		if reset:
			self.desert_points = 0
		#Void
		if land == 0:
			xind = 0
			yind = 5
			self.AP_cost = 0
		#Grassland
		if land == 1:
			xind = 0
			yind = 0
			self.AP_cost = 0
		#Grassland and Trees
		if land == 2:
			xind = 0
			yind = 2
			self.AP_cost = 0
			self.wood_level = 1
		#Light Woods
		if land == 3:
			xind = 4
			yind = 0
			self.AP_cost = 1
			self.wood_level = 2
		#Medium Woods
		if land == 4:
			xind = 4
			yind = 1
			self.AP_cost = 2
			self.wood_level = 3
		#Dense Woods
		if land == 5:
			xind = 4
			yind = 2
			self.AP_cost = 3
			self.wood_level = 4
		#Hills
		if land == 6:
			xind = 0
			yind = 1
			self.AP_cost = 1
		#Scrub
		if land == 7:
			xind = 1
			yind = 0
			self.AP_cost = 1
			self.desert_level = 1
		#Dunes
		if land == 8:
			xind = 1
			yind = 1
			self.AP_cost = 2
			self.desert_level = 2
		#Gravel
		if land == 9:
			xind = 2
			yind = 0
			self.AP_cost = 1
		#Mountain
		if land == 10:
			xind = 2
			yind = 1
			self.AP_cost = 2
		#Extinct Volcano
		if land == 11:
			xind = 2
			yind = 2
			self.AP_cost = 2
		#Active Volcano
		if land == 12:
			xind = 2
			yind = 3
			self.AP_cost = 3
		#Water
		if land == 13:
			xind = 3
			yind = 0
			self.AP_cost = 2
			self.desert_level = -6
		#Ocean
		if land == 14:
			xind = 3
			yind = 1
			self.AP_cost = 3
		#Whirlpool
		if land == 15:
			xind = 3
			yind = 2
			self.AP_cost = 4
		#Oasis
		if land == 16:
			xind = 1
			yind = 2
			self.AP_cost = 2
			self.desert_level = 1
			
		self.level.animator.set_Img(xind,yind)
		self.image = self.level.animator.get_Img().convert()
		#self.AP_cost = self.AP_markup[self.flavor]
		
	def fade(self):
		
		self.level.animator.set_Img(0,5)
		fadeimg = self.level.animator.get_Img().convert()
		fadeimg.set_alpha(128)
		self.image.blit(fadeimg, (0,0))
		
	def inc_dp(self, num):
		self.desert_points += num
		
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

class Landmark(pygame.sprite.Sprite):
	def __init__(self, level, *groups):
		super(Landmark, self).__init__(*groups)
		#the game level
		self.level = level
		
		#base image
		self.level.landgrabber.set_Img(0,0)
		self.level.landgrabber.set_colorkey((255,0,0))
		self.image = self.level.landgrabber.get_Img().convert()
		
	
		#location
		self.mapx = 0 
		self.mapy = 0 
		self.scrnx = 0
		self.scrny = 0
		
		#flavor
		self.flavor = "Pyramid"
		self.flavnum = 0
		self.flavor_saver = ["Pyramid","Henge"]
		self.tertype = {0:8, 1:1}
		
		
	
	def spawn(self,x,y):
		self.mapx = x
		self.mapy = y
		self.scrnx = x
		self.scrny = y
		self.rect = pygame.rect.Rect((x * self.level.tilex, y * self.level.tiley), self.image.get_size())
		self.level.mymap[self.mapx][self.mapy].set_type(self.tertype[self.flavnum])
		self.level.mymap[self.mapx+1][self.mapy].set_type(self.tertype[self.flavnum])
		self.level.mymap[self.mapx][self.mapy+1].set_type(self.tertype[self.flavnum])
		self.level.mymap[self.mapx+1][self.mapy+1].set_type(self.tertype[self.flavnum])
		
	def position(self,x,y):
		self.scrnx = x
		self.scrny = y
		self.rect = pygame.rect.Rect((self.scrnx*self.level.tilex, self.scrny*self.level.tiley), self.image.get_size())
		
	def set_type(self, land):
		self.flavor = self.flavor_saver[land]
		self.flavnum = land
		xind = 0
		yind = 0
		#Pyramid
		if land == 0:
			xind = 0
			yind = 0
		#Henge
		if land == 1:
			xind = 1
			yind = 0
			
		
		
		self.level.landgrabber.set_Img(xind,yind)
		self.level.landgrabber.set_colorkey((255,0,0))
		self.image = self.level.landgrabber.get_Img().convert()
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

	def draw(self):
		self.level.screen.blit(self.image, (self.rect.x,self.rect.y))
