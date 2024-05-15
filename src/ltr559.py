import smbus2

bus = smbus2.SMBus(1)

try:
    # Transitional fix for breaking change in LTR559
    from ltr559 import LTR559
    ltr559 = LTR559(i2c_dev=bus)
except ImportError:
    import ltr559