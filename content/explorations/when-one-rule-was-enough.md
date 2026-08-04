---
id: "when-one-rule-was-enough"
category: "Operating Systems"
series: "Operating Systems"
title: "When One Rule Was Enough"
subtitle: "Understanding Non-Preemptive Scheduling"
date: "3rd August, 2026"
tags: ["Kernel", "Scheduling", "Non-Preemptive", "FCFS", "SJF", "Priority"]
---

In *The Rules of Fairness*, we saw that the scheduler requires rules to make consistent choices. The earliest generation of scheduling policies shared one simple, absolute assumption: once the CPU began executing a process, it stayed with that process until its work was complete. 

This philosophy is known as **Non-Preemptive Scheduling**.

Under a non-preemptive model, a running process cannot be interrupted by the operating system. Once it receives the CPU, it retains complete control until it either:
*   Finishes its execution (terminates), or
*   Voluntarily blocks (e.g., yields control or waits for an external input/output operation).

---

## The Non-Preemptive Execution Flow

To visualize this philosophy, consider the lifecycle of execution. Once a process is selected from the Ready Queue, it enters the running state and remains there. The CPU cannot swap it out mid-way.

<div class="custom-diagram-wrapper" style="margin: 2.5rem 0; text-align: center;">
  <svg viewBox="0 0 800 120" xmlns="http://www.w3.org/2000/svg" style="max-width: 100%; height: auto; display: block; margin: 0 auto; background: #0b0f19; border: 1px solid rgba(148, 163, 184, 0.08); border-radius: 12px; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);">
    <defs>
      <linearGradient id="flowGrad" x1="0%" y1="0%" x2="100%" y2="0%">
        <stop offset="0%" stop-color="#3b82f6" stop-opacity="0.25"/>
        <stop offset="100%" stop-color="#8b5cf6" stop-opacity="0.05"/>
      </linearGradient>
    </defs>
    <!-- Connectors -->
    <path d="M 150 60 L 220 60" stroke="rgba(148, 163, 184, 0.15)" stroke-width="2" fill="none"/>
    <polygon points="220,60 212,55 212,65" fill="rgba(148, 163, 184, 0.25)"/>
    <path d="M 370 60 L 440 60" stroke="rgba(148, 163, 184, 0.15)" stroke-width="2" fill="none"/>
    <polygon points="440,60 432,55 432,65" fill="rgba(148, 163, 184, 0.25)"/>
    <path d="M 590 60 L 660 60" stroke="rgba(148, 163, 184, 0.15)" stroke-width="2" fill="none"/>
    <polygon points="660,60 652,55 652,65" fill="rgba(148, 163, 184, 0.25)"/>
    <!-- Ready Queue State -->
    <g transform="translate(20, 30)">
      <rect x="0" y="0" width="130" height="60" rx="6" fill="rgba(30, 41, 59, 0.3)" stroke="rgba(148, 163, 184, 0.12)" stroke-width="1.5"/>
      <text x="65" y="25" fill="#64748B" font-family="'IBM Plex Mono', monospace" font-size="10" font-weight="bold" text-anchor="middle" letter-spacing="0.05em">READY QUEUE</text>
      <text x="65" y="45" fill="#E2E8F0" font-family="'DM Sans', sans-serif" font-size="12" text-anchor="middle">Processes Wait</text>
    </g>
    <!-- Running State -->
    <g transform="translate(240, 30)">
      <rect x="0" y="0" width="130" height="60" rx="6" fill="url(#flowGrad)" stroke="rgba(59, 130, 246, 0.3)" stroke-width="1.5"/>
      <text x="65" y="25" fill="#3b82f6" font-family="'IBM Plex Mono', monospace" font-size="10" font-weight="bold" text-anchor="middle" letter-spacing="0.05em">CPU RUNNING</text>
      <text x="65" y="45" fill="#E2E8F0" font-family="'DM Sans', sans-serif" font-size="12" text-anchor="middle">Active Process</text>
    </g>
    <!-- Non-Preemptive Guard -->
    <g transform="translate(460, 30)">
      <rect x="0" y="0" width="130" height="60" rx="6" fill="rgba(139, 92, 246, 0.1)" stroke="rgba(139, 92, 246, 0.2)" stroke-width="1.5"/>
      <text x="65" y="25" fill="#a78bfa" font-family="'IBM Plex Mono', monospace" font-size="10" font-weight="bold" text-anchor="middle" letter-spacing="0.05em">NO INTERRUPT</text>
      <text x="65" y="45" fill="#E2E8F0" font-family="'DM Sans', sans-serif" font-size="12" text-anchor="middle">Runs to Finish</text>
    </g>
    <!-- Finished State -->
    <g transform="translate(680, 30)">
      <rect x="0" y="0" width="100" height="60" rx="6" fill="rgba(16, 185, 129, 0.1)" stroke="rgba(16, 185, 129, 0.2)" stroke-width="1.5"/>
      <text x="50" y="25" fill="#10b981" font-family="'IBM Plex Mono', monospace" font-size="10" font-weight="bold" text-anchor="middle" letter-spacing="0.05em">COMPLETED</text>
      <text x="50" y="45" fill="#E2E8F0" font-family="'DM Sans', sans-serif" font-size="12" text-anchor="middle">Yields CPU</text>
    </g>
  </svg>
