import pygame
import ss
import random


class Mob(pygame.sprite.Sprite):
	def __init__(self, level, *groups):
		super(Mob, self).__init__(*groups)
		#the game level
		self.level = level
		#load images
		self.sheet = pygame.image.load('exp100.png').convert()
		self.animator = ss.Cutout(self.sheet, 100, 100)
		self.animator.set_Img(4,5)
		self.image = self.animator.get_Img().convert()
		self.image.set_colorkey((255,0,0))
		
		#Mob spawn point/location
		self.spawnx = 1
		self.spawny = 1
		self.indx = self.spawnx
		self.indy = self.spawny
		self.rect = pygame.rect.Rect((self.spawnx * self.level.tilex, self.spawny * self.level.tiley), self.image.get_size())
		#terrain/item interaction
		self.unpassable = pygame.sprite.Group()
		#player stats
		self.name = "Bad Guy"
		self.inventory = { 'axe' : 0 }
		self.AP_max = 3
		self.AP_c = 3
		self.HP_max = 10
		self.HP_c = 10
		self.Att = 5
		self.Def = 5
		self.Att_Dam = 2
		self.Alive = True
		self.end_turn = False
		self.flavor = "Static"
		
	def set_type(self, flavor):
		self.flavor = flavor
	
	def spawn(self):
		self.indx = self.spawnx
		self.indy = self.spawny
		self.rect = pygame.rect.Rect((self.spawnx * self.level.tilex, self.spawny * self.level.tiley), self.image.get_size())	
		
	def set_spawn(self, x, y):
		self.spawnx = x
		self.spawny = y
		
	def command(self, cmd):
		prev = self.rect.copy()
		
		newx = self.indx
		newy = self.indy
		#print cmd, self.indx, self.indy
		
		#move up
		if cmd == "U":
			if self.reckonAP(1):
				newy -= 1
				self.rect.y -= self.level.tiley
					
		#move down
		if cmd == "D":
			if self.reckonAP(1):
				newy += 1
				self.rect.y += self.level.tiley
					
		# move left
		if cmd == "L":
			if self.reckonAP(1):
				newx -= 1
				self.rect.x -= self.level.tilex
					
		#move up and left 
		if cmd == "UL":
			if self.reckonAP(2):
				newx -= 1
				newy -= 1
				self.rect.x -=  self.level.tilex
				self.rect.y -= self.level.tiley	
						
		#move down and left
		if cmd == "LL":
			if self.reckonAP(2):
				newx -= 1
				newy += 1
				self.rect.x -= self.level.tilex
				self.rect.y += self.level.tiley
					
		#move right
		if cmd == "R":
			if self.reckonAP(1):
				newx += 1
				self.rect.x += self.level.tilex
					
		#move up and right
		if cmd == "UR":
			if self.reckonAP(2):
				newx += 1
				newy -= 1
				self.rect.x += self.level.tilex
				self.rect.y -= self.level.tiley
					
		#move down and right
		if cmd == "LR":
			if self.reckonAP(2):
				newx += 1
				newy += 1
				self.rect.x += self.level.tilex
				self.rect.y += self.level.tiley
				
		if cmd == "CHOP":
			if self.reckonAP(3):
				terlab = ['Dense Woods', 'Medium Woods', 'Light Woods', 'Plain with Trees']
				tertyp = {'Dense Woods': 13, 'Medium Woods': 12,  'Light Woods' : 1, 'Plain with Trees': 0}
				if self.inventory['axe'] > 0:
					for flava in terlab:
						if self.level.maptiles[self.indx][self.indy].flavor == flava:
							self.level.maptiles[self.indx][self.indy].set_Biome(tertyp[flava])
							break	
				
		if cmd == "Plant":
			if self.reckonAP(3):
				if self.level.maptiles[self.indx][self.indy].flavor == "Plain":
					self.level.maptiles[self.indx][self.indy].set_Biome(1)
				
		#print self.indx, self.indy, newx, newy		
		if newx < 0 or newx >= len(self.level.maptiles):
			self.Alive = False	
			
		elif newy < 0 or newy >= len(self.level.maptiles[newx]):
			self.Alive = False	
		
			
		for mob in pygame.sprite.spritecollide(self, self.level.mobs, False):
			if mob == self:
				pass
			else:
				self.fight(mob)			
				
		new = self.rect
		
		xsig = True
		ysig = True
		for loc in pygame.sprite.spritecollide(self, self.unpassable, False):
			loc = loc.rect
				
			if prev.right <= loc.left and new.right > loc.left:
				new.right = loc.left
				xsig = False
			if prev.left >= loc.right and new.left < loc.right:
				new.left = loc.right
				xsig = False
			if prev.bottom <= loc.top and new.bottom > loc.top:
				new.bottom = loc.top
				ysig = False
			if prev.top >= loc.bottom and new.top < loc.bottom:
				new.top = loc.bottom
				ysig = False
		if xsig:
			self.indx = newx
		if ysig:
			self.indy = newy
				
		
		
				
		for thing in pygame.sprite.spritecollide(self, self.level.items, False):
			if thing.flavor == 'gem':
				pass
				
			elif thing.flavor == 'axe':
				pass		
				#self.inventory['axe'] += 1
		
		if self.AP_c < 1:
			self.end_turn = True		
				
		
	def update(self):
		pass
	
	def reckonAP(self, cost):
		if self.AP_c >= cost:
			self.AP_c -= cost
			return True
		else:
			return False	
			
	def damage(self, dmg):
		self.HP_c -= dmg
		if self.HP_c < 1:
			self.Alive = False
				
		
	def fight(self, opponent):
		attval = self.Att = random.randrange(10)
		if attval > opponent.Def:
			opponent.damage(self.Att_Dam)
			
	def take_turn(self):
		if self.flavor == "Static":
			pass
		else:	
			while self.AP_c > 0:
				if self.flavor == "Charger":
					
					if self.indx < self.level.player1.indx and self.AP_c > 0:
						self.command("R")
					if self.indy < self.level.player1.indy and self.AP_c > 0:
						self.command("D")
					if self.indx > self.level.player1.indx and self.AP_c > 0:
						self.command("L")
					if self.indy > self.level.player1.indy and self.AP_c > 0:
						self.command("U")
	
	def set_Index(self, x, y):
		self.indx = x
		self.rect.x = x*100
		self.indy = y
		self.rect.y = y*100 
		
	def get_Index(self, axis):
		if axis == 'X':
			return self.indx
		if axis == 'Y':
			return self.indy
		return -1
