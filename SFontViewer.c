#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#include "SDL.h"
#include "SFont.h"

#include "SDL_image.h"

SDL_Window *sdlWindow;
SDL_Renderer *sdlRenderer;
SDL_Texture *sdlTexture;
SDL_Surface *screen;

void init_SDL()
{
	int width=640, height=480;

	if (SDL_CreateWindowAndRenderer(width, height, SDL_WINDOW_FULLSCREEN_DESKTOP, &sdlWindow, &sdlRenderer)) {
		fprintf(stderr,
			"Couldn't initialize SDL: %s\n", SDL_GetError());
		exit(1);
	}
	atexit(SDL_Quit);			/* Clean up on exit */
	sdlTexture = SDL_CreateTexture(sdlRenderer,
				       SDL_PIXELFORMAT_ARGB8888,
				       SDL_TEXTUREACCESS_STATIC,
				       width, height);
	screen = SDL_CreateRGBSurface(0, width, height, 32,
						0x00FF0000,
						0x0000FF00,
						0x000000FF,
						0xFF000000);
}

void update_screen()
{
	SDL_UpdateTexture(sdlTexture, NULL, screen->pixels, screen->pitch);
	SDL_RenderClear(sdlRenderer);
	SDL_RenderCopy(sdlRenderer, sdlTexture, NULL, NULL);
	SDL_RenderPresent(sdlRenderer);
}

int main(int argc, char *argv[])
{
    SDL_Event event;
    SFont_Font* Font;

    if (argc < 2 || argc > 3) {
	puts("SFont Font Viewer");
	puts("Usage:\n");
	puts("SFontViewer FONTFILE [TEXTTOPRINT]\n");
	exit(0);
    }

    init_SDL();

    // Load and Prepare the font - You don't have to use the IMGlib for this
    Font = SFont_InitFont(IMG_Load(argv[1]));
    if(!Font) {
	fprintf(stderr, "An error occured while loading the font '%s'.\n",
		argv[1]);
	exit(1);
    }
	
    if (argc > 2) {
	// a simple text blit to (0/0)
	SFont_Write(screen, Font, 0, 0, argv[2]);
    } else {
	SFont_Write(screen, Font, 0, 0, argv[1]);
	SFont_WriteCenter(screen,Font,60,"SFont Font Viewer");
	SFont_WriteCenter(screen,Font,300,"This text is for testing purposes.");
	SFont_WriteCenter(screen,Font,360,"This one, too <>%&-~|/_#+");
    }

    update_screen();
    // Let the user time to look at the font
    SDL_EventState( SDL_KEYUP, SDL_IGNORE );
    SDL_EventState( SDL_WINDOWEVENT, SDL_IGNORE );
    SDL_EventState( SDL_TEXTEDITING, SDL_IGNORE );
    SDL_EventState( SDL_MOUSEMOTION, SDL_IGNORE );
    SDL_EventState( SDL_SYSWMEVENT, SDL_IGNORE );
    SDL_WaitEvent(&event);

    // Don't forget to free our font
    SFont_FreeFont(Font);
    
    // Bye
    exit(0);
}

