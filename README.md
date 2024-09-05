# PyDoch

## Overview

This is a set of Python libraries to control "Murdock (Prototype 02)" developed by Ota Project 2024.

## Dependencies

PyDoch relies on several external libraries to function properly.
Ensure these dependencies are installed on your Raspberry Pi:

- RPi.GPIO: Used for controlling the GPIO pins of the Raspberry Pi.
- PyYAML: Loading configuration files.
- adafruit_bno055: Used for controlling the bno055 sensor.

You can install these dependencies:

```
python3 -m venv .venv
source .venv/bin/activate
```

```
pip install python3-rpi.gpio
pip install python3-yaml
pip install adafruit-circuitpython-bno055
pip install board
```

## Configuration

PyDoch uses the `conf/config.yaml` file for configuration settings.

You can create a configuration file:
```
cd conf
sh setup.sh
```

Here is an example of a `config.yaml` file:

```yaml
components:
  button:
    channel: 24
  dc_motor:
    ref_channel: 12
    in1_channel: 22
    in2_channel: 27
    power: 100
    save_power: 50
  sv_motor:
    channel: 18
    angle: 60
  bno055_sensor:
    acceleration_threshold: 0.1
    magnetic_threshold: 50
  action:
    normal_delay: 10
    sensor_interrupt_delay: 20
```
