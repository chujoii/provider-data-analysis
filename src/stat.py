#!/usr/bin/python

'''
    Copyright (C) 2020 Roman V. Prikhodchenko

    This file is part of citylink.pro-data-analysis.

    citylink.pro-data-analysis is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    citylink.pro-data-analysis is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with citylink.pro-data-analysis.  If not, see <https://www.gnu.org/licenses/>.

'''

__author__ = "Roman V. Prikhodchenko"
__copyright__ = "Copyright 2020"
__license__ = "GPL"
__version__ = "0.1"
__maintainer__ = "Roman V. Prikhodchenko"
__email__ = "rvprihod@gmail.com"
__status__ = "Prototype"


import sys
import csv
import math
import statistics
import re

if len(sys.argv) < 2:
    print('\tuse:\n./stat.py ../path/to/data-file.csv')
    sys.exit(0)
csv_file_name = sys.argv[1]

csv_index = 0
csv_internet = 1
csv_tv = 2
csv_number_of_tv = 3
csv_payment_for_internet = 4
csv_payment_for_tv = 5
csv_payment_for_all = 6
csv_apartment_or_house = 7

counter_row = 0
stat_data=[]
counter_provider_internet = 0 # different from counter_row, because some people use two (or more) provider for example ../data/city-002.csv see: 6.08
dir_provider_internet = {}
counter_provider_tv = 0 # different from counter_row, because some people use two (or more) provider for example ../data/city-002.csv see: 6.08
dir_provider_tv = {}
dir_provider_yield = {}



pattern = re.compile('[- а-яА-Я0-9]+') # '-' for non-existent



def create_or_update_dict(key, value, dict):
    if key in dict:
        dict[key] += value
    else:
        dict[key] = value
    return dict



def calc_distribution (csv_provider, data, counter, dictionary_provider):
    used_providers = pattern.findall(data[csv_provider])
    for match in used_providers:
        counter += 1
        create_or_update_dict(match, 1, dictionary_provider)
    return counter, dictionary_provider



def calc_yield (data, dictionary_provider):
    net_providers = pattern.findall(data[csv_internet])
    tv_providers = pattern.findall(data[csv_tv])

    if int(data[csv_payment_for_all]) > 0:
        if int(data[csv_payment_for_internet]) > 0:
            diff_nt = list(set(net_providers) - set(tv_providers))
            create_or_update_dict(diff_nt[0], int(data[csv_payment_for_internet]), dictionary_provider)
        elif int(data[csv_payment_for_tv]) > 0:
            diff_tn = list(set(tv_providers) - set(net_providers))
            create_or_update_dict(diff_tn[0], int(data[csv_payment_for_tv]), dictionary_provider)
        union_nt = list(set(net_providers) & set(tv_providers))
        if len(union_nt)>0: # fix error: city2 page2 line19
            create_or_update_dict(union_nt[0], int(data[csv_payment_for_all]), dictionary_provider)
    else:
        create_or_update_dict(net_providers[0], int(data[csv_payment_for_internet]), dictionary_provider)
        create_or_update_dict(tv_providers[0], int(data[csv_payment_for_tv]), dictionary_provider)
    return dictionary_provider



def print_sorted_dict_by_value(format, dict):
    sort_by_value = sorted(dict.items(), key=lambda x: x[1], reverse=True)
    for i in sort_by_value:
        print(format % (i[0], i[1]))



with open(csv_file_name, newline='\n') as csv_file:
    raw_data = csv.reader(csv_file, delimiter=',', quotechar='"')

    # This skips the first row of the CSV file.
    header_line = next(raw_data)

    for row in raw_data:
        counter_row += 1
        stat_data.append(float(row[csv_payment_for_internet]) +
                         float(row[csv_payment_for_tv]) +
                         float(row[csv_payment_for_all]))
        counter_provider_internet, dir_provider_internet = calc_distribution(csv_internet, row, counter_provider_internet, dir_provider_internet)
        counter_provider_tv, dir_provider_tv = calc_distribution(csv_tv, row, counter_provider_tv, dir_provider_tv)
        dir_provider_yield = calc_yield(row, dir_provider_yield)


print ("медиана чека = %.0f"% (statistics.median(stat_data)))
mean_value = statistics.mean(stat_data)
variance = statistics.variance(stat_data, mean_value)
students_coeff = 2.0 # Student's t-distributions for 95%
print ("средний чек = %.0f ± %.2f"% (mean_value, students_coeff * math.sqrt(variance/(counter_row*(counter_row - 1)))))

print("\nпользователей интернет:")
print_sorted_dict_by_value("'%s':\t%d\t", dir_provider_internet)

print("\nдоли рынка интернет (%):")
print_sorted_dict_by_value("'%s':\t%.2f%%\t", dict(map(lambda x:(x[0], x[1]*100.0/counter_provider_internet), dir_provider_internet.items())))

print("\nпроникновение услуг интернет:")
print_sorted_dict_by_value("'%s': %.2f\t", dict(map(lambda x:(x[0], x[1]/counter_row), dir_provider_internet.items())))

print("\nтелезрителей:")
print_sorted_dict_by_value("'%s':\t%d\t", dir_provider_tv)

print("\nдоли рынка ТВ(%):")
print_sorted_dict_by_value("'%s': %.2f%%\t", dict(map(lambda x:(x[0], x[1]*100.0/counter_provider_tv), dir_provider_tv.items())))

print("\nпроникновение услуг ТВ:")
print_sorted_dict_by_value("'%s': %.2f\t", dict(map(lambda x:(x[0], x[1]/counter_row), dir_provider_tv.items())))

print('\nприбыль:')
print_sorted_dict_by_value("'%s': %d\t", dir_provider_yield)

print()

