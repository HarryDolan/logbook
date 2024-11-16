#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 16:11:37 2024

@author: dolan
"""

import csv
import pandas as pd

path='test.csv'
section = None
df_aircraft = None
df_flights = None

with open (path, 'r') as ff_file:
    lines = csv.reader(ff_file)
    for line in lines:
        if line[0]=='ForeFlight Logbook Import':
            section = "header"
        elif line[0]=='Aircraft Table':
            section = 'aircraft'
            df_aircraft = pd.DataFrame (columns=next(lines))
        elif line[0]=='Flights Table':
            section = 'flights'
            df_flights = pd.DataFrame (columns=next(lines))
        elif section=='aircraft':
            if line[0]=='': continue
            df_aircraft.loc[len(df_aircraft)] = line
        elif section=='flights':
            df_flights.loc[len(df_flights)] = line

df_aircraft.set_index("AircraftID", inplace = True)

for index, row in df_flights.iterrows():
    num = index+1
    page = num//7 + 1
    if num%7 == 1:
        print (100*'=')
        print ("Page")

    ac_row = df_aircraft.loc[row['AircraftID']]
    ac_make = ac_row['Make']
    print (f'{row['Date']:} {row['AircraftID']:} {row['From']:} {row['To']:}')
    if (index+1)%7 == 0:
        print ('---------------------------')