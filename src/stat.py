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

stat_data=[]
provider_internet={}

pattern = re.compile('[- а-яА-Я0-9]+') # '-' for non-existent

with open(csv_file_name, newline='\n') as csv_file:
    raw_data = csv.reader(csv_file, delimiter=',', quotechar='"')

    # This skips the first row of the CSV file.
    header_line = next(raw_data)

    row_count = 0
    provider_internet_count = 0 # different from row_count, because some people use two (or more) provider for example ../data/city-002.csv see: 6.08

    for row in raw_data:
        row_count += 1
        stat_data.append(float(row[csv_payment_for_internet]) +
                         float(row[csv_payment_for_tv]) +
                         float(row[csv_payment_for_all]))

        provider = pattern.findall(row[csv_internet])
        for match in provider:
            provider_internet_count += 1
            if match in provider_internet:
                provider_internet[match] += 1
            else:
                provider_internet[match] = 1


    print ("median = %.0f"% (statistics.median(stat_data)))
    mean_value = statistics.mean(stat_data)
    variance = statistics.variance(stat_data, mean_value)
    students_coeff = 2.0 # Student's t-distributions for 95%
    print ("mean = %.0f ± %.2f"% (mean_value, students_coeff * math.sqrt(variance/(row_count*(row_count - 1))))) 

    print("internet:", provider_internet)
