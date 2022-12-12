from fastapi import FastAPI
import uvicorn
import json
from threading import Thread

import weatherDataHandle
import UDP_Server

app = FastAPI()


@app.get("/")
async def root():
    return "Hello From Weather-API WeatherServer!!"


@app.get("/{request}")
async def getData(request: str):
    # just a hack-around, custom function in 'weatherDataHandle' for API-request not defined yet
    req = weatherDataHandle.getData(request + "?")  # request eats the question mark, must be added manualy
    msg = json.dumps({"response": req})
    data = json.dumps(msg).encode('utf8')
    return data


if __name__ == "__main__":
    # UDP-WeatherServer
    Udp = UDP_Server.UdpServer()
    UdpThread = Thread(target=Udp.loop)
    UdpThread.start()
    # API-WeatherServer
    config = json.load(open("config.json"))
    host = config["api"]["ip"]
    port = config["api"]["port"]
    debug = bool(config["api"]["debug"])
    if debug:
        logLevel = "debug"
    else:
        logLevel = "info"
    uvicorn.run("main:app", host=host, port=port, reload=debug, log_level=logLevel)
