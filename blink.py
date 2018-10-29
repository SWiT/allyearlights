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
import json
import os


# Signal Handler for clearing LEDs on exit
def signal_handler(signal, frame):
    leds.setAll(Color(0,0,0))
    print "\nClear LEDs and quit."
    sys.exit(0)
    return
    
# Parse any command line arguments or options 
def parseCommandLine():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', action='store_true', help='clear the display on exit')
    args = parser.parse_args()
    if args.c:
        signal.signal(signal.SIGINT, signal_handler)
    return    
        
class AllYearLights:

    def __init__(self):
        # LED strip configuration:
        LED_COUNT      = 150      # Number of LED pixels.
        LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
        LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
        LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
        LED_BRIGHTNESS = 10     # Set to 0 for darkest and 255 for brightest
        LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
        LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
        LED_STRIP      = ws.WS2811_STRIP_RGB   # Strip type and colour ordering
    
        # Create NeoPixel object with appropriate configuration.
        self.strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
        # Intialize the library (must be called once before other functions).
        self.strip.begin()
        self.colors = list()
        self.currcolor = 0
        self.curroffset = 0
        
        return
    
    def getSchedule(self):
        dirpath = os.path.dirname(os.path.realpath(__file__))
        with open(dirpath + '/schedule.json') as f:
            self.schedule = json.load(f)
            f.close()
        print "Schedule loaded."
        return
    
    def getToday(self):
        self.today = datetime.date.today()
		#self.today = datetime.date(today.year, 4, 1)
        print "Today:", self.today, datetime.datetime.now().time()
        return
    
    def getEvents(self):
        today =  self.today
        found = False
        for holiday in self.schedule:
            event = datetime.date(today.year, holiday['month'], holiday['day'])
            turnon = event - datetime.timedelta(days = holiday['daysprior'])
            turnoff = event + datetime.timedelta(days = holiday['daysafter'])
            if turnon <= today and today < turnoff:
                print holiday['name']
                colors = list()
                for c in holiday['colors']:
                    print c
                    colors.append(Color(c[0],c[1],c[2]))
                self.setColors(colors)
                self.dealColors()
                found = True
                continue    
        if not found:
            print "No Event" 
            self.setAll(Color(0,0,0))
        return
        
    def getNextColor(self):
        """apply the current offset"""
        i = (self.currcolor + self.curroffset) % len(self.colors)
        color = self.colors[i]
        self.currcolor += 1
        self.currcolor = self.currcolor % len(self.colors)
        return color
        return
    
    def resetColor(self):
        self.currcolor = 0
        return
        
    def nextOffset(self):
        self.curroffset += 1
        self.curroffset = self.curroffset % len(self.colors)
        return
        
    def setColors(self, colors):
        self.colors = colors
        return
        
    def dealColors(self):
        """Deal out each color and repeat the pattern across all pixels"""
        self.resetColor()
        for i in range(self.strip.numPixels()):
            color = self.getNextColor()
            self.strip.setPixelColor(i, color)
        self.strip.show()
        time.sleep(1)
        self.nextOffset()
        return
        
    def setAll(self, color):
        """Set all pixel to a given colors"""
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, color)
        self.strip.show()
        return
        
    def runLights(self):
        self.getToday()
        self.getSchedule()
        self.getEvents()
        return
	
# Main program logic follows:
if __name__ == '__main__':
    # Process arguments
    parseCommandLine()
    
    # Initialize the LEDPi object
    print "AllYearLights"
    leds = AllYearLights()
    print "Press Ctrl-C to quit."

    while True:
        leds.runLights()
        pass
