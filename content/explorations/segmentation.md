---
id: "segmentation"
category: "Operating Systems"
series: "Operating Systems"
title: "When Memory Follows Meaning"
subtitle: "Organizing memory around the logical structure of a program."
date: "9th August, 2026"
tags: ["Operating Systems", "Memory Management", "Segmentation", "Logical Address Space", "Fragmentation"]
---

## 1. The Scattered Spaces

At the end of our previous exploration, we ran into a fundamental memory allocation bottleneck: **External Fragmentation**.

External fragmentation occurs when the total amount of free physical memory in the system is technically large enough to satisfy an allocation request, but because that free memory is scattered across non-contiguous, separate regions, a single sufficiently large contiguous allocation cannot be fulfilled.

When page references demand a contiguous physical boundary, even the most optimal page replacement algorithms cannot solve external fragmentation once it occurs. The physical spaces are simply too fragmented to coalesce.

This limitation forces us to ask a different design question:

> What if memory did not have to be treated as one continuous block?

---

## 2. Logical Components of a Program

In practice, a running program does not view its own memory as a single, uniform linear array of bytes. Instead, compilers and programmers organize a program into distinct logical components, each serving a different purpose:

*   **CODE**: The compiled executable instructions (read-only and executable).
*   **DATA**: Global variables and static constants initialized at load time.
*   **STACK**: Function frames, parameters, return addresses, and local variables.
*   **HEAP**: Dynamic memory allocated at runtime by the programmer.

Each of these components is a **Segment**—a logical unit of variable size. 

**Segmentation** is a memory-management strategy that maps these logical divisions directly to physical memory.

Rather than partitioning everything into arbitrary, equal-sized pages as Paging does, Segmentation recognizes the logical boundaries of the program itself. 

*   **Paging** → Divides the address space into fixed-size, uniform blocks (**Pages**).
*   **Segmentation** → Divides the address space into logical, variable-sized units (**Segments**).

---

## 3. EdgeCase: Logical-to-Physical Segment Mapping

Let us look at how the logical segments of a program are placed into physical memory. 

In this scenario, a program is composed of four logical segments of varying sizes: a **CODE** segment (8 KB), a **DATA** segment (4 KB), a **STACK** segment (6 KB), and a **HEAP** segment (12 KB). 

Unlike paging, these segments are not chopped up into equal-sized pages; they are mapped directly to physical RAM locations as whole units.

<div id="segmentation-edgecase" class="edgecase-container"></div>

---

## 4. Manthana: The Allocation Challenge

By moving from fixed-size paging to variable-sized segments, we solved the problem of dividing programs into arbitrary blocks. 

However, variable-sized segment allocation introduces a new trade-off. Because segments are dynamic and vary in size, the hardware or the operating system must align them to specific boundary constraints (such as 4 KB or 8 KB physical alignments) to simplify translation circuitry.

Suppose a logical segment requires exactly **7 KB** of space, but the physical slot allocated to it must be aligned to a **10 KB** boundary.

<div id="manthana-segmentation-internal" class="edgecase-container"></div>

What happens to that unused space inside the allocated segment region?

This unused, wasted memory trapped inside an allocated block is called **Internal Fragmentation**. 

Segmentation solves the external fragmentation of linear programs by allowing logical blocks to be scattered non-contiguously in RAM, but it can still leave us with internal fragmentation when physical allocations exceed logical needs. 

---

## 5. The Search for the Perfect Fit

We have now encountered two different forms of memory waste.

External fragmentation leaves free memory scattered between allocations.
Internal fragmentation leaves unused space inside an allocated region.

Can any memory-management strategy avoid both?
