---
id: before-main
category: Bare Metal
series: System Explorations
title: Before main()
subtitle: The hidden choreography that prepares raw silicon for your first line of C.
date: 23rd July, 2026
tags: [Bare Metal, Bootloader, Linker Script, Reset Vector, C Runtime]
closing_heading: The Genesis of the Loop
closing_paragraphs:
  - Every embedded application starts long before the code we write. Before the first statement of main() executes, a silent, complex dance of analog voltage detectors, memory transfers, and clock trees has already laid the foundation.
  - The code begins at main(). The machine became itself before the first line was read.
closing_quote: We write main() to dictate what the machine will do. The startup code executes to decide what the machine is.
footer: Analyzing the low-level boundaries of embedded boot sequences, stack validation, and segment migration - PrajnaEdge.dev
---

## 1. The Myth of the Beginning

To the software engineer, the universe of an application begins with a familiar and comforting signature:

`int main(void) { ... }`

It is the genesis of our code, the entry point for our debuggers, and the boundary line where high-level state starts its execution. We write our routines under the quiet assumption that the machine starts here, waiting as a clean, blank slate for our first instruction to call it to action.

But this starting line is an artificial boundary. The CPU did not begin at main(), nor does it understand the high-level syntax of a C function. Long before the first line of your main loop runs, the microcontroller has already completed a massive journey. It has left its analog reset state, evaluated physical boot flags, routed through vendor ROMs, set up stack space, copied segments across physical memories, and configured clock frequencies. Before C can exist, the machine must build the world C assumes already exists.

> main() is not the beginning of computation. It is the final handoff from hardware reality to software abstraction.

## 2. Hardware Wakes: The Reset State

When power climbs the capacitive rails of a microcontroller, or the physical reset line is toggled, digital logic does not instantly begin computing. The core starts in an architecture-defined reset state where pipelines are flushed, registers are set to default values, and interrupts are globally disabled.

<span style="display:inline-block; border-left: 2px solid var(--blue); padding-left: 0.75rem; margin: 0.5rem 0; font-style: italic; color: var(--muted);">We have seen this moment before. In [The First Instruction](the-first-instruction), we traced how analog supervisors release the CPU to fetch its initial Stack Pointer and Reset Vector. Here, we step back to examine the branching boot systems that govern this transition.</span>

How the processor finds its first executable byte depends on its silicon architecture. There is no single universal embedded boot sequence. While a simple microcontroller might immediately point its Program Counter (PC) to a fixed vector table in Flash, a complex SoC or application processor might boot into an immutable on-chip Boot ROM, check boot pins, or load custom bootloader binaries from external media.

## 3. The Boot Decision Tree

Rather than following one mandatory sequence, microcontrollers and SoCs branch into different boot configurations depending on vendor design, boot configurations, and product architecture. A simple MCU boots directly into application code, while a production-grade secure system routes through multiple stages of software validation.

