import urllib3
import json

http = urllib3.PoolManager()

root = "http://192.168.1.142:6900"

serverID = input("What is the ID of the server you'd like to join? ")
serverPass = input("What is the servers password? ")
result = http.request("GET", f"{root}/JoinServer/{serverID}/{serverPass}")
#print(result.data.decode("utf-8"))
result = json.loads(result.data.decode('utf-8'))
if result:
    localPass = result["yourPass"]
    localID = result["yourID"]

    print("Your local ID is "+str(localID))
    print("Your local password is "+str(localPass))

    while True:
        info = input("What info would you like to send?\n")

        print(http.request("GET", f"{root}/SendInfo/{serverID}/{serverPass}/{localID}/{localPass}/{info}").data.decode("utf-8"))
