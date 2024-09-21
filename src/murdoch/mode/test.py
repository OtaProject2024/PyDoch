import threading
import time

from .. import component


# Test mode
class Test:
    def __init__(self, conf, log):
        self.config = conf
        self.logger = log

        self.methods = {
            "BUTTON": self.__bt(),
            "SENSOR": self.__bo(),
            "DCMOTOR": self.__dc(),
            "SVMOTOR": self.__sv(),
            "SOUND": self.__so(),
        }

    # Button thread calls
    def __bt(self):
        b = component.Button(
            self.config["components"]["button"]["channel"],
            self.config["components"]["button"]["delay"],
        )
        for i in range(self.config["test"]["target"]["times"]):
            button_state = b.run()
            self.logger.debug(f"Button state: {button_state}")
        b.stop()

    # Sensor thread calls
    def __bo(self):
        o = component.BNO055Sensor(
            self.config["components"]["bno055_sensor"]["frequency"],
            self.config["components"]["bno055_sensor"]["interval"],
            self.config["components"]["bno055_sensor"]["magnetic_threshold"],
            self.config["components"]["bno055_sensor"]["acceleration_threshold"]
        )
        for i in range(self.config["test"]["target"]["times"]):
            contact, stationary, mag_magnitude, acc_magnitude = o.run()
            self.logger.debug(f"Sensor state: {contact}, {stationary}")
            self.logger.debug(f"magnet_magnitude: {mag_magnitude}")
            self.logger.debug(f"acceleration_magnitude: {acc_magnitude}")
            time.sleep(self.config["test"]["target"]["delay"])

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
        self.logger.debug(f'Action state: {self.config["test"]["target"]["state"]}')
        for i in range(self.config["test"]["target"]["times"]):
            d.run(self.config["test"]["target"]["state"])
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
            s.run(self.config["test"]["target"]["state"])
        s.stop()

    # Sound thread calls
    def __so(self):
        u = component.Sound(
            self.config["components"]["sound"]["file"],
            self.config["components"]["sound"]["volume"],
        )
        for i in range(self.config["test"]["target"]["times"]):
            self.logger.debug("Sound state: play")
            u.run(True)
            self.logger.debug("Sound state: stop")
            u.run(False)
            time.sleep(self.config["test"]["target"]["delay"])

    # Main thread calls
    def run(self):
        self.logger.info("Start testing")
        method = self.methods.get(self.config["test"]["target"]["name"].upper, self.__dc())
        key = [k for k, v in self.methods.items() if v == method]
        t = threading.Thread(target=method, daemon=True)
        t.start()
        self.logger.debug(f"Start thread: {key}")
        t.join()
        self.logger.debug(f"Start thread: {key}")
