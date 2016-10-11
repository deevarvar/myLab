CC=gcc
bin=two_sum
objs=two_sum.o
all: $(bin)

$(objs): two_sum.c testarray.h
	$(CC) -c two_sum.c
$(bin): $(objs)
	$(CC) -o $(bin) $(objs)

.PHONY : clean
clean :
	rm $(bin) $(objs) 	
