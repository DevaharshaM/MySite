---
id: "the-rules-of-fairness"
category: "Operating Systems"
series: "Operating Systems"
title: "The Rules of Fairness"
subtitle: "How the Kernel turns difficult choices into predictable decisions."
date: "3rd August, 2026"
tags: ["Kernel", "Scheduling", "Policies", "Architecture"]
---
In Manthana, every scheduling decision produced a different consequence. Prioritizing the sensor starved the diagnostics; protecting the audio buffer delayed the flash logger. There was no obvious "correct" choice.

If intuition is not enough, then how does the Kernel decide?

The answer lies in Scheduling Policies.

---

## Policies vs. Mechanisms

To understand how a scheduler works, we must distinguish between two related concepts:

*   **The Mechanism (The Scheduler):** This is the code that performs the transition from one Process to another. The technical details of this transition, known as a **Context Switch**, will be explored later in our Operating Systems journey.
*   **The Policy (The Ruleset):** This is the algorithm or set of rules that determines *which* process from the Ready Queue should be selected next.

The mechanism is universal—it remains the same regardless of what programs you are running. The policy is configurable—it changes depending on what goals the system is trying to optimize.

---

<div class="custom-diagram-wrapper" style="margin: 2.5rem 0; text-align: center;">
  <svg viewBox="0 0 800 240" xmlns="http://www.w3.org/2000/svg" style="max-width: 100%; height: auto; display: block; margin: 0 auto; background: #0b0f19; border: 1px solid rgba(148, 163, 184, 0.08); border-radius: 12px; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);">
    <!-- Gradients -->
    <defs>
      <linearGradient id="policyGrad" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#14b8a6" stop-opacity="0.2"/>
        <stop offset="100%" stop-color="#0d9488" stop-opacity="0.05"/>
      </linearGradient>
      <linearGradient id="schedulerGrad" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#3b82f6" stop-opacity="0.2"/>
        <stop offset="100%" stop-color="#1d4ed8" stop-opacity="0.05"/>
      </linearGradient>
      <linearGradient id="cpuGrad" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#8b5cf6" stop-opacity="0.25"/>
        <stop offset="100%" stop-color="#6d28d9" stop-opacity="0.05"/>
      </linearGradient>
    </defs>
    <!-- Connectors -->
    <!-- Ready Queue to Policy -->
    <path d="M 180 120 L 250 120" stroke="rgba(148, 163, 184, 0.15)" stroke-width="2" fill="none" stroke-dasharray="4"/>
    <polygon points="250,120 242,115 242,125" fill="rgba(148, 163, 184, 0.25)"/>
    <!-- Policy to Scheduler -->
    <path d="M 410 120 L 460 120" stroke="rgba(20, 184, 166, 0.4)" stroke-width="2" fill="none"/>
    <polygon points="460,120 452,115 452,125" fill="#14b8a6"/>
    <!-- Scheduler to CPU -->
    <path d="M 610 120 L 660 120" stroke="rgba(59, 130, 246, 0.4)" stroke-width="2" fill="none"/>
    <polygon points="660,120 652,115 652,125" fill="#3b82f6"/>
    <!-- Ready Queue (Left) -->
    <g transform="translate(30, 60)">
      <rect x="0" y="0" width="150" height="120" rx="8" fill="rgba(30, 41, 59, 0.3)" stroke="rgba(148, 163, 184, 0.12)" stroke-width="1.5"/>
      <text x="75" y="25" fill="#64748B" font-family="'IBM Plex Mono', monospace" font-size="11" font-weight="bold" text-anchor="middle" letter-spacing="0.05em">READY QUEUE</text>
      <!-- Queue elements -->
      <g transform="translate(15, 45)">
        <rect x="0" y="0" width="35" height="50" rx="4" fill="#1E293B" stroke="rgba(148, 163, 184, 0.2)" stroke-width="1"/>
        <text x="17.5" y="28" fill="#E2E8F0" font-family="'IBM Plex Mono', monospace" font-size="11" text-anchor="middle">P1</text>
      </g>
      <g transform="translate(60, 45)">
        <rect x="0" y="0" width="35" height="50" rx="4" fill="#1E293B" stroke="rgba(148, 163, 184, 0.2)" stroke-width="1"/>
        <text x="17.5" y="28" fill="#E2E8F0" font-family="'IBM Plex Mono', monospace" font-size="11" text-anchor="middle">P2</text>
      </g>
      <g transform="translate(105, 45)">
        <rect x="0" y="0" width="35" height="50" rx="4" fill="#1E293B" stroke="rgba(148, 163, 184, 0.2)" stroke-width="1"/>
        <text x="17.5" y="28" fill="#E2E8F0" font-family="'IBM Plex Mono', monospace" font-size="11" text-anchor="middle">P3</text>
      </g>
    </g>
    <!-- Scheduling Policy (Center-Left) -->
    <g transform="translate(260, 60)">
      <rect x="0" y="0" width="150" height="120" rx="8" fill="url(#policyGrad)" stroke="rgba(20, 184, 166, 0.3)" stroke-width="1.5"/>
      <text x="75" y="25" fill="#14b8a6" font-family="'IBM Plex Mono', monospace" font-size="11" font-weight="bold" text-anchor="middle" letter-spacing="0.05em">SCHEDULING POLICY</text>
      <text x="75" y="55" fill="#E2E8F0" font-family="'DM Sans', sans-serif" font-size="13" font-weight="bold" text-anchor="middle">The Ruleset</text>
      <rect x="25" y="75" width="100" height="26" rx="4" fill="rgba(20, 184, 166, 0.1)" stroke="rgba(20, 184, 166, 0.2)" stroke-width="1"/>
      <text x="75" y="91" fill="#14b8a6" font-family="'IBM Plex Mono', monospace" font-size="10" text-anchor="middle">Determines "How"</text>
    </g>
    <!-- Scheduler (Center-Right) -->
    <g transform="translate(470, 60)">
      <rect x="0" y="0" width="140" height="120" rx="8" fill="url(#schedulerGrad)" stroke="rgba(59, 130, 246, 0.3)" stroke-width="1.5"/>
      <text x="70" y="25" fill="#3b82f6" font-family="'IBM Plex Mono', monospace" font-size="11" font-weight="bold" text-anchor="middle" letter-spacing="0.05em">SCHEDULER</text>
      <text x="70" y="55" fill="#E2E8F0" font-family="'DM Sans', sans-serif" font-size="13" font-weight="bold" text-anchor="middle">The Mechanism</text>
      <rect x="20" y="75" width="100" height="26" rx="4" fill="rgba(59, 130, 246, 0.1)" stroke="rgba(59, 130, 246, 0.2)" stroke-width="1"/>
      <text x="70" y="91" fill="#3b82f6" font-family="'IBM Plex Mono', monospace" font-size="10" text-anchor="middle">Executes Choice</text>
    </g>
    <!-- CPU Core (Right) -->
    <g transform="translate(670, 60)">
      <rect x="0" y="0" width="100" height="120" rx="8" fill="url(#cpuGrad)" stroke="rgba(139, 92, 246, 0.4)" stroke-width="1.5"/>
      <!-- CPU Inner Details -->
      <rect x="10" y="10" width="80" height="100" rx="6" fill="none" stroke="rgba(139, 92, 246, 0.15)" stroke-width="1" stroke-dasharray="3"/>
      <text x="50" y="55" fill="#a78bfa" font-family="'Syne', sans-serif" font-weight="bold" font-size="14" text-anchor="middle">CPU</text>
      <text x="50" y="75" fill="#64748B" font-family="'IBM Plex Mono', monospace" font-size="9" text-anchor="middle">ACTIVE CORE</text>
    </g>
  </svg>
