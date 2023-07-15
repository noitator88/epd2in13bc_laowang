"""
MicroPython Waveshare 2.13" Black/White/Red GDEW0213Z16 e-paper display driver
https://github.com/mcauser/micropython-waveshare-epaper

Modified for a cheap epd : https://item.taobao.com/item.htm?spm=a1z09.2.0.0.7ef72e8dOGFu9a&id=704511276535&_u=f1la2tr06c8
The epd is driven by the breakout board : https://item.taobao.com/item.htm?spm=a1z09.2.0.0.7ef72e8dOGFu9a&id=680144088419&_u=f1la2tr653e

At this time, the busy pin does not work. It keeps at LOW level when the epd is powered on (via \x04 command) and never return to HIGH before the epd is powered off (\x02 command).

I include a landscape mode, which is modified from the code given by JumpZero @ https://forum.micropython.org/viewtopic.php?f=18&t=6319#p36047
"""

from micropython import const
from time import sleep_ms
import ustruct

# Display resolution
EPD_WIDTH  = const(152)
EPD_HEIGHT = const(296)

# Display commands
PANEL_SETTING                  = const(0x00)
POWER_SETTING                  = const(0x01)
POWER_OFF                      = const(0x02)
#POWER_OFF_SEQUENCE_SETTING     = const(0x03)
POWER_ON                       = const(0x04)
#POWER_ON_MEASURE               = const(0x05)
BOOSTER_SOFT_START             = const(0x06)
#DEEP_SLEEP                     = const(0x07)
DATA_START_TRANSMISSION_1      = const(0x10)
#DATA_STOP                      = const(0x11)
DISPLAY_REFRESH                = const(0x12)
DATA_START_TRANSMISSION_2      = const(0x13)
VCOM_AND_DATA_INTERVAL_SETTING = const(0x50)
RESOLUTION_SETTING             = const(0x61)
VCM_DC_SETTING                 = const(0x82)
#PARTIAL_WINDOW                 = const(0x90)
PARTIAL_IN                     = const(0x91)
PARTIAL_OUT                    = const(0x92)
#PROGRAM_MODE                   = const(0xA0)
#ACTIVE_PROGRAM                 = const(0xA1)
#READ_OTP_DATA                  = const(0xA2)
#POWER_SAVING                   = const(0xE3)

BUSY = const(0)  # 0=busy, 1=idle

