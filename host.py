import urllib3
import json

http = urllib3.PoolManager()

root = "http://192.168.1.142:6900"

password = str(input("What would you like the password to be for your server? "))
serverInfo = http.request("GET", f"{root}/createserver/{password}")
serverInfo = json.loads(serverInfo.data.decode('utf-8'))
if serverInfo:
    localPass = serverInfo["yourPass"]
    serverNo = serverInfo["serverID"]

    print("You've been given server number "+str(serverNo))
    print("Your local password is "+localPass)

    while True:
        input("Recieve data")

        result = http.request("GET", f"{root}/GetHostInfo/{serverNo}/{password}/{localPass}")
        result = json.loads(result.data.decode('utf-8'))
        if result:
            print(result)
        else:
            print("No new data\n")
