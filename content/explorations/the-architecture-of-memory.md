---
id: the-architecture-of-memory
category: Computation
series: System Explorations
title: The Architecture of Memory
subtitle: How physical constraints and electrical charge define the boundaries of digital state.
date: 28th May, 2026
tags: [Memory, SRAM, DRAM, Flash, Embedded Systems]
closing_heading: The Architecture of State
closing_paragraphs:
  - Memory is not just a passive buffer; it is the physical medium where logic meets reality. The boundaries of digital state are defined by the speeds, densities, and physical layout structures of silicon.
  - Understanding these hardware constraints is what allows us to write firmware that pushes performance to the very edge.
closing_quote: True efficiency is achieved when you align your software execution path with the physical layout of the silicon.
footer: Reflections on Memory and State - PrajnaEdge.dev
---

## 1. The Hierarchy of State

Every processor is fundamentally a state machine. It executes instructions by reading data from memory, transforming it, and writing it back. But not all memory is created equal. The physical reality of silicon forces a compromise between speed, capacity, and cost.

To build a useful system, we construct a hierarchy: registers and SRAM at the very top (tapering down near the CPU core for speed), backed by main DRAM system memory, and finally persistent NOR and NAND flash for mass storage. This tiered architecture ensures the CPU is never starved of instructions while keeping persistent data accessible.

![The Memory Hierarchy showing speed vs density trade-offs](Images/memory_hierarchy.png)

*A vertical structural view of memory layers tapering down as they approach the CPU core.*

## 2. The Battle for the Bit: SRAM vs DRAM

At the volatile layer, the choice comes down to topology: how do we store a single bit of data?

Static RAM (SRAM) uses a cross-coupled latch constructed with 6 transistors (6T). This design creates an active, stable state that holds its value as long as power is applied. However, this complexity makes SRAM physically large and expensive, limiting its use to small, fast CPU caches and microcontroller registers.

Dynamic RAM (DRAM) takes the opposite approach. It shrinks the cell down to a single transistor and a single storage capacitor (1T1C). While this allows massive densities (gigabytes on a single chip), the capacitor is a leaky reservoir. It naturally drains its charge within milliseconds, requiring a continuous refresh loop to prevent data corruption.

![SRAM 6T vs DRAM 1T1C circuit diagram](Images/sram_vs_dram.png)

*Circuit topologies representing the active stable latch of SRAM versus the leaky reservoir of DRAM.*

## 3. Persistence: NOR vs NAND Flash

When power is removed, we rely on non-volatile flash memory to retain our programs and data. Flash operates by trapping charge within a floating gate transistor. The layout configuration of these gates determines how they can be accessed.

NOR Flash connects storage transistors in parallel directly across word lines. This parallel alignment allows the processor to perform instant random byte reads, making it the standard choice for executing firmware binary code directly on-board.

NAND Flash daisy-chains transistor arrays in a tight serial configuration. By eliminating the individual contacts needed for parallel routing, NAND achieves extraordinary densities. However, this serial chain prevents byte-level access, requiring the processor to read and write data in sequential sector blocks, ideal for mass storage filesystems.

![NOR parallel vs NAND serial micro-architectural layouts](Images/nor_vs_nand.png)

*Transistor cell layout detailing parallel random-access lines in NOR vs serial block lines in NAND.*

## 4. The Address Map: Dividing Space

To the developer, all of these physical layers are abstracted into a single, contiguous address space. The microcontroller registers map specific memory regions to Flash and SRAM boundaries.

From top to bottom, the register space is divided into proportional segments: .text (NOR Flash for execution), .data and .bss (RAM for initialized and zeroed variables), followed by the Stack (runtime context engine) and the Heap (dynamic allocation workspace).

![Microcontroller memory map segment boundaries](Images/embedded_memory_map.png)

*The vertical register allocation of persistent Flash versus internal SRAM workspace segments.*
