""" diskHelper Module
PsUtils function to get disks informations
"""
import psutil

from enum import Enum


class Disk_Usage_Properties(Enum):
    """
            class enum to know wich field is accessible in result of psutil.disk_usage()
    """
    SIZE = "total"
    USED = "used"
    FREE = "free"
    PERCENT = "percent"


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


def get_all_partitions_usage(disk, property_in_result):
    """
            function to get all partitions usage percent

           get an array of dict with all
           device name and usage percent
           of each disk partitions


            :param disk: dict {'device': '/dev/disk1s1s1', 'path': '/'}
            :param property_in_result: Enum Disk_Usage_Properties value
            :return: A dict with all disk partitions's device name and path
            :rtype: dict

            :Example:

            >>> get_all_partitions_usage({'device': '/dev/disk1s1s1', 'path': '/'},Disk_Usage_Properties.PERCENT)
             [{'device': '/dev/disk1s1s1', 'percent': 2.6}, {'device': '/dev/disk1s5', 'percent': 0.3}]
    """

    return dict({"device": disk.get("device"),
                 property_in_result.value: getattr(psutil.disk_usage(disk.get("path")), property_in_result.value)})


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
    result = dict({"read_count": io_data.read_count,
                   "write_count": io_data.write_count,
                   "read_bytes": io_data.read_bytes,
                   "write_bytes": io_data.write_bytes})
    return result


