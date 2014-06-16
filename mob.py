import pygame

class Mob(pygame.sprite.Sprite):
	def __init__(self, level, *groups):
		super(Mob, self).__init__(*groups)
		#the game level
		self.level = level
		
		#base image
		self.level.animator.set_Img(4,5)
		self.image = self.level.animator.get_Img().convert()
		self.image.set_colorkey((255,0,0))
		
		#type
		self.flavor = "Static"
		self.flavor_saver = ["Static", "Lemming", "Wanderer", "Charger"]
		
		#location
		self.firstflag = True
		self.mapx = 0 
		self.mapy = 0 
		self.scrnx = 0
		self.scrny = 0
		
		#status
		self.Turn_Over = False
		self.Alive = True
		self.AP_max = 4
		self.AP_c = 4
		self.APcost = {"U": 1, "D": 1, "L": 1, "R": 1, "UL":2, "UR": 2, "LL": 2, "LR":2, "Chop":3, "Plant": 3}
		
		
	def set_type(self, personality):
			self.flavor = self.flavor_saver[personality]
			if personality == 0:
				xind = 4
				yind = 5
			else:
				xind = 4
				yind = 5
			self.level.animator.set_Img(xind,yind)
			self.image = self.level.animator.get_Img().convert()
			self.image.set_colorkey((255,0,0))
		
	def spawn(self,x,y):
		self.scrnx = x
		self.mapx = x
		self.scrny = y
		self.mapy = y
		self.rect = pygame.rect.Rect((x * self.level.tilex, y * self.level.tiley), self.image.get_size())

	def spacecheck(self):
		for space in pygame.sprite.spritecollide(self, self.level.space, False):
			self.Alive = False
			self.kill()
		
	def command(self, cmd):
		if self.reckonAP(self.APcost[cmd]):
			if cmd == "U":
				self.move("U")
			if cmd == "D":
				self.move("D")
			if cmd == "L":
				self.move("L")
			if cmd == "R":
				self.move("R")
			if cmd == "UL":
				self.move("UL")
			if cmd == "UR":
				self.move("UR")
			if cmd == "LL":
				self.move("LL")
			if cmd == "LR":
				self.move("LR")
					
		else:
			pass	
			
		if self.AP_c <= 0:
			self.Turn_Over = True
			
		self.spacecheck()
		
				
	def move(self, vec):
		if vec == "U":
			self.mapy -= 1
			self.scrny -= 1
		if vec == "D":
			self.mapy += 1
			self.scrny += 1
		if vec == "L":
			self.set_Image('L')
			self.mapx -= 1
			self.scrnx -= 1
		if vec == "R":
			self.set_Image('R')
			self.mapx += 1
			self.scrnx += 1
		if vec == "UL":
			self.set_Image('L')
			self.mapy -= 1
			self.mapx -= 1
			self.scrny -= 1
			self.scrnx -= 1
		if vec == "UR":
			self.set_Image('R')
			self.mapy -= 1
			self.mapx += 1
			self.scrny -= 1
			self.scrnx += 1
		if vec == "LL":
			self.set_Image('L')
			self.mapy += 1
			self.mapx -= 1
			self.scrny += 1
			self.scrnx -= 1
		if vec == "LR":
			self.set_Image('R')
			self.mapy += 1
			self.mapx += 1
			self.scrny += 1
			self. scrnx += 1
		self.rect.x = self.mapx*self.level.tilex
		self.rect.y = self.mapy*self.level.tiley

	def reckonAP(self, cost):
		if self.AP_c >= cost:
			self.AP_c -= cost
			return True
		else:
			return False
	
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

	def take_turn(self):
		self.Turn_Over = False
		if self.flavor == "Static":
			self.Turn_Over = True
			return
			