</div>

---

## Why Multiple Policies Exist

There is no single "correct" policy because there is no single engineering goal. Different computer systems prioritize different objectives:

*   **Fairness:** Ensuring that every active process eventually gets a turn on the processor. No process should starve in memory indefinitely.
*   **Responsiveness:** Prioritizing user interaction. A text editor or cursor should respond within milliseconds, even if heavy background calculations are running.
*   **Throughput:** Maximizing the total number of processes completed per hour. This is vital for servers running background data-processing batches.
*   **Real-Time Behaviour:** Guaranteeing that critical tasks execute within strict deadlines. An engine controller sensor loop must run on time, no matter what.

A scheduling policy is an expression of what a system values most.

---

## Four Classic Scheduling Policies

Modern operating systems like Linux, Windows, or macOS use highly sophisticated scheduling architectures. However, these complex production schedulers are built upon a small set of classic, foundational concepts.

Before we can understand how modern schedulers combine these ideas, we must first understand the four classic policies that represent the historical foundations of scheduling:

### 1. First-Come, First-Served (FCFS)
*   **The Idea:** "Respect arrival."
*   The scheduler selects whichever process arrived first in the Ready Queue. It runs until it yields or terminates.

### 2. Shortest Job First (SJF)
*   **The Idea:** "Finish quickly."
*   The scheduler examines all ready processes and runs the one with the shortest estimated execution duration first.

### 3. Priority Scheduling
*   **The Idea:** "Protect what matters most."
*   Each process is assigned a priority value. The scheduler always executes the process with the highest priority first.

### 4. Round Robin (RR)
*   **The Idea:** "Everyone deserves a turn."
*   The scheduler gives each process a tiny, fixed slice of execution time (a quantum). When time runs out, the process is preempted and sent to the back of the queue.

---

These classic policies introduced different ways of thinking about fairness. Each solved a particular engineering problem, but each also revealed new, unforeseen limitations.

Before we understand how modern operating systems schedule processes, we must first understand these foundations.

Let's begin with the simplest scheduling rule.
