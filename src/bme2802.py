import time
import smbus2
import logging

logging.basicConfig(
    format="%(asctime)s.%(msecs)03d %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S"
)

class BME280:
    def __init__(self, address=0x76, bus_number=1):
        self.address = address
        self.bus = smbus2.SMBus(bus_number)
        self.setup()

    def setup(self):
        self.write_register(0xF2, 0x01)  # Humidity oversampling x1
        self.write_register(0xF4, 0x27)  # Pressure and temperature oversampling x1, mode normal
        self.write_register(0xF5, 0xA0)  # Standby time 1000ms, filter off

    def read_temperature(self):
        calib = self.read_register(0x88, 24)
        dig_T1 = self._get_unsigned(calib[0], calib[1])
        dig_T2 = self._get_signed(calib[2], calib[3])
        dig_T3 = self._get_signed(calib[4], calib[5])

        data = self.read_register(0xFA, 3)
        adc_t = (data[0] << 12) | (data[1] << 4) | (data[2] >> 4)

        var1 = ((((adc_t >> 3) - (dig_T1 << 1))) * (dig_T2)) >> 11
        var2 = (((((adc_t >> 4) - (dig_T1)) * ((adc_t >> 4) - (dig_T1))) >> 12) * (dig_T3)) >> 14
        t_fine = var1 + var2
        temperature = (t_fine * 5 + 128) >> 8
        return temperature / 100.0

    def read_register(self, reg_addr, length):
        return self.bus.read_i2c_block_data(self.address, reg_addr, length)

    def write_register(self, reg_addr, value):
        self.bus.write_byte_data(self.address, reg_addr, value)

    def _get_unsigned(self, LSB, MSB):
        return (MSB << 8) + LSB

    def _get_signed(self, LSB, MSB):
        unsigned = self._get_unsigned(LSB, MSB)
        return unsigned if unsigned < 32768 else unsigned - 65536

def get_cpu_temperature():
    with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
        temp = f.read()
    return int(temp) / 1000.0

def main():
    sensor = BME280()
    factor = 14
    cpu_temps = [get_cpu_temperature()] * 5

    while True:
        cpu_temp = get_cpu_temperature()
        cpu_temps = cpu_temps[1:] + [cpu_temp]
        avg_cpu_temp = sum(cpu_temps) / float(len(cpu_temps))
        raw_temp = sensor.read_temperature()
        comp_temp = raw_temp - ((avg_cpu_temp - raw_temp) / factor)
        comp_ftemp = (comp_temp * (9/5)) + 32
        logging.info(f"Compensated temperature: {comp_temp:.2f} °C")
        logging.info(f"Compensated temperature: {comp_ftemp:.2f} °F")
        time.sleep(1)

if __name__ == "__main__":
    main()
