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

#ifdef SFONT_INC_FONT_MAIN

/*
** example way to build:
**
**  cc `sdl-config --cflags` `sdl-config --libs` -DSFONT_INC_FONT_MAIN SFont.c %(hdr_name)s.h -o %(hdr_name)s
**
*/

#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#include "SDL.h"
#include "SFont.h"

#include "SDL_image.h"

SDL_Surface *screen;

void init_SDL()
{
    if ( SDL_Init(SDL_INIT_VIDEO) < 0 ) {
    fprintf(stderr,
        "Couldn't initialize SDL: %%s\\n", SDL_GetError());
    exit(1);
    }
    atexit(SDL_Quit);            /* Clean up on exit */
    
    /* Initialize the display */
    screen = SDL_SetVideoMode(640, 480, 0, 16);
    if ( screen == NULL ) {
    fprintf(stderr, "Couldn't set %%dx%%dx%%d video mode: %%s\\n",
        640, 480, 16, SDL_GetError());
    exit(1);
    }
    
    /* Set the window manager title bar */
    SDL_WM_SetCaption("SFont Font Viewer", "SFontViewer");
}

int main(int argc, char *argv[])
{
    SDL_Event event;
    SDL_Surface *font_bitmap_surface=NULL;
    SFont_Font* Font;

    font_bitmap_surface = SDL_LoadBMP("24P_Copperplate_Blue.bmp"); /* NOTE only needs base SDL, no need for SDL_Image */
    if(!font_bitmap_surface)
    {
        fprintf(stderr, "Using default");
        font_bitmap_surface = get_%(hdr_name)s_font();
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


    init_SDL();

    if (argc > 2) {
    /* a simple text blit to (0/0) */
    SFont_Write(screen, Font, 0, 0, argv[2]);
    } else {
    SFont_Write(screen, Font, 0, 0, argv[1]);
    SFont_WriteCenter(screen,Font,60,"SFont Font Viewer");
    SFont_WriteCenter(screen,Font,300,"This text is for testing purposes.");
    SFont_WriteCenter(screen,Font,360,"This one, too <>%%&-~|/_#+");
    }

    /* Update the screen */
    SDL_UpdateRect(screen, 0, 0, 0, 0);
    /* Let the user time to look at the font */
    SDL_EventState( SDL_KEYUP, SDL_IGNORE );
    SDL_EventState( SDL_ACTIVEEVENT, SDL_IGNORE );
    SDL_EventState( SDL_MOUSEMOTION, SDL_IGNORE );
    SDL_EventState( SDL_SYSWMEVENT, SDL_IGNORE );
    SDL_WaitEvent(&event);

    /* Don't forget to free our font */
    SFont_FreeFont(Font);
    
    /* Bye */
    exit(0);
}


#endif /* SFONT_INC_FONT_MAIN */

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

    def dumb_wrap_calc(x):
        if x % 13 == 0:
            return 1
        else:
            return 0
        
    file_bytes_str = ['0x%02x%s' % (ord(x), dumb_wrap_calc(y)*'\n') for y, x in enumerate(file_bytes)]  # list comprehension python 2.4 feature

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
        print 'Usage: gen_sfont_header.py file_name.bmp [name]'
        print ''
        return 1
        
    name, extn = os.path.splitext(os.path.basename(bmp_filename))
    if extn.lower() != '.bmp':
        print 'WARNING! file name does not contain BMP.'
    try:
        name = argv[2]
    except IndexError:
        name = '_'+name
    bmp2header(bmp_filename, name)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())


