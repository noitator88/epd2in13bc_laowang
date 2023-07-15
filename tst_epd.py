from machine import Pin, SPI
from time import sleep

spi = SPI(1, baudrate=4000000)  # 8000000 works
spi.init()

import epaper2in13b
cs = Pin(15,Pin.OUT)
dc = Pin(4,Pin.OUT)
rst = Pin(5,Pin.OUT)
busy = Pin(16,Pin.IN)

epd = epaper2in13b.EPD(spi, cs, dc, rst, busy)
epd.init()

# # basic test ##############################################################################
# ##epd.clear_frame()
# 
# # busy pin does not work, so just wait more than 12 scends
# import framebuf
# fb_size = int(epd.width * epd.height / 8)
# buf_b = bytearray(fb_size)
# buf_r = bytearray(fb_size)
# 
# fb_b = framebuf.FrameBuffer(buf_b, epd.width, epd.height, framebuf.MONO_HLSB)
# fb_r = framebuf.FrameBuffer(buf_r, epd.width, epd.height, framebuf.MONO_HLSB)
# black = 0
# white = 1
# # clear
# fb_b.fill(white)
# fb_r.fill(white)
# #fb_b.text('Hello Black World',10,30,black)
# #fb_r.text('Hello Red World',10,90,black)
# fb_b.rect(1, 1, 100, 100, black)
# fb_r.fill_rect(30, 110, 10, 10, black)
# 
# # one can display them together
# epd.send_frame(buf_b, buf_r)
# epd.display_frame()
# 
# # or one by one, this can save memory
# #epd.send_frame(buf_r, None)
# #epd.send_frame(None, buf_b)
# #epd.display_frame()



# # landscape mode test ##############################################################################
# 
# h = 152;  w = 296 # e-paper heigth and width. It will be used in landscape mode
# 
# buf_black        = bytearray(w * h // 8) # used by frame buffer (landscape)
# buf_epaper_black = bytearray(w * h // 8) # used to display on e-paper after bytes have been
# 
# import framebuf
# fb_black = framebuf.FrameBuffer(buf_black, w, h, framebuf.MONO_VLSB) #landscape
# fb_final_black = framebuf.FrameBuffer(buf_epaper_black, h, w, framebuf.MONO_HLSB) #portrait
# 
# black = 0 # will be black on buf_black, red on buf_red
# white = 1
# 
# #clear red & black screens, then write 
# fb_black.fill(white)
# fb_black.text('Hello world!', 5, 10, black)
# 
# ref: https://forum.micropython.org/viewtopic.php?f=18&t=6319#p36047
# Move frame buffer bytes to e-paper buffer to match e-paper bytes oranisation.
# That is landscape mode to portrait mode. (for red and black buffers) 
# x=0; y=0; n=1; R=0
# for 152x296
# 152/8 = 19
# for i in range(1, 20):
#     for j in range(1, 297):
#         R = (n-x)+((n-y)*18)
#         buf_epaper_black[R-1] = buf_black[n-1]
#         n +=1
#     x = n+i-1
#     y = n-1
# 
# the two lines do the same thing
# epd.send_frame(buf_epaper_black, None)
# #epd.send_frame_landscape(buf_black, None)
# 
# epd.display_frame()





