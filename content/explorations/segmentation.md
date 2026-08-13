---
id: "segmentation"
category: "Operating Systems"
series: "Operating Systems"
title: "When Memory Follows Meaning"
subtitle: "Organizing memory around the logical structure of a program."
date: "9th August, 2026"
tags: ["Operating Systems", "Memory Management", "Segmentation", "Logical Address Space", "Fragmentation"]
---

## 1. Beyond Fixed-Size Pages

Paging gives us a powerful way to manage physical memory by breaking a program into fixed-size pages. Because these pages are uniform and can occupy any available, non-contiguous physical frame in RAM, paging generally avoids external fragmentation entirely.

But a program is not just a collection of anonymous, fixed-size pages. It consists of logical components with distinct purposes and boundaries—such as code, data, stack, and heap. What if memory did not have to be organized only as fixed-size pages?

What if memory management followed the logical boundaries of the program itself instead? This approach is called **Segmentation**.

However, organizing memory around variable-sized logical segments introduces its own challenges. While different segments of a program can be placed at different locations in physical memory, each individual segment must occupy a contiguous physical region. Because these segments vary in size, allocating and deallocating them over time as processes start and stop leaves physical memory divided into scattered, variable-sized free holes.

This creates the problem of **External Fragmentation**: a state where total free memory is technically sufficient to satisfy a segment allocation request, but no single contiguous physical block is large enough to host it.

---

## 2. Logical Components of a Program

In practice, a running program does not view its own memory as a single, uniform linear array of bytes. Instead, compilers and programmers organize a program into distinct logical components, each serving a different purpose:

*   **CODE**: The compiled executable instructions (read-only and executable).
*   **DATA**: Global variables and static constants initialized at load time.
*   **STACK**: Function frames, parameters, return addresses, and local variables.
*   **HEAP**: Dynamic memory allocated at runtime by the programmer.

Each of these components is a **Segment**—a logical unit of variable size. 

**Segmentation** is a memory-management strategy that maps these logical divisions directly to physical memory.

*   **Paging**:
    *   Uses fixed-size Pages.
    *   Pages can be placed in non-contiguous physical Frames.
    *   External fragmentation is avoided.
    *   Internal fragmentation is possible within the final page block.
*   **Segmentation**:
    *   Uses variable-sized logical Segments.
    *   Each segment occupies a contiguous physical region.
    *   Different segments can be located at different places in RAM.
    *   External fragmentation is possible as segments are created and destroyed.


---

## 3. EdgeCase: Logical-to-Physical Segment Mapping

Let us look at how the logical segments of a program are placed into physical memory. 

In this scenario, a program is composed of four logical segments of varying sizes: a **CODE** segment (8 KB), a **DATA** segment (4 KB), a **STACK** segment (6 KB), and a **HEAP** segment (12 KB). 

Unlike paging, these segments are not chopped up into equal-sized pages; they are mapped directly to physical RAM locations as whole units.

<div id="segmentation-edgecase" class="edgecase-container"></div>

---

## 4. Manthana: External Fragmentation

By organizing memory around variable-sized segments, we align physical allocation with the logical structure of a program. 

However, this flexibility introduces a major constraint: each individual segment requires a contiguous physical region. As segments of varying sizes are allocated and freed over time, physical memory becomes divided into a series of scattered free holes and allocated blocks.

What happens when we need to allocate a new segment under these conditions?

<div id="manthana-segmentation-external" class="edgecase-container"></div>

---

## 5. The Search for a Strategy

We have now encountered a different memory-allocation problem.

External fragmentation leaves free memory scattered between allocations. If a segment needs one contiguous region, scattered free space may not be enough.

Can we choose where to place a segment intelligently so that fragmentation is reduced?

