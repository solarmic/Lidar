
import numpy as np
from rplidar import RPLidar

class LidarInterface:
    def __init__(self, port):
        self.port = port
        self.lidar = RPLidar(port)
        self.lidar.connect()
        self.lidar.start_motor()
        self.scanner = self.lidar.iter_measurments()

    def read_points(self):
        points = []
        for _ in range(360):
            try:
                _, quality, angle, distance = next(self.scanner)
                if quality > 7 and distance > 0:
                    angle_rad = np.radians(angle)
                    x = (distance / 1000.0) * np.cos(angle_rad)
                    y = (distance / 1000.0) * np.sin(angle_rad)
                    points.append((x, y))
            except StopIteration:
                continue
        return points

    def stop(self):
        self.lidar.stop_motor()
        self.lidar.stop()
        self.lidar.disconnect()
