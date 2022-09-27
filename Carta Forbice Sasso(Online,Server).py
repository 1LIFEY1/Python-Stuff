import socket
import threading
from time import sleep
import json

# Objects:(
#   1:Checking Names
# 
# )


Server = socket.socket(socket.AF_INET,socket.SOCK_STREAM) # Creating The Obj
Server.bind(("192.168.1.101",8888)) # Binding To The Main Host
Server.listen() # Listen For Connection

Clients = [] # Containing Every Player Till He Gets On A Game
Sessions = [] # Objects Which Will Contain The Players Of A Game


class User():
    def __init__(self,Nick,Connection,Id):
        self.Nick = Nick # His Nickname
        self.Connection = Connection # Socket Which Containts The Connection Within A User/Player
        self.Id = Id # The Pass For Enter Into The Game With SomeoneElse Which Put It Exactly Like Him


class Session():
    def __init__(self,User1,User2,IsOn):
        self.User1 = User1 # Player 1
        self.User2 = User2 # Player 2
        self.IsOn = IsOn # Used To Check If The Session Is Already In Use

    
def GetClient():
        conn,addr = Server.accept() # Accepting The Connection With A User
        nickname = conn.recv(1024).decode('utf-8') # His Nickname
        Id = conn.recv(1024).decode('utf-8')  # The Password To Enter Into A Game
        Client = User(nickname,conn,Id) # Assembling The User
        Clients.append(Client) # Saving Him Up Cause Of The Scope Of The Function

                

def Game():
    # SELF EXPLAINING
    for game in Sessions:
        if not game.IsOn:
                game.IsOn = True
                Points = {"1":0,"2":0}
                game.User1.Connection.send(f"{game.User2.Nick} Has Logged In".encode('utf-8'))
                game.User2.Connection.send(f"{game.User1.Nick} Has Logged In".encode('utf-8'))    

                while not Points["1"] == 3 or not Points["2"] == 3 :
                    m1 = game.User1.Connection.recv(1024).decode('utf-8')
                    m2 = game.User2.Connection.recv(1024).decode('utf-8')
                    if m1 == m2:
                        Json = json.dumps(Points)
                        game.User1.Connection.send(f"{game.User2.Nick}:{m2}".encode('utf-8'))
                        game.User2.Connection.send(f"{game.User1.Nick}:{m1}".encode('utf-8'))   
                        sleep(.1)          
                        game.User1.Connection.send(f"The Moves Were Equal".encode('utf-8'))
                        game.User2.Connection.send(f"The Moves Were Equal".encode('utf-8'))
                        sleep(.1)
                        game.User1.Connection.send(str(Points).encode('utf-8'))
                        game.User2.Connection.send(str(Points).encode('utf-8'))
                        sleep(.1)
                        game.User1.Connection.send(Json.encode('utf-8'))
                        game.User2.Connection.send(Json.encode('utf-8'))      
                    elif m1 == 'rock' and m2 == 'scissors' or m1 == 'paper' and m2 == 'rock' or m1 == 'scissors' and m2 == 'paper':
                        Points["1"] = Points["1"] + 1
                        Json = json.dumps(Points)
                        game.User1.Connection.send(f"{game.User2.Nick}:{m2}".encode('utf-8'))
                        game.User2.Connection.send(f"{game.User1.Nick}:{m1}".encode('utf-8'))    
                        sleep(.1)                    
                        game.User1.Connection.send(f"{game.User1.Nick} Has Won".encode('utf-8'))
                        game.User2.Connection.send(f"{game.User1.Nick} Has Won".encode('utf-8'))
                        sleep(.1)
                        game.User1.Connection.send(str(Points).encode('utf-8'))
                        game.User2.Connection.send(str(Points).encode('utf-8'))
                        sleep(.1)
                        game.User1.Connection.send(Json.encode('utf-8'))
                        game.User2.Connection.send(Json.encode('utf-8'))          
                    elif m2 == 'rock' and m1 == 'scissors' or m2 == 'paper' and m1 == 'rock' or m2 == 'scissors' and m1 == 'paper':      
                        Points["2"] = Points["2"] + 1
                        Json = json.dumps(Points)
                        game.User1.Connection.send(f"{game.User2.Nick}:{m2}".encode('utf-8'))
                        game.User2.Connection.send(f"{game.User1.Nick}:{m1}".encode('utf-8'))  
                        sleep(.1)  
                        game.User1.Connection.send(f"{game.User2.Nick} Has Won".encode('utf-8'))
                        game.User2.Connection.send(f"{game.User2.Nick} Has Won".encode('utf-8'))
                        sleep(.1)
                        game.User1.Connection.send(str(Points).encode('utf-8'))
                        game.User2.Connection.send(str(Points).encode('utf-8'))
                        sleep(.1)
                        game.User1.Connection.send(Json.encode('utf-8'))
                        game.User2.Connection.send(Json.encode('utf-8'))                                
                game.User2.Connection.close()
                game.User2.Connection.close()
                del game
while True:
    try:
        threading.Thread(target=GetClient).start()
        for x in range(0,len(Clients) - 1): # Checking Id's With A Semi-Sorting Method
            for i in range(0,len(Clients)):
                if x == len(Clients):
                    i = 0
                if i == x:
                    i = x + 1
                if Clients[x].Id == Clients[i].Id: #If Two Id's Match They'll Get Transported To The game
                    Clients[x].Connection.send("Game Starting".encode('utf-8'))
                    Clients[i].Connection.send("Game Starting".encode('utf-8'))               
                    game = Session(Clients[x],Clients[i],False)
                    Clients.pop(i)
                    Clients.pop(x)
                    Sessions.append(game)
                    threading.Thread(target=Game).start()
                    break
            break
        #Restarting The Check
    except ConnectionAbortedError:
        Left = True
        

# this game is still a draft,One Of my first projects in python :)
# Took Me 5 or 6 days.

