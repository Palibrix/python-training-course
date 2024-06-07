from datetime import datetime, timedelta

import pytz
import requests

from geopy.geocoders import Nominatim

import openmeteo_requests

import pandas as pd
from openmeteo_requests.Client import OpenMeteoRequestsError


def get_location(_city):
    geolocator = Nominatim(user_agent="app_name")
    _location = geolocator.geocode(f"{_city}")
    return {"lat": _location.latitude, "lon": _location.longitude} if _location else None


def get_weather(point, start_time, end_time):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": point['lat'],
        "longitude": point['lon'],
        "hourly": ["temperature_2m", "precipitation_probability", "weather_code"],
        "start_date": f"{start_time.strftime('%Y-%m-%d')}",
        "end_date": f"{end_time.strftime('%Y-%m-%d')}",
        "timezone": "auto",
    }
    try:
        responses = openmeteo.weather_api(url, params=params)
        return responses[0]
    except (OpenMeteoRequestsError, requests.exceptions.HTTPError) as e:
        return e


def form_table(response):
    hourly = response.Hourly()
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
    hourly_precipitation_prob = hourly.Variables(1).ValuesAsNumpy()
    hourly_weather_code = hourly.Variables(2).ValuesAsNumpy()

    tz = pytz.timezone(response.Timezone())
    hourly_time = pd.to_datetime(hourly.Time(), unit="s", utc=True).tz_convert(tz)
    hourly_time_end = pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True).tz_convert(tz)

    hourly_data = {"date": pd.date_range(
        start=hourly_time,
        end=hourly_time_end,
        freq=pd.Timedelta(seconds=hourly.Interval()),
        inclusive="left"
    )}

    data = [
        (time.strftime('%H:%M'),
         time.strftime('%Y-%m-%d'),
         str(f'{round(temp)}°C'), str(f'{int(rain)}%'),
         get_weather_status(code))
        for time, temp, rain, code in zip(hourly_data['date'],
                                          hourly_temperature_2m, hourly_precipitation_prob, hourly_weather_code)
    ]

    df = pd.DataFrame(data, columns=['Hour', 'Day', 'Temperature', 'Rain Prob', 'Weather'])

    pd.set_option('display.max_columns', 100)
    # pd.set_option('display.max_colwidth', 1)

    df['Compiled'] = (df['Temperature'].astype(str) + ' -- ' + df['Rain Prob'].astype(str) + ' -- '
                      + df['Weather'].astype(str))

    df_pivot_temp_rain = df.pivot(index='Hour', columns='Day', values='Compiled')

    return df_pivot_temp_rain


def get_weather_status(code):
    """
    Code Description
        0	Clear sky
        1, 2, 3	Mainly clear, partly cloudy, and overcast
        45, 48	Fog and depositing rime fog
        51, 53, 55	Drizzle: Light, moderate, and dense intensity
        56, 57	Freezing Drizzle: Light and dense intensity
        61, 63, 65	Rain: Slight, moderate and heavy intensity
        66, 67	Freezing Rain: Light and heavy intensity
        71, 73, 75	Snow fall: Slight, moderate, and heavy intensity
        77	Snow grains
        80, 81, 82	Rain showers: Slight, moderate, and violent
        85, 86	Snow showers slight and heavy
        95 *	Thunderstorm: Slight or moderate
        96, 99 *	Thunderstorm with slight and heavy hail
    """
    match code:
        case 0 | 1:
            meaning = 'Clear'
        case 2:
            meaning = 'Cloudy'
        case 3:
            meaning = 'Overcast'
        case 45 | 48:
            meaning = 'Fog'
        case 51 | 53 | 55 | 56 | 57:
            meaning = 'Drizzle'
        case 61 | 63 | 65 | 66 | 67:
            meaning = 'Rain'
        case 71 | 73 | 75 | 76 | 77:
            meaning = 'Snowy'
        case 80 | 81 | 83 | 82 | 84 | 85:
            meaning = 'Rain shower'
        case 95 | 96 | 97:
            meaning = 'Thunderstorm'
        case _:
            meaning = f'Unknown code: {code}'
    return meaning


def get_date_input(blank=False):
    placeholder = "Please enter a start date in the format DD-MM-YYYY: " if not blank else \
        "Please enter an end date in the format DD-MM-YYYY. Blank if the same: "
    while True:
        user_input = input(placeholder)
        if user_input == '' and blank:
            return None
        try:
            user_date = datetime.strptime(user_input, "%d-%m-%Y")
            return user_date
        except ValueError:
            print("Invalid date format. Please try again.")


if __name__ == '__main__':
    openmeteo = openmeteo_requests.Client()
    while True:
        location = None
        while not location:
            city = input('\nEnter city name (any caps) or 0 to exit: ')
            if city == '0':
                exit(0)
            location = get_location(city)
            if not location:
                print('Please provide correct city name')
            start_date = get_date_input()
            while True:
                end_date = get_date_input(blank=True)
                if not end_date:
                    end_date = start_date
                    break
                elif start_date + timedelta(days=7) >= end_date >= start_date:
                    break
                else:
                    print("End date must be later than or equal to start date and be within 7 days after the start date. "
                          "Please try again.")

            weather = get_weather(location, start_date, end_date)
            if weather.__class__ == OpenMeteoRequestsError:
                print(weather.args[0]['reason'])
                print('Please try again.')
                continue
            elif weather.__class__ == requests.HTTPError:
                print(weather)
            else:
                table = form_table(weather)
                print(table)
                location = None
