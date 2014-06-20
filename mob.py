import pygame
import random

class Mob(pygame.sprite.Sprite):
	def __init__(self, level, *groups):
		super(Mob, self).__init__(*groups)
		#the game level
		self.level = level
		
		#sprite groups
		self.unpassable = pygame.sprite.Group()
		
		#base image
		self.level.animator.set_Img(4,5)
		self.secretimage = self.level.animator.get_Img().convert()
		self.secretimage.set_colorkey((255,0,0))
		self.level.animator.set_Img(0,5)
		self.image = self.level.animator.get_Img().convert()
		
		
		#type
		self.flavor = "Static"
		self.flavor_saver = ["Static", "Lemming", "Wanderer", "Charger"]
		self.ATflag = 0#All-Terrain flag
		
		#location
		self.firstflag = True
		self.mapx = 0 
		self.mapy = 0 
		self.scrnx = 0
		self.scrny = 0
		
		#status
		self.Turn_Over = False
		self.Alive = True
		self.AP_max = 1
		self.AP_c = 1
		self.APcost = {"U": 1, "D": 1, "L": 1, "R": 1, "UL":2, "UR": 2, "LL": 2, "LR":2, "Chop":3, "Plant": 3}
		self.trycount = 0
		
		#fighting
		self.HP_max = 5
		self.HP_c = 5
		self.ATT = 2
		self.DEF = 1
		self.DMG = 0
		
	def reveal(self):
		self.image = self.secretimage
		
	def set_type(self, personality):
			self.flavor = self.flavor_saver[personality]
			#static
			if personality == 0:
				xind = 4
				yind = 5
				self.ATflag = 0
			#lemming
			if personality == 1:
				xind = 4
				yind = 5
				self.ATflag = 0
			#wanderer
			if personality == 2:
				xind = 4
				yind = 5
				self.ATflag = 1
			#charger
			if personality == 3:
				xind = 4
				yind = 5
				self.ATflag = 0
			#default
			else:
				xind = 4
				yind = 5
				self.ATflag = 0
				
				
			self.level.animator.set_Img(xind,yind)
			self.secretimage = self.level.animator.get_Img().convert()
			self.secretimage.set_colorkey((255,0,0))
	
	def fight(self, opponent):
		if self.ATT > opponent.DEF:
			opponent.damage(self.DMG)				
	
	def damage(self, dmg):
		self.HP_c -= dmg
		if self.HP_c <= 0:
			self.Alive = False
			self.level.mymobs.remove(self)
			self.level.spawnmob()	
									
		
	def spawn(self,x,y):
		self.scrnx = self.level.mymap[x][y].scrnx
		self.mapx = x
		self.scrny = self.level.mymap[x][y].scrny
		self.mapy = y
		self.rect = pygame.rect.Rect((self.scrnx * self.level.tilex, self.scrny * self.level.tiley), self.image.get_size())

	def spacecheck(self):
		for space in pygame.sprite.spritecollide(self, self.level.space, False):
			self.Alive = False
			self.kill()
			self.level.mymobs.remove(self)
			
	def mobcheck(self):
		for mob in pygame.sprite.spritecollide(self, self.level.fightable, False):
			if mob == self:
				pass
			else:
				self.fight(mob)
				if mob.Alive == False:
					mob.kill()
					return True
				return False
		return True
		
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
					self.move("U")
		if cmd == "D":
			if self.level.mymap[self.mapx][self.mapy+1] in self.unpassable:
				pass
			else:
				if self.reckonAP(self.APcost[cmd]):
					self.move("D")
		if cmd == "L":
			if self.level.mymap[self.mapx-1][self.mapy] in self.unpassable:
				pass
			else:
				if self.reckonAP(self.APcost[cmd]):
					self.move("L")
		if cmd == "R":
			if self.level.mymap[self.mapx+1][self.mapy] in self.unpassable:
				pass
			else:
				if self.reckonAP(self.APcost[cmd]):
					self.move("R")
		if cmd == "UL":
			if self.level.mymap[self.mapx-1][self.mapy-1] in self.unpassable:
				pass
			else:
				if self.reckonAP(self.APcost[cmd]):
					self.move("UL")
		if cmd == "UR":
			if self.level.mymap[self.mapx+1][self.mapy-1] in self.unpassable:
				pass
			else:
				if self.reckonAP(self.APcost[cmd]):
					self.move("UR")
		if cmd == "LL":
			if self.level.mymap[self.mapx-1][self.mapy+1] in self.unpassable:
				pass
			else:
				if self.reckonAP(self.APcost[cmd]):
					self.move("LL")
		if cmd == "LR":
			if self.level.mymap[self.mapx+1][self.mapy+1] in self.unpassable:
				pass
			else:
				if self.reckonAP(self.APcost[cmd]):
					self.move("LR")
			
		self.spacecheck()
		if self.mobcheck() == False:
			self.rect = prevrect
			self.scrnx = pxs
			self.scrny = pys
			self.mapx = pmx
			self.mapy = pmy	
									
		if self.AP_c <= 0:
			self.Turn_Over = True
			
				
	def move(self, vec):
		if vec == "U":
			self.mapy -= 1
			self.scrny -= 1
		if vec == "D":
			self.mapy += 1
			self.scrny += 1
		if vec == "L":
			#self.set_Image('L')
			self.mapx -= 1
			self.scrnx -= 1
		if vec == "R":
			#self.set_Image('R')
			self.mapx += 1
			self.scrnx += 1
		if vec == "UL":
			#self.set_Image('L')
			self.mapy -= 1
			self.mapx -= 1
			self.scrny -= 1
			self.scrnx -= 1
		if vec == "UR":
			#self.set_Image('R')
			self.mapy -= 1
			self.mapx += 1
			self.scrny -= 1
			self.scrnx += 1
		if vec == "LL":
			#self.set_Image('L')
			self.mapy += 1
			self.mapx -= 1
			self.scrny += 1
			self.scrnx -= 1
		if vec == "LR":
			#self.set_Image('R')
			self.mapy += 1
			self.mapx += 1
			self.scrny += 1
			self. scrnx += 1
		self.rect.x = self.scrnx*self.level.tilex
		self.rect.y = self.scrny*self.level.tiley

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
		self.trycount = 0
		self.Turn_Over = False
		
		if self.flavor == "Static":
			self.Turn_Over = True
			return
			
		if self.flavor == "Lemming":
			while self.Turn_Over == False:
				self.trycount+=1
				if self.trycount >=20:
					self.Turn_Over = True
				self.command("L")
			return
						
		if self.flavor == "Wanderer":
			while self.Turn_Over == False:
				self.trycount+=1
				if self.trycount >=20:
					self.Turn_Over = True
				dirs = ["U", "D", "L", "R", "UL", "UR", "LL", "LR"]
				self.command(random.choice(dirs))
			return
			
		if self.flavor == "Charger":
			while self.Turn_Over == False:
				self.trycount+=1
				if self.trycount >=20:
					self.Turn_Over = True
				if self.AP_c >= 2:
					if self.mapx > self.level.player1.mapx and self.mapy > self.level.player1.mapy:
						self.command("UL")
					if self.mapx < self.level.player1.mapx and self.mapy > self.level.player1.mapy:
						self.command("UR")
					if self.mapx > self.level.player1.mapx and self.mapy < self.level.player1.mapy:
						self.command("LL")
					if self.mapx < self.level.player1.mapx and self.mapy < self.level.player1.mapy:
						self.command("LR")
				if self.mapx > self.level.player1.mapx:
					self.command("L")
				if self.mapx < self.level.player1.mapx:
					self.command("R")
				if self.mapy > self.level.player1.mapy:
					self.command("U")
				if self.mapy < self.level.player1.mapy:
					self.command("D")
			return
			
		return
