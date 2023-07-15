from machine import Pin, SPI
from time import sleep

spi = SPI(1, baudrate=4000000)  # 8000000 also works
spi.init()

import epaper2in13b
cs = Pin(15,Pin.OUT)
dc = Pin(4,Pin.OUT)
rst = Pin(5,Pin.OUT)
busy = Pin(16,Pin.IN)

epd = epaper2in13b.EPD(spi, cs, dc, rst, busy)
epd.init()

epd.clear_frame()

# custom font with writer ##############################################################################
# Peter Hinch's font
# ref: https://forum.micropython.org/viewtopic.php?f=18&t=6319&start=10
import framebuf
from writer import Writer
# create a dummy device so that writer can manipulate the framebuffer
class DummyDisplay(framebuf.FrameBuffer):
    def __init__(self, buffer, width, height, format):
        self.height = height
        self.width = width
        self.buffer = buffer
        self.format = format
        super().__init__(buffer, width, height, format)
import courier20, gc
gc.collect()  # gc to avoid memory overflow

# must use monospace font
# about 130 chars for courier20
# only works for one line
str_b = 'Lorem       dolor sit amet, consectetur adipiscing elit. Etiam vel , consectetur            elit. Etiam vel, consectetur adip 1 23'
str_r = '      ipsum '

fb_size = int(epd.width * epd.height / 8)
buf = bytearray(fb_size)
fb = DummyDisplay(buf, epd.height, epd.width, framebuf.MONO_VLSB)

black = 0  # black/red
white = 1  # white

fb.fill(white)

wri_b = Writer(fb, courier20, verbose=False) # verbose = False to suppress console output
wri_b.set_textpos(fb, 0, 0)
wri_b._printline(str_b, invert=True)

epd.send_frame_landscape(buf, None)
sleep(2)

## red frame
gc.collect()  # gc to avoid memory overflow
fb.fill(white)
 
wri_b.set_textpos(fb, 0, 0)
wri_b._printline(str_r, invert=True)

epd.send_frame_landscape(None, buf)

## refresh epd
epd.display_frame()

# power off
epd.sleep()
