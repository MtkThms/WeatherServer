import math
import json

config = json.load(open("config.json"))
REQUEST_TABLE = config["requestTable"]
AVAILABLE_REQUESTS: [str] = list(REQUEST_TABLE)


def _calcAbsolutHumidity(relativeHumidity: float, temperature: float):
    _rH = relativeHumidity
    _V = temperature
    # some const
    _alpha = 6.112
    _beta = 17.62
    _lambda = 243.12
    # denominator
    _A = 216.7 * _rH / 100.0 * _alpha * math.exp(_beta * _V / (_lambda + _V))
    # nominator
    _B = _V + 273.15
    return round(_A / _B, config["calc"]["roundDigits"])


def readData():
    try:
        folderPath = config["files"]["folderPath"]
        lastMeasureFile = config["files"]["lastMeasureFileName"]
        path = f'{folderPath}/{lastMeasureFile}'

        with open(path, 'r') as file_lastMeasure:
            # file has only two lines
            headList, dataList = file_lastMeasure.readlines()
            headList = headList.split(";")
            dataList = dataList.split(";")
            # create empty file and fill it with data
            measureDict: dict = {}
            for i in range(len(list(headList))):
                measureDict[headList[i]] = dataList[i]
            return measureDict
    except FileExistsError as err:
        print(f"File error: {err}")
        return None
    except FileNotFoundError as err:
        print(f"File error: {err}")
        return None

def _calcWaterVaporPressure(relativeHumidity, temperature) -> float:
    absolutHumidity = _calcAbsolutHumidity(relativeHumidity, temperature)
    _gasConstant = 461.5
    return round(temperature * absolutHumidity * _gasConstant, config["calc"]["roundDigits"])


def getData(request: str):
    if request == "help?":
        reqeustString: str = ""
        for i in AVAILABLE_REQUESTS:
            reqeustString += f"{i} "
        return reqeustString

    elif request not in AVAILABLE_REQUESTS:
        return f"Error: Request '{request}' not available. Send 'help?' for a list of available requests"

    measureFile = readData()
    if measureFile == None:
        return "file error, contact system admin"

    if request == "aH?":
        relativeHumidity = float(measureFile[REQUEST_TABLE["rH?"]["dataName"]])
        temperature = float(measureFile[REQUEST_TABLE["Temp?"]["dataName"]])
        measureData = _calcAbsolutHumidity(relativeHumidity, temperature)

    elif request == "WVP?":
        relativeHumidity = float(measureFile[REQUEST_TABLE["rH?"]["dataName"]])
        temperature = float(measureFile[REQUEST_TABLE["Temp?"]["dataName"]])
        # absolutHumidity = _calcAbsolutHumidity(relativeHumidity, temperature)
        # gasConstant = 461.5  # constant for water vape
        # measureData = round(temperature * absolutHumidity * gasConstant, 3)
        measureData = _calcWaterVaporPressure(relativeHumidity, temperature)
    else:

        measureData = measureFile[REQUEST_TABLE[request]["dataName"]]

    _timeStamp = measureFile["Timestamp"]
    _outputName = REQUEST_TABLE[request]['name']
    _unit = REQUEST_TABLE[request]['unit']

    return f"{_timeStamp}; {_outputName}={measureData}{_unit}"


if __name__ == "__main__":

    for i in list(REQUEST_TABLE):
        print(getData(i))

    print(getData("not a request"))
