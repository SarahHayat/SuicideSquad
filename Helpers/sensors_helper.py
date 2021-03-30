"""
Module Collecting cpu's Informations
by Juan-Fernando Herrada
"""
import psutil


def get_battery_data():
    """
           get data of the battery


            :return: dictionnary on data
            :rtype: dict

            :Example:

            >>> get_battery_data()
            {'charge': 82, 'status': 'charging', 'left': 0}

    """
    if not hasattr(psutil, "sensors_battery"):
        return "platform not supported"
    batt = psutil.sensors_battery()
    if batt is None:
        return "no battery is installed"

    return dict({"charge": round(batt.percent, 2),
                 "status": "charging" if batt.power_plugged else "discharging",
                 "left": batt.secsleft if type(batt.secsleft) == int else 0})


print(get_battery_data())
