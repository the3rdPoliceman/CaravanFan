DHT22 = 'DHT22'

def read_retry(sensor, pin):
    print(f'Reading sensor {sensor} on pin {pin}')
    return 50, 40  # Returns a mock humidity and temperature
