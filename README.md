# PyDoch

## Overview

This is a set of Python libraries to control "Murdock (Prototype 01)" developed by Ota Project 2024.

## Dependencies

PyDoch relies on several external libraries to function properly.
Ensure these dependencies are installed on your Raspberry Pi:

- RPi.GPIO: Used for controlling the GPIO pins of the Raspberry Pi.
- PyYAML: Loading configuration files.

You can install these dependencies:

```
sudo apt install python3-rpi.gpio
sudo apt install python3-yaml
```

## Configuration

PyDoch uses the `src/config.yaml` file for configuration settings.
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
  sv_motor:
    channel: 18
    angle: 60
```
