BCM = 'BCM'
OUT = 'OUT'
HIGH = 'HIGH'
LOW = 'LOW'

def setmode(mode):
    print(f'Set mode to {mode}')

def setup(pin, mode):
    print(f'Set up pin {pin} with mode {mode}')

def output(pin, state):
    print(f'Output on pin {pin} set to {state}')