#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import time
import calendar
import csv
from PIL import Image, ImageFont
import inkyphat
import os


# INIT
inkyphat.set_border(inkyphat.BLACK)
skm_timetable_file = os.path.abspath("/home/pi/eink-screen/raspberrypi/python/skm.csv")
calendar_file = os.path.abspath("/home/pi/inky/examples/resources/calendar.png")
background_file = os.path.abspath("/home/pi/inky/examples/resources/empty-backdrop.png")

text = Image.open(calendar_file)
text_mask = inkyphat.create_mask(text, [inkyphat.WHITE])
inkyphat.set_image(background_file)

col_w = 20
col_h = 13
cols = 3
rows = 6

cal_w = 1 + ((col_w + 1) * cols)
cal_h = 1 + ((col_h + 1) * rows)

cal_x = inkyphat.WIDTH - cal_w - 2
cal_y = 2

# Paint out a black rectangle onto which we'll draw our canvas
inkyphat.rectangle((cal_x, cal_y, cal_x + cal_w - 1, cal_y + cal_h - 1), fill=inkyphat.BLACK, outline=inkyphat.WHITE)


# Draw the vertical lines which separate the columns
# and also draw the day names into the table header
for x in range(cols):
    # Figure out the left edge of the column
    o_x = (col_w + 1) * x
    o_x += cal_x
    # Offset to the right side of the column and draw the vertical line
    o_x += col_w + 1
    inkyphat.line((o_x, cal_y, o_x, cal_h))

# Draw the horizontal lines which separate the rows
for y in range(rows):
    o_y = (col_h + 1) * y
    o_y += cal_y + col_h + 1
    inkyphat.line((cal_x, o_y, cal_w + cal_x - 1, o_y))

def print_digit(position, digit, colour):

    o_x, o_y = position

    num_margin = 2
    num_width = 6
    num_height = 7

    s_y = 11
    s_x = num_margin + (digit * (num_width + num_margin))

    sprite = text_mask.crop((s_x, s_y, s_x + num_width, s_y + num_height))

    inkyphat.paste(colour, (o_x, o_y), sprite)

def print_number(position, number, colour):

    for digit in str(number):
        print_digit(position, int(digit), colour)
        position = (position[0] + 8, position[1])

#TODO get data from skm.csv 6 first rows

skm_data = []

skm_timetable = open(skm_timetable_file, 'r')
skm_reader = csv.reader(skm_timetable, delimiter='\t', lineterminator='\n')

for row in skm_reader:
    train_time = row[0].split(':')
    skm_data.append([train_time[0], train_time[1], row[1]])

skm_from = 0
skm_to = skm_from + rows
closest_trains = skm_data[skm_from:skm_to]

for row, train in enumerate(closest_trains):
    y = (col_h + 1) * row
    y += cal_y + 1

    for col, number in enumerate(train):
        x = (col_w + 1) * col
        x += cal_x + 1
        number = number if int(number) >= 10 else '0' + str(int(number))
        if int(train[2]) == 1:
            draw.rectangle((x, y, x + col_w - 1, y + col_h - 1), fill=127)
            print_number((x+3, y+3), number, 255 if col == 2 else 0)
        else:
            print_number((x+3, y+3), number, 0 if col == 2 else 127)

# And show it!
inkyphat.show()
