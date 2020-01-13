
from datetime import datetime
from lxml import html
import requests
import dateutil.parser as parser
import numpy as np
import pandas as pd

page = requests.get('https://en.wikipedia.org/wiki/2019_in_spaceflight#Orbital_launches')
tree = html.fromstring(page.text)


#construct a table#
table = tree.xpath('//table')[3]

#get all the rows from the table#
years = [item.text_content().replace("\n","") for item in table.xpath('./tbody/tr')[4:]]


'''
a list of rows which has either digits in the beginning or 
keywords like Operational, Successful and Enroute in the last column
'''
datelist=[]
for i in range(len(years)):
    if years[i].split()[0].isdigit():
        datelist.append(years[i])
    elif 'Operational' in years[i].split()[-1] or 'Successful' in years[i].split()[-1] or ('route' in years[i].split()[-1] and 'En' in years[i].split()[-2]):
        
        datelist.append(years[i])

# iterating in the list of rows of the datelist and checking if the row next to the current row has date in the beginning#        
year_list=[]
for i in range(len(datelist)-1):
    if not datelist[i+1].split()[0].isdigit() and datelist[i].split()[0].isdigit():
        date = parser.parse(("".join(datelist[i].split()[0:2]).split("[")[0]))
        year_list.append(date.isoformat().replace('2020','2019'))

#formatting the output, as mentioned in the question, overode the times with default T00:00:00+00:00 for all the dates        
year_list=list(map(lambda x:x.split('T')[0]+'T00:00:00+00:00',year_list))

#using dataframes on the year list
data_set = pd.DataFrame(year_list, columns=["date"])

#keeping track of the count of all the dates
data_set['value'] = data_set.groupby('date')['date'].transform('count')

#removing duplicates from the dataframe
data_set.drop_duplicates(subset=None, keep="first", inplace=True) 

f = open('output.csv', 'r')
try:
    data_set.to_csv('output.csv',index=False)         
finally:
    f.close()