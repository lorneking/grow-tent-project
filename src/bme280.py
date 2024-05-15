import smbus2
import time

class BME280:
    def __init__(self, address=0x76, bus_number=1):
        self.address = address
        self.bus = smbus2.SMBus(bus_number)
        self.setup()

    def setup(self):
        # Wake up the sensor
        self.write_register(0xF2, 0x01)  # Humidity oversampling x1
        self.write_register(0xF4, 0x27)  # Pressure and temperature oversampling x1, mode normal
        self.write_register(0xF5, 0xA0)  # Standby time 1000ms, filter off

    def read_register(self, reg_addr, length):
        return self.bus.read_i2c_block_data(self.address, reg_addr, length)

    def write_register(self, reg_addr, value):
        self.bus.write_byte_data(self.address, reg_addr, value)

    def get_data(self):
        # Read calibration data
        calib = self.read_register(0x88, 24)

        # Convert byte data to word values
        dig_T1 = self._get_unsigned(calib[0], calib[1])
        dig_T2 = self._get_signed(calib[2], calib[3])
        dig_T3 = self._get_signed(calib[4], calib[5])
        dig_P1 = self._get_unsigned(calib[6], calib[7])
        dig_P2 = self._get_signed(calib[8], calib[9])
        dig_P3 = self._get_signed(calib[10], calib[11])
        dig_P4 = self._get_signed(calib[12], calib[13])
        dig_P5 = self._get_signed(calib[14], calib[15])
        dig_P6 = self._get_signed(calib[16], calib[17])
        dig_P7 = self._get_signed(calib[18], calib[19])
        dig_P8 = self._get_signed(calib[20], calib[21])
        dig_P9 = self._get_signed(calib[22], calib[23])

        # Read temperature and pressure
        data = self.read_register(0xF7, 8)
        adc_p = (data[0] << 12) | (data[1] << 4) | (data[2] >> 4)
        adc_t = (data[3] << 12) | (data[4] << 4) | (data[5] >> 4)

        # Temperature calculations
        var1 = ((((adc_t >> 3) - (dig_T1 << 1))) * (dig_T2)) >> 11
        var2 = (((((adc_t >> 4) - (dig_T1)) * ((adc_t >> 4) - (dig_T1))) >> 12) * (dig_T3)) >> 14
        t_fine = var1 + var2
        temperature = (t_fine * 5 + 128) >> 8

        # Pressure calculations
        var1 = (t_fine) - 128000
        var2 = var1 * var1 * dig_P6
        var2 = var2 + ((var1 * dig_P5) << 17)
        var2 = var2 + ((dig_P4) << 35)
        var1 = ((var1 * var1 * dig_P3) >> 8) + ((var1 * dig_P2) << 12)
        var1 = (((1 << 47) + var1)) * (dig_P1) >> 33
        if var1 == 0:
            pressure = 0
        else:
            p = 1048576 - adc_p
            p = (((p << 31) - var2) * 3125) // var1
            var1 = (dig_P9 * (p >> 13) * (p >> 13)) >> 25
            var2 = (dig_P8 * p) >> 19
            pressure = ((p + var1 + var2) >> 8) + ((dig_P7) << 4)

        return temperature / 100.0, pressure / 25600.0

    def _get_unsigned(self, LSB, MSB):
        return (MSB << 8) + LSB

    def _get_signed(self, LSB, MSB):
        unsigned = self._get_unsigned(LSB, MSB)
        return unsigned if unsigned < 32768 else unsigned - 65536

