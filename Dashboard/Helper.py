""" name Module
Description
"""
from datetime import datetime

import numpy as np


def extract_list_of_value(data, field):
    result = list(map(lambda item: dict(
        {field: item.get(field), "time": format_time(item.get("time")), "user": item.get("host")}), data))
    return [i for i in result if i.get(field)]


def extract_list_of_host(data):
    result = list(map(lambda item: item.get('user'), data))
    return np.unique(result)


def extract_data_where_users(datas, users):
    return list(filter(lambda data: data.get("user") in users, datas))


def format_time(time):
    return datetime.strftime(datetime.strptime(time, '%a, %d %b %Y %H:%M:%S %Z'), ' %H:%M:%S %d/%m')
