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
		self.xmax = 30
		self.ymax = 30
		self.mapology = 'Random'
		self.screen = screen
		
		#spritesheet dis-aggregators
		self.tilex = 100
		self.tiley = 100
		self.sheet = pygame.image.load('exp100.png').convert()
		self.animator = ss.Cutout(self.sheet, self.tilex, self.tiley)
		self.sheet = pygame.image.load('Explm.png').convert()
		self.landgrabber = ss.Cutout(self.sheet,200,200)
		
		#sprite groups
		self.players = pygame.sprite.Group()
		self.mobs = pygame.sprite.Group()
		
		self.terrain = pygame.sprite.Group()
		self.landmarks = pygame.sprite.Group()
		self.mymap = []
		self.space = pygame.sprite.Group()
		self.items = pygame.sprite.Group()
		self.background = pygame.sprite.Group()
		self.fightable = pygame.sprite.Group()
		self.revealed = pygame.sprite.Group()
		self.fogged = pygame.sprite.Group()
		
		#player
		self.player1 = player.Player(self, self.players)
		self.player1.add(self.fightable)
		
		
		
		self.mapgen(self.xmax,self.ymax,self.mapology)
		self.iterate_Game()
	
	def spawnmob(self):
		dude = mob.Mob(self, self.mobs, self.background, self.fightable)
		dude.set_type(random.randrange(5))
		dude.set_species(random.randrange(2))
		dude.spawn(random.randrange((self.xmax)-2)+1, random.randrange((self.ymax)-2)+1)
		
		
	def mapgen(self, x,y, maptype):
		sizefactor = (x/10) + (y/10)
		
		mygem = item.Item(self, self.items)
		mygem.set_type(0)
		
		mymark = tile.Landmark(self, self.landmarks)
		mymark.set_type(1)
		mymid = tile.Landmark(self, self.landmarks)
		mymid.set_type(0)
		
		if maptype == 'Basic':
			myaxe = item.Item(self, self.items)
			myaxe.set_type(1)
			mysamm = item.Item(self, self.items)
			mysamm.set_type(2)
			mydude = mob.Mob(self, self.mobs)
			mydude.set_type(0)
			myscope = item.Item(self, self.items)
			myscope.set_type(3)
			mycant = item.Item(self, self.items)
			mycant.set_type(4)
			
		if maptype == 'Random' or 'Proced1':
			for num in range(sizefactor*3):
				itemo = item.Item(self, self.items)
				itemo.set_type(random.randrange(4)+1)
			for umb in range(sizefactor):
				mobbo = mob.Mob(self, self.mobs)
				mobbo.set_type(random.randrange(5))
				mobbo.set_species(random.randrange(2))
		
		
		for b in range(y):
			maprow = []
			for a in range(x):
				
				if maptype == 'Basic':
					landtype = 1
					
				if maptype == 'Random':
					landtype = random.randrange(16)+1
					
				if maptype == 'Proced1':
					#grassland/trees
					#common = [1,2,3,13]
					#uncommon = [4,5,6,7]
					#rare = [8,9,10]
					#vrare = [12,15]
					
					#desert
					common = [8]
					uncommon = [7,16]
					rare = [9]
					vrare = [1,2]
					
					#Forest
					#common = [3,4,5,9]
					#uncommon = [1,2,6]
					#rare = [7,13]
					#vrare = [10,11,12]
					
					landex = random.randrange(256)
					if landex < 256:
						landtype = random.choice(common)
					if landex < 64:
						landtype = random.choice(uncommon)
					if landex < 16:
						landtype = random.choice(rare)
					if landex < 2:
						landtype = random.choice(vrare)
					
					
				acre = tile.Land(self, self.terrain)
				if a == 0 or b == 0 or a == x-1 or b == y-1:
					acre.set_type(0)
					self.space.add(acre)
					for mobbo in self.mobs:
						mobbo.unpassable.add(acre)
				else:
					acre.set_type(landtype)
					#if landtype == 12 or landtype == 15:
					#	pass
						#self.player1.unpassable.add(acre)
				acre.spawn(a, b)
				self.background.add(acre)
				maprow.append(acre)
				
			self.mymap.append( maprow )
		
		if maptype == 'Basic':
			mygem.spawn(5,5)
			myaxe.spawn(8,4)
			mysamm.spawn(1,6)
			mydude.spawn(5,1)
			myscope.spawn(3,2)
			mycant.spawn(10,10)
			mymark.spawn(8,8)
			self.player1.spawn(3,3)
			self.player1.position_scrn(6,3)
			self.normalize(3,3)
			
		if maptype == 'Random' or maptype == 'Proced1':
			mygem.spawn(random.randrange(x-2)+1, random.randrange(y-2)+1)
			mymark.spawn(random.randrange(x-3)+1, random.randrange(y-3)+1)
			mymid.spawn(random.randrange(x-3)+1, random.randrange(y-3)+1)
			
			for itemo in self.items:
				itemo.spawn(random.randrange(x-2)+1, random.randrange(y-2)+1)
			for mobbo in self.mobs:
				mobbo.spawn(random.randrange(x-2)+1, random.randrange(y-2)+1)
			rnumx = random.randrange(x-2)+1
			rnumy = random.randrange(y-2)+1
			self.player1.spawn(rnumx,rnumy)
			self.player1.position_scrn(6,3)
			self.normalize(rnumx,rnumy)	
		
		self.background.add(self.landmarks)	
		self.background.add(self.items)
		self.background.add(self.mobs)
		self.fightable.add(self.mobs)
		
		
	def iterate_Game(self):
		while self.Game_Over == 0:
			
			self.Turn_Over = 0
			self.display()
			self.player1.AP_c = self.player1.AP_max
			for dude in self.mobs:
				dude.AP_c = dude.AP_max
			
			while self.Turn_Over == 0:
				self.player1.visibility = 1
				if self.Game_Over != 0:
							break
								
				#player input	
				for event in pygame.event.get():
						if event.type == pygame.QUIT:
							return
						if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
							return
						if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
							self.player1.command("")
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
						if event.type == pygame.KEYDOWN and event.key == pygame.K_t:
							self.player1.visibility = self.player1.televis
						
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
			print "R.I.P., Ranger Dan."
			return
			
		if self.Game_Over == 4:
			print "You Died of thirst."
			print "R.I.P., Ranger Dan."
		
		
	def display(self):
		screen.fill((0,0,0))
		
		#player stats
		font = pygame.font.Font(None, 20)
		HPstr = "HP: "+str(self.player1.HP_c)+"/"+str(self.player1.HP_max)+"     "
		APstr =  "AP: "+str(self.player1.AP_c)+"/"+str(self.player1.AP_max)+"     "
		HYDstr = "HYD: "+str(self.player1.HYD_c)+"/"+str(self.player1.HYD_max)+"     "
		
		text = font.render(HPstr + APstr+ HYDstr, 1, (255, 255, 255), (0,0,0))
		scrstr = "SCR: "+ str(self.player1.scrnx)+","+str(self.player1.scrny)+"     "
		mapstr = "MAP: "+str(self.player1.mapx)+","+str(self.player1.mapy)+"     "
		debugstr = scrstr + mapstr
		text2 = font.render(debugstr, 1, (255,255,255), (0,0,0))
		axstr = ""
		if self.player1.inventory['axe'] > 0:
			axstr = 'axe'+"   "
		scopestr = ""
		if self.player1.inventory['telescope'] > 0:
			scopestr = 'telescope'+"   "
		cantstr = ""
		if self.player1.inventory['canteen']> 0:
			cantstr = 'canteen'+"   "
		woodstr = ""
		if self.player1.inventory['wood'] > 0:
			woodstr = "Wood: "+ str(self.player1.inventory['wood'])+"     "
		text3 = font.render(axstr+scopestr+cantstr+woodstr, 1, (255,255,255), (0,0,0))
		
		
		#reveal visible sprites
		self.showBG()
		
		# Blit everything to the screen
		screen.set_clip(0,0,self.winx,self.winy)
		#self.revealed.draw(screen)
		for land in self.terrain:
			if land in self.fogged:
				land.draw()
			if land in self.revealed:
				land.draw()
				
		for item in self.items:
			if item in self.revealed:
				item.draw()
				
		for mob in self.mobs:
			if mob in self.revealed:
				mob.draw()
				
		for lm in self.landmarks:
			if lm in self.revealed:
				lm.draw()
				
		self.space.draw(screen)
		self.players.draw(screen)
		screen.blit(text, (0,0))
		screen.blit(text2, (0,50))
		screen.blit(text3, (0,25))
		
		pygame.display.flip()
		
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
		self.players.draw(screen)

	def showBG(self):
		
		for tile in self.terrain:
			if tile in self.revealed:
				self.revealed.remove(tile)
				self.fogged.add(tile)
				tile.fade()
			if abs(tile.mapx-self.player1.mapx)<= self.player1.visibility and abs(tile.mapy-self.player1.mapy)<= self.player1.visibility:
				self.revealed.add(tile)
				if tile in self.fogged:
					self.fogged.remove(tile)
					tile.set_type(tile.flavnum)
					
		for thing in self.items:
			self.revealed.remove(thing)
			for land in pygame.sprite.spritecollide(thing,self.revealed, False):
				self.revealed.add(thing)
				
		for villian in self.mobs:
			if villian in self.revealed:
				self.revealed.remove(villian)
			for land in pygame.sprite.spritecollide(villian,self.revealed, False):
				self.revealed.add(villian)
				
		for lndmrk in self.landmarks:
			
			for land in pygame.sprite.spritecollide(lndmrk,self.revealed, False):
				self.revealed.add(lndmrk)
	
	def normalize(self,x,y):
		#normalize x
		norx = 6- x
		if norx > 0:
			for a in range(norx):
				self.move_BG("R")
				
		elif norx == 0:
			pass
		else:
			for a in range(abs(norx)):
				self.move_BG("L")
		#normalize y	
		nory = 3- y
		if nory > 0:
			for a in range(nory):
				self.move_BG("D")
		elif nory == 0:
			pass
		else:
			for a in range(abs(nory)):
				self.move_BG("U")
		for item in self.items:
			item.position(item.mapx+norx, item.mapy+nory)
		for mob in self.mobs:
			mob.position(mob.mapx+norx, mob.mapy+nory)
		for lm in self.landmarks:
			lm.position(lm.mapx+norx, lm.mapy+nory)
			

########################################################################
if __name__ == '__main__':
	pygame.init()
	mainx = 1200
	mainy = 800
	screen = pygame.display.set_mode((mainx, mainy))#640,480
	pygame.display.set_caption("Explore!")
	Game().main(screen)
