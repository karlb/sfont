
CFLAGS = $(shell pkg-config --cflags sdl3 sdl3-image) -Wall -pedantic -ggdb
CXXFLAGS = $(CFLAGS)
LIBS = $(shell pkg-config --libs sdl3 sdl3-image)
OBJECTS = SFont.o

all: startmessage test1 test2 test3 SFontViewer endmessage

test1: $(OBJECTS) test1.o
	gcc $(CFLAGS) -o SFontTest1 $(OBJECTS) test1.o $(LIBS)

test2: $(OBJECTS) test2.o
	gcc $(CFLAGS) -o SFontTest2 $(OBJECTS) test2.o $(LIBS)

test3: $(OBJECTS) test3.o
	gcc $(CFLAGS) -o SFontTest3 $(OBJECTS) test3.o $(LIBS)

SFontViewer: $(OBJECTS) SFontViewer.o
	gcc $(CFLAGS) -o SFontViewer $(OBJECTS) SFontViewer.o $(LIBS)

clean:
	@rm -f *.o SFontTest* SFontViewer

startmessage:
	@echo ""
	@echo "These examples require SDL3_image. If you have any problems"
	@echo "or questions, please let me know. <karl@karl.berlin>"
	@echo ""

endmessage:
	@echo ""
	@echo "Thanks for trying SFont!"
	@echo ""
