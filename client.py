import urllib3
import json
import pygame

from threading import Thread

from urllib3.packages.six import MovedAttribute
from Player import Player
from Image import Image

########################################################################################################
#                                              - Setup -                                               #
########################################################################################################

global active

with open("ip.txt") as f: #Open root ip file
    root = f.read()

#Pygame Things
pygame.init()
resolution = (1280, 720)
pygame.display.set_caption("Multiplayer Client")
window = pygame.display.set_mode(resolution)
clock = pygame.time.Clock()

#Server Things
http = urllib3.PoolManager()
serverNo = input("What is the ID of the server you'd like to join? ")
password = input("What is the servers password? ")
if serverNo and password:
    result = http.request("GET", f"{root}/JoinServer/{serverNo}/{password}")
else:
    print("Bad input")
    quit()
print(result.data.decode("utf-8"))
result = json.loads(result.data.decode('utf-8'))

#If succesfully joined server
if result["success"]:
    localPass = result["yourPass"]
    localID = result["yourID"]

    print("Your local ID is "+str(localID))
    print("Your local password is "+str(localPass))

    allSpritesList = pygame.sprite.Group()

    # Create clients player
    player = Player((200, 400), localID, window)
    allSpritesList.add(player)

#If not successfully joined server
else:
    print("Unable to connect to server, Reason:")
    print(result["Error"])

########################################################################################################
#                                            - Functions -                                             #
########################################################################################################

def SendData(data):
    """
    Sends `data` to the server to be redirected to the host\n
    Sends data to `{root}/SendClientInfo/`
    """
    http.request("POST", f"{root}/SendClientInfo/{serverNo}/{password}/{localID}/{localPass}", body=json.dumps(data).encode("utf-8"), headers={"Content-Type": "application/json"}).data.decode("utf-8")

def SendDisconnect():
    """
    Sends disconnect request to the server\n
    Uses `{root}/ClientDisconnect`
    """
    http.request("POST", f"{root}/ClientDisconnect/{serverNo}/{password}/{localID}/{localPass}")

def RequestData():
    """
    Function ran forever requesting new data from the server for the client to use\n
    Requests data from `{root}/GetClientInfo/`
    """
    global active
    global newData
    while active:
        result = http.request("GET", f"{root}/GetClientInfo/{serverNo}/{password}/{localID}/{localPass}")
        newData = json.loads(result.data.decode('utf-8'))

def RequestStartData():
    """
    Initial request for the client to get basic data to start game
    Requests data from `{root}/GetClientInfo/`
    """
    result = http.request("GET", f"{root}/GetClientInfo/{serverNo}/{password}/{localID}/{localPass}")
    return json.loads(result.data.decode('utf-8'))

def Main():
    """
    Main game loop to run the pygame window
    """
    global active
    global newData #Variable containing all changes that need to be ran for this frame from clients
    
    lastShotTime = 0
    while True:
        window.fill((60, 80, 38)) #Clears the screen

        for sprite in allSpritesList:
            if isinstance(sprite, Image):
                sprite.kill()

        for item in newData: #Checks all peices of data it needs to process
            if item["Type"] == "Player": #Checks if its an update on a player instance
                created = False
                for sprite in allSpritesList:
                    if isinstance(sprite, Player):
                        if sprite.GetID() == item["PlayerID"] and sprite.GetID() != localID:
                            created = True
                            sprite.Setpos(*item["Location"])
                        if sprite.GetID() == localID:
                            created = True
                if not created: #Incase a previous packet has been lost
                    allSpritesList.add(Player(item["Location"], item["PlayerID"], window))
            if item["Type"] == "Bullet":
                allSpritesList.add(Image("Bullet.png", item["Location"]))
            if item["Type"] == "Shutdown":
                active = False
                print("The server you were connected to has been shutdown by the host")
                quit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT: #Check if user is trying to exit the game
                active = False
                SendData({
                    "Type": "Disconnect",
                    "PlayerID": localID
                    })
                SendDisconnect()
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
        if keys[pygame.K_SPACE]:
            if pygame.time.get_ticks() - lastShotTime > 1000:
                lastShotTime = pygame.time.get_ticks()
                movement = player.CalculateBulletMovement(pygame.mouse.get_pos(), player.GetPos())
                bulletThread = Thread(target=SendData, args=[{"Type":"Bullet", "Location":player.GetPos(), "ParentId":localID, "Movement":(movement[0], movement[1])}])
                bulletThread.start()


        #Final stuff
        #Starts a concurrent SendData to send the info to the server while the game still runs
        t3 = Thread(target = SendData, args = [player.GetAllInfo()])
        t3.start()

        allSpritesList.draw(window)
        pygame.display.update()
        clock.tick(30)

########################################################################################################
#                                          - Call Functions -                                          #
########################################################################################################

#Starts running constant data updates
active = True

#Initial Request
newData = RequestStartData()
for item in newData:
    if item["Type"] == "Player":
        allSpritesList.add(Player(item["Location"], item["PlayerID"], window))

t2 = Thread(target = RequestData)
t2.start()

Main()
