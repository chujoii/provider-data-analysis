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

if len(sys.argv) < 2:
    print('\tuse:\n./stat.py ../path/to/data-file.csv')
    sys.exit(0)
csv_file_name = sys.argv[1]

with open(csv_file_name, newline='\n') as csv_file:
    raw_data = csv.reader(csv_file, delimiter=',', quotechar='"')

    # This skips the first row of the CSV file.
    header_line = next(raw_data)

    amount = 0.0
    row_count = 0

    for row in raw_data:
        #print('\t'.join(row))
        amount += int(row[4])+ int(row[5]) + int(row[6])
        row_count += 1

    print ("mean = %.0f"% (amount/row_count))
