"""
Module Collecting disk's Informations
by Corentin Vallois
"""
import psutil
from enum import Enum


def get_all_partitions_path():
    """
            function to get all partitions path

           get an array of dict with all device name and path
           of each disk partitions

            :return: A array with all disk partitions's device name and path
            :rtype: array

            :Example:

            >>> get_all_partitions_path()
             [{'device': '/dev/disk1s1s1', 'path': '/'}, {'device': '/dev/disk1s5', 'path': '/System/Volumes/VM'}]
    """

    return list(
        map(lambda disk: dict({"device": disk.device, "path": disk.mountpoint}), psutil.disk_partitions(True)))


class Disk_Usage_Properties(Enum):
    """
            class enum to know wich field is accessible in result of psutil.disk_usage()
    """
    SIZE = "total"
    USED = "used"
    FREE = "free"
    PERCENT = "percent"


def get_partition_usage(disk, property_in_result):
    """
            function to get partitions of a device usage for asked field

            get dict with device name and asked field



            :param disk: dict {'device': '/dev/disk1s1s1', 'path': '/'}
            :param property_in_result: Enum Disk_Usage_Properties value
            :return: A dict with all disk partitions's device name and path
            :rtype: dict

            :Example:

            >>> get_partition_usage({'device': '/dev/disk1s1s1', 'path': '/'},Disk_Usage_Properties.PERCENT)
             [{'device': '/dev/disk1s1s1', 'percent': 2.6}, {'device': '/dev/disk1s5', 'percent': 0.3}]
    """

    return dict({"device": disk.get("device"),
                 property_in_result.value: getattr(psutil.disk_usage(disk.get("path")), property_in_result.value)})

def format_disk(disk):
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
def get_all_partition_all_usage():
    """
            function to get partitions usage of a device for asked field

            get dict with device name and asked field



            :param disk: dict {'device': '/dev/disk1s1s1', 'path': '/'}
            :param property_in_result: Enum Disk_Usage_Properties value
            :return: A dict with all disk partitions's device name and path
            :rtype: dict

            :Example:

            >>> get_partition_usage({'device': '/dev/disk1s1s1', 'path': '/'},Disk_Usage_Properties.PERCENT)
             [{'device': '/dev/disk1s1s1', 'percent': 2.6}, {'device': '/dev/disk1s5', 'percent': 0.3}]
    """
    return dict({"partitions": list(map(lambda disk: format_disk(disk), psutil.disk_partitions(True))),
                 "io_stats": get_disk_satistique_io()})


def get_disk_satistique_io():
    """
            Return system-wide disk I/O statistics as a named tuple including the following fields:

            read_count: number of reads
            write_count: number of writes
            read_bytes: number of bytes read
            write_bytes: number of bytes written

            :return: description
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






