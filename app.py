from flask import Flask
from flask import render_template, request
import config

import requests

app = Flask(__name__)


@app.route('/')
def index():
    user_ip = request.environ['REMOTE_ADDR']
    user_ip = '69.248.86.74'
    r = requests.get('https://tools.keycdn.com/geo.json?host=' + user_ip).json()['data']['geo']
    city = r['city']
    state= r['region']
    ip_coordinates = str(r['latitude']) + "," + str(r['longitude'])
    weather_info, weather_icon = get_weather(ip_coordinates)
    location = {'city': city, 'state': state}

    print(city, state, ip_coordinates)
    return render_template("index.html", location=location, weather_info=weather_info, weather_icon=weather_icon)

def get_weather(ip_coordinates):
    degree_sign = u'\N{DEGREE SIGN}'
    weather_key = config.weather_key
    print('http://api.forecast.io/forecast/%s/%s' % (weather_key, ip_coordinates))

    weather = requests.get('https://api.darksky.net/forecast/%s/%s' % (weather_key, ip_coordinates)).json()

    weather_icon = str(weather['currently']['icon'])
    temperature = str(int(weather['currently']['temperature']))
    chance_of_rain = weather['daily']['data'][0]['precipProbability']

    if chance_of_rain == 0:
        rain_comment = 'There is no chance of rain.'
    elif 0 < chance_of_rain < 0.5:
        rain_comment = 'There is a slight chance of rain!'
    elif 0.5 < chance_of_rain < 0.75:
        rain_comment = 'There is a high chance of rain!'
    elif chance_of_rain == 1:
        rain_comment = 'It is raining right now!'
    else:
        rain_comment= 'Prepare to get drenched!'

    weather_info = {'temperature' : temperature, 'rain' : rain_comment}

    return weather_info, weather_icon



if __name__ == '__main__':
    app.run(debug=True)



