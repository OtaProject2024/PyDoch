import platform
import sys
import time

import yaml


# Overview output
class Overview:
    def __init__(self, conf, mode):
        self.config = self.filter_config(conf)
        self.mode = mode

        self.left = []
        self.start_time = time.time()
        self.cnt = 3
        self.direction = 1

        self.left_side()

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
                "sound",
                "save_power",
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

    # Create left side
    def left_side(self):
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
            if ":" in line:
                key, value = line.split(":", 1)
                line = f"{key}:\033[33m{value}\033[0m"
            self.left.append(f" ┃ {line.ljust(45)}┃")
        self.left.append(" ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")

    # Update overview
    def addition(self, threads, state, action_state, times=0, st_times=0):
        mode = f"\033[34m{self.mode.ljust(7)}\033[0m".ljust(15)

        current_time = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
        uptime = time.time() - self.start_time
        hours, rem = divmod(uptime, 3600)
        minutes, seconds = divmod(rem, 60)
        uptime = f"uptime: {int(hours):02}:{int(minutes):02}:{int(seconds):02}".ljust(36)

        behavior = f"behavior: \033[31m{state}\033[0m".ljust(45)
        if state:
            behavior = f"behavior: \033[32m{state}\033[0m".ljust(45)

        if action_state == 0:
            action_state = "\033[31m" + "stop" + "\033[0m"
        elif action_state == 1:
            action_state = "\033[32m" + "forward" + "\033[0m"
        elif action_state == 2:
            action_state = "\033[33m" + "left" + "\033[0m"
        elif action_state == 3:
            action_state = "\033[34mm" + "right" + "\033[0m"
        method = f"method: {action_state}".ljust(45)

        if self.mode == "TEST":
            div = (str(times).zfill(2) + "/" + str(st_times)).rjust(5)
            per = f"{round(times / st_times * 100, 2):.02f}".rjust(6)
            times = f"times: {div}  [{per}%]".ljust(36)
        else:
            times = ("times: " + "\033[31m" + "invalid" + "\033[0m").ljust(45)

        right = [
            " ┏━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┓\n",
            f" ┃ MODE: {mode} ┃ {current_time.ljust(20)}┃\n",
            " ┗━━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━━━━━━━┛\n",
            " ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓\n",
            " ┃             ROBOT STATE             ┃\n",
            " ┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫\n",
            f" ┃ {uptime}┃\n",
            f" ┃ {behavior}┃\n",
            f" ┃ {method}┃\n",
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

        no = 1
        for thread in threads:
            c = "{0}: ".format(str(no).zfill(2))
            t = "\033[36m" + "deactivate   " + "\033[0m"
            if thread.is_alive():
                t = "\033[32m" + "activate     " + "\033[0m"
            right.append(f" ┃ {c + t + thread.name.ljust(19)}┃\n")
            no += 1
        right.append(" ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛\n")

        self.cnt += self.direction
        fish = "><>" if self.direction == 1 else "<><"
        if self.cnt == 37:
            self.direction = -1
        elif self.cnt == 3:
            self.direction = 1
        right.append(" ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓\n")
        right.append(f" ┃{fish.rjust(self.cnt).ljust(37)}┃\n")
        right.append(" ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")

        output = self.left[:]
        for i in range(2, len(self.left)):
            if i < len(right) + 2:
                output[i] += right[i - 2]
            else:
                output[i] += "\n"

        print(*output, sep="")
        print(f"\033[{len(output)}A", end="")
        time.sleep(0.5)
