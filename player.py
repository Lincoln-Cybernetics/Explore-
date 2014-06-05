import pygame
import ss

class Player(pygame.sprite.Sprite):
	def __init__(self, level, *groups):
		super(Player, self).__init__(*groups)
		self.Rimg = pygame.image.load('RangerDanR.png')
		self.Limg = pygame.image.load('RangerDanL.png')
		self.image = self.Rimg
		self.rect = pygame.rect.Rect((100,100), self.image.get_size())#320,240
		self.level = level
		
	def command(self, cmd):
		prev = self.rect.copy()
		if cmd == "U":
			if self.rect.y <= 100:
				self.level.move_BG("D")
			else:
				self.rect.y -= 100
		if cmd == "D":
			if self.rect.y >= self.level.mastery - 200:
				self.level.move_BG("U")
			else:
				self.rect.y += 100
		if cmd == "L":
			self.image = self.Limg
			if self.rect.x <= 100:
				self.level.move_BG("R")
			else:
				self.rect.x -= 100
		if cmd == "R":
			self.image = self.Rimg
			if self.rect.x >= self.level.masterx - 200:
				self.level.move_BG("L")
			else:
				self.rect.x += 100
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
		
		
		
