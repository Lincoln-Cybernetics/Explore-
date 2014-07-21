import pygame
import random
import item
import mob
import tile

class Mapgen(object):
    def __init__(self, level):
        self.xsiz = 10
        self.ysiz = 10
        self.biome = "random"
        self.procedure = 0
        self.zone = []
        self.level = level
        self.sizefactor = 2
        #self.items = pygame.sprite.Group()
        #self.mobs = pygame.sprite.Group()
        
        
    #creates the base map    
    def generate(self,x,y,biome):
        self.zone = []
        self.xsiz = x
        self.ysiz = y
        self.biome = biome
        self.sizefactor = (x/10)+(y/10)
        landtype = 0
        #for num in range(sizefactor*3):
        #    itemo = item.Item(self.level, self.level.items)
        #    itemo.set_type(random.randrange(6)+1)
        #for umb in range(sizefactor*3):
        #    mobbo = mob.Mob(self.level, self.level.mobs)
        #    mobbo.set_type(random.randrange(7))
        #    mobbo.set_species(random.randrange(4)+1)
        #main land generation
        for a in range(x):
            mapcol = []
            for b in range(y):
                
                #Purely Random
                if (self.procedure == 0):
                    landtype = random.randrange(17)+1
                
                #probability manipulation   
                if (self.procedure == 1):
                    
                    if (biome == "grassland"):
                        common = [1,2,3,13]
                        uncommon = [4,5,6,7]
                        rare = [8,9,10]
                        vrare = [12,15]
                        self.level.passable = 1
                        
                    if(biome == "forest"):
                        common = [3,4,5,9]
                        uncommon = [1,2,6]
                        rare = [7,13]
                        vrare = [10,11,12]
                        self.level.passable = 2

                    if(biome == "desert"):
                        common = [8,7]
                        uncommon = [16,17]
                        rare = [9,13]
                        vrare = [1,2]
                        self.level.passable = 7
                        
                    landex = random.randrange(256)
                    if landex < 256:
                        landtype = random.choice(common)
                    if landex < 64:
                        landtype = random.choice(uncommon)
                    if landex < 16:
                        landtype = random.choice(rare)
                    if landex < 2:
                        landtype = random.choice(vrare)
                
                #generate the tiles
                acre = tile.Land(self.level, self.level.terrain)
                if a == 0 or b == 0 or a == x-1 or b == y-1:
                    acre.set_type(0)
                    self.level.space.add(acre)
                    for mobbo in self.level.mobs:
                        mobbo.unpassable.add(acre)
                else:
                    acre.set_type(landtype)
                    acre.get_image()
                    
                acre.spawn(a, b)
                self.level.background.add(acre)
                mapcol.append(acre)
                
            self.zone.append( mapcol )
            for a in range(len(self.zone)):
                for b in range(len(self.zone[0])):
                    place = self.zone[a][b]
                    if place in self.level.space:
                        pass
                    else:
                        for wa in range(3):
                            for ha in range(3):
                                if a+wa-1 >= len(self.zone) or b+ha-1 >= len(self.zone[0]):
                                    pass
                                else:
                                    place.neighbors.add(self.zone[a+wa-1][b+ha-1])
        return self.zone
        
    #causes deserts to expand
    def desertify(self):    
        for place in self.level.terrain:
            place.desert_check()
            
    #causes forests to grow
    def grow_forest(self):
        for place in self.level.terrain:
            place.forest_check()
    
    #lowers sea level        
    def sea_lower(self):
        for place in self.level.terrain:
            if place.flavnum == 15:
                if random.randrange(100) < 80:
                    place.set_type(14)
            if place.flavnum == 14:
                if random.randrange(100) < 70:
                    place.set_type(13)
            if place.flavnum == 13:
                if random.randrange(100) < 60:
                    place.set_type(1)
     
     #raises sea level   
    def sea_fill(self):
        for place in self.level.terrain:
            excepts = [0,15,14,12,11,10]
            
            if place.flavnum == 15:
                
                for location in place.neighbors:
                    if location.flavnum in excepts:
                        pass
                    else:
                        location.set_type(14)
        
            if place.flavnum == 14:
                
                for location in place.neighbors:
                    if location.flavnum in excepts:
                        pass
                    else:
                        location.set_type(13)
                        
            if place.flavnum == 13:
                
                for location in place.neighbors:
                    if random.randrange(100) < 10:
                        if location.flavnum in excepts:
                            pass
                        else:
                            location.set_type(13)
                            
                            
    #populates the map with mobs
    def populate(self, density):
        for a in range(self.sizefactor*density):
            mobbo = mob.Mob(self.level, self.level.mobs)
            mobbo.set_type(random.randrange(7))
            mobbo.set_species(random.randrange(4)+1)
            mobbo.unpassable.add(self.level.space)
            mobbo.spawn(random.randrange(len(self.zone)-2)+1,random.randrange(len(self.zone[0])-2)+1)
            if mobbo.mapx == self.level.player1.mapx and mobbo.mapy == self.level.player1.mapy:
                mobbo.kill()

    #adds items to the map
    def litter(self, density):
        for a in range(self.sizefactor*density):
            itemo = item.Item(self.level, self.level.items)
            itemo.set_type(random.randrange(8))
            itemo.spawn(random.randrange(len(self.zone)-2)+1,random.randrange(len(self.zone[0])-2)+1)
            if itemo.mapx == self.level.player1.mapx and itemo.mapy == self.level.player1.mapy:
                itemo.kill()
                
    #adds landmarks
    def monumentalize(self, number):
        for a in range(number):
            monument = tile.Landmark(self.level, self.level.background)
            monument.set_type(random.randrange(4))
            monument.spawn(random.randrange(len(self.zone)-3)+1,random.randrange(len(self.zone[0])-3)+1)
            pygame.sprite.spritecollide(monument, self.level.landmarks, True)
            self.level.landmarks.add(monument)
    
