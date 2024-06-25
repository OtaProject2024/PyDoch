import threading

import murdoch

# state flg
flg = False


def dc():
    global flg

    d = murdoch.DCMotor()
    d.start()
    while flg:
        pass
    d.stop()


def sv():
    global flg

    s = murdoch.SVMotor()
    s.start()
    while flg:
        s.run()
    s.stop()


def bt():
    global flg

    b = murdoch.Button()
    flg = b.run()
    flg = b.run()
    b.stop()


def main():
    global flg

    t1 = threading.Thread(target=bt)
    t1.start()
    while not flg:
        pass
    t2 = threading.Thread(target=dc)
    t3 = threading.Thread(target=sv)
    t2.start()
    t3.start()

    t3.join()
    t1.join()
    t2.join()


if __name__ == '__main__':
    main()
