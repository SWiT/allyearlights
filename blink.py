# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.
import time

from neopixel import *

import argparse
import signal
import sys
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



# Define functions which animate LEDs in various ways.

def colorWipe(strip, color, wait_ms=50):
	"""Wipe color across display a pixel at a time."""
	for i in range(strip.numPixels()):
		strip.setPixelColor(i, color)
		strip.show()
		time.sleep(wait_ms/1000.0)

def theaterChase(strip, color, wait_ms=50, iterations=10):
	"""Movie theater light style chaser animation."""
	for j in range(iterations):
		for q in range(3):
			for i in range(0, strip.numPixels(), 3):
				strip.setPixelColor(i+q, color)
			strip.show()
			time.sleep(wait_ms/1000.0)
			for i in range(0, strip.numPixels(), 3):
				strip.setPixelColor(i+q, 0)

def wheel(pos):
	"""Generate rainbow colors across 0-255 positions."""
	if pos < 85:
		return Color(pos * 3, 255 - pos * 3, 0)
	elif pos < 170:
		pos -= 85
		return Color(255 - pos * 3, 0, pos * 3)
	else:
		pos -= 170
		return Color(0, pos * 3, 255 - pos * 3)

def rainbow(strip, wait_ms=20, iterations=1):
	"""Draw rainbow that fades across all pixels at once."""
	for j in range(256*iterations):
		for i in range(strip.numPixels()):
			strip.setPixelColor(i, wheel((i+j) & 255))
		strip.show()
		time.sleep(wait_ms/1000.0)

def rainbowCycle(strip, wait_ms=20, iterations=5):
	"""Draw rainbow that uniformly distributes itself across all pixels."""
	for j in range(256*iterations):
		for i in range(strip.numPixels()):
			strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
		strip.show()
		time.sleep(wait_ms/1000.0)

def theaterChaseRainbow(strip, wait_ms=50):
	"""Rainbow movie theater light style chaser animation."""
	for j in range(256):
		for q in range(3):
			for i in range(0, strip.numPixels(), 3):
				strip.setPixelColor(i+q, wheel((i+j) % 255))
			strip.show()
			time.sleep(wait_ms/1000.0)
			for i in range(0, strip.numPixels(), 3):
				strip.setPixelColor(i+q, 0)

				
###########################################
				
				
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
	while True:
		# print ('Color wipe animations.')
		#colorWipe(strip, Color(255, 0, 0))  # Red wipe
		#colorWipe(strip, Color(0, 255, 0))  # Green wipe
		#colorWipe(strip, Color(0, 0, 255))  # Blue wipe
		
		#Valentine's Day colors
		colors = list()
		colors.append(Color(206,68,68))
		colors.append(Color(101,1,92))
		colors.append(Color(255,123,210))
		colors.append(Color(101,1,92))
		colors.append(Color(206,68,68))
		dealColors(strip, colors)
		
		# colors = list()
		# colors.append(Color(255,0,0))
		# colors.append(Color(0,255,0))
		# colors.append(Color(0,0,255))
		# dealColors(strip, colors)
		
		
		# print ('Theater chase animations.')
		# theaterChase(strip, Color(127, 127, 127))  # White theater chase
		# theaterChase(strip, Color(127,   0,   0))  # Red theater chase
		# theaterChase(strip, Color(  0,   0, 127))  # Blue theater chase
		# print ('Rainbow animations.')
		# rainbow(strip)
		# rainbowCycle(strip)
		# theaterChaseRainbow(strip)
