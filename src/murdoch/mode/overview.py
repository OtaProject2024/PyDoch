import curses
import platform
import subprocess
import sys
import time

import yaml


class Overview:
    def __init__(self, mode, conf):
        self.mode = mode
        self.config = self.__filter_config(conf)
        self.threads = []
        self.behavior = False
        self.method = 0
        self.times = 0
        self.st_times = 0
        self.tag = None
        self.branch = None
        self.__latest_git_tag()
        self.__current_git_branch()

        self.content_width = 37
        self.min_width = 80
        self.min_height = 28
        self.color = []

        self.start_time = time.time()
        self.__render_time = 0
        self.cnt = 3
        self.direction = 1

    def __filter_config(self, config, exclude_keys=None):
        if exclude_keys is None:
            exclude_keys = ["operation", "times", "delay", "method", "button", "bno055_sensor", "sound"]
        if isinstance(config, dict):
            return {
                k: self.__filter_config(v, exclude_keys)
                for k, v in config.items()
                if k not in exclude_keys
            }
        elif isinstance(config, list):
            return [self.__filter_config(v, exclude_keys) for v in config]
        else:
            return config

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
        screen.addstr("- PyDoch(")
        screen.addstr("https://github.com/OtaProject2024/PyDoch", curses.A_UNDERLINE)
        screen.addstr(") -")
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
            screen.addstr("Unknown v0.0.0  ".rjust(self.min_width // 2), curses.A_DIM)
        else:
            if self.branch in ["main", "master"]:
                screen.addstr(f"Stable {self.tag}  ".rjust(self.min_width // 2), curses.A_DIM)
            else:
                screen.addstr(f"Beta {self.tag}  ".rjust(self.min_width // 2), curses.A_DIM)

    def __display(self, screen):
        screen.clear()
        self.__term_init()
        height, width = screen.getmaxyx()
        if not self.__check_size(screen, height, width): return

        start_x = (width - self.min_width) // 2
        start_y = (height - self.min_height) // 2

        self.__draw_header(screen, start_y, start_x)
        self.__draw_left(screen, start_y + 1, start_x)
        self.__draw_right(screen, start_y + 1, start_x + self.content_width + 3)
        self.__draw_footer(screen, start_y + self.min_height - 1, start_x)
        screen.refresh()

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

        screen.addstr(current_y, start_x, "┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫")
        current_y += 1

        system_information_lines = [
            f"┃ machine: {(platform.machine() + '(' + platform.architecture()[0] + ')').ljust(self.content_width - 10)}┃",
            f"┃ system: {(platform.system() + ' ' + platform.release()).ljust(self.content_width - 9)}┃",
            f"┃ python: {(str(sys.version_info.major) + '.' + str(sys.version_info.minor) + '.' + str(sys.version_info.micro)).ljust(self.content_width - 9)}┃",
            "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛"
        ]

        for line in system_information_lines:
            screen.addstr(current_y, start_x, line)
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

        for line in yaml.dump(self.config, sort_keys=False, allow_unicode=True).splitlines():
            if ":" in line:
                key, value = line.split(":", 1)

                screen.addstr(current_y, start_x, f"┃ {key}:")
                screen.addstr(f"{value}", self.color[3])
                screen.addstr(f"{' ' * (self.content_width - len(key) - len(value) - 2)}┃")
                current_y += 1

        screen.addstr(current_y, start_x, "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
        current_y += 1
        return current_y

    def __draw_left(self, screen, start_y, start_x):
        current_y = self.__draw_system_information(screen, start_y, start_x)
        _ = self.__draw_configuration(screen, current_y, start_x)

    def __draw_information(self, screen, start_y, start_x):
        current_y = start_y
        screen.addstr(start_y, start_x, "┏━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┓")
        current_y += 1

        screen.addstr(current_y, start_x, "┃ MODE: ")
        screen.addstr(f"{self.mode.ljust(7)}", self.color[4])
        screen.addstr(" ┃ ")
        screen.addstr(time.strftime("%Y/%m/%d %H:%M:%S ", time.localtime()))
        screen.addstr("┃")
        current_y += 1

        screen.addstr(current_y, start_x, "┗━━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━━━━━━━┛")
        current_y += 1

        return current_y

    def __uptime(self):
        up = time.time() - self.start_time
        h, r = divmod(up, 3600)
        m, s = divmod(r, 60)
        return int(h), int(m), int(s)

    def __draw_robot_state(self, screen, start_y, start_x):
        hours, minutes, seconds = self.__uptime()
        hours, minutes, seconds = f"{hours:02}", f"{minutes:02}", f"{seconds:02}"

        current_y = start_y
        screen.addstr(current_y, start_x, "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
        current_y += 1

        screen.addstr(current_y, start_x, "┃")
        screen.addstr("ROBOT STATE".center(self.content_width), curses.A_BOLD)
        screen.addstr("┃")
        current_y += 1

        screen.addstr(current_y, start_x, "┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫")
        current_y += 1

        screen.addstr(current_y, start_x,
                      f"┃ uptime: {(hours + ':' + minutes + ':' + seconds).ljust(self.content_width - 9)}┃")
        current_y += 1

        screen.addstr(current_y, start_x, "┃ behavior: ")
        if self.behavior:
            screen.addstr("true".ljust(5), self.color[2])
        else:
            screen.addstr("false".ljust(5), self.color[1])
        screen.addstr(f"{' ' * (self.content_width - 16)}┃")
        current_y += 1

        screen.addstr(current_y, start_x, "┃ method: ")
        if self.method == 0:
            screen.addstr("stop".ljust(7), self.color[1])
        elif self.method == 1:
            screen.addstr("forward".ljust(7), self.color[2])
        elif self.method == 2:
            screen.addstr("left".ljust(7), self.color[3])
        elif self.method == 3:
            screen.addstr("right".ljust(7), self.color[4])
        screen.addstr(f"{' ' * (self.content_width - 16)}┃")
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

        screen.addstr(current_y, start_x, "┃ times: ")
        if self.mode == "TEST" or self.mode == "DEMO":
            screen.addstr(f"{str(self.times).zfill(2)}/{str(self.st_times).zfill(2)}".ljust(7))
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
            screen.addstr(f"]{' ' * (self.content_width - 24)}┃")
            current_y += 1

            screen.addstr(current_y, start_x, "┃".ljust(9))
            screen.addstr("━" * filled, self.color[c])
            screen.addstr("━" * (25 - filled))
            screen.addstr("┃".rjust(5))
            current_y += 1
        else:
            screen.addstr("invalid".ljust(self.content_width - 17), self.color[1])
            screen.addstr(f"{' ' * (self.content_width - 28)}┃")
            current_y += 1

            screen.addstr(current_y, start_x, "┃".ljust(9))
            screen.addstr("━" * 25)
            screen.addstr("┃".rjust(5))
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
            screen.addstr(current_y, start_x, f"┃ {'{0}: '.format(str(no).zfill(2))}")
            if thread.is_alive():
                screen.addstr("activate".ljust(13), self.color[6])
            else:
                screen.addstr("deactivate".ljust(13), self.color[5])
            screen.addstr(f"{thread.name.ljust(self.content_width - 18)}┃")
            current_y += 1

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

    def __draw_right(self, screen, start_y, start_x):
        current_y = self.__draw_information(screen, start_y, start_x)
        current_y = self.__draw_robot_state(screen, current_y, start_x)
        current_y = self.__draw_test_progress(screen, current_y, start_x)
        current_y = self.__draw_threads(screen, current_y, start_x)
        _ = self.__draw_fish(screen, current_y, start_x)

    def run(self, threads, behavior, method, times=0, st_times=0):
        self.threads, self.behavior, self.method, self.times, self.st_times = threads, behavior, method, times, st_times
        curses.wrapper(self.__display)
