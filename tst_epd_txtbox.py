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

# txt in box ##############################################################################
# from mcauser's test code
import framebuf
fb_size = int(epd.width * epd.height / 8)
buf = bytearray(fb_size)
fb = framebuf.FrameBuffer(buf, epd.height, epd.width, framebuf.MONO_VLSB)

black = 0  # black/red
white = 1  # white

# display as much as this as fits in the box
along_string = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam vel neque in elit tristique vulputate at et dui. Maecenas nec felis lectus. Pellentesque sit amet facilisis dui. Maecenas ac arcu euismod, tempor massa quis, ultricies est.'

def text_wrap(fb1, str1, x, y, color, w, h, border=None, border_w=2):
    # optional box border
    if border is not None:
        fb1.rect(x, y, w, h, border)
    cols = ( w - border_w * 2 - 1 ) // 8
    # for each row
    j = 0
    for i in range(0, len(str1), cols):
        # draw as many chars fit on the line
        fb1.text(str1[i:i+cols], x + 1 + border_w, y + j + 1 + border_w, color)
        j += 8
        # dont overflow text outside the box
        if j >= h:
            break

## black frame
fb.fill(white)

# draw text box 1
# box position and dimensions
bx = 8
by = 8
bw = 296 - 16 # 112 = 14 cols
bh = 152 - 16 # 112 = 14 rows (196 chars in total)
text_wrap(fb, along_string, bx, by, black, bw, bh, black, border_w=3)

epd.send_frame_landscape(None, buf)
sleep(2)

## red frame
fb.fill(white)
fb.fill_rect(30, 110, 10, 10, black)
epd.send_frame_landscape(buf, None)
epd.display_frame()
