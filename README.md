# Simple Centipede

Python/Pygame and CircuitPython project for CS2013. The final version combines a desktop Pygame game with Circuit Playground Express hardware input.

## Project Versions

### Final Hardware-Controlled Version

Location:

```text
final/
```

This is the final assignment version. It includes:

- `final/gui`: Pygame game files
- `final/circuitpython`: Circuit Playground Express files

The Circuit Playground Express reads accelerometer and button values, sends them over serial, and provides NeoPixel feedback. The Pygame program reads that serial data to control the shooter and dart.

### Keyboard Demo Version

Location:

```text
keyboard-demo/
```

This version can be run without hardware. It uses keyboard controls and is included so the game can be demonstrated by portfolio visitors without needing a Circuit Playground Express.

## How To Run The Keyboard Demo

Install Pygame:

```bash
pip install -r requirements.txt
```

Run:

```bash
cd keyboard-demo
python3 main.py
```

Controls:

- Left Arrow: move shooter left
- Right Arrow: move shooter right
- Spacebar: fire dart
- Z: cancel/deactivate dart

## How To Run The Final Hardware Version

1. Copy these files to the Circuit Playground Express:

```text
final/circuitpython/code.py
final/circuitpython/sensorlightdisplay.py
```

2. Connect the Circuit Playground Express by USB.

3. Check the serial port in `final/gui/main.py`:

```python
serial.Serial('/dev/tty.usbmodem141101', 115200)
```

4. Run the Pygame game:

```bash
cd final/gui
python3 main.py
```

Hardware controls:

- Tilt left or right: move the shooter
- Button A: fire dart
- Button B: cancel/deactivate dart
- NeoPixels: display tilt feedback

## Object-Oriented Design

The project is structured around separate classes with clear responsibilities:

- `Shooter`: controls player position, movement, screen boundaries, and drawing.
- `Dart`: controls projectile activation, movement, deactivation, and collision shape.
- `Centipede`: controls automatic enemy movement, direction changes, halfway reset, and drawing.
- `SensorLightDisplay`: controls Circuit Playground Express NeoPixel feedback from accelerometer values.
- `EventList`: implements a linked list to record recent gameplay events such as shooter movement, dart firing, round changes, and centipede collisions.

The main game loop creates objects and coordinates interactions between them. This keeps each class focused on its own behaviour and avoids tightly coupling the objects together.

## Portfolio Note

The final assignment demonstrates hardware integration using CircuitPython and Circuit Playground Express. The keyboard version is included as a portfolio-friendly fallback so the game can still be run and reviewed without specialist hardware.
