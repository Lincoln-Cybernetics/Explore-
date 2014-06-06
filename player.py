import pygame
import ss

class Player(pygame.sprite.Sprite):
	def __init__(self, level, *groups):
		super(Player, self).__init__(*groups)
		self.level = level
		self.Rimg = pygame.image.load('RangerDanR.png')
		self.Limg = pygame.image.load('RangerDanL.png')
		self.image = self.Rimg
		self.spawnx = 1
		self.spawny = 1
		self.indx = self.spawnx
		self.indy = self.spawny
		self.rect = pygame.rect.Rect((self.spawnx * self.level.tilex, self.spawny * self.level.tiley), self.image.get_size())#320,240
	
	def spawn(self):
		self.indx = self.spawnx
		self.indy = self.spawny
		self.rect = pygame.rect.Rect((self.spawnx * self.level.tilex, self.spawny * self.level.tiley), self.image.get_size())	
		
	def set_spawn(self, x, y):
		self.spawnx = x
		self.spawny = y
		
	def command(self, cmd):
		prev = self.rect.copy()
		#move up
		if cmd == "U":
			#self.indy -= 1
			if self.rect.y <= 100:
				#if self.level.maptiles[
				self.level.move_BG("D")
			else:
				self.rect.y -= 100
		#move down
		if cmd == "D":
			#self.indy += 1
			if self.rect.y >= self.level.mastery - 200:
				self.level.move_BG("U")
			else:
				self.rect.y += 100
		# move left
		if cmd == "L":
			self.image = self.Limg
			if self.rect.x <= 100:
				self.level.move_BG("R")
			else:
				self.rect.x -= 100
		#move up and left 
		if cmd == "UL":
			self.image = self.Limg
			if self.rect.x <= self.level.tilex or self.rect.y <= self.level.tiley:
				self.level.move_BG("LR")
			else:
				self.rect.x -= 100
				self.rect.y -= 100		
		#move down and left
		if cmd == "LL":
			self.image = self.Limg
			if self.rect.x <= self.level.tilex or self.rect.y >= self.level.mastery - 2*self.level.tiley:
				self.level.move_BG("UR")
			else:
				self.rect.x -= 100
				self.rect.y += 100
		#move right
		if cmd == "R":
			self.image = self.Rimg
			if self.rect.x >= self.level.masterx - 200:
				self.level.move_BG("L")
			else:
				self.rect.x += 100
		#move up and right
		if cmd == "UR":
			self.image = self.Rimg
			if self.rect.x >= self.level.masterx - 200 or self.rect.y <= self.level.tiley:
				self.level.move_BG("LL")
			else:
				self.rect.x += 100
				self.rect.y -= 100
		#move down and right
		if cmd == "LR":
			self.image = self.Rimg
			if self.rect.x >= self.level.masterx - 200 or self.rect.y >= self.level.mastery - 2*self.level.tiley:
				self.level.move_BG("UL")
			else:
				self.rect.x += 100
				self.rect.y += 100
				
				
		new = self.rect
		for loc in pygame.sprite.spritecollide(self, self.level.unpassable, False):
			loc = loc.rect
			if prev.right <= loc.left and new.right > loc.left:
				new.right = loc.left
			if prev.left >= loc.right and new.left < loc.right:
				new.left = loc.right
			if prev.bottom <= loc.top and new.bottom > loc.top:
				new.bottom = loc.top
			if prev.top >= loc.bottom and new.top < loc.bottom:
				new.top = loc.bottom
				
		for thing in pygame.sprite.spritecollide(self, self.level.items, True):
			if thing.flavor == 'gem':
				pygame.mixer.Sound('tadaa.wav').play()
				
		
	def update(self):
		pass
		
		
		
