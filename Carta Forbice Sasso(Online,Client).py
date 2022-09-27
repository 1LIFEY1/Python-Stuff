import socket
from threading import *
from time import sleep
import json
Client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
Client.connect(("192.168.1.101",80))
Client.send(input("Enter Ur NickName:").encode('utf-8'))
Client.send(input("Enter The Game Id:").encode('utf-8'))
print(Client.recv(1024).decode('utf-8'))
print(Client.recv(1024).decode('utf-8'))
while True:
   Client.send(input("Enter 'scissors' or 'rock' or 'paper':").encode('utf-8'))
   print(Client.recv(1024).decode('utf-8'))
   print(Client.recv(1024).decode('utf-8'))
   print(Client.recv(1024).decode('utf-8'))
   packet = json.loads(Client.recv(1024).decode('utf-8'))
   if packet["1"] == 3 or packet["2"] == 3:
      Client.close()
      break
