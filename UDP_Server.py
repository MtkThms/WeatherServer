import socket  # tcp connection
import weatherDataHandle  # read weather data
import json  # handle configuration file
from datetime import datetime # generate timestamps for debugging


class UdpServer:

    def __init__(self):
        self.config = json.load(open("config.json"))  # load config file
        # put config in variables
        self.IP: str = self.config["udp"]["ip"]
        self.PORT: int = self.config["udp"]["port"]
        self.BUFFER_SIZE: int = self.config["udp"]["bufferSize"]
        self.UdpServer: socket.socket = \
            socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)  # create socket
        self.UdpServer.bind((self.IP, self.PORT))  # set it to specific ip and port
        print("Server started")

    def loop(self):
        while (True):  # start receive loop
            # wait (forever) to receive any requests
            requestFromClient, ClientAddress = self.UdpServer.recvfrom(self.BUFFER_SIZE)
            # print message on console if in debug mode
            if self.config["udp"]["debug"] == 1:
                timeStamp = datetime.now().strftime("%d.%m.%Y-%H:%M:%S")
                print(f"{timeStamp} request from {ClientAddress[0]}: {requestFromClient}")
            # decode request
            requestFromClient = requestFromClient.decode('utf-8')
            # get weather data from file
            response = weatherDataHandle.getData(requestFromClient)
            # send weather data to client
            self.UdpServer.sendto(response.encode('utf-8'), ClientAddress)


if __name__ == "__main__":
    Server = UdpServer()
    while True:
        Server.loop()
