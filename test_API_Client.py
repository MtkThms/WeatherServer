import json
import requests
from  weatherDataHandle import AVAILABLE_REQUESTS

hostURL="http://127.0.0.1:5000/"
if __name__ == "__main__":

    for req in AVAILABLE_REQUESTS:
        url=hostURL+req
        response = requests.get(url)
        response=response.json()
        response=json.loads(response)
        print(f"response :{response}")