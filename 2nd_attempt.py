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
    lnum = 0
    for line in lines:
        lnum += 1
        if line[0]=='ForeFlight Logbook Import':
            section = "header"
            print (lnum,line)
        elif line[0]=='Aircraft Table':
            section = 'aircraft'
            print (lnum,line)
            df_aircraft = pd.DataFrame (columns=next(lines))
        elif line[0]=='Flights Table':
            section = 'flights'
            print (lnum,line)
            df_flights = pd.DataFrame (columns=next(lines))
        elif section=='aircraft':
            df_aircraft.loc[len(df_aircraft)] = line
        elif section=='flights':
            df_flights.loc[len(df_flights)] = line



print (df_aircraft)
print(df_flights)