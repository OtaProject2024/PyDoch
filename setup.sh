#!/bin/sh

# Create the virtual environment
python3 -m venv .venv

# Activate the virtual environment
. .venv/bin/activate

# Install the libraries
pip install pyyaml
pip install rpi.gpio
pip install adafruit-circuitpython-bno055
pip install board
pip install pygame

# Create the config file
cat <<EOF > conf/config.yaml
operation:
  mode: "RICH"
  normal_delay: 5
  sensor_interrupt_delay: 10
test:
  target: "SVMotor"
  times: 30
  interval: 3
  method: 1
components:
  button:
    channel: 24
    delay: 1
    default: false
  bno055_sensor:
    frequency: 5
    interval: 0.5
    acceleration_threshold: 10
    magnetic_threshold: 500
  dc_motor:
    pwm_channel: 12
    in1_channel: 22
    in2_channel: 27
    power: 100
    save_power: 50
    direction: 0.3
  sv_motor:
    channel: 18
    frequency: 50
    angle: 40
  sound:
    file: "tureta.wav"
    volume: 1.0
EOF
