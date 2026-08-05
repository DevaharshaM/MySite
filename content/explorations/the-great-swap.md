---
id: "the-great-swap"
category: "Operating Systems"
series: "Operating Systems"
title: "The Great Swap"
subtitle: "How the Kernel swaps the running mind of the CPU."
date: "5th August, 2026"
tags: ["Kernel", "Process", "PCB", "Context Switching", "Operating Systems"]
---

In the previous exploration, the Kernel learned how to create a Process Control Block (PCB) to act as a bookmark for a paused task.

But a bookmark alone is static. To actually share a single CPU core among multiple processes, the Kernel must perform a high-speed maneuver: it must swap the executing state of one process for another.

This is the moment of the swap. How does the CPU transition without losing its way?

---

## 1. EdgeCase: The Choice of the Kernel

Below is a live CPU core executing a task. A high-priority process is about to arrive, triggering an interrupt. 

As the Kernel, you must decide how to handle the execution state of the currently running process before starting the new one.

<div id="swap-edgecase" class="edgecase-container"></div>

## 2. The Technical Term: Context Switching

The operation you just experienced is called a **Context Switch**. 

The "context" refers to the execution state of the process—the program counter, stack pointer, and current registers holding active values. Swapping this context is the foundational mechanism that allows operating systems to support multitasking. 

Without it, CPU sharing would be impossible, and a single crashed or frozen process would lock up the entire system.

Classic scheduling policies taught us the fundamental ideas of how to distribute execution time. But modern operating systems no longer rely on a single, simple rule.

How do Linux, Windows, macOS, and Android decide which Process runs next?
