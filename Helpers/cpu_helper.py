"""
Module Collecting cpu's Informations
by Sarah Hayat
"""
import psutil


def collecting_cpu_informations():
    """
            Collecting all CPU informations
            :parameter times: number of times you want to execute
            :return: description of cpu
    """

    # user: time spent by normal processes executing in user mode; on Linux this also includes guest time
    # system: time spent by processes executing in kernel mode
    # idle: time spent doing nothing

    # ctx_switches: number of context switches (voluntary + involuntary) since boot.
    # interrupts: number of interrupts since boot.

    return dict({"times": psutil.cpu_times(),
                 "percent": psutil.cpu_percent(interval=1, percpu=True),
                 "time_percent": psutil.cpu_times_percent(percpu=True),
                 "count": psutil.cpu_count(logical=True),
                 "freq": psutil.cpu_freq(percpu=True),
                 "stats": psutil.cpu_stats(),
                 "load_avg": psutil.getloadavg(),
                 "percent_representation": [x / psutil.cpu_count() * 100 for x in psutil.getloadavg()]
                 })


print(collecting_cpu_informations())
