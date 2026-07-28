---
id: when-hardware-learned-to-interrupt
category: Coordination
series: The Architecture of Time
title: When Hardware Learned to Interrupt
subtitle: The moment machines stopped waiting.
date: 21st June, 2026
tags: [Interrupts, NVIC, Preemption, Latency, Vector Table]
closing_heading: The Limits of Response
closing_paragraphs:
  - Polling wasted CPU time by constantly asking if anything happened. Interrupts solved this by reversing the relationship, allowing the hardware to announce its readiness directly to the core.
  - But as system speeds continued to climb, a new engineering limit emerged. Imagine a high-speed network transceiver receiving thousands of bytes every millisecond, or an ADC sampling at megahertz rates. If the CPU must pause, save registers, jump to an ISR, extract a byte, restore registers, and return for every single byte, the processor is quickly overwhelmed.
  - The CPU now spends less time waiting, but it spends all of its time responding. Handling the data has become more expensive than detecting it.
  - To break this bottleneck, data needed to be moved directly from hardware to memory without involving the CPU at all. That need would lead directly to Direct Memory Access.
closing_quote: Interrupts freed the processor from active waiting, but as speed scaled, the core became a victim of its own responsiveness.
footer: Reflections on hardware interrupt requests and vector table architectures - PrajnaEdge.dev
---

## 1. A World of Waiting

In our previous exploration, we watched a simple bare-metal embedded loop scale from a single button check to a complex array of duties. The microcontroller had to check the UART console, query an ADC sensor, inspect a CAN bus register, and toggle diagnostic LEDs. The result was a monolithic loop:

```c
while(1) {
    CheckButton();
    CheckUART();
    CheckADC();
    CheckCAN();
}
```

This is polling. Its primary flaw is structural: it ties coordination entirely to the execution path of the software. The CPU spends almost all its time and power asking if something has happened, only to receive 'no' as an answer. It keeps the core running at 100% load, consuming maximum power simply to check idle pins. It is a system built on active waiting, where responsiveness degrades as more peripherals stretch the loop cycle time.

## 2. The Reversal

What if we could reverse this relationship? Instead of the central processor constantly interrogating passive hardware components, what if the hardware could announce events instead?

This is the core philosophy of **Interrupts**. Rather than the CPU spinning in a loop asking *'Has anything happened?'*, the hardware peripherals are given a dedicated channel to signal the CPU: *'Something happened. Act now.'*

This simple reversal represents the most fundamental shift in embedded system architecture. It decouples event detection from the sequential flow of execution, freeing the CPU to execute background calculations or enter deep low-power sleep modes until the physical world demands its attention.

## 3. The Doorbell Analogy

To appreciate this shift, imagine waiting for a package delivery. Under a polling strategy, you must walk to the front door every ten seconds, open it, check the porch, close the door, and walk back. You can do nothing else; you are entirely consumed by the active wait.

An interrupt-driven approach equips the door with a bell. You sit down, read a book, or fall asleep. The visitor arrives and presses the button. The bell rings, interrupting your activity. You bookmark your page, answer the door, sign for the package, and return to exactly where you left off. The active checking is gone, replaced by a reactive trigger.

## 4. The Anatomy of an Interrupt

How does this handoff occur in raw silicon? When an external event occurs—such as a button pin falling low or a byte arriving in a UART buffer—the peripheral asserts a physical interrupt request (IRQ) line connected to the processor core. The hardware handoff then unfolds automatically:

1. **Assertion**: The peripheral drives its IRQ line to its active state (high or low).
2. **Synchronization**: The core detects the active line and waits to finish its currently executing machine instruction (typically 1 to 5 clock cycles).
3. **Context Saving**: The CPU automatically halts normal execution and pushes its current register states (such as the Program Counter, Link Register, Stack Pointer, and Status Register) onto the stack. This preserves the exact state of the background program.
4. **Vector Fetch**: The processor reads the vector table to fetch the memory address of the handler function associated with the triggering IRQ.
5. **Execution**: The Program Counter jumps to that address, and the CPU begins executing the **Interrupt Service Routine (ISR)**.
6. **Return**: Once the handler finishes, it executes a special return instruction. The CPU pops the saved registers back off the stack, restoring the CPU state, and resumes the background program exactly where it was paused.

