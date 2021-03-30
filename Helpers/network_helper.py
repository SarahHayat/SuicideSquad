"""
Module Collecting network's Informations
by Jonathan Debailleux
"""

import psutil
from psutil._common import bytes2human


def get_net_io_sent_recv():
    """
            return system-wide network I/O statistics.

            return system-wide network I/O statistics as a named tuple including
            the following attributes: bytes, packets, errors, packet dropped


    """
    io_counters = psutil.net_io_counters(pernic=True)
    for nic, addrs in psutil.net_if_addrs().items():
        print("%s:" % nic)
        if nic in io_counters:
            io = io_counters[nic]
            print("    incoming       : ", end='')
            print("bytes=%s, pkts=%s, errs=%s, drops=%s" % (
                bytes2human(io.bytes_recv), io.packets_recv, io.errin,
                io.dropin))
            print("    outgoing       : ", end='')
            print("bytes=%s, pkts=%s, errs=%s, drops=%s" % (
                bytes2human(io.bytes_sent), io.packets_sent, io.errout,
                io.dropout))


if __name__ == '__main__':
    get_net_io_sent_recv()