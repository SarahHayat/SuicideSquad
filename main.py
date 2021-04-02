import signal
import time

import yaml
from datetime import timedelta

from Bus.send import send
from CliParser import execute
from Hardware import Collect_Hardware
from Hardware.main import main

from Helpers.Task_Scheduler import Task_Scheduler


class ProgramKilled(Exception):
    pass


def signal_handler(signum, frame):
    raise ProgramKilled


if __name__ == "__main__":
    timer = execute()
    main(timer)
