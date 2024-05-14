# Whadda WPM436 Relay Driver

import RPi.GPIO as GPIO

PIN_IN1 = 29
PIN_IN2 = 31
PIN_IN3 = 33
PIN_IN4 = 35
PIN_IN5 = 37
PIN_IN6 = 32
PIN_IN7 = 36
PIN_IN8 = 38

PIN1_INITIAL_STATE = GPIO.LOW
PIN2_INITIAL_STATE = GPIO.LOW
PIN3_INITIAL_STATE = GPIO.LOW
PIN4_INITIAL_STATE = GPIO.LOW
PIN5_INITIAL_STATE = GPIO.LOW
PIN6_INITIAL_STATE = GPIO.LOW
PIN7_INITIAL_STATE = GPIO.LOW
PIN8_INITIAL_STATE = GPIO.LOW

GPIO.setmode(GPIO.BOARD)

GPIO.setup(PIN_IN1, GPIO.OUT, initial=PIN1_INITIAL_STATE) # Map RPi Pin PIN_IN1 to relay pin IN1
GPIO.setup(PIN_IN2, GPIO.OUT, initial=PIN2_INITIAL_STATE) # Map RPi Pin PIN_IN2 to relay pin IN2
GPIO.setup(PIN_IN3, GPIO.OUT, initial=PIN3_INITIAL_STATE) # Map RPi Pin PIN_IN3 to relay pin IN3
GPIO.setup(PIN_IN4, GPIO.OUT, initial=PIN4_INITIAL_STATE) # Map RPi Pin PIN_IN4 to relay pin IN4
GPIO.setup(PIN_IN5, GPIO.OUT, initial=PIN5_INITIAL_STATE) # Map RPi Pin PIN_IN5 to relay pin IN5
GPIO.setup(PIN_IN6, GPIO.OUT, initial=PIN6_INITIAL_STATE) # Map RPi Pin PIN_IN6 to relay pin IN6
GPIO.setup(PIN_IN7, GPIO.OUT, initial=PIN7_INITIAL_STATE) # Map RPi Pin PIN_IN7 to relay pin IN7
GPIO.setup(PIN_IN8, GPIO.OUT, initial=PIN8_INITIAL_STATE) # Map RPi Pin PIN_IN8 to relay pin IN8

def channelOn(channel):
    match channel:
        case 1:
            GPIO.output(PIN_IN1, GPIO.HIGH)
        case 2:
            GPIO.output(PIN_IN2, GPIO.HIGH)
        case 3:
            GPIO.output(PIN_IN3, GPIO.HIGH)
        case 4:
            GPIO.output(PIN_IN4, GPIO.HIGH)
        case 5:
            GPIO.output(PIN_IN5, GPIO.HIGH)
        case 6:
            GPIO.output(PIN_IN6, GPIO.HIGH)
        case 7:
            GPIO.output(PIN_IN7, GPIO.HIGH)
        case 8:
            GPIO.output(PIN_IN8, GPIO.HIGH)
        case _:
            return 0
        
def channelOff(channel):
    match channel:
        case 1:
            GPIO.output(PIN_IN1, GPIO.LOW)
        case 2:
            GPIO.output(PIN_IN2, GPIO.LOW)
        case 3:
            GPIO.output(PIN_IN3, GPIO.LOW)
        case 4:
            GPIO.output(PIN_IN4, GPIO.LOW)
        case 5:
            GPIO.output(PIN_IN5, GPIO.LOW)
        case 6:
            GPIO.output(PIN_IN6, GPIO.LOW)
        case 7:
            GPIO.output(PIN_IN7, GPIO.LOW)
        case 8:
            GPIO.output(PIN_IN8, GPIO.LOW)
        case _:
            return 0
        
def channelToggle(channel):
    match channel:
        case 1:
            if (GPIO.input(PIN_IN1) == 1):
                GPIO.output(PIN_IN1, GPIO.LOW)
            else:
                GPIO.output(PIN_IN1, GPIO.HIGH)
        case 2:
            if (GPIO.input(PIN_IN2) == 1):
                GPIO.output(PIN_IN2, GPIO.LOW)
            else:
                GPIO.output(PIN_IN2, GPIO.HIGH)
        case 3:
            if (GPIO.input(PIN_IN3) == 1):
                GPIO.output(PIN_IN3, GPIO.LOW)
            else:
                GPIO.output(PIN_IN3, GPIO.HIGH)
        case 4:
            if (GPIO.input(PIN_IN4) == 1):
                GPIO.output(PIN_IN4, GPIO.LOW)
            else:
                GPIO.output(PIN_IN4, GPIO.HIGH)
        case 5:
            if (GPIO.input(PIN_IN5) == 1):
                GPIO.output(PIN_IN5, GPIO.LOW)
            else:
                GPIO.output(PIN_IN5, GPIO.HIGH)
        case 6:
            if (GPIO.input(PIN_IN6) == 1):
                GPIO.output(PIN_IN6, GPIO.LOW)
            else:
                GPIO.output(PIN_IN6, GPIO.HIGH)
        case 7:
            if (GPIO.input(PIN_IN7) == 1):
                GPIO.output(PIN_IN7, GPIO.LOW)
            else:
                GPIO.output(PIN_IN7, GPIO.HIGH)
        case 8:
            if (GPIO.input(PIN_IN8) == 1):
                GPIO.output(PIN_IN8, GPIO.LOW)
            else:
                GPIO.output(PIN_IN8, GPIO.HIGH)
        case _:
            return 0


# End of program GPIO cleanup
GPIO.cleanup()