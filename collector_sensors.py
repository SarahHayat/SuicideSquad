from __future__ import print_function

import sys

import psutil
from psutil._common import sbattery


def secs2hours(secs):
    mm, ss = divmod(secs, 60)
    hh, mm = divmod(mm, 60)
    return "%d:%02d:%02d" % (hh, mm, ss)
    # '%d:%02d:%02d' means hh:mm:ss


def main():
    if hasattr(psutil, "sensor_temperature"):
        temp = psutil.sensors_temperatures()
    else:
        temp = {}
    if hasattr(psutil, "sensor_battery"):
        batt = psutil.sensors_battery()
    else:
        batt = {}
    if hasattr(psutil, "sensor_fans"):
        fans = psutil.sensors_fans()
    else:
        fans = {}

    if not any((temp, batt, fans)):
        print("Can not read any information about temperature, battery and fans")
        return

    infos = set(list(temp) + list(fans))
    for info in infos:
        print(info)
        # Temperature
        if info in temp:
            print("Temperature : ")
            for entry in temp[info]:
                print(" %-20s %s°C (high=%s°C, critical=%s°C)" % (entry.label or info, entry.current, entry.high, entry.critical))
        # Fans
        if info in fans:
            print("Fans : ")
            for entry in fans[info]:
                print("%-20s %s RPM" % (entry.label or info, entry.current))

    # Battery
    print("charge:     %s%%" % round(batt.percent, 2))
    if batt.power_plugged:
        print("status:     %s" % (
            "charging" if batt.percent < 100 else "fully charged"))
        print("plugged in: yes")
    else:
        print("left:       %s" % secs2hours(batt.secsleft))
        print("status:     %s" % "discharging")
        print("plugged in: no")


if __name__ == '__main__':
    main()
