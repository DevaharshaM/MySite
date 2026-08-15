---
id: when-the-disk-becomes-the-bottleneck
category: "Operating Systems"
series: "Operating Systems"
title: "When the Disk Becomes the Bottleneck"
subtitle: "Comparing FCFS, SSTF, SCAN, and C-SCAN disk scheduling algorithms and latency mitigation."
date: "12th August, 2026"
tags: ["Operating Systems", "Storage Management", "Scheduling", "Latency", "SSD"]
---

## 1. The Queue of Requests

When an operating system is running a modern workload, it is rarely serving one file request at a time. The system's virtual memory manager may be swapping pages, a database might be writing transaction logs, and a web browser could be downloading images simultaneously.

As these operations stack up, they form a **Request Queue** at the storage driver layer. 

For a simplified hard disk model, suppose the controller receives a queue of read/write requests targeting specific LBA cylinder tracks:

```text
98, 183, 37, 122, 14, 124, 65, 67
```

And the physical read/write head is currently positioned at:

```text
Current Head Position: 53
```

To complete these tasks, the operating system must decide the order in which to visit these locations. This coordination is known as **Disk Scheduling**.

---

## 2. The Physical Structure of a Hard Disk

To understand why the order of serving requests matters, we must look at the physical architecture of a traditional mechanical Hard Disk Drive (HDD):

```html
<div class="svg-container" style="margin: 2.5rem 0; text-align: center;">
  <svg viewBox="0 0 600 320" width="100%" height="auto" style="background: #151d2a; border-radius: 12px; border: 1px solid rgba(148, 163, 184, 0.08); font-family: system-ui, -apple-system, sans-serif;">
    <!-- Platter base shadow -->
    <ellipse cx="240" cy="160" rx="150" ry="120" fill="none" stroke="rgba(148, 163, 184, 0.1)" stroke-width="6" />

    <!-- Concentric tracks -->
    <ellipse cx="240" cy="160" rx="140" ry="110" fill="none" stroke="rgba(148, 163, 184, 0.15)" stroke-width="1" />
    <ellipse cx="240" cy="160" rx="110" ry="85" fill="none" stroke="#3b82f6" stroke-width="1.5" stroke-dasharray="3,3" /> <!-- Highlighted Track -->
    <ellipse cx="240" cy="160" rx="80" ry="60" fill="none" stroke="rgba(148, 163, 184, 0.15)" stroke-width="1" />
    <ellipse cx="240" cy="160" rx="50" ry="38" fill="none" stroke="rgba(148, 163, 184, 0.15)" stroke-width="1" />

    <!-- Sector Divisions -->
    <path d="M 240,160 L 90,160" stroke="rgba(148, 163, 184, 0.08)" stroke-width="1" />
    <path d="M 240,160 L 390,160" stroke="rgba(148, 163, 184, 0.08)" stroke-width="1" />
    <path d="M 240,160 L 240,40" stroke="rgba(148, 163, 184, 0.08)" stroke-width="1" />
    <path d="M 240,160 L 240,280" stroke="rgba(148, 163, 184, 0.08)" stroke-width="1" />
    <path d="M 240,160 L 134,75" stroke="rgba(148, 163, 184, 0.08)" stroke-width="1" />
    <path d="M 240,160 L 346,245" stroke="rgba(148, 163, 184, 0.08)" stroke-width="1" />
    
    <!-- Highlighted Sector -->
    <path d="M 240,160 L 134,245 A 140 110 0 0 1 90,160 Z" fill="rgba(16, 185, 129, 0.15)" stroke="#10b981" stroke-width="1.5" />

    <!-- Center Spindle -->
    <circle cx="240" cy="160" r="15" fill="#334155" stroke="#475569" stroke-width="2" />
    <circle cx="240" cy="160" r="4" fill="#0f172a" />

    <!-- Actuator Hub -->
    <circle cx="470" cy="120" r="22" fill="#1e293b" stroke="#475569" stroke-width="2" />
    <circle cx="470" cy="120" r="6" fill="#64748b" />

    <!-- Actuator Arm -->
    <path d="M 470,120 L 330,140" stroke="#64748b" stroke-width="6" stroke-linecap="round" />
    <path d="M 330,140 L 240,145" stroke="#94a3b8" stroke-width="3" stroke-linecap="round" />

    <!-- Read/Write Head -->
    <rect x="238" y="142" width="6" height="6" fill="#f59e0b" stroke="#d97706" stroke-width="1" />

    <!-- Label pointers & Texts -->
    <!-- Spindle -->
    <path d="M 240,160 L 200,210" fill="none" stroke="#64748b" stroke-width="1" stroke-dasharray="2,2" />
    <text x="180" y="222" fill="#94a3b8" font-size="10" text-anchor="middle">Spindle</text>

    <!-- Platter -->
    <path d="M 170,100 L 110,80" fill="none" stroke="#64748b" stroke-width="1" stroke-dasharray="2,2" />
    <text x="100" y="75" fill="#94a3b8" font-size="10" text-anchor="middle">Platter</text>

    <!-- Track -->
    <path d="M 335,115 L 390,90" fill="none" stroke="#3b82f6" stroke-width="1" stroke-dasharray="2,2" />
    <text x="410" y="85" fill="#60a5fa" font-size="10" font-weight="bold">Track (Cylinder)</text>

    <!-- Sector -->
    <path d="M 125,200 L 90,235" fill="none" stroke="#10b981" stroke-width="1" stroke-dasharray="2,2" />
    <text x="90" y="250" fill="#34d399" font-size="10" font-weight="bold">Sector</text>

    <!-- Actuator Arm -->
    <path d="M 400,132 L 440,175" fill="none" stroke="#64748b" stroke-width="1" stroke-dasharray="2,2" />
    <text x="450" y="190" fill="#94a3b8" font-size="10" text-anchor="middle">Actuator Arm</text>

    <!-- R/W Head -->
    <path d="M 241,142 L 210,100" fill="none" stroke="#f59e0b" stroke-width="1" stroke-dasharray="2,2" />
    <text x="210" y="92" fill="#fbbf24" font-size="10" font-weight="bold">Read/Write Head</text>
  </svg>
</div>
```

