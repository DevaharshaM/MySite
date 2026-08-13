---
id: "when-the-page-wasnt-there"
category: "Operating Systems"
series: "Operating Systems"
title: "When the Page Wasn't There"
subtitle: "How Demand Paging manages physical memory limits and Page Faults."
date: "9th August, 2026"
tags: ["Operating Systems", "Memory Management", "Paging", "Demand Paging", "Page Fault", "Secondary Storage"]
---

## 1. Beyond the Mapping

What you just saw is called **Paging**.

Paging divides a process's Virtual Address Space into equal-sized blocks called **Pages**, and physical memory into identically sized slots called **Frames**. The **Page Table** sits between them, serving as a translation gateway that maps virtual coordinates to physical RAM.

But paging only tells us how memory is divided and mapped. The physical reality of computer hardware introduces a critical constraint: **physical RAM is limited.**

A process might have a vast Virtual Address Space (e.g., 4 GB on a 32-bit CPU), but the system may only possess a fraction of that in actual physical RAM. If multiple processes run concurrently, physical memory becomes even more scarce.

This discrepancy raises a fundamental question:

<div class="blog-quote">If the Virtual Address Space is much larger than physical RAM, where do the Pages that are not currently in RAM exist?</div>

---

## 2. The Storage Hierarchy

To resolve the physical limits of RAM, operating systems leverage **Secondary Memory**.

Secondary Memory refers to persistent storage devices, such as Solid-State Drives (SSDs) or traditional hard disks. 

The differences between these two storage tiers shape how operating systems manage memory:

*   **Physical RAM**:
    *   **Speed**: Extremely fast (accessible in nanoseconds).
    *   **Direct Access**: Connected directly to the CPU memory bus.
    *   **Capacity**: Highly limited and expensive.
    *   **Volatility**: Volatile (loses all data when power is removed).
*   **Secondary Storage**:
    *   **Speed**: Much slower than RAM (accessible in microseconds or milliseconds).
    *   **Direct Access**: Cannot be accessed directly by the CPU instructions.
    *   **Capacity**: Much larger and significantly cheaper.
    *   **Volatility**: Persistent (retains data when powered off).

The key insight is that a Page does not have to reside in physical RAM at every moment. Some Pages can be kept in Secondary Storage until they are explicitly needed by the CPU.

---

## 3. Demand Paging

Instead of loading all Pages of a process into physical RAM immediately when the program starts, modern operating systems employ **Demand Paging**.

<div class="blog-quote">**Demand Paging** is a memory management strategy where Pages are loaded into physical memory only when the process explicitly requests them during execution.</div>

Consider a process with four Pages. Under Demand Paging, the memory state might look like this:

*   **Page 0** → Loaded in Physical RAM
*   **Page 1** → Loaded in Physical RAM
*   **Page 2** → Stored in Secondary Storage
*   **Page 3** → Loaded in Physical RAM

Even though Page 2 is not currently resident in physical RAM, it remains a valid part of the process's Virtual Address Space. The Page Table keeps track of this status using a special flag called the **Present (or Valid) Bit**.

---

## 4. The Page Fault

What happens if the CPU attempts to read an instruction or data located inside Page 2?

When the MMU queries the Page Table for Page 2, it detects that the Present Bit is set to `0` (Invalid/Not Present). The MMU cannot complete the translation. It halts the instruction and signals the processor:

$$\text{Present Bit is 0} \rightarrow \text{Trigger a Page Fault Interrupt}$$

This event is called a **Page Fault**.

<div class="blog-quote">A **Page Fault** is a hardware interrupt raised by the MMU when a program accesses a Page that is mapped in its virtual address space but is not currently loaded into physical RAM.</div>

A Page Fault is not a software crash or a programming error. It is a normal, expected control event that handoffs execution to the operating system to load the required page from disk.

---

## 5. EdgeCase: The Missing Page

Walk through the step-by-step sequence of a Page Fault. 

In this scenario, the Virtual Address Space contains Pages 0 to 3. Frames 0 to 2 are occupied, while Frame 3 is free. Page 2 is currently stored in Secondary Storage. Watch what happens when the CPU requests Page 2:

<div id="demand-paging-edgecase" class="edgecase-container"></div>

---

## 6. The Next Bottleneck

Demand Paging allows the operating system to execute programs that are much larger than the physical RAM by loading pages dynamically as they are referenced.

But this strategy works smoothly only as long as there is an empty Frame available in RAM (like Frame 3 in our simulation) to receive the page.

What happens if the physical RAM is completely full?

Imagine this physical memory state:
*   **Frame 0** $\rightarrow$ Occupied by Page A
*   **Frame 1** $\rightarrow$ Occupied by Page B
*   **Frame 2** $\rightarrow$ Occupied by Page C

Now, the CPU requests **Page D**, which is in Secondary Storage. There are no free frames left.

To bring Page D in, the operating system must first select one of the active pages (A, B, or C) to evict back to secondary storage to make room.

But how does it choose?

<div class="blog-quote">**Which Page should be replaced?**</div>
