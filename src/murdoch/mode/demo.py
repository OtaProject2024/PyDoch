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
                threads=self.threads,
                behavior=self.behavior,
                method=self.method,
                times=self.times,
                st_times=self.config["test"]["target"]["times"]
            )

    # Demo thread calls
    def __de(self):
        self.logger.debug(f'Action method: {self.config["test"]["target"]["method"]}')
        for i in range(self.config["test"]["target"]["times"]):
            if self.stop_event.is_set(): break
            self.times += 1
            time.sleep(1)
            self.method = random.randint(0, 3)
        self.behavior = False

    # Main thread calls
    def run(self):
        self.logger.info("Start demonstration")
        try:
            self.threads = [
                threading.Thread(target=self.__de, daemon=True, name="DCMotor control"),
                threading.Thread(target=self.__de, daemon=True, name="SVMotor control"),
                threading.Thread(target=self.__ov, daemon=True, name="Overview control")
            ]

            n = 0
            match self.config["test"]["target"]["name"].upper():
                case "DCMOTOR":
                    n = 0
                case "SVMOTOR":
                    n = 1

            self.threads[2].start()
            self.logger.debug(f"Start thread: {self.threads[0].name}")
            self.threads[n].start()
            self.logger.debug(f"Start thread: {self.threads[n].name}")

            self.threads[n].join()
            self.logger.debug(f"Stop thread: {self.threads[n].name}")
            self.threads[2].join()
            self.logger.debug(f"Stop thread: {self.threads[0].name}")
        except Exception as e:
            self.logger.error(e)
        finally:
            self.logger.info("Stop demonstration")
