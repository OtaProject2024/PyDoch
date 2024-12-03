import socket
import time
import getpass


# 初期状態
state = True
contact = False
stationary = False
action_state = 1

# 無限ループで表示を更新
while True:
    o1 = " ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓\n"
    u2 = " ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛\n"
    i = f" ┃ machine: {socket.gethostbyname(socket.gethostname())}@{getpass.getuser()} ┃\n"





    overline  = " ┏━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┓\n"
    underline = " ┗━━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━━━━━━━┛\n"

    current_time = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
    info = f" ┃ mode: PRODUCT ┃ {current_time} ┃\n"

    print(
        o1 + i + u2 +
        overline + info + underline + "\033[7A")

    # 少し待機
    time.sleep(0.5)

    # 状態を変更してみる（例: 状態を交互に変更）
    state = not state
    contact = not contact
    stationary = not stationary
    action_state = (action_state + 1) % 2  # 0と1を切り替える
