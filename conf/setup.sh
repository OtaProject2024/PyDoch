#!/bin/sh

cat <<EOF > config.yaml
components:
  button:
    channel: 24
    delay: 1
  action:
    normal_delay: 5
    sensor_interrupt_delay: 10
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
    file: a.wav
    volume: 1.0
EOF
