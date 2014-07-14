import pygame
import random

class Mob(pygame.sprite.Sprite):
    def __init__(self, level, *groups):
        super(Mob, self).__init__(*groups)
        #My BRAIN!
        self.brain = Brain(self)
        #the game level
        self.level = level
        
        #sprite groups
        self.unpassable = pygame.sprite.Group()
        
        #base image
        self.level.mobdraw.set_Img(3,0)
        self.level.mobdraw.set_colorkey(True,(255,0,0))
        self.image = self.level.mobdraw.get_Img().convert()
        
        
        
        
        
        #type
        self.ATflag = 0#All-Terrain flag
        self.species = "Hobnail"
        self.taxonomy = ["Hobnail", "Bear", "Yeti", "Sasquatch"]
        
        #location
        self.firstflag = True
        self.mapx = 0 
        self.mapy = 0 
        self.scrnx = 0
        self.scrny = 0
        #reference of old location data
        
        self.pxs = self.scrnx
        self.pys = self.scrny
        self.pmx = self.mapx
        self.pmy = self.mapy
        
        #status
        self.Turn_Over = False
        self.Alive = True
        self.AP_max = 5
        self.AP_c = 5
        self.APcost = {"U": 1, "D": 1, "L": 1, "R": 1, "UL":2, "UR": 2, "LL": 2, "LR":2, "Chop":3, "Plant": 3}
        self.trycount = 0
        self.trythresh = 20
        self.visibility = 1
        self.vision = 1
        self.inventory = {'axe':0,'wood':0}
        self.perks = []
        
        self.skipflag = False
        
        #fighting
        self.HP_max = 5
        self.HP_c = 5
        self.ATT = 2
        self.DEF = 1
        self.DMG = 0
        self.HYD_max = 10
        self.HYD_c = 10
        self.enemy = 0
        
    def sees_player(self):
        if abs(self.mapx-self.level.player1.mapx) <= self.visibility and abs(self.mapy-self.level.player1.mapy) <= self.visibility:
            return True
        else:
            return False
            
    def set_species(self, kind):
        self.species = self.taxonomy[kind]
        #Hobnail
        if kind == 0:
            self.ATflag = 0
            self.AP_max = 5
            self.AP_c = 5
            self.HP_max = 5
            self.HP_c = 5
            self.ATT = 2
            self.DEF = 1
            self.DMG = 0
            self.HYD_max = 10
            self.HYD_c = 10
        #Bear
        if kind == 1:
            self.ATflag = 0
            self.ATT = 4
            self.DMG = 1
            self.HP_max = 8
            self.HP_c = 8
            self.AP_max = 4
            self.AP_c = 4
            self.HYD_max = 10
            self.HYD_c = 10
            
        #Yeti
        if kind == 2:
            self.ATflag = 0
            self.ATT = 4
            self.DMG = 1
            self.HP_max = 8
            self.HP_c = 8
            self.AP_max = 4
            self.AP_c = 4
            self.HYD_max = 10
            self.HYD_c = 10
            
        #Sasquatch
        if kind == 3:
            self.ATflag = 0
            self.ATT = 4
            self.DMG = 1
            self.HP_max = 8
            self.HP_c = 8
            self.AP_max = 4
            self.AP_c = 4
            self.HYD_max = 10
            self.HYD_c = 10
        
        self.set_Image("Species")   
    
    def add_Perk(self,perk):
        self.perks.append(perk)
        if perk == "Early Bird":
            self.AP_max += 4
        if perk == "Eagle Eye":
            self.vision += 1    
        if perk == "Hearty":
            self.HP_max += 5
            self.HP_c += 5
        if perk == "Strong":
            self.DMG += 2
            self.APcost["Chop"] -= 1
        if perk == "Fighter":
            self.ATT += 2
            self.DEF += 2
        if perk == "Swimmer":
            for land in self.unpassable:
                if land.flavor == "Ocean" or land.flavor == "Whirlpool":
                    self.unpassable.remove(land)
        if perk == "Runner":
            #moves = ["U","D","L","R","UL","UR","LL","LR"]
            #for move in moves:
            #    self.APcost[move] -= 1
            pass
        
    def set_Image(self, hint):
        xind = 0
        yind = 0
        if hint == "Species":
            if self.species == "Hobnail":
                xind = 3
                yind = 0
            if self.species == "Bear":
                xind = 7
                yind = 0
            if self.species == "Yeti":
                xind = 3
                yind = 1
            if self.species == "Sasquatch":
                xind = 7
                yind = 1
                
        if hint == "Angry":
            if self.species == "Hobnail":
                xind = 1
                yind = 0
            if self.species == "Bear":
                xind = 5
                yind = 0
            if self.species == "Yeti":
                xind = 1
                yind = 1
            if self.species == "Sasquatch":
                xind = 5
                yind = 1
                
        if hint == "Scared":
            if self.species == "Hobnail":
                xind = 2
                yind = 0
            if self.species == "Bear":
                xind = 6
                yind = 0
            if self.species == "Yeti":
                xind = 2
                yind = 1
            if self.species == "Sasquatch":
                xind = 6
                yind = 1
                
        if hint == "Dead":
            if self.species == "Hobnail":
                xind = 0
                yind = 0
            if self.species == "Bear":
                xind = 4
                yind = 0
            if self.species == "Yeti":
                xind = 0
                yind = 1
            if self.species == "Sasquatch":
                xind = 4
                yind = 1
                
        if hint == "Fight":
            xind = random.randrange(4)
            yind = 5
                
        #set the sprite image
        self.level.mobdraw.set_Img(xind,yind)
        self.level.mobdraw.set_colorkey(True,(255,0,0))
        self.image = self.level.mobdraw.get_Img().convert()
        
        
    def set_type(self, personality):
            self.brain.set_personality(personality)
                
    def fight(self, opponent):
        if self.ATT > opponent.DEF:
            opponent.damage(self.DMG)               
    
    def damage(self, dmg):
        self.HP_c -= dmg
        if self.HP_c <= 0:
            self.Alive = False
            self.set_Image("Dead")
            self.brain.set_personality(0)
                                    
        
    def spawn(self,x,y):
        self.mapx = x
        self.mapy = y
        self.myloc = self.level.mymap[self.mapx][self.mapy]
        

    def position(self,x,y):
        self.scrnx = x
        self.scrny = y
        self.rect = pygame.rect.Rect((self.scrnx*self.level.tilex, self.scrny*self.level.tiley), self.image.get_size())
        self.prevrect = self.rect.copy()
        
    def mountainview(self, aug= 0):
        if self.myloc.flavor == "Mountain" or self.myloc.flavor == "Extinct Volcano" or self.myloc.flavor == "Active Volcano":
            self.visibility = self.vision + 2 + aug
        elif self.myloc.flavor == "Hills":
            self.visibility = self.vision + 1 + aug
        else:
            self.visibility = self.vision + aug

    def itemcheck(self):
        pass

    def spacecheck(self):
        for space in pygame.sprite.spritecollide(self, self.level.space, False):
            self.Alive = False
            self.kill()
        if self.mapx >= len(self.level.mymap) or self.mapx <= 0:
            self.Alive = False
            self.kill()
        if  self.mapy >= len(self.level.mymap[self.mapx]) or self.mapy <= 0:
            self.Alive = False
            self.kill()
            
    def mobcheck(self):
        self.enemy = 0
        for mob in pygame.sprite.spritecollide(self, self.level.fightable, False):
            if mob == self:
                pass
            else:
                self.enemy = mob
                self.fight(mob)
                if mob.Alive == False:
                    mob.kill()
                    return True
                return False
        return True
        
    def TOcheck(self):
        if self.skipflag == False:
            APnums = []
            APmin = self.AP_max
            APnums.append(self.AP_check( self.level.mymap[self.mapx][self.mapy-1] , "U") )
            APnums.append(self.AP_check( self.level.mymap[self.mapx][self.mapy+1] , "D") )
            APnums.append(self.AP_check( self.level.mymap[self.mapx-1][self.mapy] , "L") )
            APnums.append(self.AP_check( self.level.mymap[self.mapx+1][self.mapy] , "R") )
            APnums.append(self.AP_check( self.level.mymap[self.mapx-1][self.mapy-1] , "UL") )
            APnums.append(self.AP_check( self.level.mymap[self.mapx+1][self.mapy-1] , "UR") )
            APnums.append(self.AP_check( self.level.mymap[self.mapx-1][self.mapy+1] , "LL") )
            APnums.append(self.AP_check( self.level.mymap[self.mapx+1][self.mapy+1] , "LR") )
            if self.inventory['axe'] > 0:
                APnums.append(  self.APcost["Chop"] )
            if self.inventory['wood'] > 0:
                APnums.append(  self.APcost["Plant"] )
            for pos in APnums:
                if pos < APmin:
                    APmin = pos
            if self.AP_c <= APmin:
                self.level.Turn_Over = 1
    
    def AP_check(self, biome, com):
        tot = 0
        tot += self.APcost[com]
        tot += biome.AP_cost
        if "Swimmer" in self.perks:
            if biome.flavor == "Water" or biome.flavor == "Ocean" or biome.flavor == "Whirlpool":
                if biome in self.unpassable:
                    self.unpassable.remove(biome)
                tot -= 1
        if "Runner" in self.perks:
            if biome.flavor != "Water" or biome.flavor != "Ocean" or biome.flavor != "Whirlpool":
                tot -= 1
        if tot < 1:
            tot = 1
        return tot      

    
    def hydrate(self):
        for land in pygame.sprite.spritecollide(self, self.level.terrain, False):
            if land.flavor == "Scrub":
                self.HYD_c -= 1
            elif land.flavor == "Dunes":
                self.HYD_c -= 2
            elif land.flavor == "Water":
                self.HYD_c = self.HYD_max
            elif land.flavor == "Oasis":
                self.HYD_c += 10
        if self.HYD_c <= 0:
            self.HP_c -= 1
            if self.HP_c <= 0:
                self.alive = False
                self.set_Image("Dead")
                self.brain.set_personality(0)
        if self.HYD_c > self.HYD_max:
            self.HYD_c = self.HYD_max
        
    def command(self, cmd):
        #self.spacecheck()
        #reference of old location data
        self.prevrect = self.rect.copy()
        self.pxs = self.scrnx
        self.pys = self.scrny
        self.pmx = self.mapx
        self.pmy = self.mapy
        self.skipflag = False
        
        #Move Up
        if cmd == "U":
            target = self.level.mymap[self.mapx][self.mapy-1]
            APnum = self.AP_check(target, cmd)
            if target in self.unpassable:
                pass
            else:
                if self.reckonAP(APnum):
                    self.move("U")
                else:
                    self.skipflag = True
        
        #Move Down          
        if cmd == "D":
            target = self.level.mymap[self.mapx][self.mapy+1]
            APnum = self.AP_check(target, cmd)
            if target in self.unpassable:
                pass
            else:
                if self.reckonAP(APnum):
                    self.move("D")
                else:
                    self.skipflag = True
                    
        #Move Left
        if cmd == "L":
            target = self.level.mymap[self.mapx-1][self.mapy]
            APnum = self.AP_check(target, cmd)
            if target in self.unpassable:
                pass
            else:
                if self.reckonAP(APnum):
                    self.move("L")
                else:
                    self.skipflag = True
                    
        #Move Right
        if cmd == "R":
            target = self.level.mymap[self.mapx+1][self.mapy]
            APnum = self.AP_check(target, cmd)
            if target in self.unpassable:
                pass
            else:
                if self.reckonAP(APnum):
                    self.move("R")
                else:
                    self.skipflag = True
                    
        #Move up and left
        if cmd == "UL":
            target = self.level.mymap[self.mapx-1][self.mapy-1]
            APnum = self.AP_check(target, cmd)
            if target in self.unpassable:
                pass
            else:
                if self.reckonAP(APnum):
                    self.move("UL")
                else:
                    self.skipflag = True
                    
        #Move up and Right
        if cmd == "UR":
            target = self.level.mymap[self.mapx+1][self.mapy-1]
            APnum = self.AP_check(target, cmd)
            if target in self.unpassable:
                pass
            else:
                if self.reckonAP(APnum):
                    self.move("UR")
                else:
                    self.skipflag = True
                    
        #Move down and left
        if cmd == "LL":
            target = self.level.mymap[self.mapx-1][self.mapy+1]
            APnum = self.AP_check(target, cmd)
            if target in self.unpassable:
                pass
            else:
                if self.reckonAP(APnum):
                    self.move("LL")
                else:
                    self.skipflag = True
                    
        #Move down and right
        if cmd == "LR":
            target = self.level.mymap[self.mapx+1][self.mapy+1]
            APnum = self.AP_check(target, cmd)
            if target in self.unpassable:
                pass
            else:
                if self.reckonAP(APnum):
                    self.move("LR")
                else:
                    self.skipflag = False
                    
        #Chop Trees 
        if cmd == "Chop":
            choppable = { "Dense Woods":4, "Medium Woods":3, "Light Woods": 2, "Grass and Trees":1 }
            if self.inventory['axe'] > 0:
                if self.level.mymap[self.mapx][self.mapy].flavor in choppable:
                    if self.reckonAP(self.APcost[cmd]):
                        self.inventory['wood'] += self.level.mymap[self.mapx][self.mapy].wood_level
                        self.level.mymap[self.mapx][self.mapy].set_type(choppable[self.level.mymap[self.mapx][self.mapy].flavor])
                        self.level.mymap[self.mapx][self.mapy].reset()
                    else:
                        self.skipflag = True
            
        #Plant Trees
        if cmd == "Plant":
            if self.level.mymap[self.mapx][self.mapy].flavor == "Grassland":
                if self.inventory['wood'] > 0:
                    if self.reckonAP(self.APcost[cmd]):
                        self.level.mymap[self.mapx][self.mapy].set_type(2)
                        self.inventory['wood'] -= 1
                        self.level.mymap[self.mapx][self.mapy].reset()
                    else:
                        self.skipflag = True
                
        #Do Nothing         
        if cmd == "":
            pass
            
        self.spacecheck()
        if self.mobcheck() == False:
            self.rect = self.prevrect
            self.scrnx = self.pxs
            self.scrny = self.pys
            self.mapx = self.pmx
            self.mapy = self.pmy
            self.enemy.set_Image("Fight")
            self.level.display()
            pygame.time.wait(500)
            self.enemy.remember('img')
            self.level.display()    
        
        self.myloc = self.level.mymap[self.mapx][self.mapy] 
        
        if self.skipflag == False:
            self.mountainview() 
            self.spacecheck()
            self.itemcheck()
            self.hydrate()
            self.TOcheck()
                                
        #if self.AP_c <= 0:
        #   self.Turn_Over = True
            
                
    def move(self, vec):
        if vec == "U":
            self.mapy -= 1
            self.scrny -= 1
        if vec == "D":
            self.mapy += 1
            self.scrny += 1
        if vec == "L":
            #self.set_Image('L')
            self.mapx -= 1
            self.scrnx -= 1
        if vec == "R":
            #self.set_Image('R')
            self.mapx += 1
            self.scrnx += 1
        if vec == "UL":
            #self.set_Image('L')
            self.mapy -= 1
            self.mapx -= 1
            self.scrny -= 1
            self.scrnx -= 1
        if vec == "UR":
            #self.set_Image('R')
            self.mapy -= 1
            self.mapx += 1
            self.scrny -= 1
            self.scrnx += 1
        if vec == "LL":
            #self.set_Image('L')
            self.mapy += 1
            self.mapx -= 1
            self.scrny += 1
            self.scrnx -= 1
        if vec == "LR":
            #self.set_Image('R')
            self.mapy += 1
            self.mapx += 1
            self.scrny += 1
            self. scrnx += 1
        self.rect.x = self.scrnx*self.level.tilex
        self.rect.y = self.scrny*self.level.tiley

    def reckonAP(self, cost):
        if self.AP_c >= cost:
            self.AP_c -= cost
            return True
        else:
            return False
    
    def set_Index(self, x, y):
        self.scrnx = x
        self.rect.x = x*self.level.tilex
        self.scrny = y
        self.rect.y = y*self.level.tiley
        
    def get_Index(self, axis):
        if axis == 'X':
            return self.scrnx
        if axis == 'Y':
            return self.scrny
        return -1

    def take_turn(self):
        self.trycount = 0
        self.Turn_Over = False
        while self.Turn_Over == False:
            self.trycount += 1
            self.brain.think()
            self.brain.get_Action()
            if self.AP_c <= 0 or self.trycount > self.trythresh:
                self.Turn_Over = True
        
        return
        
    def remember(self, param):
        if param == "img":
            if self.brain.state == "Charger":
                self.set_Image("Angry")
            elif self.brain.state == "Scared":
                self.set_Image("Scared")
            elif self.Alive == False:
                self.set_Image("Dead")
            else:
                self.set_Image("Species")
        else:
            pass
            
        
    def draw(self):
        self.level.screen.blit(self.image, (self.rect.x,self.rect.y))
