import pygame
import copy as _copy

class Player(pygame.sprite.Sprite):
    def __init__(self, location, Id, window):
        #Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)    
        
        self.window = window
        self.ID = Id
        self.sprite = "sprite.png"

        #Load the image
        self.image = pygame.image.load(self.sprite).convert()
        self.image.set_colorkey((69, 0, 69))

        #set up rectangle locations        
        self.location = location

        self.rect = self.image.get_rect()
        self.rect.center = self.location

    def MoveUp(self):
        self.location += pygame.Vector2(0, -5)
        self.ConfirmMove()
    def MoveDown(self):
        self.location += pygame.Vector2(0, 5)
        self.ConfirmMove()
    def MoveLeft(self):
        self.location += pygame.Vector2(-5, 0)
        self.ConfirmMove()
    def MoveRight(self):
        self.location += pygame.Vector2(5, 0)
        self.ConfirmMove()

    def ConfirmMove(self):
        if self.location[0] > 1280:
            self.location[0] = 1280
        
        elif self.location[0] < 0:
            self.location[0] = 0
        
        if self.location[1] > 720:
            self.location[1] = 720
        
        elif self.location[1] < 0:
            self.location[1] = 0
        
        self.rect.center = self.location
    
    def GetPos(self):
        return (self.location[0], self.location[1])
        
    def Setpos(self, x, y):
        self.location = pygame.Vector2(x, y)
        self.rect.center = self.location

    def GetID(self):
        return self.ID

    def GetAllInfo(self):
        return {
            "Type":"Player",
            "Location":(self.location[0], self.location[1]),
            "PlayerID":self.ID
        }