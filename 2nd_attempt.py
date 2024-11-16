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

df_flights = df_flights.assign (TypeCode = lambda x: (df_aircraft.loc[x.loc[1]['AircraftID']]['TypeCode']))
df_flights['Glider'] = '0.0'
df_flights['Helicopter'] = '0.0'
df_flights['ASEL'] = '0.0'
df_flights['AMEL'] = '0.0'
df_flights['Day'] = '0.0'


for index, row in df_flights.iterrows():
    num = index+1
    page = num//7 + 1
    if num%7 == 1:
        print (183*'=')
        print (f'Page {page:}')
        print ('Date       Model    Ident   From To   Comments                       Ldgs  Gldr  Heli      SEL      MEL      X/C      Day    Night  Act.Ins.  Hooded   Dual R      PIC   Dual G    Total')

    print (f'{row['Date']:} {row['TypeCode']:>5} ', end='')
    print (f'{row['AircraftID']:>8s} {row['From']:>6} {row['To']:>6} ', end='')
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
    if (index+1)%7 == 0:
        print (52*' ',130*'-')
        print (52*' ','Page Total        0')
        print (52*' ','Amount forward    0')
        print (52*' ','Total to date     0')
        print ()