# # txt + img ##############################################################################
# #
# import framebuf
# 
# # Load the array image into the framebuffer (the image is 32x32)
# pic = bytearray(b'\x00\x00\x00\x01\xff\xf0\x00\x00\x00\x00\x00\x7f\xc0?\xc0\x00\x00\x00\x03\xe0\x00\x01\xf8\x00\x00\x00\x1e\x00\x00\x00\x0f\x80\x00\x00x\x00\x00\x00\x01\xe0\x00\x01\xc0\x00\x00\x00\x00p\x00\x07\x00\x00\x00\x00\x00\x1c\x00\x0c\x00\x00\x00\x00\x00\x06\x008\x00\x00\x00\x00\x00\x18\x00`\x00\x00\x00\x00\x000\x01\xc0\x00\x00\x00\x00\x00\xe0\x01\x80\x00\x00\x00\x00\x01\xc0\x03\x00\x00\x00\x00\x00\x03\x00\x06\x00\x00\x00\x00\x00\x06\x00\x0c\x00\x00\x00\x00\x00\x18\x00\x18\x00\x00\x00\x00\x000\x00\x18\x00\x00\x00\x00\x00`\x000\x00\x00\x00\x00\x01\x80\x00 \x00\x00\x00\x00\x03\x00\x00`\x00\x00\x00\x00\x0e\x00\x00`\x00\x00\x00\x00\x1c\x00\x00@\x00\x00\x00\x000\x00\x00\xc0\x00\x00\x1f\x80`\x00\x00\xc3\xff\xf0q\xc1\x80\x00\x00\x82\x000`c\x00\x00\x00\x82\x000\x80.\x00\x00\x00\x83\x000\x806\x00\x00\x00\x82\x000\xc0#\x00\x00\x00\xc2\x00 `a\xc0\x00\x00\xc2\x00 {\xc0`\x00\x00\xc2\x000\x1f\x008\x00\x00B\x003\xff\xfc\x0c\x00\x00b\x002\xcc\xcc\x07\x00\x00c\x002\x00\x0c\x01\x80\x00"\x00"\x00\x0c\x00\xe0\x002\x00"\x00\x0c\x00p\x00\x1a\x002\x00\x0c\x00\x1c\x00\x1a\x002\x00\x0c\x00\x0e\x00\x0e\x002\x00\x0c\x00\x03\x00\x06\x002\x00\x0c\x00\x01\xc0\x03\x002\x00\x0c\x00\x00`\x02\x00"\x00\x0c\x00\x008\x03\x00"\x00\x0c\x00\x00\x1c\x02\x002\x00\x0c\x00\x00\x07\x02\x002\x00\x0c\x00\x00\x0e\x02\x002\x00\x0c\x00\x008\x02\x003\xff\xfc\x00\x00\xe0\x02\x000\x00\x00\x00\x07\x80\x02\x00>\x00\x00\x00>\x00\x03\x00\'\xc0\x00\x01\xf0\x00\x02\x000\xff\xff\xff\x00\x00\x02\x000\x07\xff\xf0\x00\x00\x02\x008a\x8c\x00\x00\x00\x02\x00?\xff\xfc\x00\x00\x00\x02\x00\x00\x00\x0c\x00\x00\x00\x02\x00\x00\x00\x0c\x00\x00\x00\x02\x00\x00\x00\x0c\x00\x00\x00\x02\x00\x00\x00\x0c\x00\x00\x00\x03\x00\x00\x00\x0c\x00\x00\x00\x02\x00\x00\x00\x0c\x00\x00\x00\x02\x00\x00\x00\x0c\x00\x00\x00\x02\x00\x00\x00\x0c\x00\x00\x00\x02\x00\x00\x00\x0c\x00\x00\x00\x03\xff\xff\xff\xfc\x00\x00\x00')
# fb_pic = framebuf.FrameBuffer(pic, 32, 32, framebuf.MONO_HLSB)
# 
# fb_size = int(epd.width * epd.height / 8)
# buf = bytearray(fb_size)
# 
# fb = framebuf.FrameBuffer(buf, epd.height, epd.width, framebuf.MONO_VLSB)
# 
# black = 0  # black/red
# white = 1  # white
# 
# # black frame
# fb.fill(white)
# fb.blit(fb_pic, 12, 12)
# epd.send_frame_landscape(buf, None)
# sleep(2)  # wait 15s
# 
# 
# # red frame
# fb.fill(white)
# fb.blit(fb_pic, 120, 120)
# epd.send_frame_landscape(None, buf)
# epd.display_frame()
# sleep(15)  # wait 15s
# 
# # power off
# epd.sleep()





