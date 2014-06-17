import pygame

class Player(pygame.sprite.Sprite):
	def __init__(self, level, *groups):
		super(Player, self).__init__(*groups)
		#the game level
		self.level = level
		
		#spritegrups
		self.unpassable = pygame.sprite.Group()
		
		#base image
		self.set_Image('R')
		self.scrnx = 0
		self.mapx = 0
		self.scrny = 0
		self.mapy = 0
		#item inventory
		self.inventory = {'axe': 0, 'wood': 0}
		
		#player stats
		self.visibility = 1
		self.AP_max = 4
		self.AP_c = 4
		self.APcost = {"U": 1, "D": 1, "L": 1, "R": 1, "UL":2, "UR": 2, "LL": 2, "LR":2, "Chop":3, "Plant": 3}
		
		#fighting
		self.HP_max = 10
		self.HP_c = 10
		self.ATT = 3
		self.DEF = 2
		self.DMG = 2
		
	def spawn(self,x,y):
		self.scrnx = x
		self.mapx = x
		self.scrny = y
		self.mapy = y
		self.rect = pygame.rect.Rect((x * self.level.tilex, y * self.level.tiley), self.image.get_size())

	def command(self, cmd):
			#reference of old location data
			prevrect = self.rect.copy()
			pxs = self.scrnx
			pys = self.scrny
			pmx = self.mapx
			pmy = self.mapy
			
			if cmd == "U":
				if self.level.mymap[self.mapx][self.mapy-1] in self.unpassable:
					pass
				else:
					if self.reckonAP(self.APcost[cmd]):
						if self.scrny*self.level.tiley <= self.level.tiley*self.visibility:
							self.level.move_BG("D")
							self.mapy -= 1
						else:
							self.move("U")
			if cmd == "D":
				if self.level.mymap[self.mapx][self.mapy+1] in self.unpassable:
					pass
				else:
					if self.reckonAP(self.APcost[cmd]):
						if self.scrny*self.level.tiley >= self.level.winy-((self.level.tiley*(self.visibility+1))):
							self.level.move_BG("U")
							self.mapy += 1
						else:
							self.move("D")
			if cmd == "L":
				if self.level.mymap[self.mapx-1][self.mapy] in self.unpassable:
					pass
				else:
					if self.reckonAP(self.APcost[cmd]):
						if self.scrnx*self.level.tilex <= self.level.tilex*self.visibility:
							self.level.move_BG("R")
							self.mapx -= 1
						else:
							self.move("L")
			if cmd == "R":
				if self.level.mymap[self.mapx+1][self.mapy] in self.unpassable:
					pass
				else:
					if self.reckonAP(self.APcost[cmd]):
						if self.scrnx*self.level.tilex >= self.level.winx-((self.level.tilex*(self.visibility+1))):
							self.level.move_BG("L")
							self.mapx += 1
						else:
							self.move("R")
			if cmd == "UL":
				if self.level.mymap[self.mapx-1][self.mapy-1] in self.unpassable:
					pass
				else:
					if self.reckonAP(self.APcost[cmd]):
						if self.scrny*self.level.tiley <= self.level.tiley*self.visibility or self.scrnx*self.level.tilex <= self.level.tilex*self.visibility:
							self.level.move_BG("LR")
							self.mapx -= 1
							self.mapy -= 1
						else:
							self.move("UL")
			if cmd == "UR":
				if self.level.mymap[self.mapx+1][self.mapy-1] in self.unpassable:
					pass
				else:
					if self.reckonAP(self.APcost[cmd]):
						if self.scrny*self.level.tiley <= self.level.tiley*self.visibility or self.scrnx*self.level.tilex >= self.level.winx-((self.level.tilex*(self.visibility+1))):
							self.level.move_BG("LL")
							self.mapx += 1
							self.mapy -= 1
						else:
							self.move("UR")
			if cmd == "LL":
				if self.level.mymap[self.mapx-1][self.mapy+1] in self.unpassable:
					pass
				else:
					if self.reckonAP(self.APcost[cmd]):
						if self.scrny*self.level.tiley >= self.level.winy-((self.level.tiley*(self.visibility+1))) or self.scrnx*self.level.tilex <= self.level.tilex*self.visibility:
							self.level.move_BG("UR")
							self.mapx -= 1
							self.mapy += 1
						else:
							self.move("LL")
			if cmd == "LR":
				if self.level.mymap[self.mapx+1][self.mapy+1] in self.unpassable:
					pass
				else:
					if self.reckonAP(self.APcost[cmd]):
						if self.scrny*self.level.tiley >= self.level.winy-((self.level.tiley*(self.visibility+1))) or self.scrnx*self.level.tilex >= self.level.winx-((self.level.tilex*(self.visibility+1))):
							self.level.move_BG("UL")
							self.mapx += 1
							self.mapy += 1
						else:
							self.move("LR")
					
			if cmd == "Chop":
				choppable = { "Dense Woods":4, "Medium Woods":3, "Light Woods": 2, "Grass and Trees":1 }
				if choppable[self.level.mymap[self.mapx][self.mapy].flavor] > 0:
					if self.reckonAP(self.APcost[cmd]):
						self.inventory['wood'] += choppable[self.level.mymap[self.mapx][self.mapy].flavor]
						self.level.mymap[self.mapx][self.mapy].set_type(choppable[self.level.mymap[self.mapx][self.mapy].flavor])
			
			if self.AP_c <= 0:
				self.level.Turn_Over = 1
			
			self.spacecheck()
			self.itemcheck()
			if self.mobcheck() == False:
				self.rect = prevrect
				self.scrnx = pxs
				self.scrny = pys
				self.mapx = pmx
				self.mapy = pmy	
				
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
		self.rect.x = self.scrnx*self.level.tilex
		self.rect.y = self.scrny*self.level.tiley
		
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

	def mobcheck(self):
		for mob in pygame.sprite.spritecollide(self, self.level.mobs, False):
			self.fight(mob)
			if mob.Alive == False:
				mob.kill()
				return True
			return False
		return True
		
	def fight(self, opponent):
		if self.ATT > opponent.DEF:
			opponent.damage(self.DMG)
			
	def damage(self, dmg):
		self.HP_c -= dmg
		if self.HP_c <= 0:
			self.level.Game_Over = 3
			
