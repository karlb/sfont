#!/usr/bin/python
#!/usr/bin/env python
# -*- coding: ascii -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
#
#

"""Generate a default font from a BMP file (and can only be BMP)
for use with SFont and SDL. See http://www.linux-games.com/sfont/

It sort of defeats the purpose of SFont in that it creates code
without a file system dependency but this is useful for a default
font.

Basically an automated version of bin2h on a BMP and code generator.

Possible ideas, use PIL to load any file and then convert to BMP.
BMP is preferred as SDL supportds BMP out of the box, other image
formats require SDL_image

Recommended usage:

...
    #include "default_data.h"
...
    SDL_Surface *font_bitmap_surface=NULL;
    SFont_Font* Font;
    
    font_bitmap_surface = SDL_LoadBMP("24P_Copperplate_Blue.bmp");
    if(!font_bitmap_surface)
    {
        fprintf(stderr, "Using default");
        font_bitmap_surface = get_default_data_font();
    }
    
    if(!font_bitmap_surface)
    {
        fprintf(stderr, "An error occured while loading the font.");
        exit(1);
    }
    
    Font = SFont_InitFont(font_bitmap_surface);
    if(!Font)
    {
        fprintf(stderr, "An error occured while setting up font.");
        exit(1);
    }
...

"""

import sys
import os

c_header_template = """/*
** Generated with gen_sfont_header.py for use with
** SFont http://www.linux-games.com/sfont/
*/
#ifndef __%(hdr_name)s_h__
#define __%(hdr_name)s_h__


#ifdef __cplusplus
extern "C" {
#endif

#include "SDL.h"
#include "SDL_video.h"

%(hdr_include)s

#define get_%(hdr_name)s_font() SDL_LoadBMP_RW(SDL_RWFromMem(%(hdr_name)s, sizeof(%(hdr_name)s)), 1);
%(type_name)s   %(hdr_name)s[%(byte_len)d] = {
%(hex_byte_str_list)s
};

#ifdef __cplusplus
}
#endif

#endif

"""

def bmp2header(bmp_filename, name=None, use_c99_types=False):
    name = name or 'default_data'
    f = open(bmp_filename)
    file_bytes = f.read()
    f.close()
    byte_len = len(file_bytes)

    file_bytes_str = ['0x%02x'%ord(x) for x in file_bytes]  # list comprehension python 2.4 feature

    hdr_name = name
    if use_c99_types:
        hdr_include = '#include <stdint.h>'
        type_name = 'uint8_t'
    else:
        hdr_include = ''
        type_name = 'unsigned char'
    hex_byte_str_list = ', '.join(file_bytes_str)  ## TODO add newlines
    print c_header_template % locals()


def main(argv=None):
    if argv is None:
        argv = sys.argv
    
    bmp_filename = '2bit_8pxfont.bmp'
    try:
        bmp_filename = argv[1]
    except IndexError:
        print ''
        print 'Error missing file name'
        print ''
        print 'Usage: gen_sfont_header.py file_name.bmp'
        print ''
        return 1
    name, extn = os.path.splitext(os.path.basename(bmp_filename))
    if extn.lower() != '.bmp':
        print 'WARNING! file name does not contain BMP.'
    name = '_'+name
    bmp2header(bmp_filename, name)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())


