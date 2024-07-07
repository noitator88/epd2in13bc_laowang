# initial display
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

epd.text('NanoBM initializing...', epd_x0, epd_y0, black)

import uasyncio, ntptime, os, utime, btree, network, ujson #, sh1106
from nanoweb import Nanoweb

# get my ip address
sta_if = network.WLAN(network.STA_IF)
ipaddr, netmask, gateway, dns = sta_if.ifconfig()

s = 'IP: {0}'.format(ipaddr)
epd.text(s, epd_x0, epd_y0 + epd_ch + epd_ls,black)

# set the correct local time via ntptime
ntp_ok = 0
try:
    ntptime.settime()
    ntp_ok = 1
    epd.text("NTP success!", epd_x0, epd_y0 + 2*epd_ch + 2*epd_ls, black)
except:
    ntp_ok = 0
    epd.text("NTP failed!", epd_x0, epd_y0 + 2*epd_ch + 2*epd_ls, black)    
    pass

def fill_zero(n):  
    if n < 10:  
        return '0' + str(n)
    else:  
        return str(n)

week={0:'Mon',1:'Tue',2:'Wed',3:'Thu',4:'Fri',5:'Sat',6:'Sun'}
def show_time():
    # fetch the time
    utc_epoch        = utime.mktime(utime.localtime())
    Y,M,D,H,m,S,W,DY = utime.localtime(utc_epoch + 28800)
    MD               = '%s-%s' % (fill_zero(M),fill_zero(D))
    WD               = week[W]
    Day              = '%s %s' % (MD, WD)
    Hm               = '%s:%s' % (fill_zero(H),fill_zero(m))

    return Day, Hm

# free disk space
def df():
    s = os.statvfs('//')
    return ('{0} MB'.format((s[0]*s[3])/1048576))

s = 'Free space : {0}'.format(df())
epd.text(s, epd_x0, epd_y0 + 3*epd_ch + 3*epd_ls, black)

# free memory space
def mem():
    s = gc.mem_free()
    return ('{0} KB'.format(s/1024))

s = 'Free memory : {0}'.format(mem())
epd.text(s, epd_x0, epd_y0 + 4*epd_ch + 4*epd_ls, black)

epd.show()

def text_wrap(fb1, str1, x, y, color, w, h, border=None, border_w=2):
    # optional box border
    if border is not None:
        fb1.rect(x, y, w, h, border)
    cols = ( w - border_w * 2 - 1 ) // 8
    # for each row
    j = 0
    txt_ls = 4
    for i in range(0, len(str1), cols):
        # draw as many chars fit on the line
        fb1.text(str1[i:i+cols], x + 1 + border_w, y + j + txt_ls + border_w, color)
        j += 8
        # dont overflow text outside the box
        if j >= h:
            break

# display as much as this as fits in the box
along_string = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam vel neque in elit tristique vulputate at et dui. Maecenas nec felis lectus. Pellentesque sit amet facilisis dui. Maecenas ac arcu euismod, tempor massa quis, ultricies est.'

# draw text box 1
# box position and dimensions
bx = 8
by = 8
bw = epd_w - 16 # 
bh = epd_h - 16 # 
text_wrap(epd, along_string, bx, by, black, bw, bh, white, border_w=1)

epd.show()