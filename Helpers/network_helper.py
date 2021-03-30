"""
Module Collecting network's Informations
by Jonathan Debailleux
"""

import psutil


def get_net_io_sent_recv():
    """
            return system-wide network I/O statistics.

            return system-wide network I/O statistics as a named tuple including
            the following attributes: bytes, packets, errors, packet dropped


    """
    io_counters = psutil.net_io_counters(pernic=True)
    result = {}
    for network_interface, addrs in psutil.net_if_addrs().items():
        if network_interface in io_counters:
            io = io_counters[network_interface]
            result[network_interface] = dict({
                "incoming": dict({"bytes": io.bytes_recv,
                                  "pkts": io.packets_recv,
                                  "errs": io.errin,
                                  "drops": io.dropin}),
                "out": dict({"bytes": io.bytes_sent,
                             "pkts": io.packets_sent,
                             "errs": io.errout,
                             "drops": io.dropout})})

    return result



