from random import randint
import socket
from threading import Thread
from time import sleep

ThisIP = '127.0.0.1'
ThisPORT = 2020

packet_size = 65535

usedNums = [int]
PeddingPackets = [str]

NeedServer = True
MCSoc = socket.socket()

SerSoc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SerSoc.bind((ThisIP, ThisPORT))
print("Port BINDED!")
SerSoc.listen(5)

def HandleClientRECV(s: socket.socket, num: int):
    print("Client Connected! Setting up evrithing (1/2)...")
    th = Thread(target=HandleClientSEND, args=(s, num))
    th.start()

    while True:
        msg = s.recv(packet_size).decode()
        if msg.startswith('main_server'):# and NeedServer:
            NeedServer = False
            MCSoc = s
        else:
            MCSoc.send(str(num, ":").encode())
            

def HandleClientSEND(s: socket.socket, num: int):
    print("Client Connected! Done (2/2) ...")
    while True:
        while len(PeddingPackets) <= 0:
            sleep(120)
        
        rmBle = [str]
        for nj in PeddingPackets:
            if nj.startswith(str(num)):
                s.send(nj[len(str(num)) + 1:].encode())
                rmBle.append(nj)
        
        for hbj in rmBle:
            PeddingPackets.remove(hbj)

def SearchForPackets():
    print("Searching For Packets... (Pedding)")
    while True:
        msg = SerSoc.recv(packet_size).decode
        PeddingPackets.append(msg)

while True:
    soc, ip = SerSoc.accept()
    print("Incoming connection(0/2)! Generating key")
    fnNum = 0
    while True:
        nm = randint(1,999999)
        if not usedNums.__contains__(nm):
            fnNum = nm
            break
    
    thr = Thread(target=HandleClientRECV, args=(soc, fnNum))
    thr.start()
