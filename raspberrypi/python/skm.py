#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# SKM scrapper

import urllib2
import urllib
import csv
from datetime import datetime
from bs4 import BeautifulSoup
import os

skm_from = '6064' #Gdynia Leszcznki
skm_to = '7567' #Gdańsk śródmieście
skm_date = '2018-02-19'
skm_hour = datetime.today().strftime('%Y-%m-%d')

url_base = 'https://skm.trojmiasto.pl/rozklad/'
quote = '?from={0}&to={1}&date_mode=1&date={2}&hour={3}&via1=0&via2=0&time_min=&time_max='
quote = quote.format(skm_from, skm_to, skm_date, skm_hour).replace(':', '%3A')

page = urllib2.urlopen(url_base + quote)

soup = BeautifulSoup(page, 'html.parser')

elements = soup.find_all('div', attrs={'class': 'timetable'})

skm_timetable_file = os.path.abspath("/home/pi/eink-screen/raspberrypi/python/skm.csv")

with open(skm_timetable_file,'w') as f1:
    writer=csv.writer(f1, delimiter='\t',lineterminator='\n',)
    for index, el in enumerate(elements):
        hour = el.find('h3').text
        train_type = el.find('p', attrs={'class': 'line-symbol'})
        train_type = train_type.text[1] if train_type else 0
        row = [hour, train_type]
        print row
        writer.writerow(row)
