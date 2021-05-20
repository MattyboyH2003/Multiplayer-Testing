import urllib3
import json

http = urllib3.PoolManager()

password = str(input("What would you like the password to be for your server? "))
serverInfo = http.request("GET", f"http://192.168.1.142:6900/createserver/{password}")
serverInfo = json.loads(serverInfo.data.decode('utf-8'))
if serverInfo:
    localPass = serverInfo["yourPass"]
    serverNo = serverInfo["serverID"]

    print("You've been given server number "+str(serverNo))
    print("Your local password is "+localPass)

    while True:
        input("Recieve data")

        result = http.request("GET", f"http://192.168.1.142:6900/GetHostInfo/{serverNo}/{password}/{localPass}")
        if result:
            print(result.data.decode('utf-8'))
        else:
            print("No new data\n")
