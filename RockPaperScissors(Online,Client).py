import socket
from threading import *
from time import sleep
import json

# Connnection To The Host
Client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
Client.connect(("192.168.1.101",80))

# Send To The Server Info For Creating A Client
Nick = input("Enter Ur NickName:")
Pass = input("Enter The Game Id:")

Client.send(Nick.encode('utf-8'))
Client.send(Pass.encode('utf-8'))
# Waiting For A Response
packets = (Client.recv(1023).decode('utf-8'),Client.recv(1023).decode('utf-8'))
print(packets[1],"\n",packets[2])

# Game
while True:
   Client.send(input("Enter 'scissors' or 'rock' or 'paper':").encode('utf-8'))
   packets2 = (Client.recv(1023).decode('utf-8'),Client.recv(1023).decode('utf-8'),Client.recv(1023).decode('utf-8'))
   print(packets2[1],"\n",packets2[2],"\n",packets2[3])
   packet = json.loads(Client.recv(1024).decode('utf-8'))
   if packet["1"] == 3 or packet["2"] == 3:
      Client.close()
      break

# Notes: A Nice Fact Is That Almost Everything is On The Server side
