# PyDoch

## Overview

This is a set of Python scripts to control Murdock (Prototype 01) and Gyobot (Prototype 02) developed by Ota
Project 2024.

## Dependencies

PyDoch relies on several external libraries to function properly.
Ensure these dependencies are installed on your Raspberry Pi:

- PyYAML: Loading configuration files.
- RPi.GPIO: Used for controlling the GPIO pins of the Raspberry Pi.
- adafruit_bno055: Used for controlling the bno055 sensor.
- board: Specify board-specific pins.
- PyGame: Sound control.

You can install these dependencies:

```shell
python -m venv .venv
source .venv/bin/activate
```

```shell
pip install pyyaml
pip install rpi.gpio
pip install adafruit-circuitpython-bno055
pip install board
pip install pygame
```

## How to use

#### Table of Contents

- [Preparation (First Time Only)](#preparation-first-time-only)
- [Reflect Latest Changes (Subsequent Times)](#reflect-latest-changes-subsequent-times)
- [Editing Configuration Files](#editing-configuration-files)
- [Log File Review](#log-file-review)
- [Startup Instructions](#startup-instructions)

### Preparation (First Time Only)

1. Clone the repository from GitHub:

    ```shell
    git clone https://github.com/OtaProject2024/PyDoch.git
    ```

2. Navigate to the repository:

    ```shell
    cd PyDoch
    ```

3. Set up the Python virtual environment and install dependencies:

    ```shell
    sh setup.sh
    ```

   Please sit back and enjoy a cup of coffee while you wait. ☕️

### Reflect Latest Changes (Subsequent Times)

1. Navigate to the repository:

    ```shell
    cd PyDoch
    ```

2. Fetch the latest commits from the remote repository:

    ```shell
    git pull
    ```

### Editing Configuration Files

1. Navigate to the repository:

    ```shell
    cd PyDoch
    ```
2. Open the configuration file with an editor:

    ```shell
    nano conf/config.yaml
    ```

3. Edit the configuration:

    ```yaml:conf/config.yaml
    operation:
      interface:
        mode: "NORMAL"                  # TUI mode (experimental feature)
      action:
        normal_delay: 5
        sensor_interrupt_delay: 10
    test:
      target:
        name: "SVMotor"                 # Target for test mode
        times: 30                       # Repeat count
        delay: 3                        # Interval between repeats
        method: 1
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
        pwm_channel: 12                 # GPIO pin for PWM (BCM)
        in1_channel: 22                 # GPIO pin for IN1 (BCM)
        in2_channel: 27                 # GPIO pin for IN2 (BCM)
        power: 100                      # Motor speed (duty cycle)
        save_power: 50
        direction: 0.3                  # Motor direction change interval
      sv_motor:
        channel: 18                     # GPIO pin for PWM (BCM)
        frequency: 50                   # Frequency
        angle: 40                       # Rotation angle (degrees)
      sound:
        file: "tureta.wav"
        volume: 1.0
    ```
   [!WARNING]
   Make sure to edit ``conf/config.yaml`` rather than ``conf/default_config.yaml``.

4. If ``conf/config.yaml`` does not exist, create it:

    ```shell
    sh setup_config.sh
    ```

### Log File Review

1. Navigate to the repository:

    ```shell
    cd PyDoch
    ```

2. List the log files:

    ```shell
    ls log
    ```

   Identify the log file you wish to view, e.g., ``murdoch_200101011234.log``.

3. View the log file:

    ```shell
    cat log/murdoch_200101011234.log
    ```

   Replace with the actual log file name to display its contents.

### Startup Instructions

1. Navigate to the repository:

    ```shell
    cd PyDoch
    ```

2. Run the boot script:

    - For PRODUCT Mode (Production use):

         ```shell
         sh boot.sh -p
         ```

    - For TEST Mode (Testing use):

         ```shell
         sh boot.sh -t
         ```

    - For DEMO Mode (Demonstration use):

         ```shell
         sh boot.sh -d
         ```

## Experimental feature

- **Implemented TUI mode.**

  By changing ``mode: "NORMAL"`` to ``mode: "RICH"`` in ``conf/config.yaml``, you can enable it.

  ![demo](assets/demo/demo.gif)

  [!NOTE]
    - The image is being simulated on a macOS environment.
    - The image was created using [charmbracelet/vhs](https://github.com/charmbracelet/vhs). thx!
