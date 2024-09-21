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
  action:
    normal_delay: 5
    sensor_interrupt_delay: 10
test:
  target:
    name: "SVMotor"
    times: 30
    delay: 3
    state: 1
components:
  button:
    channel: 24
    delay: 1
  bno055_sensor:
    frequency: 5
    interval: 0.5
    acceleration_threshold: 10
    magnetic_threshold: 500
  dc_motor:
    ref_channel: 12
    in1_channel: 22
    in2_channel: 27
    power: 100
    save_power: 50
  sv_motor:
    channel: 18
    frequency: 50
    angle: 60
  sound:
    file: "tureta.wav"
    volume: 1.0
EOF
