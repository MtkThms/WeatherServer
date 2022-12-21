import math
import json

config = json.load(open("config.json"))  # load config file
REQUEST_TABLE = config["requestTable"]  # get available requests
# put available request names in list
AVAILABLE_REQUESTS: [str] = list(REQUEST_TABLE)


def _calcAbsolutHumidity(relativeHumidity: float, temperature: float):
    _rH = relativeHumidity
    _V = temperature
    # get constants from config file
    _alpha = config["calc"]["absolutHumidity"]["alpha"]
    _beta = config["calc"]["absolutHumidity"]["beta"]
    _lambda = config["calc"]["absolutHumidity"]["lambda"]
    # numerator
    _A = 216.7 * _rH / 100.0 * _alpha * math.exp(_beta * _V / (_lambda + _V))
    # denominator
    _B = _V + 273.15
    return round(_A / _B, config["calc"]["roundDigits"])


def _calcWaterVaporPressure(relativeHumidity, temperature) -> float:
    absolutHumidity = _calcAbsolutHumidity(relativeHumidity, temperature)
    _gasConstant = config["calc"]["waterVaporPressure"]["gasConstant"]
    return round(temperature * absolutHumidity * _gasConstant,
                 config["calc"]["roundDigits"])


def readData():
    try:
        folderPath = config["files"]["folderPath"]
        lastMeasureFile = config["files"]["lastMeasureFileName"]
        path = f'{folderPath}/{lastMeasureFile}'

        with open(path, 'r') as file_lastMeasure:
            # read frist two lines
            headList, dataList = file_lastMeasure.readlines()
            # create list of headline and data, separated by <;>
            headList = headList.split(";")
            dataList = dataList.split(";")
            # create empty dictionary
            measureDict: dict = {}
            # fill dictionary with data
            for i in range(len(list(headList))):
                measureDict[headList[i]] = dataList[i]
            return measureDict
    except FileNotFoundError as err:
        print(f"File error: {err}")
        return None


def getData(request: str):
    if request == "help?":  # detect request
        requestString: str = ""  # create empty string
        for i in AVAILABLE_REQUESTS:  # loop through request list
            requestString += f"{i} "  # add available requests to string
        return requestString

    elif request not in AVAILABLE_REQUESTS:
        return f"Error: Request '{request}' not available. Send 'help?'" \
               f" for a list of available requests"

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
        measureData = _calcWaterVaporPressure(relativeHumidity, temperature)
    else:

        measureData = measureFile[REQUEST_TABLE[request]["dataName"]]

    _timeStamp = measureFile["Timestamp"]
    _outputName = REQUEST_TABLE[request]['name']
    _unit = REQUEST_TABLE[request]['unit']

    return f"{_timeStamp}; {_outputName}={measureData}{_unit}"

    # #  copy weather data from database in python-dictionary
    # measureFile: dict = readData()
    # # get weather data and timestamp from file
    # _measureData = measureFile[REQUEST_TABLE[request]["dataName"]]
    # _timeStamp = measureFile["Timestamp"]
    # # get name and unit from config file
    # _outputName = REQUEST_TABLE[request]['name']
    # _unit = REQUEST_TABLE[request]['unit']
    # #  format and values and return
    # return f"{_timeStamp}; {_outputName}={_measureData}{_unit}"


if __name__ == "__main__":

    for i in list(REQUEST_TABLE):
        print(getData(i))

    print(getData("not a request"))
