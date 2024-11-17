#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 16:11:37 2024

@author: dolan
"""

import csv
import pandas as pd
import numpy as np

path='test.csv'
path='logbook_2024-11-15_02_59_43.csv'
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


df_flights['Glider'] = '0.0'
df_flights['Helicopter'] = '0.0'
df_flights['ASEL'] = '0.0'
df_flights['AMEL'] = '0.0'
df_flights['Day'] = '0.0'
df_flights['Model'] = ''
for index in range(len(df_flights)):
    aircraftID = df_flights['AircraftID'][index]
    if aircraftID!='':
        aircraftModel = df_aircraft.loc[aircraftID]['TypeCode']
        df_flights.loc[index,'Model'] = aircraftModel
        aircraftCategory = df_aircraft.loc[aircraftID]['Category/Class']
        if aircraftCategory=='glider':
            df_flights.loc[index,'Glider'] = df_flights['TotalTime'].loc[index]
        elif aircraftCategory=='rotorcraft_helicopter':
            df_flights.loc[index,'Helicopter'] = df_flights['TotalTime'].loc[index]
        elif aircraftCategory=='airplane_single_engine_land':
            df_flights.loc[index,'ASEL'] = df_flights['TotalTime'].loc[index]
        elif aircraftCategory=='airplane_multi_engine_land':
            df_flights.loc[index,'AMEL'] = df_flights['TotalTime'].loc[index]
        if df_flights['TotalTime'].loc[index] and df_flights['Night'].loc[index]:
            day = float(df_flights['TotalTime'].loc[index]) - float(df_flights['Night'].loc[index])
            df_flights.loc[index,'Day'] = f'{day:8.1f}'


if df_flights.loc[0]['Date'] > df_flights.loc[len(df_flights)-1]['Date']:
    df_flights = df_flights.iloc[::-1]      # reverse order of rows

num = 0
for index, row in df_flights.iterrows():
    num += 1
    page = num//7 + 1
    if num%7 == 1:
        print (185*'=')
        print (f'Page {page:}')
        print ('Date       Model      Ident   From To  Comments                       Ldgs  Gldr  Heli      SEL      MEL      X/C      Day    Night  Act.Ins.  Hooded   Dual R      PIC   Dual G    Total')

    print (f'{row['Date']:10} {row['Model']:10} ', end='')
    print (f'{row['AircraftID']:>6} {row['From']:>4} {row['To']:>4} ', end='')
    print (f'{row['PilotComments'][:30]:>30s} {int(row['AllLandings']):4d} ', end='')
    print (f'{row['Glider']:>5} {row['Helicopter']:>5} ', end='')
    print (f'{row['ASEL']:>8} {row['AMEL']:>8} ', end='')
    print (f'{row['CrossCountry']:>8} ', end='')
    print (f'{row['Day']:>8} {row['Night']:>8} ', end='')
    print (f'{row['ActualInstrument']:>8} {row['SimulatedInstrument']:>8} ', end='')
    print (f'{row['DualGiven']:>8} {row['PIC']:>8} ', end='')
    print (f'{row['DualReceived']:>8} ', end='')
    print (f'{row['TotalTime']:>8} ', end='')
    print ()
    if num%7 == 0:
        nlandings = df_flights.iloc[num-7:num]['AllLandings'].astype(int).sum()
        print (51*' ',133*'-')
        print (51*' ',f'Page Total       {nlandings:>5}')
        print (51*' ','Amount forward    0')
        print (51*' ','Total to date     0')
        print ()
