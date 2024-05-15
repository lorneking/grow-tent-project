import smbus2

class Zero2GoOmini:
    I2C_ADDRESS = 0x29  # Default I2C address

    # Register addresses
    REG_FIRMWARE_ID = 0
    REG_VOLTAGE_A_INT = 1
    REG_VOLTAGE_A_DEC = 2
    REG_VOLTAGE_B_INT = 3
    REG_VOLTAGE_B_DEC = 4
    REG_VOLTAGE_C_INT = 5
    REG_VOLTAGE_C_DEC = 6
    REG_WORKING_MODE = 7
    REG_LOW_VOLTAGE_FLAG = 8
    REG_I2C_ADDRESS = 9
    REG_POWER_STATE = 10
    REG_LED_BLINK_INTERVAL = 11
    REG_LOW_VOLTAGE_THRESHOLD = 12
    REG_BULK_ALWAYS_ON = 13
    REG_POWER_CUT_DELAY = 14
    REG_RECOVERY_VOLTAGE_THRESHOLD = 15

    def __init__(self, bus_number=1):
        self.bus = smbus2.SMBus(bus_number)

    def read_register(self, reg_addr):
        """Read a single byte from a given register"""
        return self.bus.read_byte_data(self.I2C_ADDRESS, reg_addr)

    def write_register(self, reg_addr, value):
        """Write a single byte to a given register"""
        self.bus.write_byte_data(self.I2C_ADDRESS, reg_addr, value)

    def get_firmware_id(self):
        """Read the firmware ID"""
        return self.read_register(self.REG_FIRMWARE_ID)

    def get_voltage(self, channel):
        """Get the voltage from a specified channel (A, B, or C)"""
        if channel.upper() == 'A':
            int_part = self.read_register(self.REG_VOLTAGE_A_INT)
            dec_part = self.read_register(self.REG_VOLTAGE_A_DEC)
        elif channel.upper() == 'B':
            int_part = self.read_register(self.REG_VOLTAGE_B_INT)
            dec_part = self.read_register(self.REG_VOLTAGE_B_DEC)
        elif channel.upper() == 'C':
            int_part = self.read_register(self.REG_VOLTAGE_C_INT)
            dec_part = self.read_register(self.REG_VOLTAGE_C_DEC)
        else:
            raise ValueError("Invalid channel. Choose 'A', 'B', or 'C'.")

        return int_part + dec_part / 100.0

    def set_led_blink_interval(self, interval):
        """Set the LED blink interval"""
        valid_intervals = [6, 7, 8, 9]
        if interval in valid_intervals:
            self.write_register(self.REG_LED_BLINK_INTERVAL, interval)
        else:
            raise ValueError("Invalid interval. Use one of these values: 6 (1 sec), 7 (2 sec), 8 (4 sec), 9 (8 sec)")