The device is composed of the following physical units:
* **Platter**: Magnetic circular disk spinning at high speeds (e.g., 7200 RPM).
* **Spindle**: The central shaft that rotates the platters.
* **Tracks**: Concentric logical rings on the platter surface where data is recorded.
* **Sectors**: Segments dividing each track. Each sector holds a fixed amount of data (traditionally 512 bytes or 4 KB).
* **Read/Write Head**: A tiny sensor that floats just above the platter surface, reading magnetic orientations.
* **Actuator Arm**: A mechanical arm that moves the head radially inward or outward to target different tracks.

---

## 3. HDD Access Performance

Because of this mechanical design, reading or writing data from a physical track requires mechanical movements that introduce physical delay:

### Seek Time
The time required for the actuator arm to physically move the read/write head from its current track to the target track.

### Rotational Latency
The time the head must wait for the platter to spin around until the target sector passes directly underneath the read/write head.

### Access Time
The total time elapsed from the moment the OS requests a block to the moment it is retrieved. Conceptually:

$$\text{Access Time} \approx \text{Seek Time} + \text{Rotational Latency} + \text{Transfer Time}$$

Mechanical seek time and rotational latency take milliseconds—an eternity compared to CPU registers or memory. If the head must repeatedly jump between distant tracks, the actuator arm spends all its time seeking, causing overall I/O performance to plummet.

---

## 4. First-In, First-Out (FCFS)

The simplest scheduling policy is **First-Come, First-Served (FCFS)**:

```text
53 → 98 → 183 → 37 → 122 → 14 → 124 → 65 → 67
```

* **Advantage**: It is simple to implement and perfectly fair. Requests are served in the exact order they arrive, ensuring zero starvation.
* **Problem**: It completely ignores the head's physical location. The head is forced to sweep wildly back and forth across the platter, resulting in massive cumulative seek distance (640 cylinders for our sequence).

---

## 5. Shortest Seek Time First (SSTF)

To minimize seek overhead, **Shortest Seek Time First (SSTF)** prioritizes proximity:

```text
53 → 65 → 67 → 37 → 14 → 98 → 122 → 124 → 183
```

