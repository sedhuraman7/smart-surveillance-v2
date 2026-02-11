import serial
import threading
import time
import random
import config
import pynmea2

class GPSService:
    def __init__(self):
        self.latitude = 13.0827  # Default: Chennai
        self.longitude = 80.2707
        self.running = False
        self.ser = None

        if not config.IS_SIMULATION:
            try:
                self.ser = serial.Serial(config.GPS_SERIAL_PORT, config.GPS_BAUD_RATE, timeout=1)
            except Exception as e:
                print(f"[GPS] Hardware not found. Switching to Simulation Mode.")
                config.IS_SIMULATION = True

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._update_loop, daemon=True)
        self.thread.start()

    def _update_loop(self):
        while self.running:
            if config.IS_SIMULATION:
                # Mock GPS Movement (Simulating slight drift)
                self.latitude += random.uniform(-0.0001, 0.0001)
                self.longitude += random.uniform(-0.0001, 0.0001)
                time.sleep(1)
            else:
                # Real Hardware Logic
                try:
                    line = self.ser.readline().decode('utf-8', errors='ignore')
                    if line.startswith('$GNGGA') or line.startswith('$GPGGA'):
                        msg = pynmea2.parse(line)
                        if msg.lat and msg.lon:
                            self.latitude = msg.latitude
                            self.longitude = msg.longitude
                except Exception:
                    pass
                time.sleep(0.1)

    def get_location(self):
        return self.latitude, self.longitude

    def stop(self):
        self.running = False
        if self.ser:
            self.ser.close()
