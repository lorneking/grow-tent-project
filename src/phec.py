import smbus2
import time
import csv
from datetime import datetime
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

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

PH1 = 4.01 # pH of buffer calibration solution - low
PH2 = 6.86 # pH of buffer calibration solution - mid
PH3 = 9.18 # pH of buffer calibration solution - high

PH1POINT = 31302.29 # Average measured analog calibration value - low
PH2POINT = 27695.95 # Average measured analog calibration value - mid
PH3POINT = 23900.11 # Average measured analog calibration value - high

VREF = 5.15 # VREF measured between +/- pins of WPM356 TDS sensor
SCOUNT = 30 # Number of samples to average for TDS median filtering
TEMPERATURE = 25  # Assuming a fixed temperature for simplicity
#ADCRESOLUTION = 1024.0 # Resolution of 10-bit ADC (Arduino)
ADCRESOLUTION = 32767.0 # Resolution of 16-bit ADC (ADS1115)

raw_values = np.array([PH1POINT, PH2POINT, PH3POINT])
pH_values = np.array([PH1, PH2, PH3])

# Logarithmic function to fit
def log_model(x, a, b):
    return a * np.log(x) + b

# Fit the model to the data
params, covariance = curve_fit(log_model, raw_values, pH_values)

# Extract the parameters
a, b = params
# print("Fitted parameters: a =", a, ", b =", b)

def get_median_num(buffer):
    """ Compute the median of the buffer """
    buffer_sorted = sorted(buffer)
    mid = len(buffer_sorted) // 2
    if len(buffer_sorted) % 2 == 0:
        return (buffer_sorted[mid - 1] + buffer_sorted[mid]) / 2.0
    else:
        return buffer_sorted[mid]

def read_ads1115(channel):
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

def main():
    analog_buffer = [0] * SCOUNT
    with open('sensor_data.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Timestamp', 'TDS Value', 'pH Value', 'Temperature Value'])
        
        while True:

            for i in range(SCOUNT):
                analog_buffer[i] = read_ads1115(0)  # Read TDS sensor values into buffer
                time.sleep(0.04)  # Sampling rate of 40 milliseconds
            
            average_voltage = get_median_num(analog_buffer) * VREF / ADCRESOLUTION
            compensation_coefficient = 1.0 + 0.02 * (TEMPERATURE - 25.0)
            compensation_voltage = average_voltage / compensation_coefficient
            tds_value = (133.42 * compensation_voltage**3 - 255.86 * compensation_voltage**2 + 857.39 * compensation_voltage) * 0.5

            phread = read_ads1115(1)
            phtempread = read_ads1115(2)
            #value3 = read_ads1115(3)
            now = datetime.now()

            phVal = a * np.log(phread) + b

            writer.writerow([now.strftime("%Y-%m-%d %H:%M:%S"), tds_value, phVal, phtempread])
            print(f"Logged values at {now.strftime('%Y-%m-%d %H:%M:%S')}")
            #print(f"Raw pH value: {phread:.2f}")
            #print(f"Measured pH value: {phVal:.2f}")
            print(f"Measured EC value: {tds_value:.2f}")
            time.sleep(1)

if __name__ == "__main__":
    main()
