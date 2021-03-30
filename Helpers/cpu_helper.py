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
    times_dict = dict({"times_user": psutil.cpu_times().user,
                      "times_system": psutil.cpu_times().system,
                       "times_idle": psutil.cpu_times().idle})


    times_percent_dict = dict()
    for item in psutil.cpu_times_percent(percpu=True):
        times_percent_dict = dict({"time_percent_user": item.user,
                                   "time_percent_system": item.system,
                                   "time_percent_idle": item.idle})

    stats_dict = dict({"stats_ctx_switches": psutil.cpu_stats().ctx_switches,
                       "stats_interrupts": psutil.cpu_stats().interrupts,
                       "stats_soft_interrupts": psutil.cpu_stats().soft_interrupts,
                       "stats_syscalls": psutil.cpu_stats().syscalls,
                       })
    # user: time spent by normal processes executing in user mode; on Linux this also includes guest time
    # system: time spent by processes executing in kernel mode
    # idle: time spent doing nothing

    # ctx_switches: number of context switches (voluntary + involuntary) since boot.
    # interrupts: number of interrupts since boot.

    return dict({"times_dict": times_dict,
                 "percent": psutil.cpu_percent(interval=1, percpu=True),
                 "time_percent": times_percent_dict,
                 "count": psutil.cpu_count(logical=True),
                 "freq": psutil.cpu_freq(percpu=True),
                 "stats": stats_dict,
                 "load_avg": psutil.getloadavg(),
                 "percent_representation": [x / psutil.cpu_count() * 100 for x in psutil.getloadavg()]
                 })


print(collecting_cpu_informations())
