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
    acceleration_threshold: 0.1
    magnetic_threshold: 50
  action:
    normal_delay: 10
    sensor_interrupt_delay: 20
EOF
