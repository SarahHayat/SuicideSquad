""" Module Collect_Hardware.py
All function to collect and format data from hardware
"""
import time

import psutil


def get_partition(disk):
    """
          get and format data of a partition at path

          :return: dict of a partition data
          :rtype: dict

    """
    usage = psutil.disk_usage(disk.mountpoint)
    return dict({"device": disk.device,
                 "mountpoint": disk.mountpoint,
                 "fstype": disk.fstype,
                 "opts": disk.opts,
                 "maxfile": disk.maxfile,
                 "maxpath": disk.maxpath,
                 "size": usage.total,
                 "used": usage.used,
                 "free": usage.free,
                 "percent": usage.percent
                 })


def get_disk_satistique_io():
    """
            Return system-wide disk I/O statistics as dict including the following fields:

            read_count: number of reads
            write_count: number of writes
            read_bytes: number of bytes read
            write_bytes: number of bytes written

            :return: dict of system-wide disk I/O statistics
            :rtype: dict

             :Example:

            >>> get_disk_satistique_io()
             {'read_count': 21011429, 'write_count': 25194117, 'read_bytes': 475790487552, 'write_bytes': 491047813120}

    """
    io_data = psutil.disk_io_counters()
    return dict({"read_count": io_data.read_count,
                 "write_count": io_data.write_count,
                 "read_bytes": io_data.read_bytes,
                 "write_bytes": io_data.write_bytes})


def get_disk_data():
    """
            Return a dict who contains data of all partition and system-wide disk I/O statistics

             :return: dict all partition and system-wide disk I/O statistics
            :rtype: dict

    """
    return dict({"partitions": list(map(lambda disk: get_partition(disk), psutil.disk_partitions(True))),
                 "io_stats": get_disk_satistique_io()})


def get_battery_data():
    """
           get data of the battery


            :return: dictionnary on data
            :rtype: dict

            :Example:

            >>> get_battery_data()
            {'charge': 82, 'status': 0, 'left': 0}

    """
    if not hasattr(psutil, "sensors_battery"):
        return "platform not supported"
    batt = psutil.sensors_battery()
    if batt is None:
        return "no battery is installed"
    return dict({"charge": round(batt.percent, 2),
                 "status": 0 if batt.power_plugged else 1,
                 "left": batt.secsleft if type(batt.secsleft) == int else 0})


def get_net_io_sent_recv():
    """
            return system-wide network I/O statistics.

            return system-wide network I/O statistics as a named tuple including
            the following attributes: bytes, packets, errors, packet dropped

    """
    io_counters = psutil.net_io_counters(pernic=False, nowrap=True)
    result = dict({
        "incoming": dict({"bytes": io_counters.bytes_recv,
                          "pkts": io_counters.packets_recv,
                          "errs": io_counters.errin,
                          "drops": io_counters.dropin}),
        "out": dict({"bytes": io_counters.bytes_sent,
                     "pkts": io_counters.packets_sent,
                     "errs": io_counters.errout,
                     "drops": io_counters.dropout})})

    return result


def get_cpu_informations():
    """
            Collecting all CPU informations

            :return: dict of all cpu
            :rtype: dict
    """
    times_dict = dict({"times_user": psutil.cpu_times().user,
                       "times_system": psutil.cpu_times().system,
                       "times_idle": psutil.cpu_times().idle})

    stats_dict = dict({"stats_ctx_switches": psutil.cpu_stats().ctx_switches,
                       "stats_interrupts": psutil.cpu_stats().interrupts,
                       "stats_soft_interrupts": psutil.cpu_stats().soft_interrupts,
                       "stats_syscalls": psutil.cpu_stats().syscalls,
                       })

    times_percent = list()
    for item in psutil.cpu_times_percent(percpu=True):
        times_percent.append(dict({"time_percent_user": item.user,
                                   "time_percent_system": item.system,
                                   "time_percent_idle": item.idle}))

    freq = list()
    for item in psutil.cpu_freq(percpu=True):
        freq.append(dict({"current": item.current,
                          "min": item.min,
                          "max": item.max
                          }))

    return dict({"times_dict": times_dict,
                 "percent": psutil.cpu_percent(interval=1, percpu=True),
                 "time_percent": times_percent,
                 "count": psutil.cpu_count(logical=True),
                 "freq": freq,
                 "stats": stats_dict,
                 "percent_representation": [x / psutil.cpu_count() * 100 for x in psutil.getloadavg()]
                 })


def collect_all_data():
    """
           Return a dict with all collectible datas of the hardware.

            :return: all collectible datas of the hardware
            :rtype: dict

            :Example:

            >>> collect_all_data()
            {"disk": get_all_partition_all_usage(),
                "cpu": get_cpu_informations(),
                "battery": get_battery_data(),
                "network": get_net_io_sent_recv()}

    """
    time.ctime()
    return dict({"disk": get_disk_data(),
                 "cpu": get_cpu_informations(),
                 "battery": get_battery_data(),
                 "network": get_net_io_sent_recv()})


def collect_data(component):
    """
               switch case the call the wright function for the wright component
               :param component: name of the component
    """
    send_component = {
        "battery": get_battery_data,
        "network": get_net_io_sent_recv,
        "disk": get_disk_data,
        "cpu": get_cpu_informations

    }
    return send_component.get(component)()
