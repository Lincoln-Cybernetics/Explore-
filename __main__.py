import pygame
import player
import ss
import tile
import random
import item
import mob
import mapgen

class Game(object):
    def main (self, screen):
        
        #general signals
        self.Game_Over = 0
        self.Turn_Over = 0
        self.winx = mainx
        self.winy = mainy
        self.counter = 0
        self.screen = screen
        
        #World
        self.xmax = 40
        self.ymax = 40
        self.mapology = 'Proced1'
        self.season = 0
        self.daycount = 0
        self.daymax = 10
        self.passable = 1
        self.terraformer = mapgen.Mapgen(self)
        
        #spritesheet dis-aggregators
        self.tilex = 100
        self.tiley = 100
        self.sheet = pygame.image.load('Spring.png').convert()
        self.animator = ss.Cutout(self.sheet, self.tilex, self.tiley)
        self.sheet = pygame.image.load('Explm.png').convert()
        self.landgrabber = ss.Cutout(self.sheet,200,200)
        self.sheet = pygame.image.load('mobs.png').convert()
        self.mobdraw = ss.Cutout(self.sheet, self.tilex, self.tiley)
        self.sheet = pygame.image.load('items.png').convert()
        self.warehouse = ss.Cutout(self.sheet, self.tilex, self.tiley)
        
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
        self.visible = pygame.sprite.Group()
        
        #player
        self.player1 = player.Player(self, self.players)
        self.player1.add(self.fightable)
        
        self.mymap = self.terraformer.generate(self.xmax, self.ymax,"grassland")
        self.terraformer.populate(1)
        self.terraformer.litter(5)
        self.terraformer.monumentalize(5)
        self.mapgen(self.xmax,self.ymax,self.mapology)
        
        #self.player1.add_Perk("Swimmer")
        #self.player1.add_Perk("Mountaineer")
        self.iterate_Game()
    
    
        
        
    def mapgen(self, x,y, maptype):
       
        
        if maptype == 'Basic':
        
            self.mymap[4][4].set_type(5)
            self.player1.spawn(3,3)
            self.player1.position_scrn(6,3)
            self.normalize(3,3)
            
        elif maptype == 'Random' or maptype == 'Proced1':
        
            rnumx = random.randrange(x-2)+1
            rnumy = random.randrange(y-2)+1
            self.player1.spawn(rnumx,rnumy)
            for mobbo in self.mobs:
                if mobbo.mapx == self.player1.mapx and mobbo.mapy == self.player1.mapy:
                    mobbo.kill()
            for itemo in self.items:
                if itemo.mapx == self.player1.mapx and itemo.mapy == self.player1.mapy:
                    itemo.kill()
            self.player1.position_scrn(6,3)
            self.normalize(rnumx,rnumy) 
        
        self.background.add(self.landmarks) 
        self.background.add(self.items)
        self.background.add(self.mobs)
        self.fightable.add(self.mobs)
        
        
        #self.terraformer.sea_lower()
        #self.terraformer.sea_fill()  
        #for i in range(1000):
            #self.terraformer.desertify()
            #self.terraformer.grow_forest()
            #self.advance_lands()
        self.terraformer.sea_lower()
        self.terraformer.sea_fill() 
        self.set_unpass() 
        
    def advance_season(self):
        if self.season == 0:
            self.season = 1
            self.sheet = pygame.image.load('Summer.png').convert()
        elif self.season == 1:
            self.season = 2
            self.sheet = pygame.image.load('Fall.png').convert()
        elif self.season == 2:
            self.season = 3
            self.sheet = pygame.image.load('Winter.png').convert()
        elif self.season == 3:
            self.season = 0
            self.sheet = pygame.image.load('Spring.png').convert()  
        self.animator.set_Sheet(self.sheet,100,100)
        #for land in self.terrain:
        #   land.get_image()
        
           
    
   
            
    def advance_lands(self):
        for place in self.terrain:
            place.advance()
            
    def get_passable(self):
        return self.passable
        
    def set_unpass(self):
        for land in self.terrain:
            if land.flavnum == 12:
                for fighter in self.fightable:
                    if "Mountaineer" in fighter.perks:
                        pass
                    else:
                        fighter.unpassable.add(land)
            if land.flavnum == 14 or land.flavnum == 15:
                for fighter in self.fightable:
                    if "Swimmer" in fighter.perks:
                        pass
                    else:
                        fighter.unpassable.add(land)
        
    def iterate_Game(self):
        while self.Game_Over == 0:
            
            self.Turn_Over = 0
            self.display()
            self.player1.AP_c = self.player1.AP_max
            for dude in self.mobs:
                dude.AP_c = dude.AP_max
            
            while self.Turn_Over == 0:
                #self.player1.visibility = 1
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
                            self.player1.mountainview(self.player1.televis)
                        if pygame.key.get_pressed()[pygame.K_t] == False:
                            self.player1.mountainview()
                        
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
            
            self.daycount += 1
            if self.daycount >= self.daymax:
                self.daycount = 0
                self.advance_season()
            if self.season == 1 or self.season == 2:
                self.terraformer.desertify()
            if self.season == 0 or self.season == 1:
                self.terraformer.grow_forest()
            self.advance_lands()
            self.set_unpass()
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
        font = pygame.font.Font(None, 40)
        HPstr = "HP: "+str(self.player1.HP_c)+"/"+str(self.player1.HP_max)+"     "
        APstr =  "AP: "+str(self.player1.AP_c)+"/"+str(self.player1.AP_max)+"     "
        HYDstr = "HYD: "+str(self.player1.HYD_c)+"/"+str(self.player1.HYD_max)+"     "
        SCOREstr = "Score: "+str(self.player1.score)+"     "
        
        text = font.render(HPstr + APstr+ HYDstr+SCOREstr, 1, (255, 255, 255), (0,0,0))
        #scrstr = "SCR: "+ str(self.player1.scrnx)+","+str(self.player1.scrny)+"     "
        #mapstr = "MAP: "+str(self.player1.mapx)+","+str(self.player1.mapy)+"     "
        #debugstr = scrstr + mapstr
        #text2 = font.render(debugstr, 1, (255,255,255), (0,0,0))
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
        self.fogged.draw(screen)
        for thing in self.visible:
            if thing in self.terrain:
                thing.draw()
        for thing in self.visible:
            if thing in self.items:
                thing.draw()
        for thing in self.visible:
            if thing in self.mobs:
                thing.draw()
        for thing in self.visible:
            if thing in self.landmarks:
                thing.draw()
        
                
        self.space.draw(screen)
        self.players.draw(screen)
        screen.blit(text, (0,0))
        #screen.blit(text2, (0,50))
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
                self.visible.remove(tile)
                self.fogged.add(tile)
                tile.fade()
            if abs(tile.mapx-self.player1.mapx)<= self.player1.visibility and abs(tile.mapy-self.player1.mapy)<= self.player1.visibility:
                self.revealed.add(tile)
                self.visible.add(tile)
                if tile in self.fogged:
                    self.fogged.remove(tile)
                    tile.visify()
            
                    
        for thing in self.items:
            self.visible.remove(thing)
            for land in pygame.sprite.spritecollide(thing,self.visible, False):
                if land in self.terrain:
                    self.revealed.add(thing)
                    self.visible.add(thing)
                
        for villian in self.mobs:
            if villian in self.visible:
                self.visible.remove(villian)
            for land in pygame.sprite.spritecollide(villian,self.visible, False):
                if land in self.terrain:
                    self.revealed.add(villian)
                    self.visible.add(villian)
                
        for lndmrk in self.landmarks:
            
            for land in pygame.sprite.spritecollide(lndmrk,self.visible, False):
                self.revealed.add(lndmrk)
                self.visible.add(lndmrk)
                if(lndmrk.revealed == False):
					lndmrk.revealed = True
					self.player1.score += lndmrk.points
    
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
