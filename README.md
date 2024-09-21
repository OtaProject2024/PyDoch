# PyDoch

## Overview

This is a set of Python libraries to control "Murdock (Prototype 02)" developed by Ota Project 2024.

## Dependencies

PyDoch relies on several external libraries to function properly.
Ensure these dependencies are installed on your Raspberry Pi:

- PyYAML: Loading configuration files.
- RPi.GPIO: Used for controlling the GPIO pins of the Raspberry Pi.
- adafruit_bno055: Used for controlling the bno055 sensor.
- board: Specify board-specific pins.
- PyGame: Sound Control.

You can install these dependencies:

```
python3 -m venv .venv
source .venv/bin/activate
```

```
pip install pyyaml
pip install rpi.gpio
pip install adafruit-circuitpython-bno055
pip install board
pip install pygame
```

## Configuration

PyDoch uses the `conf/config.yaml` file for configuration settings.

You can create a configuration file:
```
cd conf
sh setup.sh
```

```
sudo cp pydoch.service /etc/systemd/system
sudo systemctl daemon-reload
sudo systemctl enable pydoch.service
sudo systemctl start pydoch.service
sudo systemctl status pydoch.service
```
