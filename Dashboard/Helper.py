""" name Module
Description
"""
from datetime import datetime

import numpy as np


def extract_list_of_value(data, field):
    return [i for i in data if i.get(field)]


def extract_list_of_unique_value(data,value):
    result = list(map(lambda item: item.get(value), data))
    result=[i for i in result if i]
    return np.unique(result)


def extract_data_where_is_value(datas, value,label):
    return list(filter(lambda data: data.get(label) in value, datas))


def format_time(time):
    return datetime.strftime(datetime.strptime(time, '%a, %d %b %Y %H:%M:%S %Z'), ' %H:%M %d-%m')
