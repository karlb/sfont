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
	SFont_Font* Font;

	init_SDL();

	// Load and Prepare the font - You don't have to use the IMGlib for this
	Font = SFont_InitFont(IMG_Load("24P_Copperplate_Blue.png"));
	if(!Font) {
		fprintf(stderr, "An error occured while loading the font.");
		exit(1);
	}
	
	// a simple text blit to (0/0)
	SFont_Write(screen, Font, 0, 0, "Top Left");
	// License Info...
	SFont_Write(screen, Font, 60, 120, "SFont by Karl Bartel is GPL'ed!");
	// show some special chars
	SFont_Write(screen, Font, 300, 260, "@--~!%&'_*,.:;");
	// demonstrates the use of TextWidth
	SFont_Write(screen, Font, 640-SFont_TextWidth(Font, "Bottom Right!"),
							  480-SFont_TextHeight(Font), "Bottom Right!");
	update_screen();

	SFont_FreeFont(Font);

	// wait a bit
	SDL_Delay(4000);
	
	// Bye
	exit(0);
}
