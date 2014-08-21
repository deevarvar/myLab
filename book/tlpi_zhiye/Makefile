CC=gcc
MAKE=make

DIRS = ch3



all: 
	@for dir in ${DIRS}; do \
	(cd $$dir  && make);\
	done



clean:
	@for dir in ${DIRS}; do \
	(cd $$dir && make clean);\
	done

.PHONY: clean
