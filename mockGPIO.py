import logging

logger = logging.getLogger(__name__)

BCM = 'BCM'
OUT = 'OUT'
HIGH = 'HIGH'
LOW = 'LOW'

def setmode(mode):
    logger.debug(f'Set mode to {mode}')

def setup(pin, mode):
    logger.debug(f'Set up pin {pin} with mode {mode}')

def output(pin, state):
    logger.debug(f'Output on pin {pin} set to {state}')
