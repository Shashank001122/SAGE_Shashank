'''
from datetime import datetime
from lxml import html
import requests
import dateutil.parser as parser
import numpy as np
import pandas as pd

page = requests.get('https://en.wikipedia.org/wiki/2018_in_spaceflight#Orbital_launches')
tree = html.fromstring(page.text)


#Build the table for orbital#
table = tree.xpath('//table')[3]

#Fetch all the dates for 2019#
years = [item.text_content().replace("\n","") for item in table.xpath('./tbody/tr')[4:]]


datelist=[]
for i in range(len(years)):
    if years[i][0:2].isdigit() or years[i][0].isdigit() and years[i][3:5]!='th':
        datelist.append(years[i])
    elif 'Operational' in years[i].split()[-1] or 'Successful' in years[i].split()[-1] or 'En Route' in years[i].split()[-1]:
        datelist.append(years[i])
        
year_list=[]
for i in range(len(datelist)-1):
    if not datelist[i+1][0:2].isdigit() and datelist[i][0:2].isdigit() or not datelist[i+1][0].isdigit() and datelist[i][0].isdigit():
        date = parser.parse(datelist[i].split('[')[0])
        year_list.append(date.isoformat().replace('2020','2019'))

year_list=list(map(lambda x:x.split('T')[0]+'T00:00:00+00:00',year_list))
data_set = pd.DataFrame(year_list, columns=["date"])
data_set['value'] = data_set.groupby('date')['date'].transform('count')
data_set.drop_duplicates(subset=None, keep="first", inplace=True) 
data_set.to_csv('output.csv',index=False) 
'''

from datetime import datetime
from lxml import html
import requests
import dateutil.parser as parser
#text = 'Thu, 16 Dec 2010 12:14:05 +0000'
import numpy as np
import pandas as pd

page = requests.get('https://en.wikipedia.org/wiki/2019_in_spaceflight#Orbital_launches')
tree = html.fromstring(page.text)

table = tree.xpath('//table')[3]
years = [item.text_content().replace("\n","") for item in table.xpath('./tbody/tr')[4:]]

datelist=[]
for i in range(len(years)):
    if years[i].split()[0].isdigit():
        datelist.append(years[i])
    elif 'Operational' in years[i].split()[-1] or 'Successful' in years[i].split()[-1] or ('route' in years[i].split()[-1] and 'En' in years[i].split()[-2]):
        
        datelist.append(years[i])

#datelist

year_list=[]
for i in range(len(datelist)-1):
    if not datelist[i+1].split()[0].isdigit() and datelist[i].split()[0].isdigit():
        date = parser.parse(("".join(datelist[i].split()[0:2]).split("[")[0]))
        #print(date.isoformat())
        year_list.append(date.isoformat().replace('2020','2019'))

year_list=list(map(lambda x:x.split('T')[0]+'T00:00:00+00:00',year_list))
data_set = pd.DataFrame(year_list, columns=["date"])
data_set['value'] = data_set.groupby('date')['date'].transform('count')
data_set.drop_duplicates(subset=None, keep="first", inplace=True) 
f = open('output.csv', 'r')
try:
    data_set.to_csv('output.csv',index=False)         
finally:
    f.close()