#
# this reads two 1-wire sensors and the motherboard temperatures
# and displays them on the nokia 5110 using the adafruit libraries
#
# the sensor ids are hard-coded below because this is a total quickie
#
# errors are Vince's, not the original example author's....
#
# to use - call this periodically via cron, every fewminutes is 
# a reasonable value.  Temperatures don't change 'that' often.
#
# FWIW, I call it every 3 minutes
#
#---------------------------------------------------------------
#
# (original copyright from the Adafruit example programs)
#
#
# Copyright (c) 2014 Adafruit Industries
# Author: Tony DiCola
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
#--------------------------------------------------------------

from subprocess import *
from time import sleep, strftime
from datetime import datetime

import Adafruit_Nokia_LCD as LCD
import Adafruit_GPIO.SPI as SPI

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

# Raspberry Pi hardware SPI config:
DC = 23
RST = 24
SPI_PORT = 0
SPI_DEVICE = 0

# Hardware SPI usage:
disp = LCD.PCD8544(DC, RST, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=4000000))

# Software SPI usage (defaults to bit-bang SPI interface):
#disp = LCD.PCD8544(DC, RST, SCLK, DIN, CS)

# Initialize library.
###disp.begin(contrast=47)
###disp.begin(contrast=40)
disp.begin(contrast=35)

# Clear display.
disp.clear()
disp.display()

timeOfDay=datetime.now().strftime('%H:%M:%S\n')

# sensor 1,2,mobo values hardcoded
#  t1="123.45"
#  t2="234.56"
#  moboTemp = "345.67"

# get temps from sensors
devices=["28-000005ab3d0c","28-000005bbe53e"]
sensorNumber=0
temps=["unavailable","unavailable"]
for d in devices:
	filename="/sys/bus/w1/devices/" + d + "/w1_slave"
	tfile=open(filename)
	code=tfile.read()
	tfile.close()
	linetwo=code.split("\n")[1]
	tempdata=linetwo.split(" ")[9]
	temp=float(tempdata[2:])
	tempF=temp/1000 * 9/5 + 32
	temps[sensorNumber] = tempF
	sensorNumber+=1

#--- mobo temp --
cmd="/opt/vc/bin/vcgencmd measure_temp"
def run_cmd(cmd):
    p = Popen(cmd, shell=True, stdout=PIPE)
    output = p.communicate()[0]
    return output
moboTemp = run_cmd(cmd)
moboTemp=moboTemp.split("=")[1]
moboTemp=moboTemp.split("'")[0]
moboTemp=float(moboTemp)*9/5 + 32.00

text1 = "  " + timeOfDay
text2 = "  t1: " + str(temps[0])
text3 = "  t2: " + str(temps[1])
text4 = "  pi: " + str(moboTemp)

# create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
image = Image.new('1', (LCD.LCDWIDTH, LCD.LCDHEIGHT))
 
# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)
 
# Draw a white filled box to clear the image.
draw.rectangle((0,0,LCD.LCDWIDTH,LCD.LCDHEIGHT), outline=255, fill=255)
 
# Load default font.
font = ImageFont.load_default()
 
# Alternatively load a TTF font.
# Some nice fonts to try: http://www.dafont.com/bitmap.php
# font = ImageFont.truetype('Minecraftia.ttf', 8)
 
# Write some text.
draw.text((9,0 ), text1, font=font)
draw.text((0,14), text2, font=font)
draw.text((0,25), text3, font=font)
draw.text((0,36), text4, font=font)
 
# Display image.
disp.image(image)
disp.display()

#------------
