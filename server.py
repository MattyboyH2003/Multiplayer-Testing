import flask
import string
import random
from flask import jsonify

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
    
    def AddPlayer(self):
        password = CreatePass()
        self.playerPasswords.append(password)
        return {"yourID":len(self.playerPasswords)-1, "yourPass":password}

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

def CreatePass():
    return "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(12))

@app.route("/send/<id>/<string>")
def connect(id, string):
    dataList[id] = string

@app.route("/recieve/<id>")
def recieve(id):
    return jsonify({"Data":dataList[id]})

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

@app.route("/SendInfo/<server>/<serverPass>/<playerID>/<playerPass>/<info>")
def GiveInfo(server, serverPass, playerID, playerPass, info):
    if serverList[int(server)].GetPass() == serverPass:
        if serverList[int(server)].GetPlayerPass(int(playerID)) == playerPass:
            serverList[int(server)].AddInfo(info)
            return "Info recieved successfully :)"
    return "fail"

@app.route("/GetHostInfo/<server>/<serverPass>/<playerPass>")
def GetHostInfo(server, serverPass, playerPass):
    if serverList[int(server)].GetPass() == serverPass:
        if serverList[int(server)].GetPlayerPass(0) == playerPass:
            return serverList[int(server)].RelayInfo()

if __name__ == "__main__":
    app.run(debug=True, port="6900", host="0.0.0.0")
