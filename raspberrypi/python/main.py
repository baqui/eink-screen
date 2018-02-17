##
 #  @filename   :   main.cpp
 #  @brief      :   7.5inch e-paper display demo
 #  @author     :   Yehui from Waveshare
 #
 #  Copyright (C) Waveshare     July 28 2017
 #
 # Permission is hereby granted, free of charge, to any person obtaining a copy
 # of this software and associated documnetation files (the "Software"), to deal
 # in the Software without restriction, including without limitation the rights
 # to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 # copies of the Software, and to permit persons to  whom the Software is
 # furished to do so, subject to the following conditions:
 #
 # The above copyright notice and this permission notice shall be included in
 # all copies or substantial portions of the Software.
 #
 # THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 # IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 # FITNESS OR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 # AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 # LIABILITY WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 # OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 # THE SOFTWARE.
 ##

import epd7in5b
import Image
import ImageDraw
import ImageFont
import csv
import os
#import imagedata

EPD_WIDTH = 640
EPD_HEIGHT = 384

def main():
    epd = epd7in5b.EPD()
    epd.init()

    skm_timetable_file = os.path.abspath("/home/pi/eink-screen/raspberrypi/python/skm.csv")
    image = Image.new('L', (EPD_WIDTH, EPD_HEIGHT), 255)    # 255: clear the frame
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 20)

    col_w = 60
    col_h = 39
    cols = 3
    rows = 6

    cal_w = 1 + ((col_w + 1) * cols)
    cal_h = 1 + ((col_h + 1) * rows)

    cal_x = EPD_WIDTH - cal_w - 2
    cal_y = 2

    # Paint out a black rectangle onto which we'll draw our canvas
    draw.rectangle((cal_x, cal_y, cal_x + cal_w - 1, cal_y + cal_h - 1), fill=0, outline=255)


    # Draw the vertical lines which separate the columns
    # and also draw the day names into the table header
    for x in range(cols):
        # Figure out the left edge of the column
        o_x = (col_w + 1) * x
        o_x += cal_x
        # Offset to the right side of the column and draw the vertical line
        o_x += col_w + 1
        draw.line((o_x, cal_y, o_x, cal_h), fill=255)

    # Draw the horizontal lines which separate the rows
    for y in range(rows):
        o_y = (col_h + 1) * y
        o_y += cal_y + col_h + 1
        draw.line((cal_x, o_y, cal_w + cal_x - 1, o_y), fill=255)

    skm_data = []

    skm_timetable = open(skm_timetable_file, 'r')
    skm_reader = csv.reader(skm_timetable, delimiter='\t', lineterminator='\n')

    for row in skm_reader:
        train_time = row[0].split(':')
        skm_data.append([train_time[0], train_time[1], row[1]])

    skm_from = 0
    skm_to = skm_from + rows
    closest_trains = skm_data[skm_from:skm_to]

    def print_digit(position, digit, colour):

        o_x, o_y = position
        draw.text((o_x, o_y), str(digit), font = font, fill = colour)

    def print_number(position, number, colour):

        for digit in str(number):
            print_digit(position, int(digit), colour)
            position = (position[0] + 8, position[1])


    for row, train in enumerate(closest_trains):
        y = (col_h + 1) * row
        y += cal_y + 1

        for col, number in enumerate(train):
            x = (col_w + 1) * col
            x += cal_x + 1
            number = number if int(number) >= 10 else '0' + str(int(number))
            print_number((x+3, y+3), str(number), 127 if col == 2 else 255)

    epd.display_frame(epd.get_frame_buffer(image))

if __name__ == '__main__':
    main()
