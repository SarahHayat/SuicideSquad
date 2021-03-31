import signal
import time
import yaml
from datetime import timedelta

import Helpers
from InfluxDb import Client
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

    collecting_battery = Task_Scheduler(interval=timedelta(seconds=WAIT_TIME_SECONDS),
                                        execute=Client.send_battery_influx)
    collecting_battery.start()

    collecting_disk = Task_Scheduler(interval=timedelta(seconds=WAIT_TIME_SECONDS),
                                        execute=Client.send_disk_influx)
    collecting_disk.start()

    collecting_network = Task_Scheduler(interval=timedelta(seconds=WAIT_TIME_SECONDS),
                                     execute=Client.send_network_influx)
    collecting_network.start()

    collecting_cpu = Task_Scheduler(interval=timedelta(seconds=WAIT_TIME_SECONDS),
                                        execute=Client.send_cpu_influx)
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
