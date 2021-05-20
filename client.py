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
player = Player(pygame.math.Vector2(200, 200), window)
allSpritesList.add(player)

def RequestData():
    result = http.request("GET", f"{root}/GetClientInfo/{serverNo}/{password}/{localID}/{localPass}")
    return json.loads(result.data.decode('utf-8'))
    
if result:
    localPass = result["yourPass"]
    localID = result["yourID"]

    print("Your local ID is "+str(localID))
    print("Your local password is "+str(localPass))
    frameCount = 0
    while True:
        window.fill((60, 80, 38))

        newData = RequestData()
        player.Setpos(*newData[0]["Location"])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        #Final stuff

        frameCount += 1

        allSpritesList.draw(window)
        pygame.display.update()
        clock.tick(30)


"""
        msg = input("Message: ")
        print(http.request("POST", f"{root}/SendInfo/{serverID}/{serverPass}/{localID}/{localPass}", body=json.dumps({"Player": localID, "Message": msg}).encode("utf-8"), headers={"Content-Type": "application/json"}).data.decode("utf-8"))
"""
