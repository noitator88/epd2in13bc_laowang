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

epd.clear_frame() # busy pin does not work, so just wait 12s

import framebuf
fb_size = int(epd.width * epd.height / 8)
buf_b = bytearray(fb_size)
buf_r = bytearray(fb_size)

fb_b = framebuf.FrameBuffer(buf_b, epd.width, epd.height, framebuf.MONO_HLSB)
fb_r = framebuf.FrameBuffer(buf_r, epd.width, epd.height, framebuf.MONO_HLSB)
black = 0
white = 1
# clear
fb_b.fill(white)
fb_r.fill(white)
fb_b.text('Hello Black World',10,30,black)
fb_r.text('Hello Red World',10,90,black)
fb_b.rect(10, 110, 100, 100, black)
fb_r.fill_rect(30, 240, 10, 10, black)

# one can display them together
epd.send_frame(buf_b, buf_r)
epd.display_frame()

# or one by one, this can save memory
#epd.send_frame(buf_r, None)
#epd.send_frame(None, buf_b)
#epd.display_frame()
