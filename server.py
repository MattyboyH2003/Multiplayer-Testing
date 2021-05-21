import flask
import string
import random
from flask import request, jsonify

app = flask.Flask(__name__)

global dataList
dataList = {}

global serverList
serverList = [None, None, None, None, None]

class GameServer:
    def __init__(self, password, hostPass):
        self.password = password
        self.playerPasswords = [hostPass]
        self.infoList = []
        self.currentState = {}
    
    def AddPlayer(self):
        password = CreatePass()
        added = False
        counter = 0
        for item in self.playerPasswords:
            if item == None:
                added = True
                self.playerPasswords[counter] = password
                id = counter
                break
            counter += 1
            
        if not added:
            self.playerPasswords.append(password)
            id = len(self.playerPasswords)-1

        self.playerPasswords.append(password)
        self.infoList.append({"Type":"Connect", "ID":id})
        return {"yourID":id, "yourPass":password}
    
    def DisconnectPlayer(self, id):
        self.playerPasswords[int(id)] = None

    def AddInfo(self, info):
        self.infoList.append(info)

    def RelayInfo(self):
        toReturn = jsonify(self.infoList)
        self.infoList = []
        return toReturn
        
    def GetPass(self):
        return self.password
    def GetNumOfPlayers(self):
        return self.numOfPlayers
    def GetPlayerPass(self, id):
        return self.playerPasswords[id]
    def GetCurrentState(self):
        return self.currentState
    
    def SetCurrentState(self, state):
        self.currentState = state

def CreatePass():
    return "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(12))

@app.route("/createserver/<password>")
def CreateServer(password):
    counter = 0
    for i in serverList:
        if i == None:
            hostPass = CreatePass()
            serverList[counter] = GameServer(password, hostPass)
            return jsonify({"serverID":counter, "yourPass":hostPass})
        counter += 1
    return jsonify(False)

@app.route("/JoinServer/<id>/<password>")
def JoinServer(id, password):
    if serverList[int(id)].GetPass() == password:
        return jsonify(serverList[int(id)].AddPlayer())
    return jsonify(False)

@app.route("/SendClientInfo/<server>/<serverPass>/<playerID>/<playerPass>", methods=["GET", "POST"])
def GiveClientInfo(server, serverPass, playerID, playerPass):
    print(request.get_json())
    if serverList[int(server)].GetPass() == serverPass:
        if serverList[int(server)].GetPlayerPass(int(playerID)) == playerPass:
            serverList[int(server)].AddInfo(request.get_json())
            return "Info recieved successfully :)"
    return "fail"

@app.route("/SendHostInfo/<server>/<serverPass>/<playerPass>", methods=["GET", "POST"])
def HostGiveInfo(server, serverPass, playerPass):
    if serverList[int(server)].GetPass() == serverPass:
        if serverList[int(server)].GetPlayerPass(int(0)) == playerPass:
            serverList[int(server)].SetCurrentState(request.get_json())
            return "Info recieved successfully :)"
    return "fail"

@app.route("/GetHostInfo/<server>/<serverPass>/<playerPass>")
def GetHostInfo(server, serverPass, playerPass):
    if serverList[int(server)].GetPass() == serverPass:
        if serverList[int(server)].GetPlayerPass(0) == playerPass:
            return serverList[int(server)].RelayInfo()

@app.route("/GetClientInfo/<server>/<serverPass>/<playerID>/<playerPass>")
def GetClientInfo(server, serverPass, playerID, playerPass):
    if serverList[int(server)].GetPass() == serverPass:
        if serverList[int(server)].GetPlayerPass(int(playerID)) == playerPass:
            return jsonify(serverList[int(server)].GetCurrentState())

@app.route("/ClientDisconnect/<server>/<serverPass>/<playerID>/<playerPass>")
def ClientDisconnect(server, serverPass, playerID, playerPass):
    if serverList[int(server)].GetPass() == serverPass:
        if serverList[int(server)].GetPlayerPass(playerID) == playerPass:
            serverList[int(server)].DisconnectPlayer(playerID)

if __name__ == "__main__":
    app.run(debug=True, port="6900", host="0.0.0.0")
