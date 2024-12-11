import signal
import threading


# Test mode
class Test:
    def __init__(self, conf, log, overview):
        from .. import component
        self.component = component

        self.config = conf
        self.logger = log
        self.threads = []
        self.__sigs()
        self.stop_event = threading.Event()

        self.overview = overview
        self.behavior = True
        self.times = 0

    # Stop signal control
    def __sigs(self):
        signal.signal(signal.SIGINT, self.__stop)
        signal.signal(signal.SIGTERM, self.__stop)

    # Stop processing after receiving signal
    def __stop(self, signum, frame):
        if signum == signal.SIGINT:
            self.logger.info("Received signal: SIGINT")
        elif signum == signal.SIGTERM:
            self.logger.info("Received signal: SIGTERM")
        self.stop_event.set()

    # Overview thread calls
    def __ov(self):
        while not self.stop_event.is_set():
            self.overview.run(
                self.threads,
                self.behavior,
                self.config["test"]["method"],
                self.times,
                self.config["test"]["times"]
            )

    # Button thread calls
    def __bt(self):
        b = self.component.Button(
            self.config["components"]["button"]["channel"],
            self.config["components"]["button"]["delay"],
            self.config["components"]["button"]["default"]
        )
        for i in range(self.config["test"]["times"]):
            if self.stop_event.is_set(): break
            self.times += 1
            while not self.stop_event.is_set():
                previous_behavior = self.behavior
                self.behavior = b.run()
                if self.behavior != previous_behavior:
                    if self.behavior:
                        self.logger.info("Button: ON")
                    else:
                        self.logger.info("Button: OFF")
                    break
        b.stop()

    # Sensor thread calls
    # def __bo(self):
    #     o = self.component.BNO055Sensor(
    #         self.config["components"]["bno055_sensor"]["frequency"],
    #         self.config["components"]["bno055_sensor"]["interval"],
    #         self.config["components"]["bno055_sensor"]["magnetic_threshold"],
    #         self.config["components"]["bno055_sensor"]["acceleration_threshold"]
    #     )
    #     for i in range(self.config["test"]["times"]):
    #         if self.stop_event.is_set(): break
    #         contact, stationary, mag_magnitude, acc_magnitude = o.run()
    #         self.logger.debug(f"Sensor state: {contact}, {stationary}")
    #         self.logger.debug(f"magnet_magnitude: {mag_magnitude}")
    #         self.logger.debug(f"acceleration_magnitude: {acc_magnitude}")
    #         time.sleep(self.config["test"]["delay"])

    # DCMotor thread calls
    def __dc(self):
        d = self.component.DCMotor(
            self.config["components"]["dc_motor"]["pwm_channel"],
            self.config["components"]["dc_motor"]["in1_channel"],
            self.config["components"]["dc_motor"]["in2_channel"],
            self.config["components"]["dc_motor"]["power"],
            self.config["components"]["dc_motor"]["save_power"],
            self.config["components"]["dc_motor"]["direction"]
        )
        d.start()
        self.logger.debug(f'Action method: {self.config["test"]["method"]}')
        for i in range(self.config["test"]["times"]):
            if self.stop_event.is_set(): break
            self.times += 1
            d.run(self.config["test"]["method"])
        self.behavior = False
        d.stop()

    # SVMotor thread calls
    def __sv(self):
        s = self.component.SVMotor(
            self.config["components"]["sv_motor"]["channel"],
            self.config["components"]["sv_motor"]["frequency"],
            self.config["components"]["sv_motor"]["angle"]
        )
        s.start()
        self.logger.debug(f'Action method: {self.config["test"]["method"]}')
        for i in range(self.config["test"]["times"]):
            if self.stop_event.is_set(): break
            self.times += 1
            s.run(self.config["test"]["method"])
        self.behavior = False
        s.stop()

    # Sound thread calls
    # def __so(self):
    #     u = self.component.Sound(
    #         self.config["components"]["sound"]["file"],
    #         self.config["components"]["sound"]["volume"],
    #     )
    #     for i in range(self.config["test"]["times"]):
    #         if self.stop_event.is_set(): break
    #         self.logger.debug("Sound state: play")
    #         u.run(True)
    #         self.logger.debug("Sound state: stop")
    #         u.run(False)
    #         time.sleep(self.config["test"]["delay"])

    # Main thread calls
    def run(self):
        self.logger.info("Start testing")
        try:
            self.threads = [
                threading.Thread(target=self.__bt, daemon=True, name="button control"),
                threading.Thread(target=self.__dc, daemon=True, name="dc_motor control"),
                threading.Thread(target=self.__sv, daemon=True, name="sv_motor control")
            ]
            if self.overview is not None:
                self.threads.append(threading.Thread(target=self.__ov, daemon=True, name="overview control"))

            n = 0
            match self.config["test"]["target"].upper():
                case "BUTTON":
                    n = 0
                case "DCMOTOR":
                    n = 1
                case "SVMOTOR":
                    n = 2

            if self.overview is not None:
                self.threads[3].start()
                self.logger.debug(f"Start thread: {self.threads[0].name}")
            self.threads[n].start()
            self.logger.debug(f"Start thread: {self.threads[n].name}")

            self.threads[n].join()
            self.logger.debug(f"Stop thread: {self.threads[n].name}")
            if self.overview is not None:
                self.threads[3].join()
                self.logger.debug(f"Stop thread: {self.threads[0].name}")
        except Exception as e:
            self.logger.error(e)
        finally:
            self.logger.info("Stop testing")
