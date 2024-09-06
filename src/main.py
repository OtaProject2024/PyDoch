import logging
import os
import platform
import random
import signal
import sys
import threading
import time

import yaml

import murdoch


class Main:
    def __init__(self):
        self.logger = None
        self.config = None
        self.__sigs()
        self.__conf()
        self.__log()

        self.button_state = False
        self.contact = False
        self.stationary = False
        self.action_state = 0

    def __conf(self, path=os.path.join("..", "conf", "config.yaml")):
        with open(path, 'r') as file:
            self.config = yaml.safe_load(file)

    def __log(self):
        self.logger = logging.getLogger("Murdoch")
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter("[%(levelname).4s] %(name)s:%(asctime)s - %(message)s")

        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(formatter)
        self.logger.addHandler(stream_handler)

        file_handler = logging.FileHandler("murdoch.log")
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def __sigs(self):
        signal.signal(signal.SIGINT, self.stop)
        signal.signal(signal.SIGTERM, self.stop)
        signal.signal(signal.SIGALRM, self.stop)

    def stop(self, sig, frame):
        if sig == signal.SIGINT:
            self.logger.info("Received signal: SIGINT")
        elif sig == signal.SIGTERM:
            self.logger.info("Received signal: SIGTERM")
        elif sig == signal.SIGALRM:
            self.logger.info("Received signal: SIGALRM")

        if self.button_state:
            self.button_state = False
        else:
            self.button_state = True
            time.sleep(0.1)
            self.button_state = False
        time.sleep(0.1)
        self.logger.info("Stop processing")
        sys.exit()

    def __info(self):
        print("- PyDoch -")
        print("Program for controlling \"Murdoch\".")
        print()

        print("SYSTEM INFORMATION")
        print(f"system: {platform.system()}")
        print(f"node name: {platform.node()}")
        print(f"release: {platform.release()}")
        print(f"version: {platform.version()}")
        print(f"machine: {platform.machine()}")
        print(f"architecture: {platform.architecture()}")
        print(f"python: {sys.version}")
        print()

        print("CONFIG")
        print(yaml.dump(self.config, sort_keys=False, allow_unicode=True))
        print()

    def __bt(self):
        b = murdoch.Button(
            self.config["components"]["button"]["channel"],
            self.config["components"]["button"]["delay"],
        )
        for p in ("ON", "OFF"):
            self.button_state = b.run()
            self.logger.info(f"Button state: {p}")
        b.stop()

    def __ac(self):
        delay = self.config["components"]["action"]["normal_delay"]
        irq_delay = self.config["components"]["action"]["sensor_interrupt_delay"]
        while self.button_state:
            if self.contact:
                self.action_state = 1
                self.logger.info("Sensor state: PULLED")
                time.sleep(delay)
            else:
                if self.stationary:
                    self.logger.info("Sensor state: STATIONARY")
                    self.action_state = random.randint(2, 3)
                    self.logger.debug(f"state: {self.action_state}")
                    time.sleep(irq_delay)
                else:
                    self.action_state = random.randint(0, 3)
                    self.logger.debug(f"state: {self.action_state}")
                    time.sleep(delay)

    def __bo(self):
        o = murdoch.BNO055Sensor(
            self.config["components"]["bno055_sensor"]["frequency"],
            self.config["components"]["bno055_sensor"]["interval"],
            self.config["components"]["bno055_sensor"]["magnetic_threshold"],
            self.config["components"]["bno055_sensor"]["acceleration_threshold"]
        )
        while self.button_state:
            self.contact, self.stationary, mag_magnitude, acc_magnitude = o.run()
            self.logger.debug(f"magnet_magnitude: {mag_magnitude}")
            self.logger.debug(f"acceleration_magnitude: {acc_magnitude}")

    def __dc(self):
        d = murdoch.DCMotor(
            self.config["components"]["dc_motor"]["ref_channel"],
            self.config["components"]["dc_motor"]["in1_channel"],
            self.config["components"]["dc_motor"]["in2_channel"],
            self.config["components"]["dc_motor"]["power"],
            self.config["components"]["dc_motor"]["save_power"],
        )
        d.start()
        while self.button_state:
            d.run(self.action_state)
        d.stop()

    def __sv(self):
        s = murdoch.SVMotor(
            self.config["components"]["sv_motor"]["channel"],
            self.config["components"]["sv_motor"]["frequency"],
            self.config["components"]["sv_motor"]["angle"]
        )
        s.start()
        while self.button_state:
            s.run(self.action_state)
        s.stop()

    def run(self):
        self.__info()
        self.logger.info("Start processing")
        try:
            while True:
                threads = [
                    threading.Thread(target=self.__bt, daemon=True, name="Button control"),
                    threading.Thread(target=self.__ac, daemon=True, name="Action control"),
                    threading.Thread(target=self.__bo, daemon=True, name="Sensor control"),
                    threading.Thread(target=self.__dc, daemon=True, name="DCMotor control"),
                    threading.Thread(target=self.__sv, daemon=True, name="SVMotor control")
                ]

                threads[0].start()
                self.logger.debug(f"Start thread: {threads[0].name}")
                while not self.button_state:
                    pass

                for thread in threads[1:]:
                    thread.start()
                    self.logger.debug(f"Start thread: {thread.name}")

                for thread in threads:
                    thread.join()
                    self.logger.debug(f"Stop thread: {thread.name}")
        except Exception as e:
            self.logger.error(e)
        finally:
            signal.alarm(0)


if __name__ == '__main__':
    Main().run()