###end of mob class###

class Brain(object):
    def __init__(self, body):
        #attach the brain to the body
        self.body = body
        #personality types
        self.ptypes = ["Static", "Lemming", "Wanderer", "Charger", "Scared", "Hunter"]
        self.flavor = "Static"
        self.fnum = 0
        #states
        self.state = "Static"
        self.turncount = 0
        #preferred direction
        self.perferred_d = "L"
        self.goax = 0
        self.goaly = 0
        #count attempted, unsuccessful actions
        self.trycount = 0
        
        
    def set_personality(self, persona):
        self.flavor = self.ptypes[persona]
        self.fnum = persona
        if persona < 5:
            self.state = self.flavor
            if persona == 3:
                self.body.set_Image("Angry")
            if persona == 4:
                self.body.set_Image("Scared")
        if persona == 5:
            if self.body.sees_player():
                self.state = "Charger"
                self.body.set_Image("Angry")
            else:
                self.state = "Wanderer"
                self.set_Image("Species")
        
    def get_Action(self):
        
        if self.state == "Static":
            self.body.Turn_Over = True
            return
            
        if self.state == "Lemming":
            self.body.command(self.perferred_d)
            return
                
        if self.state == "Wanderer":
            dirs = ["U", "D", "L", "R", "UL", "UR", "LL", "LR"]
            self.body.command(random.choice(dirs))
            return

        if self.state == "Charger":
            if self.body.AP_c >= 2:
                if self.body.mapx > self.body.level.player1.mapx and self.body.mapy > self.body.level.player1.mapy:
                    self.body.command("UL")
                if self.body.mapx < self.body.level.player1.mapx and self.body.mapy > self.body.level.player1.mapy:
                    self.body.command("UR")
                if self.body.mapx > self.body.level.player1.mapx and self.body.mapy < self.body.level.player1.mapy:
                    self.body.command("LL")
                if self.body.mapx < self.body.level.player1.mapx and self.body.mapy < self.body.level.player1.mapy:
                    self.body.command("LR")
            if self.body.mapx > self.body.level.player1.mapx:
                self.body.command("L")
            if self.body.mapx < self.body.level.player1.mapx:
                self.body.command("R")
            if self.body.mapy > self.body.level.player1.mapy:
                self.body.command("U")
            if self.body.mapy < self.body.level.player1.mapy:
                self.body.command("D")
            return
            
        if self.state == "Scared":
            if self.body.AP_c >= 2:
                if self.body.mapx > self.body.level.player1.mapx and self.body.mapy > self.body.level.player1.mapy:
                    self.body.command("LR")
                if self.body.mapx < self.body.level.player1.mapx and self.body.mapy > self.body.level.player1.mapy:
                    self.body.command("LL")
                if self.body.mapx > self.body.level.player1.mapx and self.body.mapy < self.body.level.player1.mapy:
                    self.body.command("UR")
                if self.body.mapx < self.body.level.player1.mapx and self.body.mapy < self.body.level.player1.mapy:
                    self.body.command("UL")
            if self.body.mapx > self.body.level.player1.mapx:
                self.body.command("R")
            if self.body.mapx < self.body.level.player1.mapx:
                self.body.command("L")
            if self.body.mapy > self.body.level.player1.mapy:
                self.body.command("D")
            if self.body.mapy < self.body.level.player1.mapy:
                self.body.command("U")
            return
            
    def think(self):
        if self.fnum < 5:
            if self.fnum == 3:
                self.body.set_Image("Angry")
            if self.fnum == 4:
                self.body.set_Image("Scared")
            return
        if self.fnum == 5:
            if self.state == "Charger":
                self.body.set_Image("Angry")
            else:
                if self.body.sees_player():
                    self.state = "Charger"
                    self.body.set_Image("Angry")
                else:
                    self.state = "Wanderer"
                    self.body.set_Image("Species")
            
            
###end of Brain class###
