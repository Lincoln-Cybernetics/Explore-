import pygame
import player
import ss
import tile
import random
import item
import mob

class Game(object):
	def main (self, screen):
		
		#general signals
		self.Game_Over = 0
		self.Turn_Over = 0
		self.winx = mainx
		self.winy = mainy
		
		#spritesheet dis-aggregator
		self.tilex = 100
		self.tiley = 100
		self.sheet = pygame.image.load('exp100.png').convert()
		self.animator = ss.Cutout(self.sheet, self.tilex, self.tiley)
		
		#sprite groups
		self.players = pygame.sprite.Group()
		self.mobs = pygame.sprite.Group()
		self.mymobs = []
		self.terrain = pygame.sprite.Group()
		self.mymap = []
		self.space = pygame.sprite.Group()
		self.items = pygame.sprite.Group()
		self.background = pygame.sprite.Group()
		
		#player
		self.player1 = player.Player(self, self.players)
		
		
		self.mapgen(19,19,'Random')
		self.iterate_Game()
		
	def mapgen(self, x,y, maptype):
		mygem = item.Item(self, self.items)
		mygem.set_type(0)
		myaxe = item.Item(self, self.items)
		myaxe.set_type(1)
		mydude = mob.Mob(self, self.mobs)
		mydude.set_type(0)
		self.mymobs.append(mydude)
		for a in range(x):
			maprow = []
			for b in range(y):
				if maptype == 'Basic':
					landtype = 1
				if maptype == 'Random':
					landtype = random.randrange(15)+1
				acre = tile.Land(self, self.terrain)
				if a == 0 or b == 0 or a == x-1 or b == y-1:
					acre.set_type(0)
					self.space.add(acre)
				else:
					acre.set_type(landtype)
				acre.spawn(a, b)
				self.background.add(acre)
				maprow.append(acre)
			self.mymap.append( maprow )
		self.player1.spawn(1,1)
		if maptype == 'Basic':
			mygem.spawn(4,5)
			myaxe.spawn(5,4)
			mydude.spawn(6,6)
		if maptype == 'Random':
			mygem.spawn(random.randrange(x-2)+1, random.randrange(y-2)+1)
			myaxe.spawn(random.randrange(x-2)+1, random.randrange(y-2)+1)
			mydude.spawn(random.randrange(x-2)+1, random.randrange(y-2)+1)
		self.background.add(mygem)
		self.background.add(myaxe)
		self.background.add(mydude)
		
	def iterate_Game(self):
		while self.Game_Over == 0:
			
			self.Turn_Over = 0
			self.display()
			self.player1.AP_c = self.player1.AP_max
			for dude in self.mobs:
				dude.AP_c = dude.AP_max
			
			while self.Turn_Over == 0:
				if self.Game_Over != 0:
							break		
				for event in pygame.event.get():
						if event.type == pygame.QUIT:
							return
						if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
							return
						if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
							self.Turn_Over = 1
							break
						if event.type == pygame.KEYDOWN and event.key == pygame.K_KP8:
							self.player1.command("U")
						if event.type == pygame.KEYDOWN and event.key == pygame.K_KP2:
							self.player1.command("D")
						if event.type == pygame.KEYDOWN and event.key == pygame.K_KP4:
							self.player1.command("L")
						if event.type == pygame.KEYDOWN and event.key == pygame.K_KP6:
							self.player1.command("R")	
						if event.type == pygame.KEYDOWN and event.key == pygame.K_KP7:
							self.player1.command("UL")	
						if event.type == pygame.KEYDOWN and event.key == pygame.K_KP9:
							self.player1.command("UR")	
						if event.type == pygame.KEYDOWN and event.key == pygame.K_KP1:
							self.player1.command("LL")	
						if event.type == pygame.KEYDOWN and event.key == pygame.K_KP3:
							self.player1.command("LR")	
							
						self.display()		
			for dude in self.mobs:
				dude.take_turn()			
			while self.Turn_Over == 1:
				if self.Game_Over:
					break
				# Display some text
				font = pygame.font.Font(None, 64)
				text = font.render("Turn Over", 1, (255, 10, 10), (0,0,255))
				# Blit everything to the screen
				screen.blit(text, (self.winx/2-self.tilex, self.winy/2-self.tiley))
				pygame.display.flip()
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						return
					if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
						return
					if event.type == pygame.KEYDOWN and  (event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER):
						self.Turn_Over = 0
						break
						
						
		if self.Game_Over == 1:
			print "You have walked off the edge of the world."
			print "You are doomed to drift away into OUTER SPACE."
			return
		
		if self.Game_Over == 2:
			print "You got the gem."
			print "You win!"
			return
		
		
		
	def display(self):
		self.terrain.draw(screen)
		self.mobs.draw(screen)
		self.items.draw(screen)
		self.players.draw(screen)
		
		pygame.display.flip()
		
	def move_BG(self, d):
		for tile in self.background:
			#tile.set_type(tile.fnum)
			if d == 'U':
				tile.set_Index(tile.get_Index('X'), tile.get_Index('Y')-1)
			if d == 'D':
				tile.set_Index(tile.get_Index('X'), tile.get_Index('Y')+1)
			if d == 'L':
				tile.set_Index(tile.get_Index('X')-1, tile.get_Index('Y'))
			if d == 'R':
				tile.set_Index(tile.get_Index('X')+1, tile.get_Index('Y'))
			if d == 'UL':
				tile.set_Index(tile.get_Index('X')-1, tile.get_Index('Y')-1)
			if d == 'UR':
				tile.set_Index(tile.get_Index('X')+1, tile.get_Index('Y')-1)
			if d == 'LL':
				tile.set_Index(tile.get_Index('X')-1, tile.get_Index('Y')+1)
			if d == 'LR':
				tile.set_Index(tile.get_Index('X')+1, tile.get_Index('Y')+1)

########################################################################
if __name__ == '__main__':
	pygame.init()
	mainx = 1200
	mainy = 800
	screen = pygame.display.set_mode((mainx, mainy))#640,480
	pygame.display.set_caption("Explore!")
	Game().main(screen)
