import signal
import time

import yaml
from datetime import timedelta

from Bus.send import send
from CliParser import execute
from Hardware import Collect_Hardware

from Helpers.Task_Scheduler import Task_Scheduler


class ProgramKilled(Exception):
    pass


def signal_handler(signum, frame):
    raise ProgramKilled


if __name__ == "__main__":
    execute()
    with open(r'config.yaml') as file:
        yaml = yaml.load(file, Loader=yaml.FullLoader)

    WAIT_TIME_SECONDS = yaml.get("timer")
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)

    collecting_battery = Task_Scheduler(interval=timedelta(seconds=WAIT_TIME_SECONDS),
                                        execute=send,
                                        component="battery")

    collecting_battery.start()
    time.sleep(1)
    collecting_disk = Task_Scheduler(interval=timedelta(seconds=WAIT_TIME_SECONDS),
                                     execute=send,
                                     component="disk")
    collecting_disk.start()
    time.sleep(1)
    collecting_network = Task_Scheduler(interval=timedelta(seconds=WAIT_TIME_SECONDS),
                                        execute=send,
                                        component="network")
    collecting_network.start()
    time.sleep(1)
    collecting_cpu = Task_Scheduler(interval=timedelta(seconds=WAIT_TIME_SECONDS),
                                    execute=send,
                                    component="cpu")
    collecting_cpu.start()

    while True:
        try:
            time.sleep(1)
        except ProgramKilled:
            print("Program killed: running cleanup code")
            collecting_battery.stop()
            collecting_disk.stop()
            collecting_network.stop()
            collecting_cpu.stop()
        break
