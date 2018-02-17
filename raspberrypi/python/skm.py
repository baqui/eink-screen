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
skm_date = '18  Luty, 2018'
skm_hour = '00:06'

url_base = 'http://www.skm.pkp.pl/pelny-rozklad-jazdy/'
quote = '?{0}{1}[action]=show&{0}{1}[controller]=Connection&{0}{1}[__referrer][@request]=a:3:{{s:13:"extensionName";s:18:"Fnxpassengercenter";s:14:"controllerName";s:10:"Connection";s:10:"actionName";s:4:"find";}}4d4cfc4571ff33e626c3e4cce1354b6601b85178&{0}{1}[__referrer][extensionName]=Fnxpassengercenter&{0}{1}[__referrer][controllerName]=Connection&{0}{1}[__referrer][actionName]=find&{0}{1}[__hmac]=a:12:{{s:12:"station-from";i:1;s:16:"station-through1";i:1;s:16:"station-through2";i:1;s:10:"station-to";i:1;s:4:"date";i:1;s:4:"time";i:1;s:13:"depart-arrive";i:1;s:13:"min-swap-time";i:1;s:13:"max-swap-time";i:1;s:17:"direct-connection";i:1;s:6:"action";i:1;s:10:"controller";i:1;}}3c30b2e5e154892f42bdef11e3b9d41745fa3027&{0}{1}[station-from]={2}&{0}{1}[station-through1]=&{0}{1}[station-through2]=&{0}{1}[station-to]={3}&{0}{1}[date]={4}&{0}{1}[time]={5}&{0}{1}[depart-arrive]=1&{0}{1}[min-swap-time]=0&{0}{1}[max-swap-time]=0&{0}{1}[direct-connection]=&{0}{1}[depart-date]=2018-02-17 {5}:00&{0}{1}[arrive-date]=&{0}[action]=showFullTimetable&{0}[controller]=Connection'
quote = quote.format('tx_fnxpassengercenter_fulltimetable', '[data]', skm_from, skm_to, skm_date, skm_hour).replace(' ', '%20')

page = urllib2.urlopen(url_base + quote)

soup = BeautifulSoup(page, 'html.parser')

elements = soup.find_all('div', attrs={'class': 'schedule__row'})

skm_timetable_file = os.path.abspath("/home/pi/eink-screen/raspberrypi/python/skm.csv")

with open(skm_timetable_file,'w') as f1:
    writer=csv.writer(f1, delimiter='\t',lineterminator='\n',)
    for index, el in enumerate(elements):
        hour = el.find('span', attrs={'class': 'schedule__hour'}).text
        minutes = el.find('span', attrs={'class': 'schedule__minutes'}).text
        train_type = el.find('span', attrs={'class': 'schedule__traintype'})
        train_type = train_type.text[1] if train_type else 0
        row = "{}:{} {}".format(hour, minutes, train_type).split(' ')
        print row
        writer.writerow(row)
