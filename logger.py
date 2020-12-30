import os
import time
from constants import LOG_DIRECTORY

DEFAULT_CONSOLE_PREFIX = ""

class Logger():
    def __init__(self):
        if not os.path.exists(LOG_DIRECTORY):
            os.mkdir(LOG_DIRECTORY)
        self.log_path = os.path.join(
            LOG_DIRECTORY,
            "{}.log".format(time.strftime("%Y-%m-%d-T%H%M%S", time.localtime()))
        )
        # Create empty log file
        log_file = open(self.log_path, "w")
        log_file.close()

    def get_timestamp(self):
        return time.strftime("%H:%M:%S", time.localtime())

    def console_text(self, text, console_prefix):
        if console_prefix != DEFAULT_CONSOLE_PREFIX:
            return console_prefix + " " + text
        else:
            return text

    def write_to_console(self, text, console_prefix):
        print(self.console_text(text, console_prefix))

    def write_to_file(self, text):
        prefix_text = "[{}] ".format(self.get_timestamp())
        with open(self.log_path, "a") as log_file:
            log_file.write(prefix_text + text + "\n")

    def print_progress(self, name, current, total, console_prefix = DEFAULT_CONSOLE_PREFIX):
        text = "{} {} von {}".format(name, current, total)
        print("{}\r".format(self.console_text(text, console_prefix)), end = "")

    def log(self, text, console_prefix = DEFAULT_CONSOLE_PREFIX):
        self.write_to_console(text, console_prefix)
        self.write_to_file(text)
