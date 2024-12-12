import curses
import platform
import subprocess
import sys
import time


class Overview:
    def __init__(self, mode, conf):
        self.mode = mode
        self.config = conf
        self.threads = []
        self.__current_time = time.strftime('%Y/%m/%d %H:%M:%S', time.localtime())
        self.behavior = False
        self.dc_wait = False
        self.sv_wait = False
        self.method = 0
        self.times = 0
        self.st_times = 0
        self.tag = None
        self.branch = None
        self.__latest_git_tag()
        self.__current_git_branch()

        self.content_width = 37
        self.min_width = 80
        self.min_height = 31
        self.color = []

        self.start_time = time.time()
        self.__render_time = 0
        self.cnt = 3
        self.direction = 1

    def __term_init(self):
        curses.curs_set(0)
        curses.noecho()
        curses.cbreak()
        curses.nonl()
        # curses.delay_output(100)

        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_RED, -1)
        curses.init_pair(2, curses.COLOR_GREEN, -1)
        curses.init_pair(3, curses.COLOR_YELLOW, -1)
        curses.init_pair(4, curses.COLOR_BLUE, -1)
        curses.init_pair(5, curses.COLOR_MAGENTA, -1)
        curses.init_pair(6, curses.COLOR_CYAN, -1)
        curses.init_pair(7, curses.COLOR_WHITE, -1)
        curses.init_pair(8, curses.COLOR_BLACK, -1)
        for i in range(9):
            self.color.append(curses.color_pair(i))

    def __draw_header(self, screen, start_y, start_x):
        screen.addstr(start_y, start_x, f"{' ' * ((self.min_width - 52) // 2)}")
        screen.addstr("- PyDoch( ")
        screen.addstr("https://github.com/OtaProject2024/PyDoch", curses.A_UNDERLINE)
        screen.addstr(" ) -")
        screen.addstr(f"{' ' * ((self.min_width - 52) // 2)}")

    def __latest_git_tag(self):
        try:
            self.tag = subprocess.check_output(
                ["git", "describe", "--tags", "--abbrev=0"],
                stderr=subprocess.DEVNULL
            ).strip().decode("utf-8")
        except subprocess.CalledProcessError:
            return

    def __current_git_branch(self):
        try:
            self.branch = subprocess.check_output(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                stderr=subprocess.DEVNULL
            ).strip().decode("utf-8")
        except subprocess.CalledProcessError:
            return

    def __draw_footer(self, screen, start_y, start_x):
        screen.addstr(start_y, start_x, " exit: Ctrl+C".ljust(self.min_width // 2), curses.A_DIM)

        if self.tag is None or self.branch is None:
            screen.addstr("Unknown v0.0.0".rjust(self.min_width // 2 - 2), curses.A_DIM)
        else:
            if self.branch in ["main", "master"]:
                screen.addstr(f"Stable {self.tag}".rjust(self.min_width // 2 - 2), curses.A_DIM)
            else:
                screen.addstr(f"Beta {self.tag}".rjust(self.min_width // 2 - 2), curses.A_DIM)

    def __display(self, screen):
        screen.clear()
        self.__term_init()
        height, width = screen.getmaxyx()
        if not self.__check_size(screen, height, width): return

        start_x = (width - self.min_width) // 2 + 1
        start_y = (height - self.min_height) // 2

        self.__draw_header(screen, start_y, start_x)
        self.__draw_left(screen, start_y + 1, start_x)
        self.__draw_right(screen, start_y + 1, start_x + self.content_width + 3)
        self.__draw_footer(screen, start_y + self.min_height - 1, start_x)
        screen.refresh()
        curses.napms(2000)

    def __simple_display(self, screen):
        screen.addstr(2, 0, f"time: {time.strftime('%Y/%m/%d %H:%M:%S', time.localtime())}")
        screen.addstr(3, 0, f"mode: {self.mode}")
        screen.addstr(4, 0, f"behavior: {self.behavior}")
        screen.addstr(5, 0, f"method: {self.method}")
        screen.addstr(6, 0, f"times: {self.times}/{self.st_times}")
        screen.addstr(7, 0, f"activate threads: {[i.name for i in self.threads if i.is_alive()]}")

    def __check_size(self, screen, height, width):
        if height < self.min_height or width < self.min_width:
            screen.addstr(0, 0, "Terminal too small. Resize the terminal.", self.color[1])
            self.__simple_display(screen)
            screen.refresh()
            time.sleep(1)
            return False
        return True

    def __draw_system_information(self, screen, start_y, start_x):
        current_y = start_y
        screen.addstr(current_y, start_x, "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
        current_y += 1

        screen.addstr(current_y, start_x, "┃")
        screen.addstr("SYSTEM INFORMATION".center(self.content_width), curses.A_BOLD)
        screen.addstr("┃")
        current_y += 1

        screen.addstr(current_y, start_x, "┣━━━━━━━━━┯━━━━━━━━━━━━━━━━━━━━━━━━━━━┫")
        current_y += 1

        system_information_lines = [
            f"┃ machine │ {(platform.machine() + '(' + platform.architecture()[0] + ')').ljust(self.content_width - 11)}┃",
            f"┃ system  │ {(platform.system() + ' ' + platform.release()).ljust(self.content_width - 11)}┃",
            f"┃ python  │ {(str(sys.version_info.major) + '.' + str(sys.version_info.minor) + '.' + str(sys.version_info.micro)).ljust(self.content_width - 11)}┃",
            "┗━━━━━━━━━┷━━━━━━━━━━━━━━━━━━━━━━━━━━━┛"
        ]

        for line in system_information_lines:
            screen.addstr(current_y, start_x, line)
            current_y += 1
        return current_y

    def __test_target(self, screen, start_y, start_x):
        current_y = start_y
        screen.addstr(current_y, start_x, "┃   test ─── target ")
        screen.addstr(f"{self.config['test']['target'].ljust(18)}", self.color[3])
        screen.addstr("┃")
        current_y += 1
        return current_y

    def __component(self, screen, start_y, start_x):
        current_y = start_y
        screen.addstr(current_y, start_x, "┃ ┌─────────── component ───────────┐ ┃")
        current_y += 1

        current_y = self.__button(screen, current_y, start_x)
        current_y = self.__dc_motor(screen, current_y, start_x)
        current_y = self.__sv_motor(screen, current_y, start_x)

        screen.addstr(current_y, start_x, "┃ └─────────────────────────────────┘ ┃")
        current_y += 1
        return current_y

    def __button(self, screen, start_y, start_x):
        current_y = start_y
        screen.addstr(current_y, start_x, "┃ │ button ─┬─ channel ")
        screen.addstr(f"{str(self.config['components']['button']['channel']).ljust(12)}", self.color[3])
        screen.addstr(" │ ┃")
        current_y += 1

        screen.addstr(current_y, start_x, "┃ │         ├─ delay ")
        screen.addstr(f"{str(self.config['components']['button']['delay']).ljust(14)}", self.color[3])
        screen.addstr(" │ ┃")
        current_y += 1

        screen.addstr(current_y, start_x, "┃ │         └─ default ")
        screen.addstr(f"{str(self.config['components']['button']['default']).ljust(12)}", self.color[3])
        screen.addstr(" │ ┃")
        current_y += 1
        return current_y

    def __dc_motor(self, screen, start_y, start_x):
        current_y = start_y
        screen.addstr(current_y, start_x, "┃ │ dc motor ─┬─ channel ─┬─ PWM ")
        screen.addstr(f"{str(self.config['components']['dc_motor']['pwm_channel']).ljust(2)}", self.color[3])
        screen.addstr(" │ ┃")
        current_y += 1

        screen.addstr(current_y, start_x, "┃ │           │           ├─ IN1 ")
        screen.addstr(f"{str(self.config['components']['dc_motor']['in1_channel']).ljust(2)}", self.color[3])
        screen.addstr(" │ ┃")
        current_y += 1

        screen.addstr(current_y, start_x, "┃ │           │           └─ IN2 ")
        screen.addstr(f"{str(self.config['components']['dc_motor']['in2_channel']).ljust(2)}", self.color[3])
        screen.addstr(" │ ┃")
        current_y += 1

        screen.addstr(current_y, start_x, "┃ │           ├─ power ")
        screen.addstr(f"{str(self.config['components']['dc_motor']['power']).ljust(12)}", self.color[3])
        screen.addstr(" │ ┃")
        current_y += 1

        screen.addstr(current_y, start_x, "┃ │           ├─ save power ")
        screen.addstr(f"{str(self.config['components']['dc_motor']['save_power']).ljust(7)}", self.color[3])
        screen.addstr(" │ ┃")
        current_y += 1

        screen.addstr(current_y, start_x, "┃ │           └─ direction ")
        screen.addstr(f"{str(self.config['components']['dc_motor']['direction']).ljust(8)}", self.color[3])
        screen.addstr(" │ ┃")
        current_y += 1
        return current_y

    def __sv_motor(self, screen, start_y, start_x):
        current_y = start_y
        screen.addstr(current_y, start_x, "┃ │ sv motor ─┬─ channel ")
        screen.addstr(f"{str(self.config['components']['sv_motor']['channel']).ljust(10)}", self.color[3])
        screen.addstr(" │ ┃")
        current_y += 1

        screen.addstr(current_y, start_x, "┃ │           ├─ frequency ")
        screen.addstr(f"{str(self.config['components']['sv_motor']['frequency']).ljust(8)}", self.color[3])
        screen.addstr(" │ ┃")
        current_y += 1

        screen.addstr(current_y, start_x, "┃ │           └─ angle ")
        screen.addstr(f"{str(self.config['components']['sv_motor']['angle']).ljust(12)}", self.color[3])
        screen.addstr(" │ ┃")
        current_y += 1
        return current_y

    def __draw_configuration(self, screen, start_y, start_x):
        current_y = start_y
        screen.addstr(current_y, start_x, "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
        current_y += 1

        screen.addstr(current_y, start_x, "┃")
        screen.addstr("CONFIGURATION".center(self.content_width), curses.A_BOLD)
        screen.addstr("┃")
        current_y += 1

        screen.addstr(current_y, start_x, "┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫")
        current_y += 1

        current_y = self.__test_target(screen, current_y, start_x)
        current_y = self.__component(screen, current_y, start_x)

        screen.addstr(current_y, start_x, "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
        current_y += 1
        return current_y

    def __draw_fish(self, screen, start_y, start_x):
        current_time = time.time()
        if current_time - self.__render_time >= 0.5:
            self.__render_time = current_time
            self.cnt += self.direction

        fish = "><>" if self.direction == 1 else "<><"
        if self.cnt == 37:
            self.direction = -1
        elif self.cnt == 3:
            self.direction = 1
        fish_lines = [
            "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓",
            f"┃{fish.rjust(self.cnt).ljust(37)}┃",
            "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛"
        ]
        current_y = start_y
        for line in fish_lines:
            screen.addstr(current_y, start_x, line, curses.A_BOLD)
            current_y += 1
        return current_y

    def __draw_left(self, screen, start_y, start_x):
        current_y = self.__draw_system_information(screen, start_y, start_x)
        current_y = self.__draw_configuration(screen, current_y, start_x)
        _ = self.__draw_fish(screen, current_y, start_x)

    def __draw_datetime(self, screen, start_y, start_x):
        current_y = start_y
        screen.addstr(current_y, start_x, "┏━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┓")
        current_y += 1

        self.__current_time = time.strftime('%Y/%m/%d  %H:%M:%S', time.localtime())
        screen.addstr(current_y, start_x, "┃")
        screen.addstr("DATETIME".center(12), curses.A_BOLD)
        screen.addstr(f"┃{self.__current_time.center(24)}┃")
        current_y += 1

        screen.addstr(current_y, start_x, "┗━━━━━━━━━━━━┻━━━━━━━━━━━━━━━━━━━━━━━━┛")
        current_y += 1

        return current_y

    def __draw_information(self, screen, start_y, start_x):
        current_y = start_y
        screen.addstr(start_y, start_x, "┏━━━━━━━━━━┓┏━━━━━━━━━━━━━━━━━━━━━━━━━┓")
        current_y += 1

        screen.addstr(current_y, start_x, "┃")
        screen.addstr("MODE".center(10), curses.A_BOLD)
        screen.addstr("┃┃")
        screen.addstr("RUNTIME".center(25), curses.A_BOLD)
        screen.addstr("┃")
        current_y += 1

        screen.addstr(current_y, start_x, "┣━━━━━━━━━━┫┣━━━━━━━━━━━━━━━━━━━━━━━━━┫")
        current_y += 1

        screen.addstr(current_y, start_x, "┃")
        if self.mode == "TEST" or self.mode == "DEMO":
            screen.addstr(f"{self.mode.center(10)}", self.color[4])
        elif self.mode == "PRODUCT":
            screen.addstr(f"{'PROD'.center(10)}", self.color[4])
        screen.addstr("┃┃")

        up = time.time() - self.start_time
        hours, r = divmod(up, 3600)
        minutes, seconds = divmod(r, 60)
        hours, minutes, seconds = f"{int(hours):02}", f"{int(minutes):02}", f"{int(seconds):02}"
        screen.addstr(f"{(hours + 'h  │  ' + minutes + 'm  │  ' + seconds + 's').center(25)}")
        screen.addstr("┃")
        current_y += 1

        screen.addstr(current_y, start_x, "┗━━━━━━━━━━┛┗━━━━━━━━━━━━━━━━━━━━━━━━━┛")
        current_y += 1

        return current_y

    def __draw_robot_state(self, screen, start_y, start_x):
        current_y = start_y
        screen.addstr(current_y, start_x, "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
        current_y += 1

        screen.addstr(current_y, start_x, "┃")
        screen.addstr("ROBOT STATE".center(self.content_width), curses.A_BOLD)
        screen.addstr("┃")
        current_y += 1

        screen.addstr(current_y, start_x, "┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫")
        current_y += 1

        screen.addstr(current_y, start_x, "┃   ┌─ behavior ─┐   ┌── method ──┐   ┃")
        current_y += 1

        screen.addstr(current_y, start_x, "┃   │")
        if self.behavior:
            screen.addstr("TRUE".center(12), self.color[2])
        else:
            screen.addstr("FLSE".center(12), self.color[1])
        screen.addstr("│   │")

        if self.method == 0:
            screen.addstr("STOP".center(12), self.color[1])
        elif self.method == 1:
            screen.addstr("FWDD".center(12), self.color[2])
        elif self.method == 2:
            screen.addstr("LEFT".center(12), self.color[3])
        elif self.method == 3:
            screen.addstr("RGHT".center(12), self.color[4])
        screen.addstr("│   ┃")
        current_y += 1

        screen.addstr(current_y, start_x, "┃   └────────────┘   └────────────┘   ┃")
        current_y += 1

        screen.addstr(current_y, start_x, "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
        current_y += 1

        return current_y

    def __progress(self):
        if self.mode == "TEST" or self.mode == "DEMO":
            div = (str(self.times).zfill(2) + "/" + str(self.st_times)).rjust(5)
            per = f"{round(self.times / self.st_times * 100, 2):.02f}".rjust(6)
            return f"{div}  [{per}%]"
        else:
            return "invalid"

    def __draw_test_progress(self, screen, start_y, start_x):
        current_y = start_y
        screen.addstr(current_y, start_x, "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
        current_y += 1

        screen.addstr(current_y, start_x, "┃")
        screen.addstr("TEST PROGRESS".center(self.content_width), curses.A_BOLD)
        screen.addstr("┃")
        current_y += 1

        screen.addstr(current_y, start_x, "┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫")
        current_y += 1

        if self.mode == "TEST" or self.mode == "DEMO":
            screen.addstr(current_y, start_x, "┃                ")
            screen.addstr(f"{str(self.times).zfill(2)}/{str(self.st_times).zfill(2)}".ljust(6))
            screen.addstr("[")
            per = round(self.times / self.st_times * 100, 2)
            filled = int(per) // 4
            per_str = f"{per:.02f}%".rjust(7)
            c = 1
            if per == 100:
                c = 4
            elif per >= 70:
                c = 2
            elif per >= 50:
                c = 3
            screen.addstr(per_str, self.color[c])
            screen.addstr(f"]      ┃")
            current_y += 1

            screen.addstr(current_y, start_x, "┃".ljust(7))
            screen.addstr("━" * filled, self.color[c])
            screen.addstr("━" * (25 - filled))
            screen.addstr("┃".rjust(7))
            current_y += 1
        else:
            screen.addstr(current_y, start_x, "┃")
            screen.addstr("invalid".center(self.content_width), self.color[1])
            screen.addstr("┃")
            current_y += 1

            screen.addstr(current_y, start_x, "┃".ljust(7))
            screen.addstr("━" * 25)
            screen.addstr("┃".rjust(7))
            current_y += 1

        screen.addstr(current_y, start_x, "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
        current_y += 1

        return current_y

    def __draw_threads(self, screen, start_y, start_x):
        current_y = start_y
        screen.addstr(current_y, start_x, "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
        current_y += 1

        screen.addstr(current_y, start_x, "┃")
        screen.addstr("THREADS".center(self.content_width), curses.A_BOLD)
        screen.addstr("┃")
        current_y += 1

        screen.addstr(current_y, start_x, "┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫")
        current_y += 1

        no = 0
        for thread in self.threads:
            no += 1
            screen.addstr(current_y, start_x, f"┃ {'{0}  ['.format(str(no).zfill(2))}")
            if thread.is_alive():
                if thread.name == "dc_motor control":
                    if self.dc_wait:
                        screen.addstr("⏸", self.color[3])
                        screen.addstr("] [")
                        screen.addstr("WAIT", self.color[3])
                    else:
                        screen.addstr("▶", self.color[6])
                        screen.addstr("] [")
                        screen.addstr("RUNN", self.color[6])
                elif thread.name == "sv_motor control":
                    if self.sv_wait:
                        screen.addstr("⏸", self.color[3])
                        screen.addstr("] [")
                        screen.addstr("WAIT", self.color[3])
                    else:
                        screen.addstr("▶", self.color[6])
                        screen.addstr("] [")
                        screen.addstr("RUNN", self.color[6])
                else:
                    screen.addstr("▶", self.color[6])
                    screen.addstr("] [")
                    screen.addstr("RUNN", self.color[6])

            else:
                screen.addstr("■", self.color[5])
                screen.addstr("] [")
                screen.addstr("STOP", self.color[5])
            screen.addstr(f"{']'.ljust(4)}{thread.name.ljust(self.content_width - 18)}┃")
            current_y += 1

        screen.addstr(current_y, start_x, "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
        current_y += 1

        return current_y

    def __draw_right(self, screen, start_y, start_x):
        current_y = self.__draw_datetime(screen, start_y, start_x)
        current_y = self.__draw_information(screen, current_y, start_x)
        current_y = self.__draw_robot_state(screen, current_y, start_x)
        current_y = self.__draw_test_progress(screen, current_y, start_x)
        _ = self.__draw_threads(screen, current_y, start_x)

    def run(self, threads, behavior, method, times=0, st_times=0, dc_wait=False, sv_wait=False):
        self.threads = threads
        self.behavior = behavior
        self.method = method
        self.times = times
        self.st_times = st_times
        self.dc_wait = dc_wait
        self.sv_wait = sv_wait

        curses.wrapper(self.__display)
