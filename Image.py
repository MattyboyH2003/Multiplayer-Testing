import pygame

class Image(pygame.sprite.Sprite):
    def __init__(self, image, location, colourKey=(69, 0, 69)):
        #Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)    
        
        #Default instance data
        self.location = location
        self.sprite = image

        #Load the image
        self.image = pygame.image.load(self.sprite).convert()
        self.image.set_colorkey(colourKey)

        #set up rect and location
        self.rect = self.image.get_rect()
        self.rect.center = self.location