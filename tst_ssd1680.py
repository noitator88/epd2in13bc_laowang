# WIRING
# ESP8266  WeAct Studio 2.9" Black and White
# 16       BUSY
# 4        DC
# 5        RST
# 15       CS
# 13       SDA (MOSI)
# 14       SCL (SCK)

from machine import Pin, SPI
import gc

# WeAct Studio 2.9" Black and White ePaper display
from epd29_ssd1680 import EPD

dc = Pin(4, Pin.OUT, value=0)
rst_pin = 5
cs = Pin(15, Pin.OUT, value=1)
busy = Pin(16, Pin.IN)

spi = SPI(1, baudrate=10000000)
gc.collect()  # Precaution before instantiating framebuf
epd = EPD(spi, cs, dc, rst_pin, busy, landscape=True)

# clean the screen
black = 1
white = 0
epd.fill(white)
epd.show()

epd_x0 = 0
epd_y0 = 7
epd_w  = 250
epd_h  = 121
epd_ch = 8    # char hight
epd_ls = 2    # line space

# # fonts
# import courier20
# from writer import Writer
# wri = Writer(epd, courier20, verbose=False) # verbose = False to suppress console output
# wri.set_textpos(epd, 0, 7)
# s1 = 'Lorem       dolor sit amet, consectetur adipiscing elit. Etiam vel , consectetur            elit. Etiam vel, consectetur adip 1 23'
# wri._printline(s1, invert=True)
# epd.show()

# # simple geometry shape
# # (0, 7)
# #
# #           (250, 128)
# # landscape=True
# # maximum size of rect.
# epd.rect(0, 7, 250, 121, black) # (x, y, w, h)
# # diagonal line
# epd.line(0, 8, 250, 127, black) # (x1, y1, x2, y2)
# # anti-diagonal line
# epd.line(0, 127, 250, 8, black)
# epd.show()

# # simple text
# # default text hight 8
# # first line (0, 8)
# # last line  (0, 120)
# epd.text('Hello Black World',0,8,black)
# epd.text('Hello Black World Again',0,16,black)
# epd.text('Hello Black World Botton',0,120,black)
# epd.show()

# simple ui
def text_wrap(fb1, str1, x, y, color, w, h, border=None, border_w=2):
    # optional box border
    if border is not None:
        fb1.rect(x, y, w, h, border)
    cols = ( w - border_w * 2 - 1 ) // 8
    # for each row
    j = 0
    txt_ls = 1
    for i in range(0, len(str1), cols):
        # draw as many chars fit on the line
        fb1.text(str1[i:i+cols], x + 1 + border_w, y + j  + border_w, color)
        j += 8 + txt_ls
        # dont overflow text outside the box
        if j >= h:
            break

epd.fill(white)
epd.text('Title',0,8,black)
epd.hline(0, 18, 64, black)
# display as much as this as fits in the box
#along_string = '  Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam vel neque in elit tristique vulputate at et dui. Maecenas nec felis lectus. Pellentesque sit amet facilisis dui. Maecenas ac arcu euismod, tempor massa quis, ultricies est.'
along_string = """
Welcome! This is the documentation for MicroPython, last updated 05 Jul 2024.
"""

# draw text box 1
# box position and dimensions
bx = 8
by = 20
bw = epd_w - 16 # 
bh = epd_h - 16 # 
text_wrap(epd, along_string, bx, by, black, bw, bh, white, border_w=1)

epd.show()