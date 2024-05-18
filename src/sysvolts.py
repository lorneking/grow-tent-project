import subprocess
import threading
import time
from ads1115 import ADS1115  # Make sure the ADS1115 class is in a file named ads1115.py

# Create instances with calibration factors and a higher data rate
VREF5 = ADS1115(0x49, 0, gain='2/3', calibration_factor=1.0028, data_rate=860)
VREF3_3 = ADS1115(0x49, 1, gain='1', calibration_factor=1.0000, data_rate=860)

def get_raspberry_pi_voltage(component):
    try:
        result = subprocess.run(['vcgencmd', 'measure_volts', component], capture_output=True, text=True, check=True)
        # Output is expected to be in the format: "volt=1.2000V"
        voltage_str = result.stdout.strip().split('=')[1].strip('V')
        voltage = float(voltage_str)
        return voltage
    except subprocess.CalledProcessError as e:
        print(f"Failed to get voltage for {component}: {e}")
        return None

def read_voltages():
    threads = []

    # Read Raspberry Pi internal voltages
    components = ['core', 'sdram_c', 'sdram_i', 'sdram_p']
    rpi_voltages = {}

    for component in components:
        thread = threading.Thread(target=lambda c=component: rpi_voltages.update({c: get_raspberry_pi_voltage(c)}))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    # Read ADS1115 external voltages directly
    ads_voltages = {
        'VREF5': VREF5.read_voltage(samples=10, delay=0.01),
        'VREF3_3': VREF3_3.read_voltage(samples=10, delay=0.01)
    }

    return rpi_voltages, ads_voltages

if __name__ == "__main__":
    while True:
        rpi_voltages, ads_voltages = read_voltages()

        # Print Raspberry Pi internal voltages
        print(f"Core Voltage: {rpi_voltages['core']} V")
        print(f"SDRAM C Voltage: {rpi_voltages['sdram_c']} V")
        print(f"SDRAM I Voltage: {rpi_voltages['sdram_i']} V")
        print(f"SDRAM P Voltage: {rpi_voltages['sdram_p']} V")

        # Print ADS1115 external voltages
        print(f"5V reference voltage: {ads_voltages['VREF5']:.4f} V")
        print(f"3.3V reference voltage: {ads_voltages['VREF3_3']:.4f} V")

        # Sleep for 1 second before the next iteration
        time.sleep(1)
