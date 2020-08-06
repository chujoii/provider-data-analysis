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



pattern = re.compile('[- а-яА-Я0-9]+') # '-' for non-existent



def calc_distribution (csv_provider, data, counter, dictionary_provider):
    used_providers = pattern.findall(data[csv_provider])
    for match in used_providers:
        counter += 1
        if match in dictionary_provider:
            dictionary_provider[match] += 1
        else:
            dictionary_provider[match] = 1
    return counter, dictionary_provider



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


print ("median = %.0f"% (statistics.median(stat_data)))
mean_value = statistics.mean(stat_data)
variance = statistics.variance(stat_data, mean_value)
students_coeff = 2.0 # Student's t-distributions for 95%
print ("mean = %.0f ± %.2f"% (mean_value, students_coeff * math.sqrt(variance/(counter_row*(counter_row - 1)))))

print("internet:", dir_provider_internet)
print("internet(%):", end =" ")
for key, value in dict(map(lambda x:(x[0], x[1]*100.0/counter_provider_internet), dir_provider_internet.items())).items():
    print("'%s': %.2f%%\t" % (key, value), end =" ")
print()

print("tv:", dir_provider_tv)
print("tv(%):", end =" ")
for key, value in dict(map(lambda x:(x[0], x[1]*100.0/counter_provider_tv), dir_provider_tv.items())).items():
    print("'%s': %.2f%%\t" % (key, value), end =" ")
print()
