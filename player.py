import pygame
import random

class Player(pygame.sprite.Sprite):
    def __init__(self, level, *groups):
        super(Player, self).__init__(*groups)
        #the game level
        self.level = level
        
        #spritegrups
        self.unpassable = pygame.sprite.Group()
        
        #base image
        self.set_Image('R')
        self.orient = 'R'
        self.scrnx = 0
        self.mapx = 0
        self.scrny = 0
        self.mapy = 0
        #self.myloc = self.level.mymap[self.mapx][self.mapy]
        
        #reference of old location data
        self.pxs = self.scrnx
        self.pys = self.scrny
        self.pmx = self.mapx
        self.pmy = self.mapy
        self.bgsig = ""
        
        #item inventory
        self.inventory = {'axe': 0, 'wood': 0, 'telescope': 0, 'canteen':0, 'bearskin':0, 'squatchhide':0, 'yetiskin':0, 'coin':0, 'binoculars':0}
        
        #player stats
        self.visibility = 1
        self.vision = 1
        self.televis = 0
        self.screen_border = 1
        self.AP_max = 10
        self.AP_c = 10
        self.APcost = {"U": 1, "D": 1, "L": 1, "R": 1, "UL":2, "UR": 2, "LL": 2, "LR":2, "Chop":3, "Plant": 3}
        self.perks = []
        
        #fighting
        self.HP_max = 10
        self.HP_c = 10
        self.ATT = 3
        self.DEF = 2
        self.DMG = 2
        self.enemy = 0
        
        #status
        self.Alive = True
        self.HYD_max = 10
        self.HYD_c = 10
        self.skipflag = False
        
    def spawn(self,x,y):
        self.mapx = x
        self.mapy = y
        self.myloc = self.level.mymap[self.mapx][self.mapy]
        
        
    def position_scrn(self,x,y):
        self.scrnx = x
        self.scrny = y
        self.rect = pygame.rect.Rect((x * self.level.tilex, y * self.level.tiley), self.image.get_size())
        self.prevrect = self.rect.copy()
        
    def add_Perk(self,perk):
        #must be called AFTER the map is created
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
            pass
        if perk == "Mountaineer":
            for land in self.unpassable:
                if land.flavor == "Active Volcano":
                    self.unpassable.remove(land)
            
            
        
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
        if "Mountaineer" in self.perks:
            if biome.flavnum == 12 or biome.flavnum == 11 or biome.flavnum == 10:
                tot -= 1
        if tot < 1:
            tot = 1
        return tot      

    def command(self, cmd):
            #print cmd
            #reference of old location data
            self.myloc = self.level.mymap[self.mapx][self.mapy]
            self.prevrect = self.rect.copy()
            self.pxs = self.scrnx
            self.pys = self.scrny
            self.pmx = self.mapx
            self.pmy = self.mapy
            self.bgsig = ""
            self.skipflag = False
            
            #Move Up
            if cmd == "U":
                target = self.level.mymap[self.mapx][self.mapy-1]
                APnum = self.AP_check(target, cmd)
                if "Runner" in self.perks and target.flavnum != 13 and target.flavnum != 14 and target.flavnum != 15:
                    APnum -= 1
                if APnum < 1:
                    APnum = 1
                if target in self.unpassable:
                    pass
                else:
                    if self.reckonAP(APnum):
                        self.mapy -= 1
                        if self.scrny*self.level.tiley <= self.level.tiley*self.screen_border:
                            self.bgsig = "D"
                            self.level.move_BG(self.bgsig)  
                        else:
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
                        self.mapy += 1
                        if self.scrny*self.level.tiley >= self.level.winy-((self.level.tiley*(self.screen_border+1))):
                            self.bgsig = "U"
                            self.level.move_BG(self.bgsig)  
                        else:
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
                        self.mapx -= 1
                        if self.scrnx*self.level.tilex <= self.level.tilex*self.screen_border:
                            self.bgsig = "R"
                            self.level.move_BG(self.bgsig)  
                        else:
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
                        self.mapx += 1
                        if self.scrnx*self.level.tilex >= self.level.winx-((self.level.tilex*(self.screen_border+1))):
                            self.bgsig = "L"
                            self.level.move_BG(self.bgsig)  
                        else:
                            self.move("R")
                    else:
                        self.skipflag = True
                        
            #Move Up and Left
            if cmd == "UL":
                target = self.level.mymap[self.mapx-1][self.mapy-1]
                APnum = self.AP_check(target, cmd)
                if  target in self.unpassable:
                    pass
                else:
                    if self.reckonAP(APnum):
                        self.mapx -= 1
                        self.mapy -= 1
                        if self.scrny*self.level.tiley <= self.level.tiley*self.screen_border or self.scrnx*self.level.tilex <= self.level.tilex*self.screen_border:
                            self.bgsig = "LR"
                            self.level.move_BG(self.bgsig)  
                        else:
                            self.move("UL")
                    else:
                        self.skipflag = True
                        
            #Move Up and Right
            if cmd == "UR":
                target = self.level.mymap[self.mapx+1][self.mapy-1]
                APnum = self.AP_check(target, cmd)
                if target in self.unpassable:
                    pass
                else:
                    if self.reckonAP(APnum):
                        self.mapx += 1
                        self.mapy -= 1
                        if self.scrny*self.level.tiley <= self.level.tiley*self.screen_border or self.scrnx*self.level.tilex >= self.level.winx-((self.level.tilex*(self.screen_border+1))):
                            self.bgsig = "LL"
                            self.level.move_BG(self.bgsig)  
                        else:
                            self.move("UR")
                    else: 
                        self.skipflag = True
                        
            #Move Down and Left
            if cmd == "LL":
                target = self.level.mymap[self.mapx-1][self.mapy+1]
                APnum = self.AP_check(target, cmd)
                if target in self.unpassable:
                    pass
                else:
                    if self.reckonAP(APnum):
                        self.mapx -= 1
                        self.mapy += 1
                        if self.scrny*self.level.tiley >= self.level.winy-((self.level.tiley*(self.screen_border+1))) or self.scrnx*self.level.tilex <= self.level.tilex*self.screen_border:
                            self.bgsig = "UR"
                            self.level.move_BG(self.bgsig)  
                        else:
                            self.move("LL")
                    else:
                        self.skipflag = True
                        
            #Move Down and Right
            if cmd == "LR":
                target = self.level.mymap[self.mapx+1][self.mapy+1]
                APnum = self.AP_check(target, cmd)
                if target in self.unpassable:
                    pass
                else:
                    if self.reckonAP(APnum):
                        self.mapx += 1
                        self.mapy += 1
                        if self.scrny*self.level.tiley >= self.level.winy-((self.level.tiley*(self.screen_border+1))) or self.scrnx*self.level.tilex >= self.level.winx-((self.level.tilex*(self.screen_border+1))):
                            self.bgsig = "UL"
                            self.level.move_BG(self.bgsig)  
                        else:
                            self.move("LR")
                    else:
                        self.skipflag = True
                
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
            
            if self.mobcheck() == False:
                self.rect = self.prevrect
                self.scrnx = self.pxs
                self.scrny = self.pys
                self.mapx = self.pmx
                self.mapy = self.pmy    
                if self.bgsig != "":
                    bs = {"U":"D", "D":"U", "L":"R", "R":"L", "UL":"LR", "LR":"UL", "UR":"LL", "LL":"UR"}
                    self.level.move_BG(bs[self.bgsig])
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
                
    def move(self, vec):
        if vec == "U":
            self.scrny -= 1
        if vec == "D":
            self.scrny += 1
        if vec == "L":
            self.set_Image('L')
            self.scrnx -= 1
        if vec == "R":
            self.set_Image('R')
            self.scrnx += 1
        if vec == "UL":
            self.set_Image('L')
            self.scrny -= 1
            self.scrnx -= 1
        if vec == "UR":
            self.set_Image('R')
            self.scrny -= 1
            self.scrnx += 1
        if vec == "LL":
            self.set_Image('L')
            self.scrny += 1
            self.scrnx -= 1
        if vec == "LR":
            self.set_Image('R')
            self.scrny += 1
            self. scrnx += 1
            
        self.rect.x = self.scrnx*self.level.tilex
        self.rect.y = self.scrny*self.level.tiley
        
    def spacecheck(self):
        for space in pygame.sprite.spritecollide(self, self.level.space, False):
            self.skipflag = True
            self.level.Game_Over = 1
        
        
    def itemcheck(self):
        for item in pygame.sprite.spritecollide(self, self.level.items, True):
            if item.flavor == 'gem':
                self.level.Game_Over = 2
                
            if item.flavor == 'axe':
                self.inventory['axe'] += 1
                
            if item.flavor == 'sammich':
                self.HP_c = self.HP_max
                
            if item.flavor == 'telescope':
                #self.visibility += 1
                #if self.visibility > 4:
                #   self.visibility = 4
                self.televis = 2
                self.screen_border = 3
                self.inventory['telescope'] += 1
                
            if item.flavor == 'binoculars':
                if self.inventory['telescope'] <= 0:
                    self.televis = 1
                    self.screen_border = 2
                self.inventory['binoculars'] += 1
                
            if item.flavor == 'canteen':
                self.HYD_max += 10
                if self.HYD_max > 40:
                    self.HYD_max = 40
                self.inventory['canteen'] += 1
                
            if item.flavor == 'coin':
                self.inventory['coin'] += 1
                
                
    def hydrate(self):
        for land in pygame.sprite.spritecollide(self, self.level.terrain, False):
            #print land.wood_level, land.wp
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
                self.level.Game_Over = 4
        if self.HYD_c > self.HYD_max:
            self.HYD_c = self.HYD_max
            
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
            if self.AP_c < APmin:
                self.level.Turn_Over = 1
                
    def mountainview(self, aug= 0):
        if self.myloc.flavor == "Mountain" or self.myloc.flavor == "Extinct Volcano" or self.myloc.flavor == "Active Volcano":
            self.visibility = self.vision + 2 + aug
        elif self.myloc.flavor == "Hills":
            self.visibility = self.vision + 1 + aug
        else:
            self.visibility = self.vision + aug

    def set_Image(self, name):
        xind = 7
        yind = 2
        if name == 'L':
            self.orient = 'L'
            xind = 7
            yind = 3
        if name == 'R':
            self.orient = 'R'
            xind = 7
            yind = 2
            
        self.level.animator.set_Img(xind,yind)
        self.image = self.level.animator.get_Img().convert()
        self.image.set_colorkey((255,0,0))
        
        if name == "Fight":
            xind = random.randrange(4)
            yind = 5
            self.level.mobdraw.set_Img(xind,yind)
            self.image = self.level.mobdraw.get_Img().convert()
            self.image.set_colorkey((255,0,0))

    def remember(self,parameter):
        if parameter == 'img':
            self.set_Image(self.orient)
        else:
            pass
    

    def reckonAP(self, cost):
        if self.AP_c >= cost:
            self.AP_c -= cost
            return True
        else:
            return False

    def mobcheck(self):
        for mob in pygame.sprite.spritecollide(self, self.level.fightable, False):
            self.enemy = 0
            if mob == self:
                pass
            else:
                self.enemy = mob
                if mob.Alive == True:
                    self.fight(mob)
                    return False
                if mob.Alive == False:
                    for item in mob.inventory.keys():
                        self.inventory[item] += mob.inventory[item]
                    mob.kill()
                    return True
        return True
        
    def fight(self, opponent):
        if self.ATT > opponent.DEF:
            opponent.damage(self.DMG, self)
            
    def damage(self, dmg, source= None):
        self.HP_c -= dmg
        if self.HP_c <= 0:
            self.level.Game_Over = 3
        
    
