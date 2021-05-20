import urllib3
import json
import pygame

from Player import Player

http = urllib3.PoolManager()

with open("ip.txt") as f:
    root = f.read()

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
player = Player(pygame.math.Vector2(200, 200), window)
allSpritesList.add(player)

def SendData(jsonData):
    http.request("POST", f"{root}/SendHostInfo/{serverNo}/{password}/{localPass}", body=json.dumps(jsonData).encode("utf-8"), headers={"Content-Type": "application/json"}).data.decode("utf-8")

def RequestData():
    result = http.request("GET", f"{root}/GetHostInfo/{serverNo}/{password}/{localPass}")
    return json.loads(result.data.decode('utf-8'))
    
# ----------------------------[ New / Old ]---------------------------- #

if serverInfo:
    localPass = serverInfo["yourPass"]
    serverNo = serverInfo["serverID"]

    print(f"You've been given server number {str(serverNo)}")
    print(f"Your local password is {localPass}")

    frameCount = 0
    while True:
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
        SendData([{"Type":"Player", "PlayerId":0, "Location":player.GetPos()}])

        frameCount += 1
        allSpritesList.draw(window)
        pygame.display.update()
        clock.tick(30)
