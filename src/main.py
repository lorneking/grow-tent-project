#!/usr/bin/env python3

import logging
import time
import relay8

from bme280 import BME280
from smbus2 import SMBus

bus = SMBus(1)
bme280 = BME280(i2c_dev=bus)

try:
    # Transitional fix for breaking change in LTR559
    from ltr559 import LTR559
    ltr559 = LTR559(i2c_dev=bus)
except ImportError:
    import ltr559

logging.basicConfig(
    format="%(asctime)s.%(msecs)03d %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S")



# Get the temperature of the CPU for compensation
def get_cpu_temperature():
    with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
        temp = f.read()
        temp = int(temp) / 1000.0
    return temp


# Tuning factor for compensation. Decrease this number to adjust the
# temperature down, and increase to adjust up
factor = 10.25

cpu_temps = [get_cpu_temperature()] * 5

while True:
    cpu_temp = get_cpu_temperature()
    lux = ltr559.get_lux()
    prox = ltr559.get_proximity()
    # Smooth out with some averaging to decrease jitter
    cpu_temps = cpu_temps[1:] + [cpu_temp]
    avg_cpu_temp = sum(cpu_temps) / float(len(cpu_temps))
    raw_temp = bme280.get_temperature()
    comp_temp = raw_temp - ((avg_cpu_temp - raw_temp) / factor)
    f_temp = ((comp_temp * (9/5)) + 32)
    #logging.info(f"Compensated temperature: {comp_temp:05.2f} °C")
    logging.info(f"Fahrenheit temperature: {f_temp:05.2f} °F")
    logging.info(f"""Light: {lux:05.02f} Lux
Proximity: {prox:05.02f}
""")
    time.sleep(1.0)



# End of program GPIO cleanup
GPIO.cleanup()