```html
<div style="background:#0F172A; padding:1.5rem; border:1px solid var(--border); border-radius:8px; display:flex; flex-direction:column; align-items:center; margin:2rem 0;">
  <div style="font-family:'Syne',sans-serif; font-size:0.9rem; font-weight:700; color:#fff; margin-bottom:1rem; text-align:center;">THE JOURNEY TO MAIN(): DEVICE-DEPENDENT BOOT PATHS</div>
  <svg viewBox="0 0 800 480" style="width:100%; height:auto; max-width:760px; font-family:var(--mono);">
    <defs>
      <marker id="arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
        <path d="M 0 1 L 10 5 L 0 9 z" fill="#3B82F6"/>
      </marker>
      <marker id="arrow-warn" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
        <path d="M 0 1 L 10 5 L 0 9 z" fill="#EF6868"/>
      </marker>
    </defs>

    <rect x="330" y="20" width="140" height="40" rx="8" fill="#1E293B" stroke="#3B82F6" stroke-width="2"/>
    <text x="400" y="44" fill="#fff" font-size="11" text-anchor="middle" font-weight="bold">POWER ON / RESET</text>

    <path d="M 400 60 L 400 90" stroke="#3B82F6" stroke-width="1.5" marker-end="url(#arrow)"/>

    <rect x="280" y="90" width="240" height="45" rx="6" fill="#1E293B" stroke="rgba(148, 163, 184, 0.3)" stroke-width="1.5"/>
    <text x="400" y="116" fill="#E2E8F0" font-size="10" text-anchor="middle">Boot Config / Pin Latches / Hardware Defaults</text>

    <path d="M 330 135 L 200 135 L 200 170" stroke="#3B82F6" stroke-width="1.5" fill="none" marker-end="url(#arrow)"/>
    <text x="265" y="128" fill="#64748B" font-size="9" text-anchor="middle">Simpler MCU Path</text>

    <path d="M 470 135 L 600 135 L 600 170" stroke="#EF6868" stroke-width="1.5" stroke-dasharray="3,3" fill="none" marker-end="url(#arrow-warn)"/>
    <text x="545" y="128" fill="#EF6868" font-size="9" text-anchor="middle">Bootloader-Based Path</text>

    <rect x="100" y="170" width="200" height="45" rx="6" fill="#1E293B" stroke="#3B82F6" stroke-width="1.5"/>
    <text x="200" y="196" fill="#E2E8F0" font-size="10" text-anchor="middle">Load Vector Table Pointer</text>

    <path d="M 200 215 L 200 250" stroke="#3B82F6" stroke-width="1.5" marker-end="url(#arrow)"/>

    <rect x="100" y="250" width="200" height="45" rx="6" fill="#1E293B" stroke="#3B82F6" stroke-width="1.5"/>
    <text x="200" y="276" fill="#E2E8F0" font-size="10" text-anchor="middle">Fetch Reset Vector (Code Start)</text>

    <rect x="500" y="170" width="200" height="45" rx="6" fill="#1E293B" stroke="#EF6868" stroke-dasharray="3,3" stroke-width="1.5"/>
    <text x="600" y="191" fill="#E2E8F0" font-size="10" text-anchor="middle" font-weight="bold">Vendor Boot ROM</text>
    <text x="600" y="204" fill="#64748B" font-size="8" text-anchor="middle">(On-Chip ROM, Immutable)</text>

    <path d="M 600 215 L 600 250" stroke="#EF6868" stroke-width="1.5" stroke-dasharray="3,3" marker-end="url(#arrow-warn)"/>

    <rect x="500" y="250" width="200" height="45" rx="6" fill="#1E293B" stroke="#EF6868" stroke-dasharray="3,3" stroke-width="1.5"/>
    <text x="600" y="271" fill="#E2E8F0" font-size="10" text-anchor="middle" font-weight="bold">Product Bootloader</text>
    <text x="600" y="284" fill="#64748B" font-size="8" text-anchor="middle">(Custom Boot Stage, OTA)</text>

    <path d="M 600 295 L 600 330" stroke="#EF6868" stroke-width="1.5" stroke-dasharray="3,3" marker-end="url(#arrow-warn)"/>

    <rect x="500" y="330" width="200" height="45" rx="6" fill="#1E293B" stroke="#EF6868" stroke-dasharray="3,3" stroke-width="1.5"/>
    <text x="600" y="356" fill="#E2E8F0" font-size="10" text-anchor="middle">Select & Validate App Entry</text>

    <path d="M 200 295 L 200 395 L 300 395" stroke="#3B82F6" stroke-width="1.5" fill="none" marker-end="url(#arrow)"/>
    <path d="M 600 375 L 600 395 L 500 395" stroke="#EF6868" stroke-width="1.5" stroke-dasharray="3,3" fill="none" marker-end="url(#arrow-warn)"/>

    <rect x="300" y="375" width="200" height="45" rx="6" fill="#1E293B" stroke="#10B981" stroke-width="2"/>
    <text x="400" y="401" fill="#FFF" font-size="11" text-anchor="middle" font-weight="bold">Startup Code (C Runtime Setup)</text>

    <path d="M 400 420 L 400 445" stroke="#10B981" stroke-width="1.5" marker-end="url(#arrow)"/>

    <rect x="330" y="445" width="140" height="30" rx="4" fill="#1E293B" stroke="#10B981" stroke-width="2"/>
    <text x="400" y="464" fill="#10B981" font-size="10" text-anchor="middle" font-weight="bold" font-family="var(--mono)">main()</text>
  </svg>
  <div style="font-size:0.75rem; color:var(--muted); font-family:var(--mono); margin-top:0.75rem; text-align:center;">Optional boot stages split basic microcontrollers from high-reliability multi-stage systems.</div>
</div>
```

## 4. The Boot ROM Sentinel

The first software executed by a processor is not necessarily the application — and it is not necessarily a user-written bootloader.

In many modern microcontrollers and SoC designs, the physical reset vector points directly into on-chip Boot ROM. This is a small, immutable block of memory mask-programmed into the silicon by the chip vendor during manufacturing. The code within it is permanent; it cannot be modified by firmware updates or device failures.

When the Boot ROM runs, it acts as a sentinel. It inspects the state of physical boot pins (latching external voltage levels to determine the boot source) or reads specific memory-mapped registers. If it detects a recovery condition—such as a specific pin pulled low or an invalid signature in the primary flash sector—it launches an internal serial bootloader interface, listening on UART, USB, or CAN for new firmware. If the system is healthy, the Boot ROM locates the secondary boot stage or application vector table and branches to it.

## 5. Second-Stage Product Bootloaders

