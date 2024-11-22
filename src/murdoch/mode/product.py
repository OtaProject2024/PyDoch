import signal
import sys
import threading
import time

from .. import component


# Product mode
class Product:
    def __init__(self, conf, log):
        self.config = conf
        self.logger = log
        self.__sigs()

        self.lock = threading.Lock()
        self.state = True
        self.contact = False
        self.stationary = False
        self.action_state = 1

    # Stop signal control
    def __sigs(self):
        signal.signal(signal.SIGINT, self.stop)
        signal.signal(signal.SIGTERM, self.stop)
        signal.signal(signal.SIGALRM, self.stop)

    # Stop processing after receiving signal
    def stop(self, sig, frame):
        if sig == signal.SIGINT:
            self.logger.info("Received signal: SIGINT")
        elif sig == signal.SIGTERM:
            self.logger.info("Received signal: SIGTERM")
        elif sig == signal.SIGALRM:
            self.logger.info("Received signal: SIGALRM")

        with self.lock:
            if self.state:
                self.state = False
            else:
                self.state = True
                time.sleep(0.1)
                self.state = False
        time.sleep(0.1)
        self.logger.info("Stop processing")
        sys.exit()

    # Action thread calls
    # def __ac(self):
    #     delay = self.config["operation"]["action"]["normal_delay"]
    #     irq_delay = self.config["operation"]["action"]["sensor_interrupt_delay"]
    #     while self.state:
    #         if self.contact:
    #             with self.lock:
    #                 self.action_state = 1
    #             self.logger.info("Sensor state: PULLED")
    #             time.sleep(delay)
    #         else:
    #             if self.stationary:
    #                 self.logger.info("Sensor state: STATIONARY")
    #                 with self.lock:
    #                     self.action_state = 1
    #                     # self.action_state = random.randint(2, 3)
    #                 # self.logger.debug(f"action state: {self.action_state}")
    #                 time.sleep(irq_delay)
    #             else:
    #                 with self.lock:
    #                     self.action_state = 1
    #                     # self.action_state = random.randint(0, 3)
    #                 # self.logger.debug(f"action state: {self.action_state}")
    #                 time.sleep(delay)

    # Sensor thread calls
    # def __bo(self):
    #     o = component.BNO055Sensor(
    #         self.config["components"]["bno055_sensor"]["frequency"],
    #         self.config["components"]["bno055_sensor"]["interval"],
    #         self.config["components"]["bno055_sensor"]["magnetic_threshold"],
    #         self.config["components"]["bno055_sensor"]["acceleration_threshold"]
    #     )
    #     while self.state:
    #         with self.lock:
    #             self.contact, self.stationary, mag_magnitude, acc_magnitude = o.run()
    #         self.logger.debug(f"magnet_magnitude: {mag_magnitude}")
    #         self.logger.debug(f"acceleration_magnitude: {acc_magnitude}")

    # DCMotor thread calls
    def __dc(self):
        d = component.DCMotor(
            self.config["components"]["dc_motor"]["ref_channel"],
            self.config["components"]["dc_motor"]["in1_channel"],
            self.config["components"]["dc_motor"]["in2_channel"],
            self.config["components"]["dc_motor"]["power"],
            self.config["components"]["dc_motor"]["save_power"],
        )
        d.start()
        while self.state:
            d.run(self.action_state)
        d.stop()

    # SVMotor thread calls
    def __sv(self):
        s = component.SVMotor(
            self.config["components"]["sv_motor"]["channel"],
            self.config["components"]["sv_motor"]["frequency"],
            self.config["components"]["sv_motor"]["angle"]
        )
        s.start()
        while self.state:
            s.run(self.action_state)
        s.stop()

    # Sound thread calls
    # def __so(self):
    #     u = component.Sound(
    #         self.config["components"]["sound"]["file"],
    #         self.config["components"]["sound"]["volume"],
    #     )
    #     while self.state:
    #         u.run(self.contact)

    # Main thread calls
    def run(self):
        self.logger.info("Start processing")
        try:
            while True:
                threads = [
                    threading.Thread(target=self.__dc, daemon=True, name="DCMotor control"),
                    threading.Thread(target=self.__sv, daemon=True, name="SVMotor control"),
                ]
                # threads = [
                #     threading.Thread(target=self.__ac, daemon=True, name="Action control"),
                #     threading.Thread(target=self.__bo, daemon=True, name="Sensor control"),
                #     threading.Thread(target=self.__dc, daemon=True, name="DCMotor control"),
                #     threading.Thread(target=self.__sv, daemon=True, name="SVMotor control"),
                #     threading.Thread(target=self.__so, daemon=True, name="Sound control"),
                # ]

                for thread in threads:
                    thread.start()
                    self.logger.debug(f"Start thread: {thread.name}")

                for thread in threads:
                    thread.join()
                    self.logger.debug(f"Stop thread: {thread.name}")
        except Exception as e:
            self.logger.error(e)
        finally:
            signal.alarm(0)
