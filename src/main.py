import datetime
import logging
import os
import platform
import sys

import yaml

from murdoch import mode


class Boot:
    def __init__(self):
        self.mode = None
        self.config = None
        self.logger = None
        self.__mode()
        self.__conf()
        self.__log()

    # Mode selection from command line arguments
    def __mode(self):
        mode_list = ["PRODUCT", "TEST"]
        args = sys.argv
        if len(args) > 1:
            mode_arg = args[1].upper()
            if mode_arg in mode_list:
                self.mode = mode_arg
            else:
                print(f"Warning: '{args[1]}' is not a valid mode. Defaulting to TEST.")
                self.mode = mode_list[1]
        else:
            self.mode = mode_list[0]

    # Loading config file
    def __conf(self, path=os.path.join("..", "conf", "config.yaml")):
        try:
            if not os.path.exists(path):
                raise FileNotFoundError(f"Config file not found: {path}")
            with open(path, 'r') as file:
                self.config = yaml.safe_load(file)
        except FileNotFoundError as fnf_error:
            print(fnf_error)
            with open(os.path.join("..", "conf", "default_config.yaml"), 'r') as file:
                self.config = yaml.safe_load(file)

    # Logger setup
    def __log(self):
        self.logger = logging.getLogger("Murdoch")
        self.logger.setLevel(logging.DEBUG)
        formatter = None
        if self.mode == "PRODUCT":
            formatter = logging.Formatter("[%(levelname).4s] %(name)s:%(asctime)s - %(message)s")
        elif self.mode == "TEST":
            formatter = logging.Formatter("[%(levelname).4s] %(name)s(TEST):%(asctime)s - %(message)s")

        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(formatter)
        self.logger.addHandler(stream_handler)

        name = "murdoch_" + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + ".log"
        file_handler = logging.FileHandler(os.path.join("..", "log", name))
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    # Outputs system information
    def __info(self):
        print(
            f"- PyDoch ({self.mode} MODE) -\n"
            "Program for controlling Murdoch.\n\n"
            "SYSTEM INFORMATION\n"
            f"system: {platform.system()}\n"
            f"node name: {platform.node()}\n"
            f"release: {platform.release()}\n"
            f"version: {platform.version()}\n"
            f"machine: {platform.machine()}\n"
            f"architecture: {platform.architecture()[0]}\n"
            f"python: {sys.version}\n\n"
            "CONFIG\n" +
            yaml.dump(self.config, sort_keys=False, allow_unicode=True) +
            "\n"
        )

    # Main thread calls
    def run(self):
        self.__info()
        if self.mode == "PRODUCT":
            mode.Product(self.config, self.logger).run()
        elif self.mode == "TEST":
            mode.Test(self.config, self.logger).run()


if __name__ == '__main__':
    Boot().run()
