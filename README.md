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

### Configuration
There are two configuration files that you need to prepare:

**config.ini**   
This file contains the configuration for the program, including the city, desired temperature, temperature delta trigger, relay pin, and temperature sensor pin. Here's an example of how it should look:

```ini
[configuration]
city = Zurich
desired_temperature = 25
temperature_delta_trigger = 2
relay_pin = 17
temp_sensor_pin = 4
relay_active_low = true
```

**weatherapi.credentials**    
This file contains your credentials for WeatherAPI. Here's an example of how it should look:
```ini
[credentials]
key = your_api_key_here
```

### Running the Project
To run the project, navigate to the project directory in your terminal and run the following command:
```
python main.py config.ini weatherapi.credentials
```
Replace config.ini and weatherapi.credentials with the paths to your actual configuration files if they're not in the same directory as main.py.
