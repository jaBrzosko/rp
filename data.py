import openmeteo_requests

import requests_cache
import pandas as pd
from retry_requests import retry
import json
import sys

year = sys.argv[1]

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = -1)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below
url = "https://archive-api.open-meteo.com/v1/archive"
params = {
	"latitude": [54.8356, 54.8356, 44.8125, 44.8125],
	"longitude": [14.1228, 24.1459, 14.1228, 24.1459],
	"start_date": f"{year}-01-01",
	"end_date": f"{year}-12-31",
	"hourly": ["temperature_2m", "pressure_msl", "surface_pressure", "cloud_cover", "soil_temperature_0_to_7cm", "soil_moisture_0_to_7cm"]
}
responses = openmeteo.weather_api(url, params=params)

for response in responses:
    print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
    print(f"Elevation {response.Elevation()} m asl")
    print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
    print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

    # Process hourly data. The order of variables needs to be the same as requested.
    hourly = response.Hourly()
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
    hourly_pressure_msl = hourly.Variables(1).ValuesAsNumpy()
    hourly_surface_pressure = hourly.Variables(2).ValuesAsNumpy()
    hourly_cloud_cover = hourly.Variables(3).ValuesAsNumpy()
    hourly_soil_temperature_0_to_7cm = hourly.Variables(4).ValuesAsNumpy()
    hourly_soil_moisture_0_to_7cm = hourly.Variables(5).ValuesAsNumpy()

    hourly_data = {"date": pd.date_range(
        start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
        end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
        freq = pd.Timedelta(seconds = hourly.Interval()),
        inclusive = "left"
    )}
    hourly_data["temperature_2m"] = hourly_temperature_2m
    hourly_data["pressure_msl"] = hourly_pressure_msl
    hourly_data["surface_pressure"] = hourly_surface_pressure
    hourly_data["cloud_cover"] = hourly_cloud_cover
    hourly_data["soil_temperature_0_to_7cm"] = hourly_soil_temperature_0_to_7cm
    hourly_data["soil_moisture_0_to_7cm"] = hourly_soil_moisture_0_to_7cm

    df_file_name = f"data/points/df_{response.Latitude()}_{response.Longitude()}_{year}.json"

    hourly_dataframe = pd.DataFrame(data = hourly_data)
    try:
        hourly_dataframe['date'] = hourly_dataframe['date'].astype(str)
        hourly_dataframe.to_json(df_file_name, orient='records', indent=4)
    except Exception as e:
        print(f"Error: {e}")
    print(hourly_dataframe)
