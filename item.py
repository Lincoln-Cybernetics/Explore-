import pygame

class Item(pygame.sprite.Sprite):
    def __init__(self, level, *groups):
        super(Item, self).__init__(*groups)
        #the game level
        self.level = level
        #base image
        self.level.animator.set_Img(6,0)
        self.level.animator.set_colorkey((255,0,0))
        self.image = self.level.animator.get_Img().convert()
        
        
        #type
        self.flavor_saver = ['gem', 'axe', 'sammich', 'telescope', 'canteen', 'coin', 'binoculars', 'ruby']
        self.flavor = 'gem'
        self.points = 0
        #location
        self.firstflag = True
        self.scrnx = 0
        self.scrny = 0
        self.mapx = 0
        self.mapy = 0
        
    def spawn(self,x,y):
        self.mapx = x
        self.mapy = y
        if self.flavor == 'coin':
            pass
        else:
            self.level.mymap[self.mapx][self.mapy].set_type(self.level.get_passable())
            self.level.player1.unpassable.remove(self.level.mymap[self.mapx][self.mapy])
        
    def position(self,x,y):
        self.scrnx = x
        self.scrny = y
        self.rect = pygame.rect.Rect((self.scrnx*self.level.tilex, self.scrny*self.level.tiley), self.image.get_size())
    
    def set_type(self, itype):
        self.flavor = self.flavor_saver[itype]
        #gem
        if itype == 0:
            xind = 6
            yind = 0
            self.points = 500
        #axe
        if itype == 1:
            xind = 6
            yind = 5
        #sammich
        if itype == 2:
            xind = 6
            yind = 4
        #telescope
        if itype == 3:
            xind = 6
            yind = 3
        #canteen
        if itype == 4:
            xind = 4
            yind = 4
        #coin
        if itype == 5:
            xind = 5
            yind = 0
            self.points = 50
        #binoculars
        if itype == 6:
            xind = 5
            yind = 3
        #ruby
        if itype == 7:
			xind = 7
			yind = 0
			self.points = 800
            
            
        self.level.warehouse.set_Img(xind,yind)
        self.level.warehouse.set_colorkey(True,(255,0,0))
        self.image = self.level.warehouse.get_Img().convert()
    


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
        
    def draw(self):
        self.level.screen.blit(self.image, (self.rect.x,self.rect.y))
