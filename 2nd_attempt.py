#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 16:11:37 2024

@author: dolan
"""

import csv
import pandas as pd

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
            df_flights.loc[index,'SEL'] = df_flights['TotalTime'].loc[index]
        elif aircraftCategory=='airplane_multi_engine_land':
            df_flights.loc[index,'MEL'] = df_flights['TotalTime'].loc[index]
        if df_flights['TotalTime'].loc[index] and df_flights['Night'].loc[index]:
            day = float(df_flights['TotalTime'].loc[index]) - float(df_flights['Night'].loc[index])
            df_flights.loc[index,'Day'] = f'{day:8.1f}'


if df_flights.loc[0]['Date'] > df_flights.loc[len(df_flights)-1]['Date']:
    df_flights = df_flights.iloc[::-1]      # reverse order of rows


columns = [
        {'key':  'Date',                 'type': 'date',  'pwidth': 11, 'ptitle':'Date'},
        {'key':  'Model',                'type': 'text',  'pwidth': 10, 'ptitle':'Model'},
        {'key':  'AircraftID',           'type': 'text',  'pwidth': 10, 'ptitle':'Ident'},
        {'key':  'From',                 'type': 'text',  'pwidth':  5, 'ptitle':'From'},
        {'key':  'To',                   'type': 'text',  'pwidth':  5, 'ptitle':'To'},
        {'key':  'PilotComments',        'type': 'text',  'pwidth': 40, 'ptitle':'Comments'},
        {'key':  'AllLandings',          'type': 'int',   'pwidth':  5, 'ptitle':'Ldgs'},
        {'key':  'Glider',               'type': 'float', 'pwidth':  8, 'ptitle':'Gldr'},
        {'key':  'Helicopter',           'type': 'float', 'pwidth':  8, 'ptitle':'Heli'},
        {'key':  'SEL',                  'type': 'float', 'pwidth':  8, 'ptitle':'SEL'},
        {'key':  'MEL',                  'type': 'float', 'pwidth':  8, 'ptitle':'MEL'},
        {'key':  'CrossCountry',         'type': 'float', 'pwidth':  8, 'ptitle':'X/C'},
        {'key':  'Day',                  'type': 'float', 'pwidth':  8, 'ptitle':'Day'},
        {'key':  'Night',                'type': 'float', 'pwidth':  8, 'ptitle':'Night'},
        {'key':  'ActualInstrument',     'type': 'float', 'pwidth':  8, 'ptitle':'Act.Ins.'},
        {'key':  'SimulatedInstrument',  'type': 'float', 'pwidth':  8, 'ptitle':'Hooded'},
        {'key':  'DualReceived',         'type': 'float', 'pwidth':  8, 'ptitle':'Dual R'},
        {'key':  'PIC',                  'type': 'float', 'pwidth':  8, 'ptitle':'PIC'},
        {'key':  'DualGiven',            'type': 'float', 'pwidth':  8, 'ptitle':'Dual G'},
        {'key':  'TotalTime',            'type': 'float', 'pwidth':  8, 'ptitle':'Total'},
    ]

###############################################################################
#
def printLogEntries (df_flights):
    COL_NUMBERS_START = 7
    tot_page    = [0]*len(columns)
    tot_forward = [0]*len(columns)
    tot_todate  = [0]*len(columns)
    for c in range(COL_NUMBERS_START-1,len(columns)):
        if columns[c]['type']=='int':
            tot_forward[c] = 0
        elif columns[c]['type']=='float':
            tot_forward[c] = 0.0


    entnum = 0
    for index, row in df_flights.iterrows():
        entry = row
        entnum += 1
        page = int(entnum / 7 + 1)
        if entnum%7==1:
            print ()
            print (190*'=')
            print ('Page ', page)
            c = 0
            for col in columns:
                c += 1
#                if col['type']==int or col['type']==float:
                if c>=COL_NUMBERS_START:
                    print ('{:>{wid}s}'.format(col['ptitle'],wid=col['pwidth']), end='')
                else:
                    print ('{:<{wid}s}'.format(col['ptitle'],wid=col['pwidth']), end='')
            print ()

        c = 0
        for col in columns:
            val = entry[col['key']]
            typ = col['type']
            pwidth = col['pwidth']
            if typ=='date':
                str = '{:{wid}s}'.format(val,wid=pwidth)
            elif typ=='text':
                if len(val)>pwidth: val = val[0:pwidth]
                str = '{:{wid}s}'.format(val,wid=pwidth)
            elif typ=='int':
                try:
                    str = '{:>{wid}d}'.format(val,wid=pwidth)
                    tot_page[c] += val
                except:
                    str = '{:>{wid}s}'.format(val,wid=pwidth)
                    if val != '':
                        tot_page[c] += int(val)
            elif typ=='float':
                try:
                    str = '{:>{wid}.1f}'.format(val,wid=pwidth)
                    tot_page[c] += val
                except:
                    str = '{:>{wid}s}'.format(val,wid=pwidth)
                    if val != '':
                        tot_page[c] += float(val)
            else:
                str = 'xxxxx'
            print (str, sep='', end='')
            c += 1
        print ()
        if entnum%7==0:
            print (66*' ', 123*'-')
            print (66*' ', 'Page total    ', end='')
            for  c in range(COL_NUMBERS_START-1,len(columns)):
                if columns[c]['type']=='int':
                    str = '{:{wid}d}'.format(tot_page[c],wid=columns[c]['pwidth'])
                elif columns[c]['type']=='float':
                    str = '{:{wid}.1f}'.format(tot_page[c],wid=columns[c]['pwidth'])
                else:
                    str = 'yyyyy'
                print (str, sep='', end='')
            print ()
            print (66*' ', 'Amt. forward  ', end='')
            for  c in range(COL_NUMBERS_START-1,len(columns)):
                if columns[c]['type']=='int':
                    str = '{:{wid}d}'.format(tot_forward[c],wid=columns[c]['pwidth'])
                elif columns[c]['type']=='float':
                    str = '{:{wid}.1f}'.format(tot_forward[c],wid=columns[c]['pwidth'])
                else:
                    str = 'yyyyy'
                print (str, sep='', end='')
            print ()
            print (66*' ', 'Total to date ', end='')
            for  c in range(COL_NUMBERS_START-1,len(columns)):
                tot_todate[c] += tot_page[c]
                if columns[c]['type']=='int':
                    str = '{:{wid}d}'.format(tot_todate[c],wid=columns[c]['pwidth'])
                elif columns[c]['type']=='float':
                    str = '{:{wid}.1f}'.format(tot_todate[c],wid=columns[c]['pwidth'])
                else:
                    str = 'yyyyy'
                print (str, sep='', end='')
                tot_forward[c] = tot_todate[c]
                tot_page[c] = 0
            print ()



printLogEntries (df_flights)
