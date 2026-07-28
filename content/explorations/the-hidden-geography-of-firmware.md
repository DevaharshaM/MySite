---
id: the-hidden-geography-of-firmware
category: Computation
series: System Explorations
title: The Hidden Geography of Firmware
subtitle: How linker scripts quietly decide where computation lives.
date: 4th June, 2026
tags: [Linker Scripts, Memory Mapping, Firmware, Systems Architecture]
closing_heading: Shaping the City of Logic
closing_paragraphs:
  - Memory architecture defines the boundaries of what is electrically possible, but the linker script defines the geography where firmware actually lives.
  - As you write embedded code, you are not just writing logic; you are organizing silicon.
closing_quote: Every firmware image is a city. The linker simply decides where its citizens reside.
footer: Exploring the hidden structures of firmware systems - PrajnaEdge.dev
---

## 1. The Illusion of Uniform Memory

To a programmer working in a high-level application space, memory is often visualized as a flat, infinite landscape of bytes—a continuous array indexed from zero to the limits of physical RAM. You allocate memory, declare variables, and write functions under the assumption that all space is structurally equivalent.

But beneath the abstraction layers of low-level firmware, this uniformity disappears. Memory is not a single contiguous pasture; it is a highly structured, compartmentalized terrain. A microcontroller's memory space is fragmented by physical and electrical realities. Code, initialized global variables, uninitialized flags, read-only constants, stack frames, and dynamic heaps must reside in completely different areas of the silicon to function.

![Embedded Firmware Memory Layout Diagram](Images/firmware_memory_layout.png)

*Firmware is not stored as one object. It is distributed across memory according to behavioral requirements.*

## 2. The Birth of Memory Sections

Why do we slice firmware into segments? It is a direct response to different behavioral requirements. Different classes of information behave differently during execution, requiring distinct storage mediums.

Consider instructions: executable code must be persistent and read-only, which is why the compiler assigns it to the '.text' section to reside in Flash memory. Constants and string literals share similar read-only behaviors and are grouped into the '.rodata' section, protected from runtime modification.

Global variables, however, present a dual behavior. They must be modifiable at runtime (residing in RAM), but they must start with a pre-configured initial value. These are grouped into '.data'. Uninitialized global variables—those that simply need to be cleared to zero on startup—are routed to '.bss' (Block Started by Symbol) to save space in the flash binary.

Finally, the Stack handles execution flow by dynamically pushing and popping function parameters and local variables, while the Heap manages runtime dynamic memory allocation workspace. The organization of these sections is the layout of digital life.

## 3. The Linker as a Cartographer

During compilation, the compiler translates individual source files (.c or .cpp) into independent object files (.o). At this stage, the compiler acts in isolation: it has no knowledge of how much total Flash or RAM exists on the chip, nor does it know where other object files will eventually be placed.

This is where the Linker enters as a cartographer. The linker compiles these fragmented objects and maps their sections into a unified, physical landscape. It decides the precise layout of the firmware—stitching together the various '.text', '.data', and '.bss' fragments and matching them to the exact address boundaries of the target processor.

![Linker to Memory Relationship Mapping](Images/linker_to_memory_relationship.png)

*The compiler generates isolated segments; the linker script guides the linker to map them into physical memory blocks.*

> The linker does not create firmware. It decides where firmware physically exists.

## 4. The Linker Script

To direct the linker, we use a linker script—a blueprint that defines the physical boundaries of the MCU's address register space. It tells the linker exactly where Flash and RAM begin and how long they are.

```c
MEMORY
{
  FLASH (rx) : ORIGIN = 0x08000000, LENGTH = 512K
  RAM (rwx)  : ORIGIN = 0x20000000, LENGTH = 128K
}
```

In this snippet, we define the region boundaries. 'FLASH' is marked as read-only and executable (rx) starting at origin address 0x08000000 with a length of 512 Kilobytes. 'RAM' is marked as readable, writable, and executable (rwx) starting at origin 0x20000000 with 128 Kilobytes.

By establishing these constraints, the compiler can output absolute addresses, knowing that the code and variable segments will fall safely within the silicon boundaries.

![Microcontroller Memory Map Diagram](Images/mcu_memory_map.png)

*Microcontroller address registers are mapped to specific Flash (executable) and RAM (read-write) regions.*

## 5. Startup: The First Migration

When power is applied, the microcontroller is in a primitive state. The RAM is filled with random electrical noise. However, global variables in the '.data' section must have their initial non-zero values ready for the application to read.

Since RAM is volatile and loses all state when powered off, these initial values must be stored persistently inside Flash memory. This creates a logical conflict: the variables must be modifiable in RAM during execution, but their initial values are trapped in Flash.

To resolve this, the system executes startup assembly or C initialization routines before your main() function is reached. This startup code performs the first migration: it reads the block of initial values from Flash and copies them into their RAM destinations. It then clears the '.bss' section in RAM to zero.

![Startup Initialization Flow Diagram](Images/startup_initialization_flow.png)

*Relocation sequence at startup, moving initialized variables from Flash to RAM and zeroing out the BSS.*

> Before the first line of user code executes, the system has already performed a carefully orchestrated relocation.

## 6. The Map File: The Firmware Census

Once the linker has completed its map, it outputs a map file—a census of the compiled firmware. The map file outlines exactly where every function, variable, and library symbol has been placed, along with the size of each segment.

Experienced embedded engineers inspect map files regularly. When a firmware image suddenly overflows memory, the map file reveals which module or library is consuming the flash. It lets you identify compiler optimizations, alignment padding issues, and variables that were accidentally declared globally instead of locally.

```c
.text           0x08000240      0x8a4
 *(.text)
 .text          0x08000240      0x1c8 build/main.o
                0x080002a0                SystemInit
 .text          0x08000408      0x6dc build/gpio.o
                0x08000420                GPIO_Init

.data           0x20000000       0x18 load address 0x08000ae4
 *(.data)
 .data          0x20000000       0x18 build/main.o
                0x20000004                system_state

.bss            0x20000018       0x40
 *(.bss)
 .bss           0x20000018       0x40 build/sensor.o
                0x20000018                sensor_buffer
```

## 7. When Geography Becomes Critical

Memory mapping eventually moves from a compiler detail to a system design challenge. In advanced architectures, you must place DMA (Direct Memory Access) buffers into specific memory regions that the DMA controller can actually access. If the buffer is mapped to a core-coupled RAM region that is inaccessible to the peripheral bus, the system will silently fail or crash.

Similarly, separating a bootloader from an application requires carving Flash memory into separate, non-overlapping regions using custom linker scripts. The developer is no longer writing software alone—they are shaping the physical layout of logic.
