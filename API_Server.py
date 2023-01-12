from fastapi import FastAPI, HTTPException
import weatherDataHandle
import uvicorn
import json


app = FastAPI()

@app.get("/")
async def root():
    last_measurement = weatherDataHandle.readData()
    return last_measurement


@app.get("/{date}")
async def measurement_by_date(date: str):
    try:
        measurement = weatherDataHandle.readDataDate(date)
        return measurement
    except (IndexError, FileNotFoundError):
        raise HTTPException(status_code=500, detail="no entry found - correct date format: year_month_day_hour_minute")


if __name__ == "__main__":
    config = json.load(open("config.json"))
    host = config["api"]["ip"]
    port = config["api"]["port"]
    debug = bool(config["api"]["debug"])
    if debug:
        logLevel = "debug"
    else:
        logLevel = "info"
    uvicorn.run("API_Server:app", host=host, port=port, reload=debug, log_level=logLevel)