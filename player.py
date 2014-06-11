import pygame
import ss


class Player(pygame.sprite.Sprite):
	def __init__(self, level, *groups):
		super(Player, self).__init__(*groups)
		self.level = level
		self.sheet = pygame.image.load('exp100.png').convert()
		self.animator = ss.Cutout(self.sheet, 100, 100)
		self.animator.set_Img(7,2)
		self.Rimg = self.animator.get_Img().convert()
		self.Rimg.set_colorkey((255,0,0))
		#self.Rimg = pygame.image.load('RangerDanR.png')
		self.animator.set_Img(7,3)
		self.Limg = self.animator.get_Img().convert()
		self.Limg.set_colorkey((255,0,0))
		#self.Limg = pygame.image.load('RangerDanL.png')
		self.image = self.Rimg
		self.spawnx = 1
		self.spawny = 1
		self.indx = self.spawnx
		self.indy = self.spawny
		self.rect = pygame.rect.Rect((self.spawnx * self.level.tilex, self.spawny * self.level.tiley), self.image.get_size())#320,240
		self.unpassable = pygame.sprite.Group()
		self.inventory = { 'axe' : 0 }
	
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
			newy -= 1
			if self.rect.y <= self.level.tiley:
				bgsig = "D"
				#self.level.move_BG("D")
			else:
				self.rect.y -= self.level.tiley
		#move down
		if cmd == "D":
			newy += 1
			if self.rect.y >= self.level.mastery - (2* self.level.tiley):
				bgsig = "U"
				#self.level.move_BG("U")
			else:
				self.rect.y += self.level.tiley
		# move left
		if cmd == "L":
			newx -= 1
			self.image = self.Limg
			if self.rect.x <= self.level.tilex:
				bgsig = "R"
				#self.level.move_BG("R")
			else:
				self.rect.x -= self.level.tilex
		#move up and left 
		if cmd == "UL":
			newx -= 1
			newy -= 1
			self.image = self.Limg
			if self.rect.x <= self.level.tilex or self.rect.y <= self.level.tiley:
				bgsig = "LR"
				#self.level.move_BG("LR")
			else:
				self.rect.x -=  self.level.tilex
				self.rect.y -= self.level.tiley		
		#move down and left
		if cmd == "LL":
			newx -= 1
			newy += 1
			self.image = self.Limg
			if self.rect.x <= self.level.tilex or self.rect.y >= self.level.mastery - 2*self.level.tiley:
				bgsig = "UR"
				#self.level.move_BG("UR")
			else:
				self.rect.x -= self.level.tilex
				self.rect.y += self.level.tiley
		#move right
		if cmd == "R":
			newx += 1
			self.image = self.Rimg
			if self.rect.x >= self.level.masterx - (2 * self.level.tiley):
				bgsig = "L"
				#self.level.move_BG("L")
			else:
				self.rect.x += self.level.tilex
		#move up and right
		if cmd == "UR":
			newx += 1
			newy -= 1
			self.image = self.Rimg
			if self.rect.x >= self.level.masterx - (2* self.level.tilex) or self.rect.y <= self.level.tiley:
				bgsig = "LL"
				#self.level.move_BG("LL")
			else:
				self.rect.x += self.level.tilex
				self.rect.y -= self.level.tiley
		#move down and right
		if cmd == "LR":
			newx += 1
			newy += 1
			self.image = self.Rimg
			if self.rect.x >= self.level.masterx - (2*self.level.tilex) or self.rect.y >= self.level.mastery - 2*self.level.tiley:
				bgsig = "UL"
				#self.level.move_BG("UL")
			else:
				self.rect.x += self.level.tilex
				self.rect.y += self.level.tiley
				
		if cmd == "CHOP":
			terlab = ['Dense Woods', 'Medium Woods', 'Light Woods', 'Plain with Trees']
			tertyp = {'Dense Woods': 13, 'Medium Woods': 12,  'Light Woods' : 1, 'Plain with Trees': 0}
			if self.inventory['axe'] > 0:
				for flava in terlab:
					if self.level.maptiles[self.indx][self.indy].flavor == flava:
						self.level.maptiles[self.indx][self.indy].set_Biome(tertyp[flava])
						break	
				
		if cmd == "Plant":
			if self.level.maptiles[self.indx][self.indy].flavor == "Plain":
				self.level.maptiles[self.indx][self.indy].set_Biome(1)
				
				
		if newx < 0 or newx >= len(self.level.maptiles):
			self.level.Game_Over = True	
			self.level.GOstr = "SPACE"
		elif newy < 0 or newy >= len(self.level.maptiles[newx]):
			self.level.Game_Over = True	
			self.level.GOstr = "SPACE"				
				
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
				
				
		
	def update(self):
		pass
		
		
		
