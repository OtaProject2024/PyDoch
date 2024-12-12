import random
import signal
import threading
import time


# Demo mode
class Demo:
    def __init__(self, conf, log, overview):
        self.config = conf
        self.logger = log
        self.threads = []
        self.__sigs()
        self.stop_event = threading.Event()

        self.overview = overview
        self.behavior = True
        self.wait = False
        self.method = 1
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
                self.method,
                self.times,
                self.config["test"]["times"],
                self.wait,
                self.wait
            )

    # Demo thread calls
    def __de(self):
        self.logger.debug(f'Action method: {self.config["test"]["method"]}')
        while not self.stop_event.is_set():
            if not self.wait:
                self.times += 1
            if self.times % 3 == 0:
                self.behavior = random.choice([True, False])
                self.method = random.randint(0, 3)
                self.wait = random.choice([True, False, False])
                if self.wait:
                    time.sleep(2)
            if self.times == self.config["test"]["times"]:
                break
            time.sleep(1)
        self.behavior = False

    # Main thread calls
    def run(self):
        self.logger.info("Start demonstration")
        try:
            self.threads = [
                threading.Thread(target=self.__de, daemon=True, name="button control"),
                threading.Thread(target=self.__de, daemon=True, name="dc_motor control"),
                threading.Thread(target=self.__de, daemon=True, name="sv_motor control"),
                threading.Thread(target=self.__ov, daemon=True, name="overview control")
            ]

            n = 2
            match self.config["test"]["target"].upper():
                case "BUTTON":
                    n = 0
                case "DCMOTOR":
                    n = 1
                case "SVMOTOR":
                    n = 2

            self.logger.debug(f"Start thread: {self.threads[3].name}")
            self.threads[3].start()
            self.logger.debug(f"Start thread: {self.threads[n].name}")
            self.threads[n].start()

            self.logger.debug(f"Stop thread: {self.threads[n].name}")
            self.threads[n].join()
            self.logger.debug(f"Stop thread: {self.threads[3].name}")
            self.threads[3].join()
        except Exception as e:
            self.logger.error(e)
        finally:
            self.logger.info("Stop demonstration")
