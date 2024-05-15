import ads1115 as ADS
import time
import math

# Constants for Steinhart-Hart Equation (assuming a 10k thermistor)
# These constants need to be determined for your specific thermistor

A = -0.001169
B = 0.000565
C = -8.99e-07

THERMISTOR_CHANNEL = 3 # ADS1115 channel of thermistor (0-3)
CORRECTION_FACTOR_C = -2.73 # Temperature correction factor is degrees C
RSERIES = 9986   # Resistor value in the voltage divider
VSUPPLY = 3.17     # Supply voltage

def readThermistor():
    
    rawADC = ADS.readADS1115(THERMISTOR_CHANNEL)

    if rawADC > 32767:  # Convert from unsigned to signed value
        rawADC -= 65535

    thermVoltage = rawADC * 4.096 / 32767  # Convert to voltage
    return thermVoltage

def calculateTemperature(voltage):
    
    # Calculate the resistance of the thermistor
    R_thermistor = RSERIES * (VSUPPLY / voltage - 1)
    
    # Steinhart-Hart Equation to calculate temperature in Kelvin
    lnR = math.log(R_thermistor)
    temp_kelvin = 1 / (A + B*lnR + C*(lnR**3))
    
    # Convert Kelvin to Celsius
    temp_celsius = (temp_kelvin - 273.15) + CORRECTION_FACTOR_C
    temp_fahrenheit = (temp_celsius * (9/5)) + 32.0
    return temp_celsius, temp_fahrenheit

def main():
    while True:
        voltage = readThermistor()
        temperatureC, temperatureF = calculateTemperature(voltage)
        print(f"Measured voltage: {voltage:.2f} V")
        print(f"Calculated temperature: {temperatureC:.2f} °C")
        print(f"Calculated temperature: {temperatureF:.2f} °F")
        time.sleep(1)

if __name__ == "__main__":
    main()