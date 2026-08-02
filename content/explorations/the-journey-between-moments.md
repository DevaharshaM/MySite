---
id: the-journey-between-moments
title: "The Journey Between Moments"
subtitle: "Understanding how a Process changes throughout its lifetime."
category: "Operating Systems"
series: "System Explorations"
date: "2nd August, 2026"
tags: ["Process", "Process State", "Kernel", "Operating System", "Lifecycle"]
---

Does a process simply start, execute, and die? 

When we write `int main()`, we often think of our code as a straight line. It enters the first brace, marches sequentially through each instruction, and exits at the return statement. 

But inside a running machine, the journey of a process is far from simple. It is not a static block of instructions. It is a living, breathing entity that constantly shifts, pauses, waits, and restarts. 

Let's trace the life of a process to see how it moves between moments.

---

## The Living Entity

A process does not have exclusive ownership of the processor. If it did, a single file download or input wait would freeze your entire system. To keep the computer responsive, the Operating System must constantly swap processes in and out of execution.

For the Kernel to coordinate this dance, it must know exactly what each process is doing at any given millisecond. 

* Is it actively executing?
* Is it waiting for a key press?
* Is it ready to run, but waiting for its turn?

To track this, the Kernel manages every process through a formal **Process Lifecycle**.

---

## The State Machine of Life

At any moment, a process exists in one of five primary states. The transitions between these states form a precise state machine managed entirely by the Kernel.

```html
<div class="svg-container" style="margin: 2.5rem 0; text-align: center;">
  <svg viewBox="0 0 800 380" width="100%" height="auto" style="background: #151d2a; border-radius: 12px; border: 1px solid rgba(148, 163, 184, 0.08); font-family: system-ui, -apple-system, sans-serif;">
    <!-- Definitions for Markers -->
    <defs>
      <marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
        <path d="M 0 1 L 10 5 L 0 9 z" fill="#94a3b8" />
      </marker>
      <marker id="arrow-blue" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
        <path d="M 0 1 L 10 5 L 0 9 z" fill="#60a5fa" />
      </marker>
      <marker id="arrow-green" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
        <path d="M 0 1 L 10 5 L 0 9 z" fill="#34d399" />
      </marker>
      <linearGradient id="grad-new" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#475569" />
        <stop offset="100%" stop-color="#334155" />
      </linearGradient>
      <linearGradient id="grad-ready" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#2563eb" />
        <stop offset="100%" stop-color="#1d4ed8" />
      </linearGradient>
      <linearGradient id="grad-running" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#059669" />
        <stop offset="100%" stop-color="#047857" />
      </linearGradient>
      <linearGradient id="grad-waiting" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#d97706" />
        <stop offset="100%" stop-color="#b45309" />
      </linearGradient>
      <linearGradient id="grad-terminated" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#3f3f46" />
        <stop offset="100%" stop-color="#27272a" />
      </linearGradient>
    </defs>

    <!-- NEW STATE -->
    <rect x="50" y="140" width="100" height="60" rx="8" fill="url(#grad-new)" stroke="rgba(255,255,255,0.05)" />
    <text x="100" y="175" fill="#f1f5f9" font-size="14" font-weight="bold" text-anchor="middle">NEW</text>
    
    <!-- READY STATE -->
    <rect x="230" y="140" width="110" height="60" rx="8" fill="url(#grad-ready)" stroke="rgba(255,255,255,0.05)" />
    <text x="285" y="175" fill="#f1f5f9" font-size="14" font-weight="bold" text-anchor="middle">READY</text>
    
    <!-- RUNNING STATE -->
    <rect x="440" y="140" width="110" height="60" rx="8" fill="url(#grad-running)" stroke="rgba(255,255,255,0.05)" />
    <text x="495" y="175" fill="#f1f5f9" font-size="14" font-weight="bold" text-anchor="middle">RUNNING</text>
    
    <!-- TERMINATED STATE -->
    <rect x="640" y="140" width="110" height="60" rx="8" fill="url(#grad-terminated)" stroke="rgba(255,255,255,0.05)" />
    <text x="695" y="175" fill="#a1a1aa" font-size="13" font-weight="bold" text-anchor="middle">TERMINATED</text>
    
    <!-- WAITING / BLOCKED STATE -->
    <rect x="335" y="270" width="130" height="60" rx="8" fill="url(#grad-waiting)" stroke="rgba(255,255,255,0.05)" />
    <text x="400" y="305" fill="#f1f5f9" font-size="14" font-weight="bold" text-anchor="middle">WAITING</text>

    <!-- CONNECTIONS & LABELS -->
    
    <!-- New -> Ready (Admitted) -->
    <line x1="150" y1="170" x2="222" y2="170" stroke="#94a3b8" stroke-width="2" marker-end="url(#arrow)" />
    <text x="186" y="155" fill="#94a3b8" font-size="11" text-anchor="middle">Admitted</text>
    
    <!-- Ready -> Running (Dispatch) -->
    <line x1="340" y1="160" x2="432" y2="160" stroke="#60a5fa" stroke-width="2" marker-end="url(#arrow-blue)" />
    <text x="390" y="148" fill="#60a5fa" font-size="11" text-anchor="middle">Dispatched</text>
    
    <!-- Running -> Ready (Interrupt / Timeout) -->
    <path d="M 440,180 Q 385,210 340,180" fill="none" stroke="#94a3b8" stroke-width="2" stroke-dasharray="4,4" marker-end="url(#arrow)" />
    <text x="390" y="215" fill="#94a3b8" font-size="11" text-anchor="middle">Interrupt / Timeout</text>
    
    <!-- Running -> Waiting (I/O or Event Wait) -->
    <path d="M 495,200 L 435,264" fill="none" stroke="#fbbf24" stroke-width="2" marker-end="url(#arrow)" />
    <text x="495" y="235" fill="#fbbf24" font-size="11" text-anchor="start">I/O or Event Wait</text>
    
    <!-- Waiting -> Ready (I/O or Event Done) -->
    <path d="M 370,270 L 305,206" fill="none" stroke="#34d399" stroke-width="2" marker-end="url(#arrow-green)" />
    <text x="295" y="250" fill="#34d399" font-size="11" text-anchor="end">Event Complete</text>
    
    <!-- Running -> Terminated -->
    <line x1="550" y1="170" x2="632" y2="170" stroke="#94a3b8" stroke-width="2" marker-end="url(#arrow)" />
    <text x="595" y="155" fill="#94a3b8" font-size="11" text-anchor="middle">Exit</text>
  </svg>
</div>
```

