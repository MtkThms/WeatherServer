import socket  # tcp connection
import weatherDataHandle  # read weather data
import json  # handle configuration file


class UdpServer:

    def __init__(self):
        config = json.load(open("config.json"))  # load config file
        # put config in variables
        self.IP: str = config["udp"]["ip"]
        self.PORT: int = config["udp"]["port"]
        self.BUFFER_SIZE: int = config["udp"]["bufferSize"]
        self.UdpServer: socket.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)  # create socket
        self.UdpServer.bind((self.IP, self.PORT))  # set it to specific ip and port
        print("server started")

    def loop(self):
        while (True):  # start receive loop
            requestFromClient, ClientAddress = self.UdpServer.recvfrom(
                self.BUFFER_SIZE)  # wait (forever) to receive any requests
            # print(f"request from client:{requestFromClient}")
            requestFromClient = requestFromClient.decode('utf-8')  # decode request
            response = weatherDataHandle.getData(requestFromClient)  # get weather data from file
            self.UdpServer.sendto(response.encode('utf-8'), ClientAddress)  # send weather data to Client


if __name__ == "__main__":
    Server = UdpServer()
    while True:
        Server.loop()