</div>

---

## Three Classic Non-Preemptive Policies

When the kernel does not interrupt, the only choice it makes is *who starts next*. This choice is guided by one of three classic rules:

*   **First-Come, First-Served (FCFS):** The simplest possible rule. Whichever process enters the Ready Queue first is run first, regardless of how long it takes or its importance.
*   **Shortest Job First (SJF):** The scheduler searches the Ready Queue and executes the process with the shortest estimated burst time first.
*   **Priority Scheduling:** Each process is tagged with an integer representing its priority. The scheduler always starts the process with the highest priority next.

---

## Investigating Scheduling Behavior

To see how these rules change the behavior of a system, let's trace them using a single, identical set of processes.

<div id="non-preemptive-scheduler" class="edgecase-container"></div>

---

## The Key Metrics: Turnaround vs. Waiting

When evaluating these schedulers, engineers look at two primary performance metrics:

*   **Turnaround Time ($TAT$):** The total elapsed time from when a process first arrives in the queue to when it completely finishes execution ($TAT = \text{Completion Time} - \text{Arrival Time}$).
*   **Waiting Time ($WT$):** The total time a process spends sitting in the Ready Queue waiting to execute ($WT = \text{Turnaround Time} - \text{Burst Time}$).

As you simulated above:
*   **FCFS** scheduled processes exactly in arrival sequence, resulting in an average waiting time of **4.67 units**.
*   **SJF** reduced average waiting time to **3.67 units** by running the shorter $P_3$ before $P_2$.
*   **Priority** prioritized the urgent $P_2$ over $P_3$, resulting in an average waiting time of **4.67 units**.

---

## The EdgeCase: Emergency Arrival

These non-preemptive rules worked well for early batch-processing computers. But what happens in a real-time system when an critical task suddenly wakes up?

Select the **EdgeCase** simulation tab above. In this scenario, we use the exact same process table, but we introduce one addition: at Time = 1, an emergency process ($P_{EM}$) with priority 0 (highest) arrives. 

Observe the timeline:
*   At Time = 0, $P_1$ begins running.
*   At Time = 1, $P_{EM}$ arrives. It is the most critical process in the system.
*   But because the scheduler is **non-preemptive**, $P_1$ cannot be interrupted. $P_{EM}$ is forced to wait in the Ready Queue for **5 full time units** until $P_1$ finishes at Time = 6.

This is the fundamental limitation of non-preemptive scheduling: **long-running tasks block critical work, and the kernel is powerless to stop them.**

---

The early policies were simple and predictable. But when a system must react to user inputs or critical hardware interrupts, waiting is no longer an option.

Should the CPU continue executing a long task, or should it force it to yield?

Let's find out how the kernel breaks the rule of non-preemption.
