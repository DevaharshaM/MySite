---
id: who-goes-next
title: "Who Goes Next?"
subtitle: "Understanding who decides which Process gets the processor."
category: "Operating Systems"
series: "System Explorations"
date: "2nd August, 2026"
tags: ["Process", "Scheduler", "Kernel", "Operating System", "Manthana"]
---

Imagine your computer has just booted up. Multiple applications are open, a file download has initialized, and audio is ready to stream. Several processes are sitting in the **Ready** state, waiting to run.

But there is only one processor core. And only one instruction sequence can execute at any single nanosecond.

Every process wants the CPU. If there are no rules, who decides which one executes? 

---

## Introducing the Scheduler

To coordinate this competition, the operating system kernel relies on a core component: the **Scheduler**.

The Scheduler is the gatekeeper of execution. Its role is simple to state, yet highly complex to engineer: it decides which process in the Ready queue receives CPU time, and when. At this stage, we do not care *how* it makes this decision (which algorithm it uses). We only care about its role as the manager of execution.

Operating systems divide this task into three distinct types of schedulers, each operating on a different timescale and handling a different state of the process lifecycle.

---

## 1. Long-Term Scheduler (Job Scheduler)

*   **The Question:** *Which programs on disk should become active processes in memory?*
*   **The Purpose:** When you start a program, it doesn't instantly run on the CPU. The Long-Term Scheduler determines if the system has enough RAM and resources to allocate a new process. It controls the **degree of multiprogramming**—the total number of active processes residing in memory. It runs slowly, only when new tasks are created.

---

## 2. Medium-Term Scheduler (Swapping Coordinator)

*   **The Question:** *Which processes should temporarily leave memory to free up RAM?*
*   **The Purpose:** If too many processes are running, the system runs out of physical memory, leading to thrashing. The Medium-Term Scheduler temporarily removes inactive or blocked processes from RAM and writes their state to a swap space on disk. This is called **Swapping**. When memory pressure drops, it swaps them back into RAM.

---

## 3. Short-Term Scheduler (CPU Scheduler)

*   **The Question:** *Among the ready processes in RAM, who gets the CPU next?*
*   **The Purpose:** This is the primary scheduler. It operates at microsecond speeds. Whenever a running process yields, finishes, or gets interrupted, the Short-Term Scheduler instantly selects the next process from the Ready Queue and dispatches it onto the CPU.

---

## Summary: Schedulers in the Lifecycle

The diagram below visualizes exactly where these three schedulers sit and operate across the process lifecycle states:

```html
<div class="svg-container" style="margin: 2.5rem 0; text-align: center;">
  <svg viewBox="0 0 800 360" width="100%" height="auto" style="background: #151d2a; border-radius: 12px; border: 1px solid rgba(148, 163, 184, 0.08); font-family: system-ui, -apple-system, sans-serif;">
    <defs>
      <marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
        <path d="M 0 1 L 10 5 L 0 9 z" fill="#94a3b8" />
      </marker>
      <linearGradient id="grad-state" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#1e293b" />
        <stop offset="100%" stop-color="#0f172a" />
      </linearGradient>
    </defs>

    <!-- Title -->
    <text x="30" y="35" fill="#ffffff" font-size="14" font-weight="bold">The Scheduler Taxonomy inside the Process Lifecycle</text>
    
    <!-- STATES -->
    <!-- New -->
    <rect x="40" y="160" width="80" height="40" rx="6" fill="url(#grad-state)" stroke="rgba(148, 163, 184, 0.2)" />
    <text x="80" y="184" fill="#94a3b8" font-size="11" font-weight="bold" text-anchor="middle">NEW</text>

    <!-- Ready -->
    <rect x="240" y="160" width="100" height="40" rx="6" fill="url(#grad-state)" stroke="#3b82f6" stroke-width="1.5" />
    <text x="290" y="184" fill="#3b82f6" font-size="11" font-weight="bold" text-anchor="middle">READY</text>

    <!-- Running -->
    <rect x="470" y="160" width="100" height="40" rx="6" fill="url(#grad-state)" stroke="#10b981" stroke-width="1.5" />
    <text x="520" y="184" fill="#10b981" font-size="11" font-weight="bold" text-anchor="middle">RUNNING</text>

    <!-- Terminated -->
    <rect x="670" y="160" width="90" height="40" rx="6" fill="url(#grad-state)" stroke="rgba(148, 163, 184, 0.2)" />
    <text x="715" y="184" fill="#94a3b8" font-size="11" font-weight="bold" text-anchor="middle">TERMINATED</text>

    <!-- Waiting -->
    <rect x="350" y="270" width="100" height="40" rx="6" fill="url(#grad-state)" stroke="#f59e0b" stroke-width="1.5" />
    <text x="400" y="294" fill="#f59e0b" font-size="11" font-weight="bold" text-anchor="middle">WAITING</text>

    <!-- Swapped Out -->
    <rect x="220" y="60" width="140" height="40" rx="6" fill="url(#grad-state)" stroke="#a855f7" stroke-width="1.5" />
    <text x="290" y="84" fill="#a855f7" font-size="11" font-weight="bold" text-anchor="middle">SWAPPED OUT</text>

    <!-- CONNECTORS -->
    <!-- New -> Ready -->
    <line x1="120" y1="180" x2="232" y2="180" stroke="#94a3b8" stroke-width="1.5" marker-end="url(#arrow)" />
    
    <!-- Ready -> Running -->
    <line x1="340" y1="180" x2="462" y2="180" stroke="#94a3b8" stroke-width="1.5" marker-end="url(#arrow)" />

    <!-- Running -> Terminated -->
    <line x1="570" y1="180" x2="662" y2="180" stroke="#94a3b8" stroke-width="1.5" marker-end="url(#arrow)" />

    <!-- Running -> Waiting -->
    <path d="M 520,200 L 450,265" fill="none" stroke="#94a3b8" stroke-width="1.5" marker-end="url(#arrow)" />

    <!-- Waiting -> Ready -->
    <path d="M 370,270 L 300,205" fill="none" stroke="#94a3b8" stroke-width="1.5" marker-end="url(#arrow)" />

    <!-- Running -> Ready (Interrupt) -->
    <path d="M 520,160 Q 405,120 290,160" fill="none" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="3,3" marker-end="url(#arrow)" />

    <!-- Ready -> Swapped Out (Swap Out) -->
    <path d="M 270,160 L 270,108" fill="none" stroke="#94a3b8" stroke-width="1.5" marker-end="url(#arrow)" />
    <!-- Swapped Out -> Ready (Swap In) -->
    <path d="M 310,100 L 310,152" fill="none" stroke="#94a3b8" stroke-width="1.5" marker-end="url(#arrow)" />

    <!-- SCHEDULERS OVERLAYS (Sea-Green Badges) -->
    
    <!-- LTS Overlay -->
    <rect x="135" y="195" width="90" height="24" rx="4" fill="#14b8a6" />
    <text x="180" y="211" fill="#fff" font-size="9" font-weight="bold" text-anchor="middle">LTS (Long-Term)</text>

    <!-- STS Overlay -->
    <rect x="365" y="195" width="90" height="24" rx="4" fill="#14b8a6" />
    <text x="410" y="211" fill="#fff" font-size="9" font-weight="bold" text-anchor="middle">STS (Short-Term)</text>

    <!-- MTS Overlay -->
    <rect x="330" y="105" width="95" height="24" rx="4" fill="#14b8a6" />
    <text x="377" y="121" fill="#fff" font-size="9" font-weight="bold" text-anchor="middle">MTS (Medium-Term)</text>
  </svg>
</div>
```

---

## Manthana

<div id="who-goes-next-manthana" class="manthana-container"></div>
