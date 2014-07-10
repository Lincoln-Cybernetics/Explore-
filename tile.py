import pygame
import random


class Land(pygame.sprite.Sprite):
	def __init__(self, level, *groups):
		super(Land, self).__init__(*groups)
		#the game level
		self.level = level
		#base image
		self.xind = 0
		self.yind = 5
		self.level.animator.set_Img(self.xind,self.yind)
		self.image = self.level.animator.get_Img().convert()
		self.hidden = self.image
		self.fog = False
		
		
		#spritegroups
		self.neighbors = pygame.sprite.Group()
		
		#location
		self.mapx = 0 
		self.mapy = 0 
		self.scrnx = 0
		self.scrny = 0
		
		#forests
		self.wood_level = 0
		self.wp = random.randrange(300)#random progress toward state change
		self.forest_prone = False
		self.forest_thresh = {"Grassland" : 400, "Grass and Trees" :200, "Scrub": 800, "Light Woods": 400, "Medium Woods": 400}
		self.forest_conv = {"Grassland" : 2, "Grass and Trees" : 3, "Scrub": 1, "Light Woods": 4, "Medium Woods": 5}
		
		#deserts
		self.desert_level = 0
		self.dp = random.randrange(300)#random progress toward state change
		self.desert_prone = False
		self.desert_thresh = { "Grassland" : 400, "Grass and Trees" : 600, "Scrub": 200, "Water": 800, "Oasis": 600}
		self.desert_conv = { "Grassland" : 7, "Grass and Trees" : 1, "Scrub": 8, "Water": 16, "Oasis": 8}
		
		
		
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
		
	def reset(self):
		
		self.dp = 0
		self.wp = 0
		
	def set_type(self, land):
		self.flavor = self.flavor_saver[land]
		self.flavnum = land
		self.desert_prone = False
		self.forest_prone = False
		#Void
		if land == 0:
			self.xind = 0
			self.yind = 5
			self.AP_cost = 0
		#Grassland
		if land == 1:
			self.xind = 0
			self.yind = 0
			self.AP_cost = 0
			self.desert_prone = True
			self.forest_prone = True
		#Grassland and Trees
		if land == 2:
			self.xind = 0
			self.yind = 2
			self.AP_cost = 0
			self.wood_level = 1
			self.desert_prone = True
			self.forest_prone = True
		#Light Woods
		if land == 3:
			self.xind = 4
			self.yind = 0
			self.AP_cost = 1
			self.wood_level = 2
			self.forest_prone = True
		#Medium Woods
		if land == 4:
			self.xind = 4
			self.yind = 1
			self.AP_cost = 2
			self.wood_level = 3
			self.forest_prone = True
		#Dense Woods
		if land == 5:
			self.xind = 4
			self.yind = 2
			self.AP_cost = 3
			self.wood_level = 4
		#Hills
		if land == 6:
			self.xind = 0
			self.yind = 1
			self.AP_cost = 1
		#Scrub
		if land == 7:
			self.xind = 1
			self.yind = 0
			self.AP_cost = 1
			self.desert_level = 1
			self.desert_prone = True
			self.forest_prone = True
		#Dunes
		if land == 8:
			self.xind = 1
			self.yind = 1
			self.AP_cost = 2
			self.desert_level = 2
		#Gravel
		if land == 9:
			self.xind = 2
			self.yind = 0
			self.AP_cost = 1
		#Mountain
		if land == 10:
			self.xind = 2
			self.yind = 1
			self.AP_cost = 2
		#Extinct Volcano
		if land == 11:
			self.xind = 2
			self.yind = 2
			self.AP_cost = 2
		#Active Volcano
		if land == 12:
			self.xind = 2
			self.yind = 3
			self.AP_cost = 3
		#Water
		if land == 13:
			self.xind = 3
			self.yind = 0
			self.AP_cost = 2
			self.desert_level = -6
			self.desert_prone = True
		#Ocean
		if land == 14:
			self.xind = 3
			self.yind = 1
			self.AP_cost = 3
		#Whirlpool
		if land == 15:
			self.xind = 3
			self.yind = 2
			self.AP_cost = 4
		#Oasis
		if land == 16:
			self.xind = 1
			self.yind = 2
			self.AP_cost = 2
			self.desert_level = 1
			self.desert_prone = True
			
		
		
	def get_image(self):
		self.level.animator.set_Img(self.xind,self.yind)
		self.image = self.level.animator.get_Img().convert()
		if self.fog == True:
			self.level.animator.set_Img(0,5)
			fadeimg = self.level.animator.get_Img().convert()
			fadeimg.set_alpha(128)
			self.image.blit(fadeimg, (0,0))
		
	def fade(self):
		if self.fog == False:
			self.fog = True
			self.get_image()
			
		
	def visify(self):
		self.fog = False
		self.get_image()
		
		
	def desert_check(self):
		if self.desert_prone:
			for zone in self.neighbors:
				self.dp += zone.desert_level
				
	def forest_check(self):
		if self.forest_prone:
			for zone in self.neighbors:
				self.wp += zone.wood_level
				
								
	def advance(self):
		if self.desert_prone and self.forest_prone:
			if self.dp > self.desert_thresh[self.flavor] and self.wp > self.forest_thresh[self.flavor]:
				self.reset()
				return
		if self.desert_prone:
			if self.dp > self.desert_thresh[self.flavor]:
				self.set_type(self.desert_conv[self.flavor])
				self.reset()
		if self.forest_prone:
			if self.wp > self.forest_thresh[self.flavor]:
				self.set_type(self.forest_conv[self.flavor])
				self.reset()
		#self.get_image()		
		
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
		self.get_image()
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
		self.level.mymap[self.mapx][self.mapy].get_image()
		self.level.mymap[self.mapx+1][self.mapy].set_type(self.tertype[self.flavnum])
		self.level.mymap[self.mapx+1][self.mapy].get_image()
		self.level.mymap[self.mapx][self.mapy+1].set_type(self.tertype[self.flavnum])
		self.level.mymap[self.mapx][self.mapy+1].get_image()
		self.level.mymap[self.mapx+1][self.mapy+1].set_type(self.tertype[self.flavnum])
		self.level.mymap[self.mapx+1][self.mapy+1].get_image()
		
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
