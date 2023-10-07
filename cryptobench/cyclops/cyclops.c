#include <stdint.h>


/// NOTE: `cyclops_init` must be called at least once before using this function.
///
/// c9, Cycle Count Register (PMCCNTR)
/// The Cycle Count Register, PMCCNTR, counts processor clock cycles.
/// Depending on the value of the PMCR.D bit, PMCCNTR increments either
/// on every processor clock cycle or on every 64th processor clock cycle.
/// See [c9, Performance Monitor Control Register
/// (PMCR)](https://developer.arm.com/documentation/ddi0406/b/Debug-Architecture/Debug-Registers-Reference/Performance-monitor-registers/c9--Performance-Monitor-Control-Register--PMCR-?lang=en).
///
/// The PMCCNTR is a:
/// - 32-bit read/write CP15 register
/// - accessible in privileged modes
/// - accessed using an MRC or MCR command with <CRn> set to c9,
///   <opc1> set to 0, <CRm> set to c13, and <opc2> set to 0.
///
/// Reference:
/// - <https://developer.arm.com/documentation/ddi0406/b/Debug-Architecture/Debug-Registers-Reference/Performance-monitor-registers/c9--Cycle-Count-Register--PMCCNTR-?lang=en>
/// - [c15, Cycle Counter Register (CCNT)](https://developer.arm.com/documentation/ddi0360/f/control-coprocessor-cp15/register-descriptions/c15--cycle-counter-register--ccnt-)
/// - [c9, Cycle Count Register (PMCCNTR)](https://developer.arm.com/documentation/ddi0406/b/Debug-Architecture/Debug-Registers-Reference/Performance-monitor-registers/c9--Cycle-Count-Register--PMCCNTR-?lang=en)
uint64_t cyclops_cycles(void) {
	uint32_t cc = 0;
	__asm__ volatile("MRC p15, 0, %0, c9, c13, 0" : "=r"(cc));
	return 64ULL * (uint64_t) cc;
}


/// NOTE: The reset bits are not stored permanently in the PMCR register. They just cause a reset
/// and then are set to 0.
///
/// Reference:
/// -
/// <https://developer.arm.com/documentation/ddi0406/b/Debug-Architecture/Debug-Registers-Reference/Performance-monitor-registers/c9--Performance-Monitor-Control-Register--PMCR-?lang=en>
/// - [c9, Performance Monitor Control Register](https://wiki.dreamrunner.org/public_html/Embedded-System/Cortex-A8/PerformanceMonitorControlRegister.html)
/// - [c9, Performance Monitor Control Register (PMCR)](https://developer.arm.com/documentation/ddi0406/b/Debug-Architecture/Debug-Registers-Reference/Performance-monitor-registers/c9--Performance-Monitor-Control-Register--PMCR-?lang=en)
/// - [c9, Count Enable Set Register (PMCNTENSET)](https://developer.arm.com/documentation/ddi0406/b/Debug-Architecture/Debug-Registers-Reference/Performance-monitor-registers/c9--Count-Enable-Set-Register--PMCNTENSET-)
/// - [c9, Overflow Flag Status Register (PMOVSR)](https://developer.arm.com/documentation/ddi0406/b/Debug-Architecture/Debug-Registers-Reference/Performance-monitor-registers/c9--Overflow-Flag-Status-Register--PMOVSR-)
void cyclops_init(void) {
	uint32_t reg = 0;

	// TODO: Read the PMCR register first and then set the relevant bits in it.
	// Read the Performance Monitor Control Register (PMCR).
	// __asm__ volatile("MRC p15, 0, %0, c9, c12, 0" : "=r"(reg));
	// printf("PMCR: 0x%08X\n", reg);

	// Enable all the counters (including cycle counter).
	reg |= 1 << 0;

	// Event counter reset.
	// reg |= 1 << 1;

	// Clock counter reset.
	// NOTE: Resetting PMCCNTR does not clear the PMCCNTR overflow flag to 0.
	reg |= 1 << 2;

	// Clock divider.
	// 0: PMCCNTR counts every clock cycle
	// 1: PMCCNTR counts once every 64 clock cycles
	reg |= 1 << 3;

	// Export enable.
	// reg |= 1 << 4;

	// Program the Performance Monitor Control Register (PMCR).
	__asm__ volatile("MCR p15, 0, %0, c9, c12, 0" ::"r"(reg));

	// Enable all counters using c9, Count Enable Set Register (PMCNTENSET).
	// __asm__ volatile("MCR p15, 0, %0, c9, c12, 1" :: "r"(0x8000000F));

	// Clear overflows using c9, Overflow Flag Status Register (PMOVSR).
	// __asm__ volatile("MCR p15, 0, %0, c9, c12, 3" :: "r"(0x8000000F));
}