While simple microcontrollers often execute their application directly from Flash, commercial products frequently introduce a second-stage, programmable product bootloader. Unlike the Boot ROM, this bootloader is stored in writeable Flash memory and can be updated in the field.

The responsibilities of this stage are critical for product reliability. It acts as a gatekeeper, validating the integrity of the application image using checksums or verifying its authenticity through cryptographic signatures. It manages the swap logic between dual-image banks (A/B partitioning) to ensure that if a wireless OTA update fails mid-transmission, the system can safely roll back to a previously known good firmware image. If validation succeeds, it initiates the handoff.

## 6. The Handoff of Control

When a bootloader transfers control to the application, it does not simply invoke the application's main() as if it were a local subroutine. If the bootloader called main() directly, the application would inherit a contaminated execution context. Bootloader-owned interrupts might still be active, the stack pointer could be misaligned, and peripherals would remain in modified states.

The handoff is a clean break. The bootloader must: disable all of its active interrupts, clear pending flags in the interrupt controller, set the main stack pointer to the application's starting stack address, relocate the Vector Table base address (e.g. by modifying the Vector Table Offset Register VTOR in Cortex-M architectures), and finally jump to the application's entry address. The application must start as if the bootloader had never been there.

## 7. The Application Startup Phase

Once control is transferred to the application's entry address—which is the Reset Handler pointed to by the application's vector table—the execution shifts into the startup code. This code, usually provided by the silicon vendor or toolchain and written in assembly or low-level C, builds the runtime environment step-by-step.

The startup sequence follows a deterministic sequence to construct the C language environment:

```c
void Reset_Handler(void) {
    /* 1. Low-level initialization */
    SystemInit();
    
    /* 2. Copy initialized data from Flash to RAM */
    copy_data_segment();
    
    /* 3. Zero-initialize BSS memory */
    zero_bss_segment();
    
    /* 4. Call static constructors and runtime libraries */
    __libc_init_array();
    
    /* 5. Transfer control to the application entry */
    main();
}
```

## 8. Constructing the Memory World

When power is first applied, the cells of volatile Static RAM (SRAM) settle into arbitrary, electrically noisy states. Yet, C language code operates under a strict promise: global and static variables initialized to a value (like `int speed = 100;`) must begin execution with that exact value, and uninitialized objects (like `static int fault_count;`) must start at zero.

Startup code constructs this expected memory layout by migrating data segments from non-volatile storage (Flash) to volatile memory (RAM). The linker script defines two distinct addresses for initialized variables: the Load Memory Address (LMA), where the initial values reside permanently in Flash, and the Virtual Memory Address (VMA), where the variables will reside in RAM during runtime. The startup routine runs a copy loop to copy these bytes from LMA to VMA. It then runs a zeroing loop over the `.bss` section in RAM, clearing it to zero.

