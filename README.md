# Raspberry Pi Caravan Temperature Controller

A Raspberry Pi project to control a fan in a caravan based on temperature readings and data from WeatherAPI.

## Overview

The project uses Python to read temperature from a local sensor and from an API, then controls a fan via a relay depending on the temperatures.

## Getting Started

These instructions will get you a copy of the project up and running on your Raspberry Pi.

### Prerequisites

You'll need to install the following libraries:

- `RPi.GPIO`: This library is used to control the Raspberry Pi's GPIO pins. Install it by running:

```bash
pip install RPi.GPIO
```

Adafruit_DHT: This library is used to read temperature data from the DHT22 sensor. Install it by running:
```bash
pip install Adafruit_DHT
```

configparser: This library is used to read configuration files. Install it by running:
```bash
pip install configparser
```

requests: This library is used to send HTTP requests to the WeatherAPI. Install it by running:
```bash
pip install requests
```

yaml: This library is used to allow configuration of logging. Install it by running:
```bash
pip3 install PyYAML
```

## Configuration
There are two configuration files that you need to prepare:

### config.ini File
This file contains the configuration for the program, including the location, temperature bounds, relay pins etc. Here's an example of how it should look:

```ini
[configuration]
city = Zurich
comfortable_temperature_lower = 19
comfortable_temperature_upper = 21
temp_sensor_pin = 4
relay_pin = 17
relay_active_low=true
```
**comfortable_temperature_lower** and **comfortable_temperature_upper** are float values which define the bounds of what is a comfortable or goal temperature. The reason for a range rather than a specific target temperature is to ensure the fan is not turned on and off very often.  
**relay_active_low** defines whether the relay module you are using sets the relay to be active when the input voltage is low


### weatherapi.credentials File
This file contains your credentials for WeatherAPI. Here's an example of how it should look:
```ini
[credentials]
key = your_api_key_here
```

## Running the Project

### Running once
To run the project, navigate to the project directory in your terminal and run the following command:
```
python3 main.py config.ini weatherapi.credentials
```
Replace config.ini and weatherapi.credentials with the paths to your actual configuration files if they're not in the same directory as main.py.  

### Setting up to run for real
When running for real, the above should be run as a cron job at whatever interval you feel is right, bearing in mind it will hit the WeatherAPI service every time it runs.

## Logging
Logging is configured via the logging.yaml file in the root directory.
