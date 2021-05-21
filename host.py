import urllib3
import json
import pygame
from threading import Thread

from Player import Player

http = urllib3.PoolManager()

#with open("ip.txt") as f:
root = "62.171.143.217:6900" # = f.read()

if __name__ == "__main__":
    #Pygame Things
    pygame.init()
    resolution = (1280, 720)
    pygame.display.set_caption("Multiplayer Host")
    window = pygame.display.set_mode(resolution)
    clock = pygame.time.Clock()

    #Server Things
    password = str(input("What would you like the password to be for your server? "))
    serverInfo = http.request("GET", f"{root}/createserver/{password}")
    serverInfo = json.loads(serverInfo.data.decode('utf-8'))
else:
    exit()

allSpritesList = pygame.sprite.Group()
player = Player(pygame.math.Vector2(200, 200), 0, window)
allSpritesList.add(player)

def SendData(jsonData):
    http.request("POST", f"{root}/SendHostInfo/{serverNo}/{password}/{localPass}", body=json.dumps(jsonData).encode("utf-8"), headers={"Content-Type": "application/json"}).data.decode("utf-8")

def RequestData():
    global newData
    while True:
        result = http.request("GET", f"{root}/GetHostInfo/{serverNo}/{password}/{localPass}")
        newData = json.loads(result.data.decode('utf-8'))



if serverInfo:
    localPass = serverInfo["yourPass"]
    serverNo = serverInfo["serverID"]

    print(f"You've been given server number {str(serverNo)}")
    print(f"Your local password is {localPass}")

newData = []
def Main():
    global newData
    frameCount = 0
    while True:
        if frameCount % 1 == 0:
            for item in newData:
                if item["Type"] == "Connect":
                    allSpritesList.add(Player((200, 400), item["ID"], window))
                if item["Type"] == "Disconnect":
                    print(f"Host Recieved Disconnect Request for player {item['PlayerID']}")
                    for sprite in allSpritesList:
                        if isinstance(sprite, Player):
                            if sprite.GetID() == item["PlayerID"]:
                                sprite.kill()
                if item["Type"] == "Player":
                    created = False
                    for sprite in allSpritesList:
                        if isinstance(sprite, Player):
                            if sprite.GetID() == item["PlayerID"]:
                                created = True
                                sprite.Setpos(*item["Location"])                
                    if not created:
                        allSpritesList.add(Player(item["Location"], item["PlayerID"], window))
                        

        window.fill((60, 80, 38))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
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
        for item in allSpritesList:
            if isinstance(item, Player):
                toSend.append(item.GetAllInfo())
        
        t3 = Thread(target=SendData, args=[toSend])
        t3.start()

        frameCount += 1
        allSpritesList.draw(window)
        pygame.display.update()
        clock.tick(30)


t2 = Thread(target = RequestData)

t2.start()
Main()
