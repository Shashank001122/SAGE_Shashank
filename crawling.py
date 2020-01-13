from datetime import datetime
from lxml import html
import requests
import dateutil.parser as parser
import numpy as np
import pandas as pd

page = requests.get('https://en.wikipedia.org/wiki/2019_in_spaceflight#Orbital_launches')
tree = html.fromstring(page.text)


#Build the table for orbital#
table = tree.xpath('//table')[3]

#Fetch all the dates for 2019#
years = [item.text_content().replace("\n","") for item in table.xpath('./tbody/tr')[4:]]


datelist=[]
for i in range(len(years)):
    if years[i][0:2].isdigit() and years[i][3:5]!='th':
        datelist.append(years[i])
    elif 'Operational' in years[i].split()[-1] or 'Successful' in years[i].split()[-1] or 'En Route' in years[i].split()[-1]:
        datelist.append(years[i])
        
year_list=[]
for i in range(len(datelist)-1):
    if not datelist[i+1][0:2].isdigit() and datelist[i][0:2].isdigit():
        date = parser.parse(datelist[i].split('[')[0])
        year_list.append(date.isoformat().replace('2020','2019'))

year_list=list(map(lambda x:x.split('T')[0]+'T00:00:00+00:00',year_list))
data_set = pd.DataFrame(year_list, columns=["date"])
data_set['value'] = data_set.groupby('date')['date'].transform('count')
data_set.drop_duplicates(subset=None, keep="first", inplace=True) 
data_set.to_csv('output.csv',index=False) 