![The step-by-step lifecycle of an interrupt request handoff.](Images/interrupt_flow.svg)

## 5. Interrupt Latency

While interrupts resolve the polling delay bottleneck, they do not respond instantly. In embedded systems engineering, **Interrupt Latency** is the exact delay between the assertion of the hardware IRQ line and the execution of the first instruction in the ISR.

Latency is a hardware tax composed of several parts: completing the current instruction, pushing CPU registers onto the stack (stacking), syncing clocks between the peripheral bus and core, and executing entry handler routines. In modern ARM Cortex-M processors, this hardware stacking and lookup process is heavily optimized, taking as few as 12 to 24 clock cycles. But in real-time systems, every cycle counts. If another interrupt is already running or interrupts are temporarily disabled by the driver, this latency can stretch, potentially causing missed deadlines.

![The timing breakdown of hardware stacking and vector fetch latencies.](Images/interrupt_latency.svg)

## 6. Priority and Preemption

A real embedded system has multiple interrupt sources. What happens if a button press occurs at the exact same millisecond a critical CAN network alarm frame arrives? How does the hardware choose?

This is solved by **Interrupt Priority**. Every interrupt source is assigned a priority value. When multiple IRQ lines are asserted simultaneously, the core's hardware interrupt controller (such as the Nested Vectored Interrupt Controller, or NVIC, in ARM architectures) compares their values and runs the highest-priority handler first. If a lower-priority handler is already running when a higher-priority event arrives, the hardware executes **Preemption**—instantly pausing the lower-priority ISR, pushing its registers to the stack, and running the higher-priority ISR. Only when the high-priority handler completes does the lower-priority handler resume.

![A multi-lane timing diagram visualizing preemption and context nesting.](Images/interrupt_priority.svg)

## 7. Nested Interrupts

This ability to preempt running handlers is called **Nesting**. Without nesting, a slow, low-priority handler (like a periodic temperature readout) would block a high-speed critical line (like a motor safety trip signal) for milliseconds, defeating the real-time guarantees of the system.

Prioritization and nesting ensure that critical routines remain deterministic, regardless of other activities. However, nesting also introduces a system risk: stack depth. Each nested layer pushes more registers onto the RAM stack. If too many interrupts nest, the stack can overrun into application variables, leading to silent memory corruption.

## 8. The Vector Table

How does the hardware translate a physical IRQ number into a software function address? It reads the **Vector Table**.

The Vector Table is an array of function pointers placed at a fixed location in memory (typically at the very bottom of the Flash partition, `0x0000_0000` or `0x0800_0000`). Each index corresponds to a specific hardware line: index 0 is the initial stack pointer, index 1 is the Reset Vector, index 2 is the Non-Maskable Interrupt (NMI), and subsequent indices map to internal faults, timers, and external peripherals.

When a peripheral triggers, the processor uses the IRQ index to offset into this table, reads the 32-bit address stored there, and jumps directly to that address. You may recognize the first entries from *The First Instruction*: the Reset Vector is simply the very first interrupt address fetched by the silicon when power is applied.

![The mapping between hardware address indexes and handler code in flash.](Images/interrupt_vector_table.svg)

## 9. Real Embedded Examples

Interrupts are the invisible coordination layer of modern electronics. In a UART interface, an interrupt triggers each time a character lands in the receive register, ensuring the CPU extracts it before it is overwritten. In a motor control loop, timer compare interrupts trigger microsecond-aligned PWM adjustments. In safety systems, CAN controllers trigger emergency handlers the moment an error frame is detected.

By replacing active waiting with reactive notifications, interrupts allow microcontrollers to sleep when inactive and respond with microsecond precision when needed. They represent the moment hardware became coordinate-aware.