At each step, the algorithm calculates the distance from the head's current position to all pending requests and moves to the closest one.
* **Advantage**: Considerably reduces total seek distance (cut from 640 to 236 cylinders in our example), boosting throughput.
* **Problem**: Prone to **starvation**. If the queue constantly receives new requests located near the active middle tracks, distant requests (such as LBA 183) may wait indefinitely.

---

## 6. SCAN: The Elevator Algorithm

To combine efficiency with fairness, **SCAN** sweeps the disk symmetrically:

```text
53 → 37 → 14 → 0 (reverses direction) → 65 → 67 → 98 → 122 → 124 → 183
```

Like a building elevator, the head moves in one direction (e.g., inward toward track 0), servicing all requests encountered along the way. Upon reaching the edge, it reverses direction and sweeps outward toward the other edge (track 199).
* **Advantage**: Eliminates starvation because the head always completes its sweep to both boundaries, ensuring every sector is eventually reached.
* **Problem**: Uniformity. Sectors near the middle are visited twice as often as those at the extreme edges, making response times uneven.

---

## 7. C-SCAN (Circular SCAN)

**C-SCAN** improves on SCAN by moving in one direction only:

```text
53 → 65 → 67 → 98 → 122 → 124 → 183 → 199 → 0 (jump) → 14 → 37
```

The head services requests while moving in a single direction (e.g., increasing track numbers). Once it reaches the outer edge (199), it jumps straight back to the inner edge (0) without servicing requests on the return run, then starts another sweep.
* **Advantage**: Provides a much more uniform waiting time distribution across all tracks.
* **Problem**: The return sweep is a wasted movement (though on real drives, a full reset sweep is optimized to be extremely fast).

---

## 8. EdgeCase: Disk Scheduling Simulator

Use the simulator below to select an algorithm tab and compare how FCFS, SSTF, SCAN, and C-SCAN schedule the same sequence of cylinder requests:

<div id="disk-scheduling-edgecase" class="edgecase-container"></div>

---

## 9. Algorithmic Comparison

Below is a summary of the trade-offs involved in each strategy:

| Algorithm | Core Selection Rule | Major Strength | Major Weakness |
| :--- | :--- | :--- | :--- |
| **FCFS** | Serves by arrival order | Simple, fair, no starvation | High seek distance |
| **SSTF** | Serves closest request | Minimizes total seek time | Vulnerable to starvation |
| **SCAN** | Sweeps back and forth | Prevents starvation | Uneven edge wait times |
| **C-SCAN** | Sweeps in one direction | Uniform response times | Wasteful return sweep |

---

## 10. Physical Cost Differences: HDD vs. SSD/NVMe

The physical characteristics of the underlying media dictate whether these scheduling algorithms are used:

### Mechanical Hard Drives (HDDs)
These algorithms were designed for HDDs. Because physical seek movement and rotational delays are mechanical actions that take milliseconds, optimizing head sweeps is the most effective way to maximize I/O operations per second (IOPS).

### Solid State Drives (SSDs & NVMe)
SSDs have no mechanical heads or platters. Blocks are accessed electrically via flash memory gates, meaning there is zero physical seek penalty. Consequently, the traditional mechanical seek-distance minimization problem that motivated algorithms such as SSTF and SCAN largely disappears.

However, storage request scheduling does not disappear completely. Modern solid-state storage stacks still must optimize:
* **Queueing & Fairness**: Ensuring multiple active processes get fair shares of device bandwidth.
* **Request Merging**: Grouping contiguous block requests into larger sequential I/O commands to reduce controller transaction overhead.
* **Latency & Controller Pipelines**: Coordinating writes and reads to leverage the controller's internal device-level parallelism without bottlenecks.

The focus changes from reducing physical arm motion to maximizing throughput in electronic controllers.

---

## 11. Important Conceptual Distinction

As you study storage, be careful not to confuse the roles of filesystem allocation and device scheduling:

* **File Allocation**: Decides *which blocks* represent a file (e.g., extents, indexed structures, or linked lists).
* **Disk Scheduling**: Decides *in what order* pending read/write blocks should be sent to the physical device.

---

## 12. The Next Question

Disk scheduling can decide which waiting request should be served first.

But storage systems have another problem.

**What happens when the system loses power or crashes in the middle of a write?**
