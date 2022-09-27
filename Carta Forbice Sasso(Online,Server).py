
from base64 import decode
from msilib.schema import Class
from multiprocessing.connection import Client
import socket
import threading
from time import sleep
import json

Server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
Server.bind(("192.168.1.101",80))
Server.listen()

Clients = []
Sessions = []
class User():
    def __init__(self,Nick,Connection,Id):
        self.Nick = Nick
        self.Connection = Connection
        self.Id = Id


class Session():
    def __init__(self,User1,User2,IsOn):
        self.User1 = User1
        self.User2 = User2
        self.IsOn = IsOn
def GetClient():
        conn,addr = Server.accept()
        nickname = conn.recv(1024).decode('utf-8')
        Id = conn.recv(1024).decode('utf-8')    
        Client = User(nickname,conn,Id)
        Clients.append(Client)     

                
        
def Game():
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
                game.User1.Connection.send(f"The Game Is Closed".encode('utf-8'))
                game.User2.Connection.send(f"The Game Is Closed".encode('utf-8'))
                game.User2.Connection.close()
                game.User2.Connection.close()
                del game
while True:
    try:
        threading.Thread(target=GetClient).start()
        for x in range(0,len(Clients) - 1):
            for i in range(0,len(Clients)):
                if x == len(Clients):
                    i = 0
                if i == x:
                    i = x + 1
                if Clients[x].Id == Clients[i].Id:
                    Clients[x].Connection.send("Game Starting".encode('utf-8'))
                    Clients[i].Connection.send("Game Starting".encode('utf-8'))               
                    game = Session(Clients[x],Clients[i],False)
                    Clients.pop(i)
                    Clients.pop(x)
                    Sessions.append(game)
                    threading.Thread(target=Game).start()
                    break
            break
    except ConnectionAbortedError:
        N = True
        
#  Notes:
#       85% Finished(server)
#           5% Finished(Client)





