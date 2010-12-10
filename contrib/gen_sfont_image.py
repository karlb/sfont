#-*- coding:utf8 -*-
from PIL import Image, ImageDraw, ImageFont
import sys

if len(sys.argv) != 5:
  sys.exit("Usage: python font.py /path/to/font.ttf font_size(e.g. 11) font_color(e.g. 000000) /path/to/save/dir/")
fontpath = sys.argv[1]
fontsize = int(sys.argv[2])
fontcolor = sys.argv[3]
fontpng = sys.argv[4]
split = (fontcolor[0:2], fontcolor[2:4], fontcolor[4:6])
# setting the font string
text = "!\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~¡¿ÀÁÈÉÌÍÒÓÙÚÝÄËÏÖÜŸÂÊÎÔÛÅÃÕÑÆÇČĎĚĽĹŇÔŘŔŠŤŮŽàáèéìíòóùúýäëïöüÿâêîôûåãõñæçčďěľĺňôřŕšťžůðßÐÞþАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюяØøąćęłńśżźĄĆĘŁŃŚŻŹ"
# converting the string to utf-8
text = unicode(text, "utf-8")
# setting the font and it's size
font = ImageFont.truetype(fontpath, fontsize)
# getting the font height value
text_height = font.getsize("{")[1]+5
# setting text_width to 0 before calculating image width
text_width = 0
# start calculating width
for i in range(0,267):
  text_width = text_width+font.getsize(text[i])[0]
# creating a new image
img = Image.new('RGBA', (text_width+536, text_height), (0,0,0,0))
draw = ImageDraw.Draw(img)
# drawing the first 2 pixels of dividing line
draw.line(((0, 0),(1,0)), fill=(255, 0, 255))
# setting X position for the first symbol
start = 2

for i in range(0,267):
  draw.text((start, 4), text[i], font=font, fill=(int(split[0], 16), int(split[1], 16), int(split[2], 16)))
  sz = draw.textsize(text[i], font=font)
  start = start + sz[0]
  draw.line(((start, 0),(start+1,0)), fill=(255, 0, 255))
  start = start+2
del draw
img.save(fontpng+"font.png", "PNG")
