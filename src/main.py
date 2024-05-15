#!/usr/bin/env python3

import logging
import time
from datetime import datetime
import csv
import relay8
import ph
import ec

logging.basicConfig(
    format="%(asctime)s.%(msecs)03d %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S")

# Get the temperature of the CPU for compensation
def getCPUTemperature():
    with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
        temp = f.read()
        temp = int(temp) / 1000.0
    return temp

# Tuning factor for compensation. Decrease this number to adjust the
# temperature down, and increase to adjust up
factor = 10.25
cpuTemps = [getCPUTemperature()] * 5

def logLine():
    
    global cpuTemps

    now = datetime.now()
    CPUTemp = getCPUTemperature()
    # Smooth out with some averaging to decrease jitter
    cpuTemps = cpuTemps[1:] + [CPUTemp]
    avgCpuTemp = sum(cpuTemps) / float(len(cpuTemps))
    # rawTemp = bme280.get_temperature    
    rawTemp = 25.0 # use 25 temp placeholder until bme280 starts working
    cTemp = rawTemp - ((avgCpuTemp - rawTemp) / factor)
    fTemp = ((cTemp * (9/5)) + 32)
    with open('sensor_data.csv', 'w', newline='') as file:
        # lux = ltr559.get_lux()
        # prox = ltr559.get_proximity()        
        tdsValue = ec.tdsRead()
        phVal = ph.phRead()
        phTempVal = ph.phTempRead()
        writer = csv.writer(file)
        writer.writerow([now.strftime("%Y-%m-%d %H:%M:%S"), tdsValue, phVal, phTempVal, cTemp, fTemp])
    print(f"Logged values at {now.strftime('%Y-%m-%d %H:%M:%S')}")  
    print(f"Measured EC value: {tdsValue:.2f}")
    print(f"Measured pH value: {phVal:.2f}")
    print(f"Compensated temperature: {cTemp:05.2f} °C ")
    print(f"Fahrenheit temperature: {fTemp:05.2f} °F")
    logging.info(f"Measured EC value: {tdsValue:.2f}")
    logging.info(f"Measured pH value: {phVal:.2f}")
    logging.info(f"Compensated temperature: {cTemp:05.2f} °C")
    logging.info(f"Fahrenheit temperature: {fTemp:05.2f} °F")
    #logging.info(f"""Light: {lux:05.02f} Lux
    #Proximity: {prox:05.02f}
    #""")
    time.sleep(1.0)

def main():
    
    try:

        while True:

            logLine()

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        print("Cleaning up GPIO...")
        relay8.GPIO.cleanup()

if __name__ == "__main__":
    main()


