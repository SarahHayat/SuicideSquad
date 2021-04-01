import signal
import time

import yaml
from datetime import timedelta

from Bus.send import send
from CliParser import execute
from Hardware import Collect_Hardware

from Helpers.Task_Scheduler import Task_Scheduler

execute()
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

    collecting_battery = Task_Scheduler(interval=timedelta(seconds=WAIT_TIME_SECONDS),
                                        execute=send,
                                        args=("battery", Collect_Hardware.get_battery_data()))

    collecting_battery.start()
    time.sleep(1)
    collecting_disk = Task_Scheduler(interval=timedelta(seconds=WAIT_TIME_SECONDS),
                                     execute=send,
                                     args=("disk", Collect_Hardware.get_disk_data()))
    collecting_disk.start()
    time.sleep(1)
    collecting_network = Task_Scheduler(interval=timedelta(seconds=WAIT_TIME_SECONDS),
                                        execute=send,
                                        args=("network", Collect_Hardware.get_net_io_sent_recv()))
    collecting_network.start()
    time.sleep(1)
    collecting_cpu = Task_Scheduler(interval=timedelta(seconds=WAIT_TIME_SECONDS),
                                    execute=send,
                                    args=("cpu", Collect_Hardware.get_cpu_informations()))
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
