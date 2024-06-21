import threading
import murdoch


def dc():
    d = murdoch.DCMotor()
    d.run(15)


def sv():
    s = murdoch.SVMotor()
    s.run(30)


if __name__ == '__main__':
    t1 = threading.Thread(target=dc)
    t2 = threading.Thread(target=sv)

    t1.start()
    t2.start()

    t1.join()
    t2.join()
