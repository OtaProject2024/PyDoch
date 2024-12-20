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
        self.overview = None
        self.__mode()
        self.__conf()
        self.__log()

    # Mode selection from command line arguments
    def __mode(self):
        mode_list = ["PRODUCT", "TEST", "DEMO"]
        args = sys.argv
        if len(args) > 1:
            mode_arg = args[1].upper()
            if mode_arg in mode_list:
                self.mode = mode_arg
            else:
                self.mode = mode_list[1]
        else:
            self.mode = mode_list[1]

    # Loading config file
    def __conf(self, path=os.path.join(os.path.dirname(os.path.dirname(__file__)), "conf", "config.yaml")):
        try:
            if not os.path.exists(path):
                raise FileNotFoundError(f"Config file not found: {path}")
            with open(path, "r") as file:
                self.config = yaml.safe_load(file)
        except FileNotFoundError as fnf_error:
            # print(fnf_error)
            with open(
                    os.path.join(os.path.dirname(os.path.dirname(__file__)), "conf", "default_config.yaml"),
                    "r"
            ) as file:
                self.config = yaml.safe_load(file)

    # Logger setup
    def __log(self):
        self.logger = logging.getLogger("Murdoch")
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter(f"[%(levelname).4s] %(name)s({self.mode[:4]}):%(asctime)s - %(message)s")

        if self.mode != "DEMO" and self.config["operation"]["mode"].upper() != "RICH":
            stream_handler = logging.StreamHandler(sys.stdout)
            stream_handler.setFormatter(formatter)
            self.logger.addHandler(stream_handler)

        name = "murdoch_" + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + ".log"
        file_handler = logging.FileHandler(os.path.join(os.path.dirname(os.path.dirname(__file__)), "log", name))
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    # Outputs system information
    def __info(self):
        print(
            f"- PyDoch ({self.mode} MODE) -\n"
            "Program for controlling Murdoch.\n\n"
            "SYSTEM INFORMATION\n"
            f"system: {platform.system()}\n"
            f"release: {platform.release()}\n"
            f"version: {platform.version()}\n"
            f"machine: {platform.machine()}\n"
            f"architecture: {platform.architecture()[0]}\n"
            f"python: {sys.version}\n\n"
            "CONFIG\n"
            f"{yaml.dump(self.config, sort_keys=False, allow_unicode=True)}\n"
        )

    # Main thread calls
    def run(self):
        if self.mode == "DEMO":
            self.overview = mode.Overview(self.mode, self.config)
            mode.Demo(self.config, self.logger, self.overview).run()
        else:
            if self.config["operation"]["mode"].upper() == "RICH":
                self.overview = mode.Overview(self.mode, self.config)
            else:
                self.__info()

            if self.mode == "TEST":
                mode.Test(self.config, self.logger, self.overview).run()
            elif self.mode == "PRODUCT":
                mode.Product(self.config, self.logger, self.overview).run()
        sys.exit(0)


if __name__ == '__main__':
    Boot().run()
