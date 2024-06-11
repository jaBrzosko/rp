import openmeteo_requests
import requests_cache
import pandas as pd
import numpy as np
from retry_requests import retry
import calendar
from pprint import pprint

cache_session = requests_cache.CachedSession('.cache', expire_after = -1)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

def generate_grid(N):
    top_left = (54.8356, 14.1228)
    top_right = (54.8356, 24.1459)
    bottom_left = (44.8125, 14.1228)
    bottom_right = (44.8125, 24.1459)
    
    latitudes = np.linspace(top_left[0], bottom_left[0], N)
    longitudes = np.linspace(top_left[1], top_right[1], N)
    
    grid_points = []
    for lat in latitudes:
        for lon in longitudes:
            grid_points.append((lat, lon))
    
    return grid_points

def days_in_month(year, month):
    _, num_days = calendar.monthrange(year, month)
    return num_days

def get_temperature(year, month, no_points):
    month = int(month)
    year = int(year)

    start_date = f"{year}-{month:02d}-01"
    end_date = f"{year}-{month:02d}-{days_in_month(year, month):02d}"

    grid = generate_grid(no_points)
    latitudes = [point[0] for point in grid]
    longitudes = [point[1] for point in grid]

    url = "https://archive-api.open-meteo.com/v1/archive"

    params = {
        "latitude": latitudes,
        "longitude": longitudes,
        "start_date": start_date,
        "end_date": end_date,
        "hourly": ["temperature_2m"]
    }

    responses = openmeteo.weather_api(url, params=params)

    result = {}
    result["points"] = []

    for p in grid:
        result["points"].append({
            "latitude": str(p[0]),
            "longitude": str(p[1])
        })

    for index, response in enumerate(responses):
        hourly = response.Hourly()
        hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
        start = pd.to_datetime(hourly.Time(), unit = "s", utc = True)
        interval = pd.Timedelta(seconds = hourly.Interval())

        result["points"][index]["date_temperature"] = [
            {
                "date": str(start + i * interval),
                "temperature": str(temperature)
            } for i, temperature in enumerate(hourly_temperature_2m)
        ]
        

    return result
