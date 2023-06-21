from flask import Flask, request
import os
import requests

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/weather')
def weather():
    city = request.args.get('city', '')
    if not city:
        return 'Please provide a city parameter.'

    geocode_url = f'https://nominatim.openstreetmap.org/search?format=json&q={city}'
    try:
        geocode_response = requests.get(geocode_url)
        geocode_data = geocode_response.json()

        if geocode_response.status_code == 200 and geocode_data:
            latitude = geocode_data[0]['lat']
            longitude = geocode_data[0]['lon']

            weather_url = f'https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true'
            weather_response = requests.get(weather_url)
            weather_data = weather_response.json()

            if weather_response.status_code == 200 and 'current_weather' in weather_data:
                weather_state = weather_data['current_weather']
                temperature = weather_state['temperature']
                return f'The temperature in {city} is {temperature}°C'
            else:
                return 'Unable to retrieve weather information.'
        else:
            return 'Unable to retrieve location information.'

    except requests.exceptions.RequestException as e:
        return f'An error occurred: {str(e)}'

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    app.run(host='0.0.0.0', port=port)