class EPD:
    def __init__(self, spi, cs, dc, rst, busy):
        self.spi = spi
        self.cs = cs
        self.dc = dc
        self.rst = rst
        self.busy = busy
        self.cs.init(self.cs.OUT, value=1)
        self.dc.init(self.dc.OUT, value=0)
        self.rst.init(self.rst.OUT, value=0)
        self.busy.init(self.busy.IN)
        self.width = EPD_WIDTH
        self.height = EPD_HEIGHT

    def _command(self, command, data=None):
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([command]))
        self.cs(1)
        if data is not None:
            self._data(data)

    def _data(self, data):
        self.dc(1)
        self.cs(0)
        self.spi.write(data)
        self.cs(1)

    def init(self):
        self.reset()
        self._command(BOOSTER_SOFT_START, b'\x17\x17\x17')
        self._command(POWER_ON)
        #self.wait_until_idle()  # busy pin remains LOW after POWER_ON
        self._command(PANEL_SETTING, b'\x8F') # (128x296, LUT from OTP, B/W/R, scan up, shift right, booster on)
        self._command(VCOM_AND_DATA_INTERVAL_SETTING, b'\x37') # may choose '\x37', '\x77', '\xf0', we choose '\x77' from gxepd2
        self._command(RESOLUTION_SETTING, ustruct.pack(">BH", EPD_WIDTH, EPD_HEIGHT))
        # here width < 256, and height can larger than 256, so this command write "width", "height/256" and "height & 256" in sequence

    def wait_until_idle(self):
        while self.busy.value() == BUSY:
            sleep_ms(100)

    def reset(self):
        self.rst(0)
        sleep_ms(10)
        self.rst(1)
        sleep_ms(200)

    def send_frame(self, frame_buffer_black, frame_buffer_red):
        #self._command(PARTIAL_IN)        
        if (frame_buffer_black != None):
            self._command(DATA_START_TRANSMISSION_1)
            sleep_ms(2)
            for i in range(0, self.width * self.height // 8):
                self._data(bytearray([frame_buffer_black[i]]))
            sleep_ms(2)
        if (frame_buffer_red != None):
            self._command(DATA_START_TRANSMISSION_2)
            sleep_ms(2)
            for i in range(0, self.width * self.height // 8):
                self._data(bytearray([frame_buffer_red[i]]))
            sleep_ms(2)
        #self._command(PARTIAL_OUT)
        
        #self._command(DISPLAY_REFRESH)
        #self.wait_until_idle()

    def send_frame_landscape(self, buf_b, buf_r):
        w = self.height
        h = self.width
        if (buf_b != None):

## this approach use an auxiliary buffer following JumpZero, which is not needed.
#        buf_epd = bytearray(w * h // 8)
# method 1:
#             x=0; y=0; n=1; R=0
#             # for 152x296
#             # 152/8 = 19
#             for i in range(1, 20):
#                 for j in range(1, 297):
#                     #R = (n-x)+((n-y)*18)
#                     #R = (n-x) + j*18
#                     R =  j - i + 1 + j*18
#                     buf_epd[R-1] = buf_b[n-1]
#                     n +=1
#                 x = n+i-1
#                 #y = n-1
# method 2:
#             for i in range(1, h//8+1):  # 20 = 19 + 1
#                 for j in range(1, w+1):  # 297 = 296 + 1
#                     R1 =  j * (h//8) - i
#                     n1 = (i-1) * w + j - 1
#                     buf_epd[R1] = buf_b[n1]
                
            self._command(DATA_START_TRANSMISSION_1)
            sleep_ms(2)
# use the auxiliary buffer:
#             for i in range(0, self.width * self.height // 8):
#                 self._data(bytearray([buf_epd[i]]))

# without auxiliary buffer:
            for R1 in range(0, self.width * self.height // 8):
                j1 = (R1+1) // (h//8) + 1
                i1 = j1 * (h//8) - R1
                if i1 > (h//8):
                    i1 = i1 - (h//8)
                    j1 = j1 - 1
                n1 = (i1-1) * w + j1 - 1
                self._data(bytearray([buf_b[n1]]))
                
            sleep_ms(2)
        if (buf_r != None):                
            self._command(DATA_START_TRANSMISSION_2)
            sleep_ms(2)
            for R1 in range(0, self.width * self.height // 8):
                j1 = (R1+1) // (h//8) + 1
                i1 = j1 * (h//8) - R1
                if i1 > (h//8):
                    i1 = i1 - (h//8)
                    j1 = j1 - 1
                n1 = (i1-1) * w + j1 - 1
                self._data(bytearray([buf_r[n1]]))
            sleep_ms(2)
        
        #self._command(DISPLAY_REFRESH)
        #self.wait_until_idle() # busy pin do not work

    def clear_frame(self):
        self._command(DATA_START_TRANSMISSION_1)
        sleep_ms(2)
        for i in range(0, self.width * self.height // 8):
            self._data(b'\xff')
        sleep_ms(2)
        self._command(DATA_START_TRANSMISSION_2)
        sleep_ms(2)
        for i in range(0, self.width * self.height // 8):
            self._data(b'\xff')
        sleep_ms(2)
        
        self._command(DISPLAY_REFRESH)
        #self.wait_until_idle()  # busy pin do not work
        sleep_ms(12000)  # I takes ~12s to refresh the whole epd

    def display_frame(self):
        self._command(DISPLAY_REFRESH)
        #self.wait_until_idle()
        sleep_ms(12000)

    # to wake call reset() or init()
    def sleep(self):
        self._command(VCOM_AND_DATA_INTERVAL_SETTING, b'\x37')
        self._command(VCM_DC_SETTING, b'\x00') # to solve Vcom drop
        self._command(POWER_SETTING, b'\x02\x00\x00\x00') # gate switch to external
        # self.wait_until_idle()  # busy pin do not work
        sleep_ms(200)
        self._command(POWER_OFF)
