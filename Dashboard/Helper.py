""" Module Dashboard.Helper
usefull function to generate chat
"""
from datetime import datetime
from dateutil.parser import parse

import numpy as np


def extract_list_of_value(data, field):
    """
            keep the data of an object list where field as value


            :param data: array to filter
            :param field: field to keep
            :type data: list
            :type field: string
            :return: filtered list
            :rtype: list

    """
    return [i for i in data if i.get(field)]


def extract_list_of_unique_value(data, field):
    """
            extract unique value of a given field in an object list


             :param data: array to filter
             :param field: field to extract unique occurrence
             :type data: list
             :type field: string
             :return: filtered list
             :rtype: list

     """
    result = list(map(lambda item: item.get(field), data))
    result = [i for i in result if i]
    return np.unique(result)


def extract_data_where_is_value(datas, value, field):
    """
                keep the data of an object list where field is egual to value

                :param datas: list to filter
                :param value: value to find
                :param field: field to filter
                :type datas: list
                :type value: any
                :type field: string

                :return: filtered list
                :rtype: list

    """
    return list(filter(lambda data: data.get(field) in value, datas))


def format_time_object(dict_to_filter):
    """
                   format gmt time string return time object of a dict

                    :param dict_to_filter: dict to filter
                    :type dict_to_filter: dict
                    :return: time
                    :rtype: dict

    """
    dict_to_filter['time'] = parse(dict_to_filter.get('time')).isoformat()
    return dict_to_filter


def format_time_req(data):
    """
                   format gmt time string return time object in list of dict

                    :param data: list to filter
                    :type data: list
                    :return: data filtered
                    :rtype: list

    """
    return list(map(lambda item: format_time_object(item), data))
