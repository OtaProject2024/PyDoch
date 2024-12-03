import signal
import sys
import threading
import time

from .. import component


# Test mode
class Test:
    def __init__(self, conf, log, overview):
        self.config = conf
        self.logger = log
        self.threads = []
        self.overview = overview

        self.state = True
        self.times = 0

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

        self.logger.info("Stop testing")
        sys.exit()

    # Overview thread calls
    def __ov(self):
        while True:
            self.overview.addition(
                threads=self.threads,
                state=self.state,
                action_state=self.config["test"]["target"]["state"],
                times=self.times,
                st_times=self.config["test"]["target"]["times"]
            )

    # Sensor thread calls
    # def __bo(self):
    #     o = component.BNO055Sensor(
    #         self.config["components"]["bno055_sensor"]["frequency"],
    #         self.config["components"]["bno055_sensor"]["interval"],
    #         self.config["components"]["bno055_sensor"]["magnetic_threshold"],
    #         self.config["components"]["bno055_sensor"]["acceleration_threshold"]
    #     )
    #     for i in range(self.config["test"]["target"]["times"]):
    #         contact, stationary, mag_magnitude, acc_magnitude = o.run()
    #         self.logger.debug(f"Sensor state: {contact}, {stationary}")
    #         self.logger.debug(f"magnet_magnitude: {mag_magnitude}")
    #         self.logger.debug(f"acceleration_magnitude: {acc_magnitude}")
    #         time.sleep(self.config["test"]["target"]["delay"])

    # DCMotor thread calls
    def __dc(self):
        d = component.DCMotor(
            self.config["components"]["dc_motor"]["ref_channel"],
            self.config["components"]["dc_motor"]["in1_channel"],
            self.config["components"]["dc_motor"]["in2_channel"],
            self.config["components"]["dc_motor"]["power"],
            self.config["components"]["dc_motor"]["save_power"],
            self.config["components"]["dc_motor"]["ward"]
        )
        d.start()
        self.logger.debug(f'Action state: {self.config["test"]["target"]["state"]}')
        for i in range(self.config["test"]["target"]["times"]):
            self.times += 1
            d.run(self.config["test"]["target"]["state"])
        self.state = False
        d.stop()

    # SVMotor thread calls
    def __sv(self):
        s = component.SVMotor(
            self.config["components"]["sv_motor"]["channel"],
            self.config["components"]["sv_motor"]["frequency"],
            self.config["components"]["sv_motor"]["angle"]
        )
        s.start()
        self.logger.debug(f'Action state: {self.config["test"]["target"]["state"]}')
        for i in range(self.config["test"]["target"]["times"]):
            time.sleep(1)
            self.times += 1
            s.run(self.config["test"]["target"]["state"])
        self.state = False
        s.stop()

    # Sound thread calls
    # def __so(self):
    #     u = component.Sound(
    #         self.config["components"]["sound"]["file"],
    #         self.config["components"]["sound"]["volume"],
    #     )
    #     for i in range(self.config["test"]["target"]["times"]):
    #         self.logger.debug("Sound state: play")
    #         u.run(True)
    #         self.logger.debug("Sound state: stop")
    #         u.run(False)
    #         time.sleep(self.config["test"]["target"]["delay"])

    # Main thread calls
    def run(self):
        self.logger.info("Start testing")
        try:
            self.threads = [
                threading.Thread(target=self.__dc, daemon=True, name="DCMotor control"),
                threading.Thread(target=self.__sv, daemon=True, name="SVMotor control")
            ]
            if self.overview is not None:
                self.threads.append(threading.Thread(target=self.__ov, daemon=True, name="Overview control"))
            # threads = [
            #     threading.Thread(target=self.__bo, daemon=True, name="Sensor control"),
            #     threading.Thread(target=self.__dc, daemon=True, name="DCMotor control"),
            #     threading.Thread(target=self.__sv, daemon=True, name="SVMotor control"),
            #     threading.Thread(target=self.__so, daemon=True, name="Sound control")
            # ]

            n = 0
            match self.config["test"]["target"]["name"].upper():
                case "DCMOTOR":
                    n = 0
                case "SVMOTOR":
                    n = 1
            # n = 2
            # match self.config["test"]["target"]["name"].upper():
            #     case "SENSOR":
            #         n = 0
            #     case "DCMOTOR":
            #         n = 1
            #     case "SVMOTOR":
            #         n = 2
            #     case "SOUND":
            #         n = 3

            if self.overview is not None:
                self.threads[2].start()
                self.logger.debug(f"Start thread: {self.threads[0].name}")
            self.threads[n].start()
            self.logger.debug(f"Start thread: {self.threads[n].name}")

            self.threads[n].join()
            self.logger.debug(f"Stop thread: {self.threads[n].name}")
            if self.overview is not None:
                self.threads[2].join()
                self.logger.debug(f"Stop thread: {self.threads[0].name}")
        except Exception as e:
            self.logger.error(e)
        finally:
            signal.alarm(0)
