# AllYearLights
# Author: Matthew Switlik (switlikm@gmail.com)
#
# Date aware decorative lights

import time
from neopixel import *
import argparse
import signal
import sys
import datetime

def signal_handler(signal, frame):
    setAll(strip, Color(0,0,0))
    print "\nquit"
    sys.exit(0)

def opt_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', action='store_true', help='clear the display on exit')
    args = parser.parse_args()
    if args.c:
        signal.signal(signal.SIGINT, signal_handler)

# LED strip configuration:
LED_COUNT      = 150      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 80     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_STRIP      = ws.WS2811_STRIP_RGB   # Strip type and colour ordering

		
def getNextColor(colors):
	global currcolor, curroffset
	
	"""apply the current offset"""
	i = (currcolor + curroffset) % len(colors)
	
	color = colors[i]
	
	currcolor += 1
	currcolor = currcolor % len(colors)
	return color
	
def resetColor():
	global currcolor
	currcolor = 0

def nextOffset(colors):
	global curroffset, currcolor
	curroffset += 1
	curroffset = curroffset % len(colors)
	
def dealColors(strip, colors):
	global curroffset, currcolor
	"""Deal out each color and repeat the pattern across all pixels"""
	resetColor()
	for i in range(strip.numPixels()):
		color = getNextColor(colors)
		strip.setPixelColor(i, color)
	
	#print curroffset
	strip.show()
	time.sleep(1)
	nextOffset(colors)
		
def setAll(strip, color):
	"""Set all pixel to a given colors"""
	for i in range(strip.numPixels()):
		strip.setPixelColor(i, color)
	strip.show()
	
# Main program logic follows:
if __name__ == '__main__':
    # Process arguments
    opt_parse()

    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    currcolor = 0
    curroffset = 0

    print ('Press Ctrl-C to quit.')
    today = datetime.date.today()
    print "today:",today
    
    while True:
        today = datetime.date.today()
	#today = datetime.date(today.year, 4, 1)
        
        # Valentine's Day colors
        event = datetime.date(today.year, 2, 14)
        turnon = event - datetime.timedelta(days = 7)
        turnoff = event + datetime.timedelta(days = 1)
        if turnon <= today and today < turnoff:
            print "Valentine's Day"
            colors = list()
            colors.append(Color(206,68,68))
            colors.append(Color(101,1,92))
            colors.append(Color(255,123,210))
            colors.append(Color(101,1,92))
            colors.append(Color(206,68,68))
            dealColors(strip, colors)
            continue
            
        # St. Patrick's Day colors
        event = datetime.date(today.year, 3, 17)
        turnon = event - datetime.timedelta(days = 7)
        turnoff = event + datetime.timedelta(days = 1)
        if turnon <= today and today < turnoff:
            print "St. Patrick's Day"
            colors = list()
            colors.append(Color(0,255,0))
            colors.append(Color(160,216,0))
            colors.append(Color(7,128,20))
            dealColors(strip, colors)
            continue
            
        # Easter
        event = datetime.date(today.year, 4, 1)
        turnon = event - datetime.timedelta(days = 7)
        turnoff = event + datetime.timedelta(days = 1)
        if turnon <= today and today < turnoff:
            print "Easter"
            colors = list()
            colors.append(Color(255,197,177))
            colors.append(Color(68,255,222))
            colors.append(Color(200,255,183))
            colors.append(Color(255,235,48))
            colors.append(Color(255,48,48))
            dealColors(strip, colors)
            continue
        
        print "No Event" 
        setAll(strip, Color(0,0,0))
