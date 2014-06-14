import pygame
import ss


class Player(pygame.sprite.Sprite):
	def __init__(self, level, *groups):
		super(Player, self).__init__(*groups)
		#the game level
		self.level = level
		#load images
		self.sheet = pygame.image.load('exp100.png').convert()
		self.animator = ss.Cutout(self.sheet, 100, 100)
		self.animator.set_Img(7,2)
		self.Rimg = self.animator.get_Img().convert()
		self.Rimg.set_colorkey((255,0,0))
		
		self.animator.set_Img(7,3)
		self.Limg = self.animator.get_Img().convert()
		self.Limg.set_colorkey((255,0,0))
		
		self.image = self.Rimg
		#player spawn point/location
		self.spawnx = 1
		self.spawny = 1
		self.indx = self.spawnx
		self.indy = self.spawny
		self.rect = pygame.rect.Rect((self.spawnx * self.level.tilex, self.spawny * self.level.tiley), self.image.get_size())#320,240
		#terrain/item interaction
		self.unpassable = pygame.sprite.Group()
		#player stats
		self.name = "Ranger Dan"
		self.inventory = { 'axe' : 0 }
		self.AP_max = 3
		self.AP_c = 3
		self.HP_max = 10
		self.HP_c = 10
		self.Att = 5
		self.Def = 5
		self.Att_Dam = 2
	
	def spawn(self):
		self.indx = self.spawnx
		self.indy = self.spawny
		self.rect = pygame.rect.Rect((self.spawnx * self.level.tilex, self.spawny * self.level.tiley), self.image.get_size())	
		
	def set_spawn(self, x, y):
		self.spawnx = x
		self.spawny = y
		
	def command(self, cmd):
		prev = self.rect.copy()
		bgsig = 'NA'
		newx = self.indx
		newy = self.indy
		
		#move up
		if cmd == "U":
			if self.reckonAP(1):
				newy -= 1
				if self.rect.y <= self.level.tiley:
					bgsig = "D"
				else:
					self.rect.y -= self.level.tiley
					
		#move down
		if cmd == "D":
			if self.reckonAP(1):
				newy += 1
				if self.rect.y >= self.level.mastery - (2* self.level.tiley):
					bgsig = "U"
				else:
					self.rect.y += self.level.tiley
					
		# move left
		if cmd == "L":
			if self.reckonAP(1):
				newx -= 1
				self.image = self.Limg
				if self.rect.x <= self.level.tilex:
					bgsig = "R"
				else:
					self.rect.x -= self.level.tilex
					
		#move up and left 
		if cmd == "UL":
			if self.reckonAP(2):
				newx -= 1
				newy -= 1
				self.image = self.Limg
				if self.rect.x <= self.level.tilex or self.rect.y <= self.level.tiley:
					bgsig = "LR"
				else:
					self.rect.x -=  self.level.tilex
					self.rect.y -= self.level.tiley	
						
		#move down and left
		if cmd == "LL":
			if self.reckonAP(2):
				newx -= 1
				newy += 1
				self.image = self.Limg
				if self.rect.x <= self.level.tilex or self.rect.y >= self.level.mastery - 2*self.level.tiley:
					bgsig = "UR"
				else:
					self.rect.x -= self.level.tilex
					self.rect.y += self.level.tiley
					
		#move right
		if cmd == "R":
			if self.reckonAP(1):
				newx += 1
				self.image = self.Rimg
				if self.rect.x >= self.level.masterx - (2 * self.level.tiley):
					bgsig = "L"
				else:
					self.rect.x += self.level.tilex
					
		#move up and right
		if cmd == "UR":
			if self.reckonAP(2):
				newx += 1
				newy -= 1
				self.image = self.Rimg
				if self.rect.x >= self.level.masterx - (2* self.level.tilex) or self.rect.y <= self.level.tiley:
					bgsig = "LL"
				else:
					self.rect.x += self.level.tilex
					self.rect.y -= self.level.tiley
					
		#move down and right
		if cmd == "LR":
			if self.reckonAP(2):
				newx += 1
				newy += 1
				self.image = self.Rimg
				if self.rect.x >= self.level.masterx - (2*self.level.tilex) or self.rect.y >= self.level.mastery - 2*self.level.tiley:
					bgsig = "UL"
				else:
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
				
				
		if newx < 0 or newx >= len(self.level.maptiles):
			self.level.Game_Over = True	
			self.level.GOstr = "SPACE"
		elif newy < 0 or newy >= len(self.level.maptiles[newx]):
			self.level.Game_Over = True	
			self.level.GOstr = "SPACE"				
		
		for badguy in pygame.sprite.spritecollide(self, self.level.baddies, False):
			self.fight(badguy)
			#if badguy.Alive == True:
			#	self.rect = prev
				
		new = self.rect
		if bgsig == 'NA':
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
				
		
		elif self.level.Game_Over == False:
			
			if self.level.maptiles[newx][newy] in self.unpassable:
				pass
			else:
				self.level.move_BG(bgsig)
				self.indx = newx
				self.indy = newy
				
		for thing in pygame.sprite.spritecollide(self, self.level.items, True):
			if thing.flavor == 'gem':
				pygame.mixer.Sound('tadaa.wav').play()
				self.level.Game_Over = True	
				self.level.GOstr = "WIN"	
			elif thing.flavor == 'axe':		
				self.inventory['axe'] += 1
				

		
		if self.AP_c < 1:
			self.level.end_turn = True		
				
		
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
			self.level.Game_Over = False
			self.level.GOstr = "Dead"	
		
	def fight(self, opponent):
		if self.Att > opponent.Def:
			opponent.damage(self.Att_Dam)
	
