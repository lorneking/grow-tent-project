import smbus2
import time

class ADS1115:
    # Possible I2C addresses for ADS1115
    VALID_ADDRESSES = [0x48, 0x49, 0x4A, 0x4B]

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

    # Gain settings
    ADS1115_REG_CONFIG_GAIN = {
        '2/3': 0x0000,  # Gain = 2/3, ±6.144V
        '1': 0x0200,    # Gain = 1, ±4.096V
        '2': 0x0400,    # Gain = 2, ±2.048V
        '4': 0x0600,    # Gain = 4, ±1.024V
        '8': 0x0800,    # Gain = 8, ±0.512V
        '16': 0x0A00    # Gain = 16, ±0.256V
    }

    # Data rate settings
    ADS1115_REG_CONFIG_DR = {
        8: 0x0000,
        16: 0x0020,
        32: 0x0040,
        64: 0x0060,
        128: 0x0080,
        250: 0x00A0,
        475: 0x00C0,
        860: 0x00E0,
        1600: 0x0080  # Default data rate (1600 SPS)
    }

    ADS1115_REG_CONFIG_MODE_SINGLE = 0x0100  # Single-shot mode
    ADS1115_REG_CONFIG_CQUE_NONE = 0x0003  # Disable the comparator

    def __init__(self, address, channel, gain='2/3', calibration_factor=1.0, data_rate=1600):
        if address not in ADS1115.VALID_ADDRESSES:
            raise ValueError(f"Invalid address: {address}. Must be one of {ADS1115.VALID_ADDRESSES}")
        
        if channel not in ADS1115.ADS1115_REG_CONFIG_MUX:
            raise ValueError("Invalid channel, must be 0-3")
        
        if gain not in ADS1115.ADS1115_REG_CONFIG_GAIN:
            raise ValueError(f"Invalid gain: {gain}. Must be one of {list(ADS1115.ADS1115_REG_CONFIG_GAIN.keys())}")
        
        if data_rate not in ADS1115.ADS1115_REG_CONFIG_DR:
            raise ValueError(f"Invalid data rate: {data_rate}. Must be one of {list(ADS1115.ADS1115_REG_CONFIG_DR.keys())}")

        self.address = address
        self.channel = channel
        self.gain = gain
        self.calibration_factor = calibration_factor
        self.data_rate = data_rate
        self.bus = smbus2.SMBus(1)  # 1 indicates /dev/i2c-1

    def read_voltage(self, samples=10, delay=0.1):
        voltages = []
        for _ in range(samples):
            # Select the correct MUX value for the channel
            mux = ADS1115.ADS1115_REG_CONFIG_MUX[self.channel]
            gain = ADS1115.ADS1115_REG_CONFIG_GAIN[self.gain]
            data_rate = ADS1115.ADS1115_REG_CONFIG_DR[self.data_rate]

            # Write config register to start conversion
            config = ADS1115.ADS1115_REG_CONFIG_OS_SINGLE | \
                     mux | \
                     gain | \
                     ADS1115.ADS1115_REG_CONFIG_MODE_SINGLE | \
                     data_rate | \
                     ADS1115.ADS1115_REG_CONFIG_CQUE_NONE

            self.bus.write_i2c_block_data(self.address, ADS1115.ADS1115_REG_POINTER_CONFIG, [(config >> 8) & 0xFF, config & 0xFF])

            # Wait for the conversion to complete
            time.sleep(delay)

            # Read the conversion results
            result = self.bus.read_i2c_block_data(self.address, ADS1115.ADS1115_REG_POINTER_CONVERT, 2)
            raw_adc = (result[0] << 8) | result[1]

            # Calculate the reference voltage based on the gain setting
            if self.gain == '2/3':
                v_ref = 6.144
            elif self.gain == '1':
                v_ref = 4.096
            elif self.gain == '2':
                v_ref = 2.048
            elif self.gain == '4':
                v_ref = 1.024
            elif self.gain == '8':
                v_ref = 0.512
            elif self.gain == '16':
                v_ref = 0.256

            # Convert raw ADC value to voltage and apply calibration factor
            voltage = raw_adc * (v_ref / 32768.0) * self.calibration_factor
            voltages.append(voltage)

        # Average the readings to filter out noise
        average_voltage = sum(voltages) / len(voltages)
        return average_voltage

if __name__ == "__main__":
    # Example usage
    while True:
    # Create instances with calibration factors and a higher data rate
        VREF5 = ADS1115(0x49, 0, gain='2/3', calibration_factor=1.0028, data_rate=860)
        VREF3_3 = ADS1115(0x49, 1, gain='1', calibration_factor=1.0000, data_rate=860)

        print("5V reference voltage: {:.4f} V".format(VREF5.read_voltage(samples=10, delay=0.01)))
        print("3.3V reference voltage: {:.4f} V".format(VREF3_3.read_voltage(samples=10, delay=0.01)))
