import smbus2
import time

class LTR559:
    def __init__(self, i2c_address=0x23, bus=1, timeout=5.0):
        self.bus = smbus2.SMBus(bus)
        self.i2c_address = i2c_address
        self.init_sensor(timeout)

    def init_sensor(self, timeout):
        part_id = self.read_register(0x86)
        print(f"Read Part ID: {part_id}")
        if (part_id >> 4) != 0x09 or (part_id & 0x0F) != 0x02:
            raise RuntimeError("LTR559 not found")

        self.write_register(0x80, 0x01)  # ALS enable
        self.write_register(0x81, 0x03)  # PS enable
        self.write_register(0x82, 0x7F)  # LED settings
        self.write_register(0x84, 0x02)  # PS measurement rate
        self.write_register(0x85, 0x03)  # ALS measurement rate

        t_start = time.time()
        while time.time() - t_start < timeout:
            status = self.read_register(0x80)
            if status & 0x02 == 0:
                break
            time.sleep(0.05)

        if self.read_register(0x80) & 0x02:
            raise RuntimeError("Timeout waiting for software reset.")
        
        self.write_register(0x94, 0x00)  # PS_OFFSET

    def read_register(self, reg):
        for _ in range(5):
            try:
                return self.bus.read_byte_data(self.i2c_address, reg)
            except Exception as e:
                print(f"Error reading register {reg}: {e}")
                time.sleep(0.1)
        raise RuntimeError(f"Failed to read register {reg} after multiple attempts")

    def write_register(self, reg, value):
        for _ in range(5):
            try:
                self.bus.write_byte_data(self.i2c_address, reg, value)
                return
            except Exception as e:
                print(f"Error writing register {reg}: {e}")
                time.sleep(0.1)
        raise RuntimeError(f"Failed to write register {reg} after multiple attempts")

    def read_als_data(self):
        ch1_low = self.read_register(0x88)
        ch1_high = self.read_register(0x89)
        ch0_low = self.read_register(0x8A)
        ch0_high = self.read_register(0x8B)
        
        ch1 = (ch1_high << 8) | ch1_low
        ch0 = (ch0_high << 8) | ch0_low
        
        return ch0, ch1

    def read_ps_data(self):
        ps_low = self.read_register(0x8D)
        ps_high = self.read_register(0x8E)
        
        ps = (ps_high & 0x07) << 8 | ps_low
        
        return ps

    def update_sensor(self):
        try:
            ch0, ch1 = self.read_als_data()
            ps = self.read_ps_data()
            return ch0, ch1, ps
        except Exception as e:
            print(f"Error updating sensor: {e}")
            return None, None, None

def lux_to_par(lux, conversion_factor):
    return lux * conversion_factor

def calculate_dli(par_values, interval_seconds):
    total_par = sum(par_values)
    total_seconds = len(par_values) * interval_seconds
    total_hours = total_seconds / 3600
    dli = (total_par * total_hours) / 1000000  # convert µmol to mol
    return dli

def main():
    sensor = LTR559()
    par_values = []
    interval_seconds = 2  # Measure every 2 seconds
    conversion_factor = 0.02  # Example conversion factor, replace with your value

    try:
        start_time = time.time()
        while True:
            ch0, ch1, ps = sensor.update_sensor()
            if ch0 is not None and ch1 is not None:
                lux = ch0  # Simplified for demonstration, you might need a better conversion
                par = lux_to_par(lux, conversion_factor)
                par_values.append(par)
                print(f"ALS CH0: {ch0}, ALS CH1: {ch1}, PS: {ps}, Lux: {lux}, PAR: {par}")

            time.sleep(interval_seconds)

            # Calculate DLI after 24 hours (86400 seconds)
            if time.time() - start_time >= 86400:
                dli = calculate_dli(par_values, interval_seconds)
                print(f"Daily Light Integral (DLI): {dli} mol/m²/day")
                par_values = []  # Reset for the next day
                start_time = time.time()

    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
