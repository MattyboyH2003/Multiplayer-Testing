import flask
import string
import random
import time
from flask import request, jsonify

########################################################################################################
#                                              - Setup -                                               #
########################################################################################################

#Initialise Flask
app = flask.Flask(__name__)

#Create all global variabels
global serverList #List to contain "server" instances
serverList = [None, None, None, None, None]

########################################################################################################
#                                              - Classes -                                             #
########################################################################################################

class GameServer:
    def __init__(self, password, hostPass):
        """
        `password` is the server password chosen by the host\n
        `hostPass` is the password generated using `CreatePass` for the host
        """
        self.password = password
        self.playerPasswords = [hostPass]
        self.infoList = []
        self.currentState = {}
    
    def AddPlayer(self):
        """
        Ran when a new player needs to be added to the server\n
        returns the json data to be sent back to the client
        """
        password = CreatePass() #Creates a new local password for the new player
        added = False
        counter = 0
        for item in self.playerPasswords: #Checks if there is a free space in the list from a user who has previously left
            if item == None:
                added = True
                self.playerPasswords[counter] = password
                id = counter
                break
            counter += 1
            
        if not added: #Incase there wasn't a free place in the list
            self.playerPasswords.append(password)
            id = len(self.playerPasswords)-1

        self.infoList.append({"Type":"Connect", "ID":id})
        return {"success":True, "yourID":id, "yourPass":password}
    
    def DisconnectPlayer(self, id):
        """
        Ran when a client requests to be disconected from the server
        `id` is the ID of the client that is disconnecting
        """
        self.playerPasswords[int(id)] = None #Removes them from the users connected

    def Shutdown(self):
        """
        Ran when the host wants to shutdown the server
        """
        self.currentState = [{"Type":"Shutdown"}]

    def AddInfo(self, info):
        """
        Adds `info` to the list of info to be sent to the host next time its requested
        """
        self.infoList.append(info)

    def RelayInfo(self):
        """
        Sends the info back to the host and clears the list of info that needs to be sent next time
        """
        toReturn = jsonify(self.infoList)
        self.infoList = []
        return toReturn
        
    def GetPass(self):
        """
        returns the password to this server
        """
        return self.password
    def GetPlayerPass(self, id):
        """
        returns the password of the player specified by `id`
        """
        return self.playerPasswords[id]
    def GetCurrentState(self):
        """
        returns the current state of the game to be sent to the client
        """
        return self.currentState
    
    def SetCurrentState(self, state):
        """
        sets the current state of the game to the `state` sent by the host
        """
        self.currentState = state

########################################################################################################
#                                            - Functions -                                             #
########################################################################################################

def CreatePass():
    """
    Creates a random local password for a client or host\n
    This password is a 12 character long string of randomly generated capital letters or numbers
    """
    return "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(12))

@app.route("/createserver/<password>")
def CreateServer(password):
    """
    Ran when `/createserver/<password>` requested\n
    `password` is given by the host\n
    Creates a server if there's a free space, returns either True or False under the `success` key and all other info needed based on whether its successful or not
    """
    counter = 0
    for i in serverList:
        if i == None:
            hostPass = CreatePass()
            serverList[counter] = GameServer(password, hostPass)
            return jsonify({"success":True, "serverID":counter, "yourPass":hostPass})
        counter += 1
    return jsonify({"success":False, "Error":"No Server Available"})

@app.route("/JoinServer/<id>/<password>")
def JoinServer(id, password):
    """
    Ran when `/JoinServer/<id>/<password>` requested\n
    `id` and `password` are both given by the host\n
    Used for a client to connect to a server under the specified `id`\n
    Returns either True or False under the `success` key and all other info needed based on whether its successful or not
    """
    try:
        if serverList[int(id)].GetPass() == password:
            return jsonify(serverList[int(id)].AddPlayer())
        else:
            return jsonify({"success":False, "Error":"Server Password Incorrect"})
    except IndexError:
        return jsonify({"success":False, "Error":"Server ID not accepted"})
    except TypeError:
        return jsonify({"success":False, "Error":"Server ID not accepted"})

