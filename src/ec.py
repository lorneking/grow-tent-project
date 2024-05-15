import ads1115 as ADS
import time

SCOUNT = 30
ADCRESOLUTION = 32767.0 # Resolution of 16-bit ADC (ADS1115)
VREF = 5.15 # VREF measured between +/- pins of WPM356 TDS sensor
TEMPERATURE = 25  # Assuming a fixed temperature for simplicity

analog_buffer = [0] * SCOUNT

def getMedianNum(buffer):
    """ Compute the median of the buffer """
    buffer_sorted = sorted(buffer)
    mid = len(buffer_sorted) // 2
    if len(buffer_sorted) % 2 == 0:
        return (buffer_sorted[mid - 1] + buffer_sorted[mid]) / 2.0
    else:
        return buffer_sorted[mid]

def tdsRead():
        
    for i in range(SCOUNT):
        analog_buffer[i] = ADS.readADS1115(0)  # Read TDS sensor values into buffer
        time.sleep(0.04)  # Sampling rate of 40 milliseconds
            
    average_voltage = getMedianNum(analog_buffer) * VREF / ADCRESOLUTION
    compensation_coefficient = 1.0 + 0.02 * (TEMPERATURE - 25.0)
    compensation_voltage = average_voltage / compensation_coefficient
    tds_value = (133.42 * compensation_voltage**3 - 255.86 * compensation_voltage**2 + 857.39 * compensation_voltage) * 0.5
    return tds_value