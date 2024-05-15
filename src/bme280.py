import smbus2
from bme280 import BME280
bus = smbus2.SMBus(1)
bme280 = BME280(i2c_dev=bus)