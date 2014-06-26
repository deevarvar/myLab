CC=gcc
IDIR=.
LIBS=-lm
CFLAGS=-I$(IDIR)
DEPS =minunit.h
OBJ= minunit_example.o
TARGET=minunit

%.o:%.c $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS)

$(TARGET): $(OBJ)
	$(CC) -o $@ $< $(CFLAGS) $(LIBS)

clean:
	rm -rf ./$(OBJ) ./$(TARGET)

.PHONY: clean
