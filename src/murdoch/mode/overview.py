import platform
import sys
import time

import yaml


# Overview output
class Overview:
    def __init__(self, conf, mode):
        self.original_config = conf
        self.config = self.filter_config(conf)
        self.mode = mode
        self.cnt = 0
        title = f"- PyDoch (https://github.com/OtaProject2024/PyDoch) - ".center(78)
        machine = f"machine: {platform.machine()}({platform.architecture()[0]})".ljust(36)
        system = f"system: {platform.system()} {platform.release()}".ljust(36)
        python = f"python: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}".ljust(36)

        self.left = [
            "\n",
            f"{title}\n",
            " ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓",
            " ┃         SYSTEM  INFORMATION         ┃",
            " ┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫",
            f" ┃ {machine}┃",
            f" ┃ {system}┃",
            f" ┃ {python}┃",
            " ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛",
            " ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓",
            " ┃            CONFIGURATION            ┃",
            " ┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫",
        ]
        for line in yaml.dump(self.config, sort_keys=False, allow_unicode=True).splitlines():
            self.left.append(f" ┃ {line.ljust(36)}┃")
        self.left.append(" ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")

    # Filter out unnecessary configuration items
    def filter_config(self, config, exclude_keys=None):
        if exclude_keys is None:
            exclude_keys = [
                "operation",
                "times",
                "delay",
                "state",
                "button",
                "bno055_sensor",
                "sound"
            ]

        if isinstance(config, dict):
            return {
                k: self.filter_config(v, exclude_keys)
                for k, v in config.items()
                if k not in exclude_keys
            }
        elif isinstance(config, list):
            return [self.filter_config(v, exclude_keys) for v in config]
        else:
            return config

    # Update overview
    def addition(self, threads, state, action_state, contact="invalid", stationary="invalid", times=0, st_times=0):
        current_time = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
        active = f"active: {state}".ljust(36)
        if action_state == 0:
            action_state = "stop"
        elif action_state == 1:
            action_state = "forward"
        elif action_state == 2:
            action_state = "left"
        elif action_state == 3:
            action_state = "right"

        action = f"action state: {action_state}".ljust(36)
        contact = f"contact: {str(contact)}".ljust(36)
        stationary = f"stationary: {str(stationary)}".ljust(36)

        if self.mode == "TEST":
            times = f"times: {times}/{st_times}".ljust(36)
        else:
            times = f"times: invalid".ljust(36)

        right = [
            " ┏━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┓\n",
            f" ┃ mode: {self.mode.ljust(7)} ┃ {current_time.ljust(20)}┃\n",
            " ┗━━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━━━━━━━┛\n",
            " ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓\n",
            " ┃             ROBOT STATE             ┃\n",
            " ┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫\n",
            f" ┃ {active}┃\n",
            f" ┃ {action}┃\n",
            f" ┃ {contact}┃\n",
            f" ┃ {stationary}┃\n",
            " ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛\n",
            " ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓\n",
            " ┃            TEST PROGRESS            ┃\n",
            " ┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫\n",
            f" ┃ {times}┃\n",
            " ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛\n",
            " ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓\n",
            " ┃               THREADS               ┃\n",
            " ┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫\n",
        ]

        cnt = 1
        for thread in threads:
            cc = "{0}: ".format(str(cnt).zfill(2))
            right.append(f" ┃ {(cc + thread.name).ljust(36)}┃\n")
            cnt += 1
        right.append(" ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛\n")

        right.append(" ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓\n")
        right.append(f" ┃{'><>'.rjust(self.cnt).ljust(37)}┃\n", )
        right.append(" ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛\n")
        self.cnt = (self.cnt + 1) % 38

        output = self.left[:]
        for i in range(2, len(self.left)):
            if i < len(right) + 2:
                output[i] += right[i - 2]
            else:
                output[i] += "\n"

        print(*output, sep="")
        print(f"\033[{len(output) + 1}A", end="")
        time.sleep(0.5)
