#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 16:11:37 2024

@author: dolan
"""
import sys
import csv
import pandas as pd

if len(sys.argv)==2:
    path = sys.argv[1]
else:
    print ("Need one argument: file name.")
    sys.exit (1)
    

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

columns = [
        {'key':  'Date',                 'pwidth': 11, 'fmt1': '{:<11}','fmt2': '{:<11s}',  'ptitle':'Date'},
        {'key':  'Model',                'pwidth': 10, 'fmt1': '{:<10}','fmt2': '{:<10s}',  'ptitle':'Model'},
        {'key':  'AircraftID',           'pwidth': 10, 'fmt1': '{:<10}','fmt2': '{:<10s}',  'ptitle':'Ident'},
        {'key':  'From',                 'pwidth':  5, 'fmt1': '{:<5}', 'fmt2': '{:<5s}',   'ptitle':'From'},
        {'key':  'To',                   'pwidth':  5, 'fmt1': '{:<5}', 'fmt2': '{:<5s}',   'ptitle':'To'},
        {'key':  'PilotComments',        'pwidth': 40, 'fmt1': '{:<40}','fmt2': '{:<40s}',  'ptitle':'Comments'},
        {'key':  'AllLandings',          'pwidth':  5, 'fmt1': '{:>5}', 'fmt2': '{:>5d}',   'ptitle':'Ldgs'},
        {'key':  'Glider',               'pwidth':  8, 'fmt1': '{:>8}', 'fmt2': '{:>8.1f}', 'ptitle':'Gldr'},
        {'key':  'Helicopter',           'pwidth':  8, 'fmt1': '{:>8}', 'fmt2': '{:>8.1f}', 'ptitle':'Heli'},
        {'key':  'SEL',                  'pwidth':  8, 'fmt1': '{:>8}', 'fmt2': '{:>8.1f}', 'ptitle':'SEL'},
        {'key':  'MEL',                  'pwidth':  8, 'fmt1': '{:>8}', 'fmt2': '{:>8.1f}', 'ptitle':'MEL'},
        {'key':  'CrossCountry',         'pwidth':  8, 'fmt1': '{:>8}', 'fmt2': '{:>8.1f}', 'ptitle':'X/C'},
        {'key':  'Day',                  'pwidth':  8, 'fmt1': '{:>8}', 'fmt2': '{:>8.1f}', 'ptitle':'Day'},
        {'key':  'Night',                'pwidth':  8, 'fmt1': '{:>8}', 'fmt2': '{:>8.1f}', 'ptitle':'Night'},
        {'key':  'ActualInstrument',     'pwidth':  8, 'fmt1': '{:>8}', 'fmt2': '{:>8.1f}', 'ptitle':'Inst'},
        {'key':  'SimulatedInstrument',  'pwidth':  8, 'fmt1': '{:>8}', 'fmt2': '{:>8.1f}', 'ptitle':'Hooded'},
        {'key':  'DualReceived',         'pwidth':  8, 'fmt1': '{:>8}', 'fmt2': '{:>8.1f}', 'ptitle':'Dual R'},
        {'key':  'PIC',                  'pwidth':  8, 'fmt1': '{:>8}', 'fmt2': '{:>8.1f}', 'ptitle':'PIC'},
        {'key':  'DualGiven',            'pwidth':  8, 'fmt1': '{:>8}', 'fmt2': '{:>8.1f}', 'ptitle':'Dual G'},
        {'key':  'TotalTime',            'pwidth':  8, 'fmt1': '{:>8}', 'fmt2': '{:>8.1f}', 'ptitle':'Total'},
    ]


keep=[]
for col in columns:
    keep.append(col['key'])

for dcol in df_flights.columns:
    if dcol not in keep:
        df_flights = df_flights.drop (dcol,axis=1)
        
df_flights['Glider'] = ''
df_flights['Helicopter'] = ''
df_flights['SEL'] = ''
df_flights['MEL'] = ''
df_flights['Day'] = ''
#df_flights['Category'] = ''
#df_flights = df_flights.assign (Category = lambda x: df_aircraft.loc[x['AircraftID']])
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
            df_flights.loc[index,'SEL'] = df_flights['TotalTime'].loc[index]
        elif aircraftCategory=='airplane_multi_engine_land':
            df_flights.loc[index,'MEL'] = df_flights['TotalTime'].loc[index]

        if df_flights['TotalTime'].loc[index] != '':
            if df_flights['TotalTime'].loc[index] and df_flights['Night'].loc[index]:
                day = float(df_flights['TotalTime'].loc[index]) - float(df_flights['Night'].loc[index])
            else:
                day = float(df_flights['TotalTime'].loc[index])
            df_flights.loc[index,'Day'] = f'{day:8.1f}'

for col in columns:
    df_flights.rename (columns={col['key']:col['ptitle']}, inplace=True)
    continue

df_flights = df_flights.replace('0.0','')

new = []
for col in columns:
    new.append (col['ptitle'])
    
df_flights = df_flights.reindex (columns=new)

if df_flights.loc[0]['Date'] > df_flights.loc[len(df_flights)-1]['Date']:
    df_flights = df_flights.iloc[::-1].reset_index(drop=True)

fmt_heading = 190*'=' + '\n' + 'Page {:}' + '\n'
for col in columns:
    width = int(col['fmt1'][3:-1])
    fmt_heading += col['fmt1'].format(col['ptitle'])[0:width]

###############################################################################
#
COL_NUMBERS_START = 6

tot_page    = [0]*len(columns)
tot_forward = [0]*len(columns)
tot_todate  = [0]*len(columns)

entnum = 0
for index, row in df_flights.iterrows():
    entnum += 1
    if entnum%7==1:
        page = int(entnum / 7 + 1)
        print (fmt_heading.format(page))

    for col in columns:
        val = row[col['ptitle']]
        width = int(col['fmt1'][3:-1])
        print (col['fmt1'].format(val)[0:width], end='')

    print()

    if entnum%7==0:
        df_page = df_flights[index-6:index+1]
        page_totals = df_page.sum(axis=0)
        print (65*' ', 124*'-')
        print (65*' ', 'Page total     ', end='')
        for  c in range(COL_NUMBERS_START,len(columns)):
            tot_page[c] = pd.to_numeric(df_page[columns[c]['ptitle']]).sum()
            str = columns[c]['fmt2'].format(tot_page[c])
            print (str, end='')
        print ()
        print (65*' ', 'Amt. forward   ', end='')
        for  c in range(COL_NUMBERS_START,len(columns)):
            str = columns[c]['fmt2'].format(tot_forward[c])
            print (str, end='')
        print ()
        print (65*' ', 'Total to date  ', end='')
        for  c in range(COL_NUMBERS_START,len(columns)):
            tot_todate[c] += tot_page[c]
            str = columns[c]['fmt2'].format(tot_todate[c])
            print (str, end='')
            tot_forward[c] = tot_todate[c]
            tot_page[c] = 0
        print ()
