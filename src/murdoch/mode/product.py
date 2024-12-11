import signal
import threading


# Product mode
class Product:
    def __init__(self, conf, log, overview):
        from .. import component
        self.component = component

        self.config = conf
        self.logger = log
        self.threads = []
        self.__sigs()
        self.stop_event = threading.Event()

        self.overview = overview
        self.lock = threading.Lock()
        self.behavior = False
        self.method = 1
        # self.contact = False
        # self.stationary = False

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
            self.overview.run(self.threads, self.behavior, self.method)

    # Button thread calls
    def __bt(self):
        b = self.component.Button(
            self.config["components"]["button"]["channel"],
            self.config["components"]["button"]["delay"],
            self.config["components"]["button"]["default"]
        )
        while not self.stop_event.is_set():
            previous_behavior = self.behavior
            with self.lock:
                self.behavior = b.run()
            if self.behavior != previous_behavior:
                if self.behavior:
                    self.logger.info("Button: ON")
                else:
                    self.logger.info("Button: OFF")
        b.stop()

    # Sensor thread calls
    # def __bo(self):
    #     o = self.component.BNO055Sensor(
    #         self.config["components"]["bno055_sensor"]["frequency"],
    #         self.config["components"]["bno055_sensor"]["interval"],
    #         self.config["components"]["bno055_sensor"]["magnetic_threshold"],
    #         self.config["components"]["bno055_sensor"]["acceleration_threshold"]
    #     )
    #     while not self.stop_event.is_set():
    #         with self.lock:
    #             self.contact, self.stationary, mag_magnitude, acc_magnitude = o.run()
    #         self.logger.debug(f"magnet_magnitude: {mag_magnitude}")
    #         self.logger.debug(f"acceleration_magnitude: {acc_magnitude}")

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
        while not self.stop_event.is_set():
            if not self.behavior: continue
            d.run(self.method)
        d.stop()

    # SVMotor thread calls
    def __sv(self):
        s = self.component.SVMotor(
            self.config["components"]["sv_motor"]["channel"],
            self.config["components"]["sv_motor"]["frequency"],
            self.config["components"]["sv_motor"]["angle"]
        )
        s.start()
        while not self.stop_event.is_set():
            if not self.behavior: continue
            s.run(self.method)
        s.stop()

    # Sound thread calls
    # def __so(self):
    #     u = self.component.Sound(
    #         self.config["components"]["sound"]["file"],
    #         self.config["components"]["sound"]["volume"],
    #     )
    #     while not self.stop_event.is_set():
    #         u.run(self.contact)

    # Main thread calls
    def run(self):
        self.logger.info("Start processing")
        try:
            self.threads = [
                threading.Thread(target=self.__bt, daemon=True, name="button control"),
                threading.Thread(target=self.__dc, daemon=True, name="dc_motor control"),
                threading.Thread(target=self.__sv, daemon=True, name="sv_motor control"),
            ]
            if self.overview is not None:
                self.threads.append(threading.Thread(target=self.__ov, daemon=True, name="overview control"))

            for thread in self.threads:
                thread.start()
                self.logger.debug(f"Start thread: {thread.name}")

            for thread in self.threads:
                thread.join()
                self.logger.debug(f"Stop thread: {thread.name}")
        except Exception as e:
            self.logger.error(e)
        finally:
            self.logger.info("Stop processing")
