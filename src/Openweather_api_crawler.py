import requests
import pandas as pd
import time

host = "http://api.openweathermap.org/data/2.5/"
query = "weather?zip="
api_key = '&APPID=1c8c44cacb87aba2ad36d7985b75248f'

#get weather by zipcode through OpenWeather api
def get_weather_by_zipcode(zipcode):
    try:
        zip = str(zipcode)
        url = host + query + zip + api_key
        weather_json = requests.get(url).json()
        time.sleep(1.001)
        weather = weather_json['weather'][0]['main']
        temperature = weather_json['main']['temp']
        pressure = weather_json['main']['pressure']
        humidity = weather_json['main']['humidity']
        visibility = weather_json['visibility']
        wind_speed = weather_json['wind']['speed']
        clouds = weather_json['clouds']['all']
        return [zipcode, weather, temperature, pressure, humidity, visibility, wind_speed, clouds]
    except:
        return [zipcode, 'None', 'None', 'None', 'None', 'None', 'None', 'None']

def get_zipcode_weather(zip_list):
    weather_info = {'zipcode':[], 'weather':[], 'temperature':[], 'pressure':[], 'humidity':[], 'visibility':[], 'wind_speed':[], 'clouds':[]}
    for zip in zip_list:
        weather_at_the_zip = get_weather_by_zipcode(zip)
        weather_info['zipcode'].append(weather_at_the_zip[0])
        weather_info['weather'].append(weather_at_the_zip[1])
        weather_info['temperature'].append(weather_at_the_zip[2])
        weather_info['pressure'].append(weather_at_the_zip[3])
        weather_info['humidity'].append(weather_at_the_zip[4])
        weather_info['visibility'].append(weather_at_the_zip[5])
        weather_info['wind_speed'].append(weather_at_the_zip[6])
        weather_info['clouds'].append(weather_at_the_zip[7])
    weather_info_df = pd.DataFrame(weather_info)
    return weather_info_df