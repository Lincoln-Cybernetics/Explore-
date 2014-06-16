import pygame

class Player(pygame.sprite.Sprite):
	def __init__(self, level, *groups):
		super(Player, self).__init__(*groups)
		#the game level
		self.level = level
		#base image
		self.set_Image('R')
		self.scrnx = 0
		self.mapx = 0
		self.scrny = 0
		self.mapy = 0
		#item inventory
		self.inventory = {'axe': 0}
		
		#player stats
		self.visibility = 1
		self.AP_max = 4
		self.AP_c = 4
		self.APcost = {"U": 1, "D": 1, "L": 1, "R": 1, "UL":2, "UR": 2, "LL": 2, "LR":2, "Chop":3, "Plant": 3}
		
	def spawn(self,x,y):
		self.scrnx = x
		self.mapx = x
		self.scrny = y
		self.mapy = y
		self.rect = pygame.rect.Rect((x * self.level.tilex, y * self.level.tiley), self.image.get_size())

	def command(self, cmd):
		if self.reckonAP(self.APcost[cmd]):
			if cmd == "U":
				if self.scrny*self.level.tiley <= self.level.tiley*self.visibility:
					self.level.move_BG("D")
				else:
					self.move("U")
			if cmd == "D":
				if self.scrny*self.level.tiley >= self.level.winy-((self.level.tiley*(self.visibility+1))):
					self.level.move_BG("U")
				else:
					self.move("D")
			if cmd == "L":
				if self.scrnx*self.level.tilex <= self.level.tilex*self.visibility:
					self.level.move_BG("R")
				else:
					self.move("L")
			if cmd == "R":
				if self.scrnx*self.level.tilex >= self.level.winx-((self.level.tilex*(self.visibility+1))):
					self.level.move_BG("L")
				else:
					self.move("R")
			if cmd == "UL":
				if self.scrny*self.level.tiley <= self.level.tiley*self.visibility or self.scrnx*self.level.tilex <= self.level.tilex*self.visibility:
					self.level.move_BG("LR")
				else:
					self.move("UL")
			if cmd == "UR":
				if self.scrny*self.level.tiley <= self.level.tiley*self.visibility or self.scrnx*self.level.tilex >= self.level.winx-((self.level.tilex*(self.visibility+1))):
					self.level.move_BG("LL")
				else:
					self.move("UR")
			if cmd == "LL":
				if self.scrny*self.level.tiley >= self.level.winy-((self.level.tiley*(self.visibility+1))) or self.scrnx*self.level.tilex <= self.level.tilex*self.visibility:
					self.level.move_BG("UR")
				else:
					self.move("LL")
			if cmd == "LR":
				if self.scrny*self.level.tiley >= self.level.winy-((self.level.tiley*(self.visibility+1))) or self.scrnx*self.level.tilex >= self.level.winx-((self.level.tilex*(self.visibility+1))):
					self.level.move_BG("UL")
				else:
					self.move("LR")
					
		else:
			pass	
			
		if self.AP_c <= 0:
			self.level.Turn_Over = 1
			
		self.spacecheck()
		self.itemcheck()	
				
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
		
	def spacecheck(self):
		for space in pygame.sprite.spritecollide(self, self.level.space, False):
			self.level.Game_Over = 1
		
		
	def itemcheck(self):
		for item in pygame.sprite.spritecollide(self, self.level.items, True):
			if item.flavor == 'gem':
				self.level.Game_Over = 2
			if item.flavor == 'axe':
				self.inventory['axe'] += 1

	def set_Image(self, name):
		xind = 7
		yind = 2
		if name == 'L':
			xind = 7
			yind = 3
		if name == 'R':
			xind = 7
			yind = 2
			
		self.level.animator.set_Img(xind,yind)
		self.image = self.level.animator.get_Img().convert()
		self.image.set_colorkey((255,0,0))

	def reckonAP(self, cost):
		if self.AP_c >= cost:
			self.AP_c -= cost
			return True
		else:
			return False
