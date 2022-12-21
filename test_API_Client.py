import json
import requests
from  weatherDataHandle import AVAILABLE_REQUESTS

config = json.load(open("config.json"))
hostIp = config["api"]["ip"]
hostPort = config["api"]["port"]


hostURL=f"http://{hostIp}:{hostPort}/"
if __name__ == "__main__":

    for req in AVAILABLE_REQUESTS:
        url=hostURL+req
        response = requests.get(url)
        response=response.json()
        response=json.loads(response)
        print(f"response :{response}")