import urllib3
import json
import pygame
from threading import Thread

from Player import Player

########################################################################################################
#                                              - Setup -                                               #
########################################################################################################

with open("ip.txt") as f: #Open root ip file
    root = f.read()

#Pygame Things
pygame.init()
resolution = (1280, 720)
pygame.display.set_caption("Multiplayer Host")
window = pygame.display.set_mode(resolution)
clock = pygame.time.Clock()

#Server Things
http = urllib3.PoolManager()
password = str(input("What would you like the password to be for your server? "))
serverInfo = http.request("GET", f"{root}/createserver/{password}")
serverInfo = json.loads(serverInfo.data.decode('utf-8'))

#If successfully connected to server
if serverInfo["success"]:
    localPass = serverInfo["yourPass"]
    serverNo = serverInfo["serverID"]

    print(f"You've been given server number {str(serverNo)}")
    print(f"Your local password is {localPass}")

    allSpritesList = pygame.sprite.Group()
    newData = []

    player = Player(pygame.math.Vector2(200, 200), 0, window)
    allSpritesList.add(player)
#Prints error of cant create a server
else:
    print("Server creation unsuccessful, Reason:")
    print(serverInfo["error"])
    exit()


########################################################################################################
#                                            - Functions -                                             #
########################################################################################################

def SendData(jsonData):
    """
    Sends given `jsonData` to the server to be recieved by the client\n
    Sends too `{root}/SendHostInfo/`
    """
    http.request("POST", f"{root}/SendHostInfo/{serverNo}/{password}/{localPass}", body=json.dumps(jsonData).encode("utf-8"), headers={"Content-Type": "application/json"}).data.decode("utf-8")

def RequestData():
    """
    Function ran forever requesting new data from the server for the host to use\n
    Requests data from `{root}/GetHostInfo/`
    """
    global newData
    while True:
        result = http.request("GET", f"{root}/GetHostInfo/{serverNo}/{password}/{localPass}")
        newData = json.loads(result.data.decode('utf-8'))

def Main():
    """
    Main game loop to run the pygame window
    """
    global newData #Variable containing all changes that need to be ran for this frame from clients
    
    while True:
        window.fill((60, 80, 38)) #Clears the screen

        for item in newData: #Checks all new peices of data it needs to process
            if item["Type"] == "Connect": #Checks if a new user has connected
                allSpritesList.add(Player((200, 400), item["ID"], window))
            if item["Type"] == "Disconnect": #Checks if a user has disconnected
                print(f"Host Recieved Disconnect Request for player {item['PlayerID']}")
                for sprite in allSpritesList:
                    if isinstance(sprite, Player):
                        if sprite.GetID() == item["PlayerID"]:
                            sprite.kill()
            if item["Type"] == "Player": #Checks if its an update on a player instance
                created = False
                for sprite in allSpritesList:
                    if isinstance(sprite, Player):
                        if sprite.GetID() == item["PlayerID"]:
                            created = True
                            sprite.Setpos(*item["Location"])                
                if not created: #Incase a previous packet has been lost
                    allSpritesList.add(Player(item["Location"], item["PlayerID"], window))
                        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #Check if user is trying to exit the game
                quit()

        #Checks if the specified keys are pressed
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player.MoveUp()
        if keys[pygame.K_a]:
            player.MoveLeft()
        if keys[pygame.K_s]:
            player.MoveDown()
        if keys[pygame.K_d]:
            player.MoveRight()

        #Final stuff
        toSend = []
        for item in allSpritesList: #Runs through all sprites that exist on host end
            if isinstance(item, Player): #If they are an instance of Player adds that instances information to the list of info to be sent
                toSend.append(item.GetAllInfo())
        
        #Starts a concurrent SendData to send the info to the server while the game still runs
        t3 = Thread(target=SendData, args=[toSend])
        t3.start()

        allSpritesList.draw(window)
        pygame.display.update()
        clock.tick(30)

########################################################################################################
#                                          - Call Functions -                                          #
########################################################################################################

#Starts running constant data updates
t2 = Thread(target = RequestData)
t2.start()

Main()
