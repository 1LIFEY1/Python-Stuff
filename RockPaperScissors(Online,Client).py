import socket
from threading import *
from time import sleep
import json

# Connnection To The Host
Client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
Client.connect(("192.168.1.101",8888))

# Send To The Server Info For Creating A Client
Nick = input("Enter Ur NickName:")
Pass = input("Enter The Game Id:")

Client.send(Nick.encode('utf-8'))
Client.send(Pass.encode('utf-8'))
# Waiting For A Response
packet,packet1 = Client.recv(1023).decode('utf-8'),Client.recv(1023).decode('utf-8')
print(packet,"\n",packet1)

# Game
while True:
   Client.send(input("Enter 'scissors' or 'rock' or 'paper':").encode('utf-8'))
   move,winner,points = Client.recv(1023).decode('utf-8'),Client.recv(1023).decode('utf-8'),Client.recv(1023).decode('utf-8')
   print(move,"\n",winner,"\n",points)
   packet = json.loads(Client.recv(1024).decode('utf-8'))
   if packet["1"] == 3 or packet["2"] == 3:
      Client.close()
      break

# Notes: A Nice Fact Is That Almost Everything is On The Server side
