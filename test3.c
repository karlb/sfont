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
	SFont_Font* Neon;
	SFont_Font* Copper;

	init_SDL();

	// Load and Prepare the fonts - You don't have to use the IMGlib for this
	Copper = SFont_InitFont(IMG_Load("24P_Copperplate_Blue.png"));
	if(!Copper) {
		fprintf(stderr, "An error occured while loading the font.");
		exit(1);
	}
	Neon = SFont_InitFont(IMG_Load("24P_Arial_NeonYellow.png"));
	if(!Neon) {
		fprintf(stderr, "An error occured while loading the font.");
		exit(1);
	}

	// a simple text blit to (0/0) with Neon font
	SFont_Write(screen, Neon, 0, 0, "Top Left");
	// License Info...
	SFont_Write(screen, Copper, 60, 120, "SFont by Karl Bartel is GPL'ed!");
	// show some special chars
	SFont_Write(screen, Copper, 300, 260, "@--~!%&'_*,.:;");
	// demonstrates the use of TextWidth
	SFont_Write(screen, Neon, 640-SFont_TextWidth(Neon, "Bottom Right!"),
							  480-SFont_TextHeight(Neon),"Bottom Right!");
	update_screen();

	// Wait a bit
	SDL_Delay(4000);

	// Don't forget to free the fonts
	SFont_FreeFont(Copper);
	SFont_FreeFont(Neon);

	// Bye
	exit(0);
}
