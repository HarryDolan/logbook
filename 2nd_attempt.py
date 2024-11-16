#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 16:11:37 2024

@author: dolan
"""

import csv
import pandas as pd


ac_col=['AircraftID','TypeCode','Year','Make','Model','GearType','EngineType','Equipment Type','Category/Class','Complex','TAA','High Performance','Pressurized','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','']
ac = [['N2450W','SGS 2-32','','Schweizer','SGS2-32','fixed_tricycle','Non-Powered','aircraft','glider','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','',''],
      ['N501HH','R22','','Robinson','R22','skids','Piston','aircraft','rotorcraft_helicopter','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','',''],
      ['NC8407','4-AT-E','1929','Ford','Trimotor','fixed_tailwheel','Piston','aircraft','airplane_multi_engine_land','','','TRUE','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','',''],
      ['N910CP','C172','1999','Cessna Aircraft','Skyhawk','fixed_tricycle','Piston','aircraft','airplane_single_engine_land','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','',''],
      ['N429CP','C172','','Cessna','C172S','fixed_tricycle','Piston','aircraft','airplane_single_engine_land','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','']]

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
            df_aircraft = pd.DataFrame (columns=ac_col)
        elif line[0]=='Flights Table':
            section = 'flights'
            df_flights = pd.DataFrame (columns=next(lines))
        elif section=='aircraft':
            if line[0]=='': continue
            df_aircraft.loc[len(df_aircraft)] = line
            x=9999
        elif section=='flights':
            df_flights.loc[len(df_flights)] = line


df2 = pd.DataFrame(columns=ac_col)

df2.loc[len(df2)] = ac[0]
df2.loc[len(df2)] = ac[1]
df2.loc[len(df2)] = ac[2]
df2.loc[len(df2)] = ac[3]
df2.loc[len(df2)] = ac[4]

df2.set_index("AircraftID", inplace = True)

result2 = df2.loc["N2450W"]

df_aircraft.set_index("AircraftID", inplace = True)

ac_row = df_aircraft.loc["N2450W"]



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