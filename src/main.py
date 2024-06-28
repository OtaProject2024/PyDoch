import logging
import sys
import threading
import time

import murdoch

# state flg
flg = False


def bt():
    global flg

    b = murdoch.Button()
    flg = b.run()
    logging.info("Button state: ON")
    time.sleep(0.5)
    flg = b.run()
    logging.info("Button state: OFF")
    b.stop()


def dc():
    global flg

    d = murdoch.DCMotor()
    d.start()
    while flg:
        d.run()
    d.stop()


def sv():
    global flg

    s = murdoch.SVMotor()
    s.start()
    while flg:
        s.run()
    s.stop()


def main():
    global flg

    log()
    logging.info("Start processing")

    t1 = threading.Thread(target=bt)
    t2 = threading.Thread(target=dc)
    t3 = threading.Thread(target=sv)

    try:
        while True:
            t1.start()
            logging.debug("Start thread Button")
            while not flg:
                pass
            t2.start()
            logging.debug("Start thread DCMotor")
            t3.start()
            logging.debug("Start thread SVMotor")

            t1.join()
            logging.debug("Stop thread Button")
            t2.join()
            logging.debug("Stop thread DCMotor")
            t3.join()
            logging.debug("Stop thread SVMotor")
    except KeyboardInterrupt:
        logging.info("Stop processing")
        if flg:
            sys.exit(1)
        else:
            sys.exit(0)


def log(lv="DEBUG"):
    logging.basicConfig(
        stream=sys.stdout,
        level=getattr(logging, lv.upper(), logging.INFO),
        format="[%(levelname).4s] %(name)s:%(asctime)s - %(message)s"
    )


if __name__ == '__main__':
    main()
