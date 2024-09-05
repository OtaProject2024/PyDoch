#!/bin/sh

cat <<EOF > config.yaml
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
    frequency: 5
    acceleration_threshold: 10
    magnetic_threshold: 500
  action:
    normal_delay: 5
    sensor_interrupt_delay: 10
EOF
