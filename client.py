import socket
from threading import Thread
from time import sleep
packet_size = 55000

toServerIP = '127.0.0.1'
toServerPORT = 2020

MCServerIP = '127.0.0.1'
MCServerPORT = 25565

peddingPackets = [str]
ActiveConns = [int]

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((toServerIP, toServerPORT))
print("Connected to SERVER HUB")
s.send("main_server".encode()) # TODO check

def HandleClientRECV(num: int):
    print("Client Thread Started 1/2, starting handler...")
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.connect((MCServerIP, MCServerPORT))

    thr = Thread(target=HandleClientSEND, args=(soc, num))
    thr.start()
    while True:
        while len(peddingPackets) <= 0:
            sleep(300)
        
        rmble = []
        for pck in peddingPackets:
            if pck.startswith(str(num)):
                soc.send(pck[len(str(num))].encode)
                rmble.append(pck)

        for kj in rmble:
            peddingPackets.remove(kj)


def HandleClientSEND(sec: socket.socket, num: int):
    print("Client Thread Started 2/2, HANDLER RUNNING to ", num)
    while True:
        msg = sec.recv(packet_size).decode
        s.send(num, ":", msg)


while True:
    msg = s.recv(packet_size).decode()
    if msg.startswith("new"):
        th = Thread(target=HandleClientRECV, args=(int(msg[3:])))
        th.start()
    else:
        peddingPackets.append(msg)
