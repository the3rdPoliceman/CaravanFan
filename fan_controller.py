import logging
import logging.config
import yaml
import configparser
import requests
import argparse

with open('logging.yaml', 'r') as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)

logger = logging.getLogger(__name__)

try:
    import RPi.GPIO as GPIO
    logger.info("Using real GPIO calls")
except ImportError:
    logger.info("Using mock GPIO calls")
    import mockGPIO as GPIO

try:
    import Adafruit_DHT
    logger.info("Using real temperature sensor")
except ImportError:
    logger.info("Using mock temperature sensor")
    import mockDHT as Adafruit_DHT


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

    logger.debug("Outside temperature received from API: %s", current_temperature)

    # Return the current temperature
    return current_temperature


def setup_gpio(pin):
    # Use GPIO numbers not pin numbers
    GPIO.setmode(GPIO.BCM)

    # set up the GPIO channels - one input and one output
    GPIO.setup(pin, GPIO.OUT)


def set_fan_state(state, pin, relay_active_low):
    # Control the relay
    relay_state = state
    if relay_active_low:
        relay_state = not relay_state

    if relay_state:
        logger.debug("Setting fan relay state to HIGH (Relay Active When Low=" + str(relay_active_low) + ")")
        GPIO.output(pin, GPIO.HIGH)
    else:
        logger.debug("Setting fan relay state to LOW (Relay Active When Low=" + str(relay_active_low) + ")")
        GPIO.output(pin, GPIO.LOW)


def get_caravan_temperature(pin, sensor=Adafruit_DHT.DHT22):
    # Read temperature
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

    logger.debug("Caravan temperature received from sensor: %s", temperature)

    # Return the temperature
    return temperature


def main(config_file, weatherapi_credentials_file):
    # Read configuration
    config = configparser.ConfigParser()
    config.read(config_file)

    city = config.get('configuration', 'city')
    comfortable_temperature_lower = float(config.get('configuration', 'comfortable_temperature_lower'))
    comfortable_temperature_upper = float(config.get('configuration', 'comfortable_temperature_upper'))
    relay_pin = int(config.get('configuration', 'relay_pin'))
    temp_sensor_pin = int(config.get('configuration', 'temp_sensor_pin'))
    relay_active_low = config.getboolean('configuration', 'relay_active_low')

    setup_gpio(relay_pin)

    outside_temperature = get_outside_temperature(city, weatherapi_credentials_file)
    caravan_temperature = get_caravan_temperature(temp_sensor_pin)

    # 1. If the caravan temperature is within the comfortable temperature bounds, we don't change the fan state
    if comfortable_temperature_lower <= caravan_temperature <= comfortable_temperature_upper:
        logger.debug("Caravan temperature (%s) is within comfortable bounds (%s to %s). Not changing fan state...", caravan_temperature, comfortable_temperature_lower, comfortable_temperature_upper)

    # 2. If the caravan temperature is below the lower comfortable temperature bound and the outside temperature is higher than the caravan temperature, the fan should be turned on in order to raise the caravan temperature.
    elif caravan_temperature < comfortable_temperature_lower and outside_temperature > caravan_temperature:
        logger.debug("Caravan temperature (%s) is below comfortable bounds and outside temperature (%s) is higher. Turning fan on...", caravan_temperature, outside_temperature)
        set_fan_state(True, relay_pin, relay_active_low)

    # 3. If the caravan temperature is above the upper comfortable temperature bound and the outside temperature is lower than the caravan temperature, the fan should be turned on in order to cool the caravan temperature.
    elif caravan_temperature > comfortable_temperature_upper and outside_temperature < caravan_temperature:
        logger.debug("Caravan temperature (%s) is above comfortable bounds and outside temperature (%s) is lower. Turning fan on...", caravan_temperature, outside_temperature)
        set_fan_state(True, relay_pin, relay_active_low)

    # 4. If none of the above if true, the fan should be turned off
    else:
        logger.debug("None of the above conditions met. Turning fan off...")
        set_fan_state(False, relay_pin, relay_active_low)


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
