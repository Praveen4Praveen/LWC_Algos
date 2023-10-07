#include <stdint.h>
#include <stdio.h>

#define PRINT_SIZE(type) printf("%18s -> %2zu bytes\n", #type, sizeof(type))

int main(void) {
	PRINT_SIZE(char);
	PRINT_SIZE(unsigned char);

	PRINT_SIZE(short);
	PRINT_SIZE(unsigned short);

	PRINT_SIZE(int);
	PRINT_SIZE(unsigned int);

	PRINT_SIZE(long);
	PRINT_SIZE(unsigned long);

	PRINT_SIZE(long long);
	PRINT_SIZE(unsigned long long);

	PRINT_SIZE(int8_t);
	PRINT_SIZE(uint8_t);

	PRINT_SIZE(int16_t);
	PRINT_SIZE(uint16_t);

	PRINT_SIZE(int32_t);
	PRINT_SIZE(uint32_t);

	PRINT_SIZE(int64_t);
	PRINT_SIZE(uint64_t);

	// PRINT_SIZE(__int128);
	// PRINT_SIZE(unsigned __int128);

	return 0;
}
