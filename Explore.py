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
		self.counter = 0
		
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
		self.fightable = pygame.sprite.Group()
		
		#player
		self.player1 = player.Player(self, self.players)
		self.player1.add(self.fightable)
		
		
		
		self.mapgen(20,20,'Basic')
		self.iterate_Game()
	
	def spawnmob(self):
		dude = mob.Mob(self, self.mobs, self.background, self.fightable)
		dude.set_type(random.randrange(4))
		dude.spawn(random.randrange((self.winx/self.tilex)-2)+1, random.randrange((self.winy/self.tiley)-2)+1)
		self.mymobs.append(dude)
		
	def mapgen(self, x,y, maptype):
		mygem = item.Item(self, self.items)
		mygem.set_type(0)
		myaxe = item.Item(self, self.items)
		myaxe.set_type(1)
		mysamm = item.Item(self, self.items)
		mysamm.set_type(2)
		mydude = mob.Mob(self, self.mobs)
		mydude.set_type(2)
		
		
		for a in range(x):
			maprow = []
			for b in range(y):
				
				if maptype == 'Basic':
					landtype = 1
					
				if maptype == 'Random':
					landtype = random.randrange(15)+1
					
				#dude = mob.Mob(self, self.mobs)
				#dude.set_type(1)
				#self.mymobs.append(dude)
				#dude.spawn(a,b)	
				acre = tile.Land(self, self.terrain)
				if a == 0 or b == 0 or a == x-1 or b == y-1:
					acre.set_type(0)
					self.space.add(acre)
				else:
					acre.set_type(landtype)
					if landtype == 12 or landtype == 15:
						self.player1.unpassable.add(acre)
				acre.spawn(a, b)
				self.background.add(acre)
				maprow.append(acre)
				
			
			self.mymap.append( maprow )
		self.player1.spawn(1,1)
		
		if maptype == 'Basic':
			mygem.spawn(4,5)
			myaxe.spawn(5,4)
			mysamm.spawn(6,6)
			mydude.spawn(7,7)
			
		if maptype == 'Random':
			mygem.spawn(random.randrange(x-2)+1, random.randrange(y-2)+1)
			myaxe.spawn(random.randrange(x-2)+1, random.randrange(y-2)+1)
			mydude.spawn(random.randrange(x-2)+1, random.randrange(y-2)+1)
			mysamm.spawn(random.randrange(x-2)+1, random.randrange(y-2)+1)
			
			
		self.background.add(mygem)
		self.background.add(myaxe)
		self.background.add(mysamm)
		self.background.add(self.mobs)
		self.fightable.add(self.mobs)
		self.mymobs.append(mydude)
		
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
								
				#player input	
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
						if event.type == pygame.KEYDOWN and event.key == pygame.K_c:
							self.player1.command("Chop")
						if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
							self.player1.command("Plant")
						
						self.display()	
						
							
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
			self.display()
				
				
			#Mobs take actions	
			for dude in self.mobs:
				dude.take_turn()
				self.display()	
						
						
		if self.Game_Over == 1:
			print "You have walked off the edge of the world."
			print "You are doomed to drift away into OUTER SPACE."
			return
		
		if self.Game_Over == 2:
			print "You got the gem."
			print "You win!"
			return
		
		if self.Game_Over == 3:
			print "You Died."
			print "R.I.P."
			return
		
		
	def display(self):
		screen.set_clip(0,0,self.winx,self.winy)
		self.terrain.draw(screen)
		self.mobs.draw(screen)
		self.items.draw(screen)
		self.players.draw(screen)
		font = pygame.font.Font(None, 20)
		HPstr = "HP: "+str(self.player1.HP_c)+"/"+str(self.player1.HP_max)+"     "
		APstr =  "AP: "+str(self.player1.AP_c)+"/"+str(self.player1.AP_max)+"     "
		woodstr = "Wood: "+ str(self.player1.inventory['wood'])
		text = font.render(HPstr + APstr+ woodstr, 1, (255, 255, 255), (0,0,0))
		scrstr = "SCR: "+ str(self.player1.scrnx)+","+str(self.player1.scrny)+"     "
		mapstr = "MAP: "+str(self.player1.mapx)+","+str(self.player1.mapy)+"     "
		debugstr = scrstr + mapstr
		text2 = font.render(debugstr, 1, (255,255,255), (0,0,0))
		axstr = ""
		if self.player1.inventory['axe'] > 0:
			axstr = 'axe'
		text3 = font.render(axstr, 1, (255,255,255), (0,0,0))
		
		# Blit everything to the screen
		screen.blit(text, (0,0))
		screen.blit(text2, (0,50))
		screen.blit(text3, (0,25))
		
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
		self.players.draw(screen)




########################################################################
if __name__ == '__main__':
	pygame.init()
	mainx = 1200
	mainy = 800
	screen = pygame.display.set_mode((mainx, mainy))#640,480
	pygame.display.set_caption("Explore!")
	Game().main(screen)
