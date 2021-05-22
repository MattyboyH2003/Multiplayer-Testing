import pygame

class Player(pygame.sprite.Sprite): #Player class for creating players
    def __init__(self, location, Id, window):
        """
        `location` as Pygame.math.Vector2\n
        `Id` as int\n
        `window` as pygame.display
        """
        #Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)    
        
        #Default instance data
        self.window = window
        self.ID = Id
        self.location = location
        self.sprite = "sprite.png"

        #Load the image
        self.image = pygame.image.load(self.sprite).convert()
        self.image.set_colorkey((69, 0, 69))

        #set up rect and location
        self.rect = self.image.get_rect()
        self.rect.center = self.location

    def MoveUp(self):
        """
        Move the player up
        """
        self.location += pygame.Vector2(0, -5)
        self.ConfirmMove()
    def MoveDown(self):
        """
        Move the player down
        """
        self.location += pygame.Vector2(0, 5)
        self.ConfirmMove()
    def MoveLeft(self):
        """
        Move the player left
        """
        self.location += pygame.Vector2(-5, 0)
        self.ConfirmMove()
    def MoveRight(self):
        """
        Move the player right
        """
        self.location += pygame.Vector2(5, 0)
        self.ConfirmMove()

    def ConfirmMove(self):
        """
        Check the user isn't trying to go off the screen\n
        Currently uses the central location of the sprite,
        Screen bounds are currently set to 720p width and height
        """
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
        """
        returns the location of the player as a 2 part tuple not pygame.math.Vector2
        """
        return (self.location[0], self.location[1])
        
    def Setpos(self, x, y):
        """
        Updates players location to given `x` and `y`
        """
        self.location = pygame.Vector2(x, y)
        self.rect.center = self.location

    def GetID(self):
        """
        returns the ID of this instance of `Player`
        """
        return self.ID

    def GetAllInfo(self):
        """
        returns a dictionary containing all necesarry data to transmit this instance of `Player` to other users
        """
        return {
            "Type":"Player",
            "Location":(self.location[0], self.location[1]),
            "PlayerID":self.ID
        }