# # ui design ##############################################################################
# #
# import framebuf
# fb_size = int(epd.width * epd.height / 8)
# buf = bytearray(fb_size)
# fb = framebuf.FrameBuffer(buf, epd.height, epd.width, framebuf.MONO_VLSB)
# 
# black = 0  # black/red
# white = 1  # white
# 
# # display as much as this as fits in the box
# along_string = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam vel neque in elit tristique vulputate at et dui. Maecenas nec felis lectus. Pellentesque sit amet facilisis dui. Maecenas ac arcu euismod, tempor massa quis, ultricies est.'
# 
# def text_wrap(fb1, str1, x, y, color, w, h, border=None, border_w=2):
#     # optional box border
#     if border is not None:
#         fb1.rect(x, y, w, h, border)
#     cols = ( w - border_w * 2 - 1 ) // 8
#     # for each row
#     j = 0
#     for i in range(0, len(str1), cols):
#         # draw as many chars fit on the line
#         fb1.text(str1[i:i+cols], x + 1 + border_w, y + j + 1 + border_w, color)
#         j += 8
#         # dont overflow text outside the box
#         if j >= h:
#             break
# 
# ## black frame
# fb.fill(white)
# 
# # draw text box 1
# # box position and dimensions
# bx = 8
# by = 8
# bw = 296 - 16 # 112 = 14 cols
# bh = 152 - 16 # 112 = 14 rows (196 chars in total)
# text_wrap(fb, along_string, bx, by, black, bw, bh, black, border_w=3)
# 
# epd.send_frame_landscape(None, buf)
# sleep(2)
# 
# ## red frame
# fb.fill(white)
# fb.fill_rect(30, 110, 10, 10, black)
# epd.send_frame_landscape(buf, None)
# epd.display_frame()
# sleep(15)  # wait 15s
# 
# # power off
# epd.sleep()




# # custom font with writer ##############################################################################
# # ref: https://forum.micropython.org/viewtopic.php?f=18&t=6319&start=10
# import framebuf
# from writer import Writer
# # create a dummy device so that writer can manipulate the framebuffer
# class DummyDisplay(framebuf.FrameBuffer):
#     def __init__(self, buffer, width, height, format):
#         self.height = height
#         self.width = width
#         self.buffer = buffer
#         self.format = format
#         super().__init__(buffer, width, height, format)
# import courier20, gc
# gc.collect()  # gc to avoid memory overflow
# 
# # must use monospace font
# # about 130 chars for courier20
# str_b = 'Lorem       dolor sit amet, consectetur adipiscing elit. Etiam vel , consectetur            elit. Etiam vel, consectetur adip 1 23'
# #str_r = '      ipsum                                                        ,             Etiam vel .'
# 
# fb_size = int(epd.width * epd.height / 8)
# buf = bytearray(fb_size)
# fb = DummyDisplay(buf, epd.height, epd.width, framebuf.MONO_VLSB)
# 
# black = 0  # black/red
# white = 1  # white
# 
# fb.fill(white)
# 
# wri_b = Writer(fb, courier20, verbose=False) # verbose = False to suppress console output
# wri_b.set_textpos(fb, 0, 0)
# wri_b._printline(str_b, invert=True)
# 
# epd.send_frame_landscape(buf, None)
# sleep(2)
# 
# ## red frame
# gc.collect()  # gc to avoid memory overflow
# fb.fill(white)
#  
# # wri_b.set_textpos(fb, 0, 0)
# # wri_b._printline(str_r, invert=True)
# 
# epd.send_frame_landscape(None, buf)
# 
# ## refresh epd
# epd.display_frame()
# sleep(15)  # wait 15s
# # power off
# epd.sleep()









# x=0; y=0; n=1; R=0
# # for 32x64
# # 32/8 = 4
# iw = 4
# ih = 64
# for i in range(1, iw+1):         # 3 + 1
#     for j in range(1, ih+1):     # 64 + 1
#         R = (n-x)+((n-y)*(iw-1)) # 3 - 1
#         R1 =  j * iw - i
#         #print("R - R1 = ", R - R1)        
#         j1 = (R1+1) // iw + 1
#         i1 = j1 * iw - R1
#         if (i1 > iw):
#             i1 = i1 - iw
#             j1 = j1 - 1
#         print(i, j, " = ", i1, j1)
#         n1 = (i-1)*ih+j-1
#         #print("n - n1 = ", n - n1)
#         n +=1
#     x = n+i-1
#     y = n-1

# x=0; y=0; n=1; R=0
# # for 32x64
# # 32/8 = 4
# for i in range(1, 5):       # 3 + 1
#     for j in range(1, 65):  # 64 + 1
#         R = n-x + j*3  # 3 - 1
#         #buf_epd[R-1] = buf_b[n-1]
#         #print("x, n = ", x, n+i-1)
#         n +=1  # n = (i-1)*64+j
#     #print("x, (i-1)*64 + i-1 :", x, (i-1)*64 + i-1)
#     x = n+i-1   # x = (i-1)*64 + i-1        