@app.route("/SendClientInfo/<server>/<serverPass>/<playerID>/<playerPass>", methods=["POST"])
def SendClientInfo(server, serverPass, playerID, playerPass):
    """
    Ran when `/SendClientInfo/<server>/<serverPass>/<playerID>/<playerPass>` requested\n
    Used by a client to send info to the server which will then be sent on to the host
    """
    if serverList[int(server)].GetPass() == serverPass:
        if serverList[int(server)].GetPlayerPass(int(playerID)) == playerPass:
            serverList[int(server)].AddInfo(request.get_json())
            return "Info recieved successfully :)"
    return "fail"

@app.route("/SendHostInfo/<server>/<serverPass>/<playerPass>", methods=["POST"])
def HostGiveInfo(server, serverPass, playerPass):
    """
    Ran when `/SendHostInfo/<server>/<serverPass>/<playerPass>` requested\n
    Used by the host to send info to the server which will then be sent on to the connected clients
    """
    if serverList[int(server)].GetPass() == serverPass:
        if serverList[int(server)].GetPlayerPass(int(0)) == playerPass:
            serverList[int(server)].SetCurrentState(request.get_json())
            return "Info recieved successfully :)"
    return "fail"

@app.route("/GetHostInfo/<server>/<serverPass>/<playerPass>")
def GetHostInfo(server, serverPass, playerPass):
    """
    Ran when `/GetHostInfo/<server>/<serverPass>/<playerPass>` requested\n
    Used by the host to get all the info sent by the clients
    """
    if serverList[int(server)].GetPass() == serverPass:
        if serverList[int(server)].GetPlayerPass(0) == playerPass:
            return serverList[int(server)].RelayInfo()

@app.route("/GetClientInfo/<server>/<serverPass>/<playerID>/<playerPass>")
def GetClientInfo(server, serverPass, playerID, playerPass):
    """
    Ran when `/GetClientInfo/<server>/<serverPass>/<playerID>/<playerPass>` requested\n
    Used by the client to get the current state of the game
    """
    if serverList[int(server)].GetPass() == serverPass:
        if serverList[int(server)].GetPlayerPass(int(playerID)) == playerPass:
            return jsonify(serverList[int(server)].GetCurrentState())

@app.route("/ClientDisconnect/<server>/<serverPass>/<playerID>/<playerPass>", methods=["POST"])
def ClientDisconnect(server, serverPass, playerID, playerPass):
    """
    Ran when `/ClientDisconnect/<server>/<serverPass>/<playerID>/<playerPass>` requested\n
    Used by the client to disconnect from the server they're connected to\n
    When recieved the server runs the `GameServer.DisconnectPlayer` function to remove info on the client that wants to disconnect
    """
    if serverList[int(server)].GetPass() == serverPass:
        if serverList[int(server)].GetPlayerPass(playerID) == playerPass:
            serverList[int(server)].DisconnectPlayer(playerID)

@app.route("/HostDisconnect/<server>/<serverPass>/<playerPass>", methods=["POST"])
def HostDisconnect(server, serverPass, playerPass):
    """
    Ran when `/HostDisconnect/<server>/<serverPass>/<playerPass>` requested\n
    Used by the host to disconnect and shut their server down\n
    When recieved the server runs the `GameServer.Shutdown` function to shutdown the server
    """
    if serverList[int(server)].GetPass() == serverPass:
        if serverList[int(server)].GetPlayerPass(0) == playerPass:
            serverList[int(server)].Shutdown()
            time.sleep(10)
            serverList[int(server)] = None
            print(serverList)


########################################################################################################
#                                          - Call Functions -                                          #
########################################################################################################

if __name__ == "__main__":
    app.run(debug=False, port="6900", host="0.0.0.0")
