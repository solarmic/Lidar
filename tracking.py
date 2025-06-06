
import threading
import numpy as np
import time
from collections import deque
from lidar_interface import LidarInterface
from osc_output import OSCOutput

class StageTracker:
    def __init__(self, lidar_port, osc_ip, osc_port):
        self.stage_size = 4.0
        self.min_distance = 0.5
        self.max_distance = 2.0
        self.min_cluster_size = 5
        self.max_cluster_distance = 0.4

        self.lidar = LidarInterface(lidar_port)
        self.osc = OSCOutput(osc_ip, osc_port)
        self.running = False
        self.lock = threading.Lock()
        self.position_buffer = deque(maxlen=5)

    def start(self):
        self.running = True
        threading.Thread(target=self._run, daemon=True).start()
        print("\n=== SISTEMA DE TRACKING INICIADO ===")
        print("Presiona Ctrl+C para salir")
        self.osc.send_active(True)

    def stop(self):
        self.running = False
        self.lidar.stop()
        self.osc.send_active(False)
        print("Sistema detenido")

    def _run(self):
        while self.running:
            points = self.lidar.read_points()
            clusters = self._cluster_points(points)
            if clusters:
                largest = max(clusters, key=len)
                centroid = np.mean(largest, axis=0)
                norm_x = (centroid[0] + self.stage_size / 2) / self.stage_size
                norm_y = (centroid[1] + self.stage_size / 2) / self.stage_size
                self.position_buffer.append((norm_x, norm_y))
                avg_x = np.mean([p[0] for p in self.position_buffer])
                avg_y = np.mean([p[1] for p in self.position_buffer])
                self.osc.send_position(avg_x, avg_y)
            time.sleep(0.1)

    def _cluster_points(self, points):
        clusters = []
        for p in points:
            found = False
            for cluster in clusters:
                if np.linalg.norm(np.array(p) - np.array(cluster[-1])) < self.max_cluster_distance:
                    cluster.append(p)
                    found = True
                    break
            if not found:
                clusters.append([p])
        return [c for c in clusters if len(c) >= self.min_cluster_size]