---

## Tracing the States

Let's understand what happens inside each of these moments:

### 1. New
The process is being born. The Kernel reads your executable program from disk, allocates a memory space (Process Control Block), but has not yet loaded it into the main scheduling queue. It is a blueprint waiting to be registered.

### 2. Ready
The process is fully loaded in RAM. It has everything it needs to run—its variables are initialized, its memory structure is set—**except CPU execution time**. It stands in line (the Ready Queue) waiting for the Kernel to hand it the processor.

### 3. Running
The Kernel has dispatched the process. The CPU is actively executing its assembly instructions. Only one process can run on a single CPU core at any literal microsecond. 

### 4. Waiting / Blocked
The process cannot execute, even if the CPU is free. It is waiting for an external event to complete.
*   **Disk Access**: Waiting for a block of file data to load.
*   **Keyboard Input**: Stalled until the user presses a key.
*   **Network Packet**: Waiting for data to arrive over a socket.
*   **Timer**: Sleeping for a specified number of milliseconds.

### 5. Terminated
The process has finished executing its code or was stopped by the system. The Kernel reclaims its memory space, releases its file descriptors, and cleans its tracking metrics. It is now a memory.

---

## Why Do States Change?

A process never changes state arbitrarily. Transitions are driven entirely by **hardware and software events**. 

Consider the typical journey of an application loading a file:

```html
<div class="svg-container" style="margin: 2.5rem 0; text-align: center;">
  <svg viewBox="0 0 800 280" width="100%" height="auto" style="background: #151d2a; border-radius: 12px; border: 1px solid rgba(148, 163, 184, 0.08); font-family: system-ui, -apple-system, sans-serif;">
    <defs>
      <!-- Gradients -->
      <linearGradient id="grad-green-timeline" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#10b981" />
        <stop offset="100%" stop-color="#047857" />
      </linearGradient>
      <linearGradient id="grad-amber-timeline" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#f59e0b" />
        <stop offset="100%" stop-color="#b45309" />
      </linearGradient>
      <linearGradient id="grad-blue-timeline" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#3b82f6" />
        <stop offset="100%" stop-color="#1d4ed8" />
      </linearGradient>
      <linearGradient id="grad-muted-timeline" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#475569" />
        <stop offset="100%" stop-color="#1e293b" />
      </linearGradient>
    </defs>

    <!-- Title / Legend -->
    <text x="30" y="38" fill="#ffffff" font-size="14" font-weight="bold">Dual-Track Process Timeline</text>
    <text x="30" y="56" fill="#94a3b8" font-size="11">Visualizing how CPU is freed for other tasks during Waiting states</text>

    <!-- Labels -->
    <text x="30" y="115" fill="#f1f5f9" font-size="11" font-weight="bold">PROCESS STATE</text>
    <text x="30" y="195" fill="#f1f5f9" font-size="11" font-weight="bold">CPU ALLOCATION</text>

    <!-- PROCESS TRACK BARS -->
    <!-- Running 1 -->
    <rect x="180" y="95" width="120" height="30" rx="6" fill="url(#grad-green-timeline)" />
    <text x="240" y="114" fill="#ffffff" font-size="10" font-weight="bold" text-anchor="middle">RUNNING</text>
    
    <!-- Waiting -->
    <rect x="305" y="95" width="210" height="30" rx="6" fill="url(#grad-amber-timeline)" />
    <text x="410" y="114" fill="#ffffff" font-size="10" font-weight="bold" text-anchor="middle">WAITING (DISK I/O)</text>
    
    <!-- Ready -->
    <rect x="520" y="95" width="130" height="30" rx="6" fill="url(#grad-blue-timeline)" />
    <text x="585" y="114" fill="#ffffff" font-size="10" font-weight="bold" text-anchor="middle">READY (IN QUEUE)</text>
    
    <!-- Running 2 -->
    <rect x="655" y="95" width="115" height="30" rx="6" fill="url(#grad-green-timeline)" />
    <text x="712" y="114" fill="#ffffff" font-size="10" font-weight="bold" text-anchor="middle">RUNNING</text>

    <!-- CPU TRACK BARS -->
    <!-- running our process -->
    <rect x="180" y="175" width="120" height="30" rx="6" fill="url(#grad-green-timeline)" />
    <text x="240" y="194" fill="#ffffff" font-size="10" font-weight="bold" text-anchor="middle">OUR PROCESS</text>
    
    <!-- running other processes -->
    <rect x="305" y="175" width="345" height="30" rx="6" fill="url(#grad-muted-timeline)" stroke="rgba(255,255,255,0.05)" />
    <text x="477" y="194" fill="#94a3b8" font-size="10" font-weight="bold" text-anchor="middle">OTHER TASKS / SYSTEM IDLE</text>
    
    <!-- running our process again -->
    <rect x="655" y="175" width="115" height="30" rx="6" fill="url(#grad-green-timeline)" />
    <text x="712" y="194" fill="#ffffff" font-size="10" font-weight="bold" text-anchor="middle">OUR PROCESS</text>

    <!-- Event connectors (dotted lines) and text -->
    
    <!-- Event 1 -->
    <line x1="302" y1="125" x2="302" y2="175" stroke="#94a3b8" stroke-width="1" stroke-dasharray="3,3" />
    <circle cx="302" cy="125" r="3" fill="#fbbf24" />
    <circle cx="302" cy="175" r="3" fill="#fbbf24" />
    <text x="302" y="146" fill="#fbbf24" font-size="9" font-weight="bold" text-anchor="middle">I/O Request</text>

    <!-- Event 2 -->
    <line x1="517" y1="125" x2="517" y2="175" stroke="#34d399" stroke-width="1" stroke-dasharray="3,3" />
    <circle cx="517" cy="125" r="3" fill="#34d399" />
    <circle cx="517" cy="175" r="3" fill="#34d399" />
    <text x="517" y="146" fill="#34d399" font-size="9" font-weight="bold" text-anchor="middle">Disk Interrupt</text>

    <!-- Event 3 -->
    <line x1="652" y1="125" x2="652" y2="175" stroke="#60a5fa" stroke-width="1" stroke-dasharray="3,3" />
    <circle cx="652" cy="125" r="3" fill="#60a5fa" />
    <circle cx="652" cy="175" r="3" fill="#60a5fa" />
    <text x="652" y="146" fill="#60a5fa" font-size="9" font-weight="bold" text-anchor="middle">Dispatched</text>
  </svg>
</div>
```

1.  **Running**: The process starts reading a file. Because disk access takes millions of CPU cycles, continuing to sit on the CPU would stall the system.
2.  **Waiting**: The process yields the CPU and enters the **Waiting** state. The Kernel parks it away. The CPU is now completely free to run other ready tasks.
3.  **Ready**: Once the disk controller reads the file, it fires an interrupt. The Kernel realizes the data is ready, pulls the process out of the Waiting pool, and moves it to the **Ready** queue.
4.  **Running Again**: The Kernel selects the process from the Ready queue and schedules it onto the CPU. The process picks up exactly where it left off, reading the loaded memory.

---

## Why States Matter

Imagine a modern operating system running hundreds of processes simultaneously. Behind the scenes, the Kernel behaves like a coordinator in a chaotic theater. It must continuously maintain lists:

*   Which process is currently using the processor? (**Running**)
*   Which processes are locked, waiting for files, keys, or networks? (**Waiting**)
*   Which processes are complete and need their resources cleaned up? (**Terminated**)
*   Which processes are ready to run right now? (**Ready**)

This constant shifting is the heartbeat of a responsive system. But as processes stream into the **Ready** queue, a critical dilemma emerges. 

If there are ten processes standing in the Ready line, but only one processor core available, they cannot all execute at once. 

Who decides which process is pulled out of line and given the CPU next? 

And how do we ensure that every process gets a fair turn without starvation?

---
