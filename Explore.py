import pygame
import random
import player
import landform
import item

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
				
    #map generation
    def map_gen(self, kind):
		
		mygem = item.Item(self, self.items)
		
		#basic map
		if kind == 'Basic':
			for a in range(self.masterx//self.tilex):
				for b in range(self.mastery//self.tiley):
					plot = landform.Acre(self, self.terrain)
					plot.set_Index(a,b)
					self.background.add(plot)
					mygem.set_Index(5,5)
					
		#Random map			
		if kind == 'Random':
			for a in range(self.masterx//self.tilex):
				for b in range(self.mastery//self.tiley):
					plot = landform.Acre(self, self.terrain)
					plot.set_Index(a,b)
					plot. set_Biome(random.choice(self.landtype))
					self.background.add(plot)
					mygem.set_Index(random.randrange(self.masterx//self.tilex), random.randrange(self.mastery//self.tiley))
		
		self.background.add(mygem)
				
	#MAIN
    def main(self, screen):
		#sprite groups
		self.sprites = pygame.sprite.Group()
		self.unpassable = pygame.sprite.Group()
		self.items = pygame.sprite.Group()
		self.terrain = pygame.sprite.Group()
		self.background = pygame.sprite.Group()
		
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
		self.landtype = ['Plain', 'Hill', 'Scrub', 'Dunes', 'Gravel', 'Mountain', 'Extinct Volcano', 'Active Volcano', 'Shallows', 'Ocean', 'Whirlpool', 'Light Woods', 'Med Woods', 'Dense Woods']
		self.map_gen('Random')
		
		#main loop
		while 1:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					return
				if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
					return
				if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
					self.player1.command("U")
				if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
					self.player1.command("D")
				if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
					self.player1.command("L")
				if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
					self.player1.command("R")	
					
					
			self.iterate_Game()
			
			
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
	mainx = 1000
	mainy = 700
	screen = pygame.display.set_mode((mainx, mainy))#640,480
	pygame.display.set_caption("Explore!")
	Game().main(screen)
