---
id: "choosing-what-to-forget"
category: "Operating Systems"
series: "Operating Systems"
title: "Choosing What to Forget"
subtitle: "When physical memory is full, which page must be evicted?"
date: "9th August, 2026"
tags: ["Operating Systems", "Memory Management", "Page Replacement", "FIFO", "LRU", "Optimal"]
---

## 1. The Saturation Point

Imagine a system running under constraint. Its physical RAM is small, containing only **3 physical frames**. Right now, physical memory is completely saturated, filled with three active pages:

$$\text{RAM Frames: } [ \text{Page 2} \ | \ \text{Page 5} \ | \ \text{Page 7} ]$$

A thread executes an instruction requesting virtual address space residing in **Page 3**. 

The MMU looks up the translation in the Page Table, finds it invalid, and raises a **Page Fault**. The Operating System traps the fault and prepares to copy Page 3 from disk into RAM. But there is a bottleneck: *all physical frames are occupied.*

To resolve the fault and bring Page 3 into memory, the operating system must choose one page currently in RAM and evict it back to disk.

This decision is known as **Page Replacement**.

## 2. Three Answers to the Same Question

How do we decide which page should leave? The policy we choose determines our system's memory efficiency. Three core algorithms answer this question:

**First-In, First-Out (FIFO)**
*"Which Page arrived first?"*
Evict the oldest page loaded into RAM, regardless of how frequently it is being used.

**Least Recently Used (LRU)**
*"Which Page has been unused the longest?"*
Evict the page that has not been accessed for the longest duration, relying on the principle of temporal locality.

**Optimal (OPT)**
*"Which Page will be needed farthest in the future?"*
Evict the page that will go the longest before being requested again.

## 3. Interactive Page Replacement Simulator

See how these three different strategies handle the exact same reference sequence under the same constraint:

$$\text{Reference Sequence: } 1 \rightarrow 2 \rightarrow 3 \rightarrow 1 \rightarrow 4$$

Observe how the exact same access trace produces completely different eviction choices and page fault rates depending on the active policy.

<div id="page-replacement-edgecase" class="edgecase-container"></div>

### The Mathematical Ideal vs. Hardware Reality

The **Optimal** policy represents the absolute ceiling of performance, guaranteeing the minimum possible Page Faults for any known reference sequence. However, in practice, a real-world operating system cannot implement the Optimal policy because it cannot know future memory references in advance. Real-world systems must approximate this behavior using historical data, making **LRU** the standard benchmark for practical implementation.

---

## 4. Manthana: The Allocation Challenge

Now that we can manage pages inside rigid slots, let's explore a different system constraints challenge.

### External Fragmentation Challenge

<div id="manthana-segmentation-reveal" class="edgecase-container"></div>

We now know how memory can become fragmented.

But fragmentation raises another question:

Can memory be organized around the logical structure of a program instead of treating it as one continuous block?

That's where we go next.
