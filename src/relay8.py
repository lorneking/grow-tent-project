# Whadda WPM436 Relay Driver

import RPi.GPIO as GPIO

relayPinMap = {
    1: 29,
    2: 31,
    3: 33,
    4: 35,
    5: 37,
    6: 32,
    7: 36,
    8: 38
}

print("Initializing Relay GPIO Pins")

GPIO.setmode(GPIO.BOARD)

for pin in relayPinMap.values():
    GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)

def relayToggle(relay_number):
    # Toggle the state of the relay
    if relay_number in relayPinMap:
        gpio_pin = relayPinMap[relay_number]
        current_state = GPIO.input(gpio_pin)
        GPIO.output(gpio_pin, not current_state)
        return f"Relay {relay_number} toggled to {'ON' if not current_state else 'OFF'}"
    else:
        return "Invalid relay number!"

def relayOn(relay_number):
    # Turn on a specific relay
    if relay_number in relayPinMap:
        GPIO.output(relayPinMap[relay_number], GPIO.HIGH)
        return f"Relay {relay_number} turned ON"
    else:
        return "Invalid relay number!"

def relayOff(relay_number):
    # Turn off a specific relay 
    if relay_number in relayPinMap:
        GPIO.output(relayPinMap[relay_number], GPIO.LOW)
        return f"Relay {relay_number} turned OFF"
    else:
        return "Invalid relay number!"
