
#!/usr/bin/env python3
"""
Sistema de detección de actores en escenario usando RPLIDAR A1.
Modularizado, con mayor precisión y estructura limpia.
"""

import time
import signal
import sys
from tracking import StageTracker

LIDAR_PORT = '/dev/cu.usbserial-0001'  # Ajusta según tu sistema
OSC_IP = '127.0.0.1'
OSC_PORT = 8000

tracker = None

def signal_handler(sig, frame):
    global tracker
    if tracker:
        tracker.stop()
    sys.exit(0)

def main():
    global tracker
    signal.signal(signal.SIGINT, signal_handler)

    try:
        tracker = StageTracker(
            lidar_port=LIDAR_PORT,
            osc_ip=OSC_IP,
            osc_port=OSC_PORT
        )
        tracker.start()

        while tracker.running:
            time.sleep(1)

    except KeyboardInterrupt:
        signal_handler(None, None)
    except Exception as e:
        print(f"Error fatal: {e}")
        if tracker:
            tracker.stop()

if __name__ == "__main__":
    main()
