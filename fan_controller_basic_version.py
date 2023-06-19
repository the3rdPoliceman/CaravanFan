import RPi.GPIO as GPIO
import argparse
import time


def set_fan_state(state, pin, relay_active_low):
    # Use GPIO numbers not pin numbers
    GPIO.setmode(GPIO.BCM)

    # set up the GPIO channels - one input and one output
    GPIO.setup(pin, GPIO.OUT)

    # Control the relay
    relay_state = state
    if relay_active_low:
        relay_state = not relay_state

    if relay_state:
        GPIO.output(pin, GPIO.HIGH)
    else:
        GPIO.output(pin, GPIO.LOW)


def main(pin):
    time.sleep(3)
    set_fan_state(True, pin)
    time.sleep(3)
    set_fan_state(False, pin)


if __name__ == "__main__":
    # Create the parser
    parser = argparse.ArgumentParser(description='Process command line arguments.')

    # Add the arguments
    parser.add_argument('pin', metavar='pin', type=int, help='Pin that activates fan via relay')
    parser.add_argument('relay_active_low', metavar='relay_active_low', type=int, help='Specify if relay is active on LOW input')

    # Parse the arguments
    args = parser.parse_args()

    # Run the main function
    main(args.pin)
