import urllib3
import json

http = urllib3.PoolManager()

root = "http://0.0.0.0:6900"

serverID = input("What is the ID of the server you'd like to join? ")
serverPass = input("What is the servers password? ")
result = http.request("GET", f"{root}/JoinServer/{serverID}/{serverPass}")
print(result.data.decode("utf-8"))
result = json.loads(result.data.decode('utf-8'))
if result:
    localPass = result["yourPass"]
    localID = result["yourID"]

    print("Your local ID is "+str(localID))
    print("Your local password is "+str(localPass))

    while True:
        msg = input("Message: ")
        print(http.request("POST", f"{root}/SendInfo/{serverID}/{serverPass}/{localID}/{localPass}", body=json.dumps({"Player": localID, "Message": msg}).encode("utf-8"), headers={"Content-Type": "application/json"}).data.decode("utf-8"))
