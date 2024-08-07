import logging
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
        self.flg = False

        self.__sigs()
        self.__conf()
        self.__log()

    def __sigs(self):
        signal.signal(signal.SIGINT, self.stop)
        signal.signal(signal.SIGTERM, self.stop)
        signal.signal(signal.SIGALRM, self.stop)

    def __conf(self, path="config.yaml"):
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

    def __bt(self):
        b = murdoch.Button(self.config["components"]["button"]["channel"])
        self.flg = b.run()
        self.logger.info("Button state: ON")
        self.flg = b.run()
        self.logger.info("Button state: OFF")
        b.stop()

    def __dc(self):
        d = murdoch.DCMotor(
            self.config["components"]["dc_motor"]["ref_channel"],
            self.config["components"]["dc_motor"]["in1_channel"],
            self.config["components"]["dc_motor"]["in2_channel"],
        )
        d.start(self.config["components"]["dc_motor"]["power"])
        while self.flg:
            d.run()
        d.stop()

    def __sv(self):
        s = murdoch.SVMotor(self.config["components"]["sv_motor"]["channel"])
        s.start(self.config["components"]["sv_motor"]["angle"])
        while self.flg:
            s.run()
        s.stop()

    def run(self):
        self.logger.info("Start processing")
        try:
            while True:
                t1 = threading.Thread(target=self.__bt, daemon=True)
                t2 = threading.Thread(target=self.__dc, daemon=True)
                t3 = threading.Thread(target=self.__sv, daemon=True)

                t1.start()
                self.logger.debug("Start thread: Button")
                while not self.flg:
                    pass

                t2.start()
                self.logger.debug("Start thread: DCMotor")
                t3.start()
                self.logger.debug("Start thread: SVMotor")

                t1.join()
                self.logger.debug("Stop thread: Button")
                t2.join()
                self.logger.debug("Stop thread: DCMotor")
                t3.join()
                self.logger.debug("Stop thread: SVMotor")
        except Exception as e:
            self.logger.error(e)
        finally:
            signal.alarm(0)

    def stop(self, sig, frame):
        if sig == signal.SIGINT:
            self.logger.info("Received signal: SIGINT")
        elif sig == signal.SIGTERM:
            self.logger.info("Received signal: SIGTERM")
        elif sig == signal.SIGALRM:
            self.logger.info("Received signal: SIGALRM")

        if self.flg:
            self.flg = False
        else:
            self.flg = True
            time.sleep(0.1)
            self.flg = False
        time.sleep(0.1)
        self.logger.info("Stop processing")
        sys.exit()


if __name__ == '__main__':
    Main().run()
