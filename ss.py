import pygame


#sprite sheet cutter-outer
class Cutout(object):
	def __init__(self, src, w, h):
		#initialize with the target Sprite sheet,
		#along with the dimensions of the sprites
		self.w = w
		self.h = h
		self.rsource = pygame.Rect(0,0,w,h)
		self.srcimg = src
		self.img = pygame.Surface(self.rsource.size).convert()
		self.img.blit(self.srcimg, (0,0), self.rsource)
		self.cktog = False
		self.ck = (0,255,0)
		
	def set_Sheet(self, src, w, h):
		#change the sprite sheet
		self.w = w
		self.h = h
		self.srcimg = src
		
	def set_Img(self, x,y):
		#pass in the indicies of the desired sprite
		myx = x*self.w
		myy = y*self.h
		self.rsource = pygame.Rect(myx,myy,self.w,self.h)
		self.img = pygame.Surface(self.rsource.size).convert()
		self.img.blit(self.srcimg, (0,0), self.rsource)
		self.cktog = False
		
	def get_Img(self):
		#applies colorkey
		if self.cktog:
			self.img.set_colorkey(self.ck)
		#returns the set image
		return self.img
		
	def set_colorkey(self, tog= True, col= (0,255,0)):
		#toggles colorkey on or off
		self.cktog = tog
		#sets colorkey color
		self.ck = col
		
