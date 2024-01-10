obj-m += enable_ccr.o

.PHONY: all build install clean

all: build install

build:
	make -C /lib/modules/$(shell uname -r)/build M=$(PWD) modules

install:
	sudo insmod enable_ccr.ko
	dmesg | tail

clean:
	make -C /lib/modules/$(shell uname -r)/build M=$(PWD) clean
