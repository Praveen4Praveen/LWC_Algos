.PHONY: all clean

all: cyclops.c
	$(CC) -c -fPIC cyclops.c -o cyclops.o
	$(CC) -shared -Wl,-soname,libcyclops.so -o libcyclops.so cyclops.o

clean:
	$(RM) -- ./cyclops.o ./libcyclops.so
