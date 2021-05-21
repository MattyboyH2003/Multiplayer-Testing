import urllib3
import json
import pygame
import time

from Player import Player

http = urllib3.PoolManager()

with open("ip.txt") as f:
    root = f.read()

if __name__ == "__main__":
    #Pygame Things
    pygame.init()
    resolution = (1280, 720)
    pygame.display.set_caption("Multiplayer Client")
    window = pygame.display.set_mode(resolution)
    clock = pygame.time.Clock()

    #Server Things
    serverNo = input("What is the ID of the server you'd like to join? ")
    password = input("What is the servers password? ")
    result = http.request("GET", f"{root}/JoinServer/{serverNo}/{password}")
    print(result.data.decode("utf-8"))
    result = json.loads(result.data.decode('utf-8'))
else:
    exit()

allSpritesList = pygame.sprite.Group()

def SendData(data):
    http.request("POST", f"{root}/SendClientInfo/{serverNo}/{password}/{localID}/{localPass}", body=json.dumps(data).encode("utf-8"), headers={"Content-Type": "application/json"}).data.decode("utf-8")

def SendDisconnect(id):
    http.request("POST", f"{root}/ClientDisconnect/{serverNo}/{password}/{localID}/{localPass}")

def RequestData():
    result = http.request("GET", f"{root}/GetClientInfo/{serverNo}/{password}/{localID}/{localPass}")
    return json.loads(result.data.decode('utf-8'))
    
if result:
    localPass = result["yourPass"]
    localID = result["yourID"]

    print("Your local ID is "+str(localID))
    print("Your local password is "+str(localPass))
    frameCount = 0

    # Create clients player
    player = Player((200, 400), localID, window)
    allSpritesList.add(player)

    #Initial Request
    newData = RequestData()
    for item in newData:
        if item["Type"] == "Player":
            allSpritesList.add(Player(item["Location"], item["PlayerID"], window))

    while True:
        window.fill((60, 80, 38))

        newData = RequestData()
        for item in newData:
            if item["Type"] == "Player":
                created = False
                for sprite in allSpritesList:
                    if isinstance(sprite, Player):
                        if sprite.GetID() == item["PlayerID"]:
                            created = True
                            sprite.Setpos(*item["Location"])                
                if not created:
                    allSpritesList.add(Player(item["Location"], item["PlayerID"], window))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player.MoveUp()
        if keys[pygame.K_a]:
            player.MoveLeft()
        if keys[pygame.K_s]:
            player.MoveDown()
        if keys[pygame.K_d]:
            player.MoveRight()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #When program closes
                print("Lemme leave pwease")
                SendData({
                    "Type": "Disconnect",
                    "PlayerID": localID
                    })
                SendDisconnect(localID)
                quit()

        #Final stuff
        frameCount += 1

        SendData(player.GetAllInfo())

        allSpritesList.draw(window)
        pygame.display.update()
        clock.tick(30)


"""
        msg = input("Message: ")
        print(http.request("POST", f"{root}/SendInfo/{serverID}/{serverPass}/{localID}/{localPass}", body=json.dumps({"Player": localID, "Message": msg}).encode("utf-8"), headers={"Content-Type": "application/json"}).data.decode("utf-8"))
"""
