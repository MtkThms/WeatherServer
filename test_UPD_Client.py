import socket
from weatherDataHandle import AVAILABLE_REQUESTS as weatherRequestList
import json  # handle configuration file

config = json.load(open("config.json"))
HOST_IP: str = config["udp"]["ip"]
HOST_PORT: int = config["udp"]["port"]
BUFFER_SIZE: int = config["udp"]["bufferSize"]

UdpClient = socket.socket(family=socket.AF_INET,
                          type=socket.SOCK_DGRAM)
# UPD_Client.settimeout(1000)
weatherRequestList.append("help?")
weatherRequestList.append("errorTest")

for request in weatherRequestList:
    print(f"Request: {request:12}", end=' ')
    UdpClient.sendto(request.encode('utf-8'), (HOST_IP, HOST_PORT))
    msgFromServer = UdpClient.recv(BUFFER_SIZE).decode('utf-8')
    requestResponse = f"Response: {msgFromServer}"
    print(requestResponse)



