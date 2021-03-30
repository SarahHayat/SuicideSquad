"""
Module Collecting Informations
by Sarah Hayat
"""
import psutil

def collecting_cpu_informations(times):
    """
            Collecting all CPU informations
            :parameter times: number of times you want to execute
            :return: description of cpu
    """
    for x in range(times):
        #user: time spent by normal processes executing in user mode; on Linux this also includes guest time
        #system: time spent by processes executing in kernel mode
        #idle: time spent doing nothing

        cpu_times = psutil.cpu_times()
        print(f'Times : {cpu_times}')

        cpu_percent = psutil.cpu_percent(interval=1, percpu=True)
        print(f'Percent : {cpu_percent}')

        cpu_times_percent = psutil.cpu_times_percent(percpu=True)
        print(f'Times Percent : {cpu_times_percent}')

        cpu_count = psutil.cpu_count(logical=True)
        print(f'Count : {cpu_count}')

        cpu_freq = psutil.cpu_freq(percpu=True)
        print(f'Freq : {cpu_freq}')

        #ctx_switches: number of context switches (voluntary + involuntary) since boot.
        #interrupts: number of interrupts since boot.
        cpu_stats = psutil.cpu_stats()
        print(f'Stats : {cpu_stats}')

        cpu_load_avg = psutil.getloadavg()
        print(f'Load AVG : {cpu_load_avg}')
        print(f'Percentage representation : {[x / psutil.cpu_count() * 100 for x in psutil.getloadavg()]} \n')

collecting_cpu_informations(5)
