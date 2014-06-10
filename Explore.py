import pygame
import random
import player
import landform
import item
import time

class Game(object):
	
	#Moves the background
    def move_BG(self, d):
		for tile in self.background:
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
				
    #map generation
    def map_gen(self, kind):
		
		if kind == 'Random':
			self.player1.set_spawn(random.randrange(self.masterx//self.tilex), random.randrange(self.mastery//self.tiley))
				
		
		mygem = item.Item(self, self.items)
		for a in range(self.masterx//self.tilex):
			maprow = []
			for b in range(self.mastery//self.tiley):
				#basic map
				if kind == 'Basic':
					tertype = 0
					mygem.set_Index(5,5)
					
				#Random map
				if kind == 'Random':
					tertype = random.randrange(15)
					mygem.set_Index(random.randrange(self.masterx//self.tilex), random.randrange(self.mastery//self.tiley))
				
				if a == self.player1.spawnx and b == self.player1.spawny:
					tertype = 	0
				plot = landform.Acre(self, self.terrain)
				plot.set_Index(a,b)
				plot. set_Biome(tertype)
				maprow.append(plot)
				self.background.add(plot)
				if plot.flavor == 'Whirlpool' or plot.flavor == 'Ocean' or plot.flavor == 'Active Volcano':
					self.player1.unpassable.add(plot)
			self.maptiles.append(maprow)
		self.background.add(mygem)
				
	#MAIN
    def main(self, screen):
		
		
		#is the Game Over?
		self.Game_Over = False
		#why is the game over?
		self.GOstr = ""
		
		#sprite groups
		self.sprites = pygame.sprite.Group()
		self.items = pygame.sprite.Group()
		self.terrain = pygame.sprite.Group()
		self.background = pygame.sprite.Group()
		
		#list of map tiles
		self. maptiles = []
		
		#masterx & mastery are the dimensions of the game window
		self.masterx = mainx
		self.mastery = mainy
		
		#
		
		#tilex & tiley are the dimensions of the graphics tiles
		self.tilex = 100
		self.tiley = 100
		
		#the player
		self.player1 = player.Player(self, self.sprites)
		
		#make a map
		#self.landtype = ['Plain', 'Plain Trees', 'Hill', 'Scrub', 'Dunes', 'Gravel', 'Mountain', 'Extinct Volcano', 'Active Volcano', 'Shallows', 'Ocean', 'Whirlpool', 'Light Woods', 'Med Woods', 'Dense Woods']
		self.map_gen('Random')
		
		#spawn the player
		self.player1.spawn()
		
		#main loop
		while self.Game_Over == False:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					return
				if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
					return
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
					
						
			self.iterate_Game()
		if self.GOstr == "SPACE":
			print "You have walked off the edge of the world.  You are now doomed to spend eternity drifting in OUTER SPACE!"
		if self.GOstr == "WIN":
			time.sleep(2)
			print" You Win!  YAY!"
		return
			
    def iterate_Game(self):
		
		self.terrain.update()
		self.sprites.update()
		
		screen.fill((0,0,0))
		
		self.terrain.draw(screen)
		self.items.draw(screen)
		self.sprites.draw(screen)
	
		pygame.display.flip()
        




########################################################################					
if __name__ == '__main__':
	pygame.init()
	mainx = 1200
	mainy = 800
	screen = pygame.display.set_mode((mainx, mainy))#640,480
	pygame.display.set_caption("Explore!")
	Game().main(screen)