```html
<div style="background:#0F172A; padding:1.5rem; border:1px solid var(--border); border-radius:8px; display:flex; flex-direction:column; align-items:center; margin:2rem 0;">
  <div style="font-family:'Syne',sans-serif; font-size:0.9rem; font-weight:700; color:#fff; margin-bottom:1rem; text-align:center;">FLASH ↔ RAM DATA MIGRATION IN STARTUP</div>
  <svg viewBox="0 0 800 320" style="width:100%; height:auto; max-width:760px; font-family:var(--mono);">
    <defs>
      <marker id="arrow-green" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
        <path d="M 0 1 L 10 5 L 0 9 z" fill="#10B981"/>
      </marker>
    </defs>

    <rect x="50" y="30" width="280" height="260" rx="8" fill="#1E293B" stroke="rgba(148, 163, 184, 0.2)" stroke-width="1.5"/>
    <text x="190" y="52" fill="#FFF" font-size="11" font-weight="bold" text-anchor="middle">FLASH (Non-Volatile / Load Area)</text>

    <rect x="70" y="70" width="240" height="35" rx="4" fill="rgba(148, 163, 184, 0.05)" stroke="rgba(148, 163, 184, 0.15)"/>
    <text x="190" y="91" fill="#E2E8F0" font-size="9" text-anchor="middle">Vector Table (Pointers)</text>

    <rect x="70" y="115" width="240" height="35" rx="4" fill="rgba(148, 163, 184, 0.05)" stroke="rgba(148, 163, 184, 0.15)"/>
    <text x="190" y="136" fill="#E2E8F0" font-size="9" text-anchor="middle">.text (Executable Instructions)</text>

    <rect x="70" y="160" width="240" height="35" rx="4" fill="rgba(148, 163, 184, 0.05)" stroke="rgba(148, 163, 184, 0.15)"/>
    <text x="190" y="181" fill="#E2E8F0" font-size="9" text-anchor="middle">.rodata (Constants & Read-Only)</text>

    <rect x="70" y="215" width="240" height="50" rx="4" fill="rgba(59, 130, 246, 0.08)" stroke="#3B82F6" stroke-width="1.5"/>
    <text x="190" y="238" fill="#FFF" font-size="10" font-weight="bold" text-anchor="middle">.data initializers (Flash image)</text>
    <text x="190" y="253" fill="var(--muted)" font-size="8" text-anchor="middle">e.g. initial value of 'int speed = 100;'</text>

    <path d="M 310 240 L 490 100" stroke="#10B981" stroke-width="2" stroke-dasharray="4,4" fill="none" marker-end="url(#arrow-green)"/>
    <text x="400" y="160" fill="#10B981" font-size="9" text-anchor="middle" font-weight="bold">1. COPY DATA</text>

    <rect x="470" y="30" width="280" height="260" rx="8" fill="#1E293B" stroke="rgba(148, 163, 184, 0.2)" stroke-width="1.5"/>
    <text x="610" y="52" fill="#FFF" font-size="11" font-weight="bold" text-anchor="middle">RAM (Volatile / Execution Area)</text>

    <rect x="490" y="70" width="240" height="50" rx="4" fill="rgba(16, 185, 129, 0.08)" stroke="#10B981" stroke-width="1.5"/>
    <text x="610" y="93" fill="#FFF" font-size="10" font-weight="bold" text-anchor="middle">.data (Initialized Variables)</text>
    <text x="610" y="108" fill="var(--muted)" font-size="8" text-anchor="middle">Variables copied to RAM address</text>

    <rect x="490" y="130" width="240" height="50" rx="4" fill="rgba(245, 158, 11, 0.08)" stroke="#F59E0B" stroke-width="1.5"/>
    <text x="610" y="153" fill="#FFF" font-size="10" font-weight="bold" text-anchor="middle">.bss (Zero-Initialized)</text>
    <text x="610" y="168" fill="var(--muted)" font-size="8" text-anchor="middle">2. ZERO LOOP (e.g. static int fault_count;)</text>

    <rect x="490" y="195" width="110" height="40" rx="4" fill="rgba(148, 163, 184, 0.05)" stroke="rgba(148, 163, 184, 0.15)"/>
    <text x="545" y="213" fill="#E2E8F0" font-size="9" text-anchor="middle">Heap</text>
    <text x="545" y="225" fill="var(--muted)" font-size="7" text-anchor="middle">(Grows Up &rarr;)</text>

    <rect x="620" y="195" width="110" height="40" rx="4" fill="rgba(148, 163, 184, 0.05)" stroke="rgba(148, 163, 184, 0.15)"/>
    <text x="675" y="213" fill="#E2E8F0" font-size="9" text-anchor="middle">Stack</text>
    <text x="675" y="225" fill="var(--muted)" font-size="7" text-anchor="middle">(&larr; Grows Down)</text>

    <text x="610" y="265" fill="#64748B" font-size="8" text-anchor="middle">Stack Pointer (SP) initialized to RAM top</text>
  </svg>
  <div style="font-size:0.75rem; color:var(--muted); font-family:var(--mono); margin-top:0.75rem; text-align:center;">Startup code copies initial values to RAM and zeros out BSS segments before main() runs.</div>
</div>
```

> Startup code constructs the memory environment that the C program assumes already exists.

## 9. Stack Initialization and System Clocks

Before any C function can be invoked, the stack must be valid. The stack is the scratch area used for local variables, local execution contexts, and return addresses. If the program counter jumps to a C function before the Stack Pointer (SP) register is loaded with a valid RAM address, the first function call or stack allocation will push data into invalid memory space, crashing the processor immediately.

Different architectures handle stack pointer setup in different ways. In ARM Cortex-M processors, the hardware automatically loads the initial Stack Pointer value from the very first entry (offset 0) of the vector table during the reset cycle. In other architectures, the stack pointer must be explicitly loaded in assembly code inside the reset handler before any other operations occur.

Simultaneously, the system clock tree must be configured. At boot, the CPU runs from a slow, low-power internal default oscillator to guarantee startup. The reset code configures the clock multipliers (PLLs) and oscillators, adjusting Flash access wait-states in tandem to avoid instruction starvation. Order matters: scaling speed without wait states locks the bus.

## 10. The Language Runtime and main()

With memory structured, clocks stabilized, and stack space verified, the hardware environment is finally complete. However, if the project is written in C++, there remains one final software initialization step: static constructors.

Global C++ objects must have their constructors executed before main() starts. The toolchain compiles a list of pointers to these constructor functions into a dedicated section (like `.init_array`). The startup code iterates through this array, executing each constructor function in sequence. Finally, the program counter loads the address of the main() symbol. The application has begun.
