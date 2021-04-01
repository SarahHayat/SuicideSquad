"""

"""

import numpy as np


def extract_list_of_value(data, *field):
    result = list(
        map(lambda item: dict({field: item.get(*field), "user": item.get("host")}), data))
    return result


def extract_list_of_host(data):
    result = list(
        map(lambda item: item.get('user'), data))
    return np.unique(result)


def extract_data_where_users(datas, users):
    result = list(filter(lambda data: data.get("user") in users, datas))
    return result[:-1]
