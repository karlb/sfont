#!/usr/bin/env python
# -*- coding: ascii -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
#
"""SFont image generator.
Converts a TTF into an Image suitable for use with SFont and SDL.
See http://www.linux-games.com/sfont/
"""

import os
import sys
from PIL import Image, ImageDraw, ImageFont


def ttf2image(ttf_font_fullpathname, fontsize=None, fontcolor=None, fontpng=None, use_unicode=False):
    # default unspecified params
    fontsize = fontsize or 11
    fontcolor = fontcolor or '000000'
    fontpng = fontpng or './'
    
    # Setup character delimiter for SFont
    PINK = (255, 0, 255)
    
    # Convert colour/color hex string into tuple of RGB strings
    split = (fontcolor[0:2], fontcolor[2:4], fontcolor[4:6])

    # setting the font string
    text = u'!"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~'
    if use_unicode:
        text = u'!"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~\xa1\xbf\xc0\xc1\xc8\xc9\xcc\xcd\xd2\xd3\xd9\xda\xdd\xc4\xcb\xcf\xd6\xdc\u0178\xc2\xca\xce\xd4\xdb\xc5\xc3\xd5\xd1\xc6\xc7\u010c\u010e\u011a\u013d\u0139\u0147\xd4\u0158\u0154\u0160\u0164\u016e\u017d\xe0\xe1\xe8\xe9\xec\xed\xf2\xf3\xf9\xfa\xfd\xe4\xeb\xef\xf6\xfc\xff\xe2\xea\xee\xf4\xfb\xe5\xe3\xf5\xf1\xe6\xe7\u010d\u010f\u011b\u013e\u013a\u0148\xf4\u0159\u0155\u0161\u0165\u017e\u016f\xf0\xdf\xd0\xde\xfe\u0410\u0411\u0412\u0413\u0414\u0415\u0401\u0416\u0417\u0418\u0419\u041a\u041b\u041c\u041d\u041e\u041f\u0420\u0421\u0422\u0423\u0424\u0425\u0426\u0427\u0428\u0429\u042a\u042b\u042c\u042d\u042e\u042f\u0430\u0431\u0432\u0433\u0434\u0435\u0451\u0436\u0437\u0438\u0439\u043a\u043b\u043c\u043d\u043e\u043f\u0440\u0441\u0442\u0443\u0444\u0445\u0446\u0447\u0448\u0449\u044a\u044b\u044c\u044d\u044e\u044f\xd8\xf8\u0105\u0107\u0119\u0142\u0144\u015b\u017c\u017a\u0104\u0106\u0118\u0141\u0143\u015a\u017b\u0179'

    number_of_codepoints = len(text)  # number of characters

    # setting the font and it's size
    font = ImageFont.truetype(ttf_font_fullpathname, fontsize)

    # getting the font height value
    text_height = font.getsize("{")[1] + 5

    # setting text_width to 0 before calculating image width
    text_width = 0

    # start calculating width
    for i in range(0, number_of_codepoints):
        text_width = text_width + font.getsize(text[i])[0]

    # creating a new image
    img = Image.new('RGBA', (text_width + 536, text_height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # drawing the first 2 pixels of dividing line
    draw.line(((0, 0), (1, 0)), fill=(255, 0, 255))

    # setting X position for the first symbol
    start = 2

    for i in range(0, number_of_codepoints):
        draw.text((start, 4), text[i], font=font, fill=(int(split[0], 16), int(split[1], 16), int(split[2], 16)))
        sz = draw.textsize(text[i], font=font)
        start = start + sz[0]
        draw.line(((start, 0), (start + 1, 0)), fill=PINK)
        start = start + 2
    del draw
    
    save_filename = os.path.join(fontpng, "font.png")
    img.save(save_filename, "PNG")


def main(argv=None):
    if argv is None:
        argv = sys.argv

    if len(argv) != 5:
        sys.exit("Usage: python font.py /path/to/font.ttf font_size(e.g. 11) font_color(e.g. 000000) /path/to/save/dir/")

    ttf_font_fullpathname = argv[1]
    fontsize = int(argv[2])
    fontcolor = argv[3]
    fontpng = argv[4]
    ttf2image(ttf_font_fullpathname, fontsize, fontcolor, fontpng)

if __name__ == "__main__":
    sys.exit(main())
