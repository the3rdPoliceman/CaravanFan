import RPi.GPIO as GPIO
import Adafruit_DHT
import configparser
import requests
import argparse


def get_outside_temperature(city, weatherapi_credentials_file):
    # Read credentials
    config = configparser.ConfigParser()
    config.read(weatherapi_credentials_file)

    api_key = config.get('credentials', 'key')

    # Define the API endpoint
    base_url = "http://api.weatherapi.com/v1/current.json"

    # Prepare the parameters for the API request
    params = {
        'key': api_key,
        'q': city,
        'aqi': "no",  # Get air quality data
    }

    # Send the API request
    response = requests.get(base_url, params=params)

    # Convert the response to JSON
    data = response.json()

    # Extract the current temperature from the response
    current_temperature = data['current']['temp_c']

    # Return the current temperature
    return current_temperature


def set_fan_state(state, pin):
    # Use GPIO numbers not pin numbers
    GPIO.setmode(GPIO.BCM)

    # set up the GPIO channels - one input and one output
    GPIO.setup(pin, GPIO.OUT)

    # Control the relay
    if state:
        GPIO.output(pin, GPIO.HIGH)
    else:
        GPIO.output(pin, GPIO.LOW)


def get_fan_state(pin):
    # Use GPIO numbers not pin numbers
    GPIO.setmode(GPIO.BCM)

    # set up the GPIO channel
    GPIO.setup(pin, GPIO.IN)

    # Read the fan state
    fan_state = GPIO.input(pin)

    # Return the fan state
    return fan_state


def get_caravan_temperature(pin, sensor=Adafruit_DHT.DHT22):
    # Read temperature
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

    # Return the temperature
    return temperature


def main(config_file, weatherapi_credentials_file):
    # Read configuration
    config = configparser.ConfigParser()
    config.read(config_file)

    city = config.get('configuration', 'city')
    desired_temperature = float(config.get('configuration', 'desired_temperature'))
    temperature_delta_trigger = float(config.get('configuration', 'temperature_delta_trigger'))
    relay_pin = int(config.get('configuration', 'relay_pin'))
    temp_sensor_pin = int(config.get('configuration', 'temp_sensor_pin'))

    outside_temperature = get_outside_temperature(city, weatherapi_credentials_file)
    caravan_temperature = get_caravan_temperature(temp_sensor_pin)

    # If it's colder than we want, we turn th fan off
    # If it's hotter than acceptable, we turn the fan on
    # otherwise, we leave the fan as it is
    if caravan_temperature < desired_temperature:
        set_fan_state(False, relay_pin)
    elif (caravan_temperature + temperature_delta_trigger) > outside_temperature:
        set_fan_state(True, relay_pin)


if __name__ == "__main__":
    # Create the parser
    parser = argparse.ArgumentParser(description='Process command line arguments.')

    # Add the arguments
    parser.add_argument('config_file', metavar='config_file', type=str, help='Path to the configuration file')
    parser.add_argument('weatherapi_credentials_file', metavar='weatherapi_credentials_file', type=str, help='Path to the WeatherAPI credentials file')

    # Parse the arguments
    args = parser.parse_args()

    # Run the main function
    main(args.config_file, args.weatherapi_credentials_file)
