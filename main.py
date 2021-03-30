import signal
import time
import yaml
from datetime import timedelta

import Helpers
from Task_Scheduler import Task_Scheduler

with open(r'config.yaml') as file:
    yaml = yaml.load(file, Loader=yaml.FullLoader)

WAIT_TIME_SECONDS = yaml.get("timer")


class ProgramKilled(Exception):
    pass


def signal_handler(signum, frame):
    raise ProgramKilled


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    collecting_data = Task_Scheduler(interval=timedelta(seconds=WAIT_TIME_SECONDS), execute=Helpers.collect_all_data)
    collecting_data.start()

    while True:
        try:
            time.sleep(1)
        except ProgramKilled:
            print("Program killed: running cleanup code")
            collecting_data.stop()
            break
