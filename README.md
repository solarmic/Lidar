
# Stage Tracker con RPLIDAR A1

Este proyecto detecta la posición de una persona en un escenario mediante un sensor RPLIDAR y envía la posición normalizada a través de OSC (Open Sound Control) a otros entornos como Max/MSP, TouchDesigner, etc.

## Archivos

- `main.py`: script principal que inicia el sistema.
- `tracking.py`: lógica de seguimiento, clustering y suavizado.
- `lidar_interface.py`: interfaz con el RPLIDAR A1.
- `osc_output.py`: manejo de salida de datos vía OSC.

## Requisitos

```bash
pip install rplidar python-osc numpy
```

## Conexión del LIDAR

- Ajusta el puerto en `main.py`:
  ```python
  LIDAR_PORT = '/dev/cu.usbserial-0001'  # En Windows puede ser 'COM3', en Linux '/dev/ttyUSB0'
  ```

## Ejecución

```bash
python main.py
```

Presiona `Ctrl+C` para detener.

## Datos OSC enviados

- `/stage/active`: 1 o 0 cuando hay detección o no.
- `/stage/position/x`: coordenada X normalizada (0 a 1).
- `/stage/position/y`: coordenada Y normalizada (0 a 1).
- `/stage/position`: `[x, y]` como lista.

## Notas

- Asegúrate de tener línea de visión clara entre el LIDAR y la persona.
- El área de detección por defecto es un cuadrado de 4x4m centrado en el sensor.
