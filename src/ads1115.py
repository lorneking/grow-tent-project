import smbus2
import time

# ADS1115 default address
ADS1115_I2C_ADDRESS = 0x48

# Pointer Register
ADS1115_REG_POINTER_CONVERT = 0x00
ADS1115_REG_POINTER_CONFIG = 0x01

# Config Register
ADS1115_REG_CONFIG_OS_SINGLE = 0x8000  # Start a single conversion

# Mux values for different channels
ADS1115_REG_CONFIG_MUX = {
    0: 0x4000,  # Single-ended A0
    1: 0x5000,  # Single-ended A1
    2: 0x6000,  # Single-ended A2
    3: 0x7000   # Single-ended A3
}

ADS1115_REG_CONFIG_GAIN_ONE = 0x0200  # Gain = 1
ADS1115_REG_CONFIG_MODE_SINGLE = 0x0100  # Single-shot mode
ADS1115_REG_CONFIG_DR_1600SPS = 0x0080  # 1600 samples per second
ADS1115_REG_CONFIG_CQUE_NONE = 0x0003  # Disable the comparator

# Initialize I2C (smbus2)
bus = smbus2.SMBus(1)  # 1 indicates /dev/i2c-1

def readADS1115(channel):
    # Select the correct MUX value for the channel
    if channel in ADS1115_REG_CONFIG_MUX:
        mux = ADS1115_REG_CONFIG_MUX[channel]
    else:
        raise ValueError("Invalid channel, must be 0-3")

    # Write config register to start conversion
    config = ADS1115_REG_CONFIG_OS_SINGLE | \
             mux | \
             ADS1115_REG_CONFIG_GAIN_ONE | \
             ADS1115_REG_CONFIG_MODE_SINGLE | \
             ADS1115_REG_CONFIG_DR_1600SPS | \
             ADS1115_REG_CONFIG_CQUE_NONE
    bus.write_i2c_block_data(ADS1115_I2C_ADDRESS, ADS1115_REG_POINTER_CONFIG, [(config >> 8) & 0xFF, config & 0xFF])

    # Wait for the conversion to complete
    time.sleep(0.1)

    # Read the conversion results
    result = bus.read_i2c_block_data(ADS1115_I2C_ADDRESS, ADS1115_REG_POINTER_CONVERT, 2)
    return (result[0] << 8) | result[1]