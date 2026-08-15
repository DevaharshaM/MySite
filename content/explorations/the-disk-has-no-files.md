---
id: the-disk-has-no-files
category: "Operating Systems"
series: "Operating Systems"
title: "The Disk Has No Files"
subtitle: "Deconstructing storage stacks, partition tables, and directory tree attachments."
date: "12th August, 2026"
tags: ["Operating Systems", "Storage Management", "Partitions", "Mounting", "Storage Stack"]
---

## 1. Start with the Familiar Assumption

When you open your computer's file explorer, you see your documents organized neatly:

```text
notes.txt
photo.jpg
resume.pdf
```

It is natural to assume that these files are written directly onto the storage disk in the same way they are represented on your screen.

But this mental model is incorrect.

Fundamentally, a physical storage device has no concept of a "file," a "directory," a "path," or "file permissions." If you inspect the copper lines of an NVMe drive or the magnetic platter of a hard disk, you will not find folders or names.

A raw storage device provides only a flat sequence of addressable sectors. Every structure—from files to directories—is a virtual arrangement created and maintained entirely by operating system software.

---

## 2. Reveal the Storage Stack

To bridge the gap between human concepts and physical hardware, operating systems organize storage into a layered hierarchy called the **Storage Stack**:

```html
<div class="svg-container" style="margin: 2.5rem 0; text-align: center;">
  <svg viewBox="0 0 600 340" width="100%" height="auto" style="background: #151d2a; border-radius: 12px; border: 1px solid rgba(148, 163, 184, 0.08); font-family: system-ui, -apple-system, sans-serif;">
    <g transform="translate(50, 20)">
      <!-- Level 5: Application -->
      <rect x="0" y="0" width="180" height="32" rx="4" fill="#1e293b" stroke="#3b82f6" stroke-width="1.5" />
      <text x="90" y="20" fill="#fff" font-size="11" font-weight="bold" text-anchor="middle">Application Layer</text>
      <text x="200" y="20" fill="#94a3b8" font-size="10">Calls open(), read(), write() API commands</text>

      <!-- Connection line -->
      <line x1="90" y1="32" x2="90" y2="50" stroke="#64748b" stroke-width="1.2" stroke-dasharray="2,2" />

      <!-- Level 4: File -->
      <rect x="0" y="50" width="180" height="32" rx="4" fill="#1e293b" stroke="#3b82f6" />
      <text x="90" y="70" fill="#fff" font-size="11" text-anchor="middle">Logical File Abstraction</text>
      <text x="200" y="70" fill="#94a3b8" font-size="10">Treats data as a continuous byte stream</text>

      <!-- Connection line -->
      <line x1="90" y1="82" x2="90" y2="100" stroke="#64748b" stroke-width="1.2" stroke-dasharray="2,2" />

      <!-- Level 3: Filesystem -->
      <rect x="0" y="100" width="180" height="32" rx="4" fill="#1e293b" stroke="#3b82f6" />
      <text x="90" y="120" fill="#fff" font-size="11" text-anchor="middle">Filesystem Driver</text>
      <text x="200" y="120" fill="#94a3b8" font-size="10">Manages directories, indexes, and block mapping</text>

      <!-- Connection line -->
      <line x1="90" y1="132" x2="90" y2="150" stroke="#64748b" stroke-width="1.2" stroke-dasharray="2,2" />

      <!-- Level 2: Volume / Partition -->
      <rect x="0" y="150" width="180" height="32" rx="4" fill="#1e293b" stroke="#10b981" />
      <text x="90" y="170" fill="#10b981" font-size="11" font-weight="bold" text-anchor="middle">Partition / Volume</text>
      <text x="200" y="170" fill="#94a3b8" font-size="10">Defines boundary limits on physical storage</text>

      <!-- Connection line -->
      <line x1="90" y1="182" x2="90" y2="200" stroke="#64748b" stroke-width="1.2" stroke-dasharray="2,2" />

      <!-- Level 1: Block Device -->
      <rect x="0" y="200" width="180" height="32" rx="4" fill="#1e293b" stroke="#10b981" />
      <text x="90" y="220" fill="#10b981" font-size="11" text-anchor="middle">Block Device Interface</text>
      <text x="200" y="220" fill="#94a3b8" font-size="10">Handles block read/write commands (LBA)</text>

      <!-- Connection line -->
      <line x1="90" y1="232" x2="90" y2="250" stroke="#64748b" stroke-width="1.2" stroke-dasharray="2,2" />

      <!-- Level 0: Storage Device -->
      <rect x="0" y="250" width="180" height="32" rx="4" fill="#111827" stroke="#10b981" stroke-width="1.5" />
      <text x="90" y="270" fill="#10b981" font-size="11" font-weight="bold" text-anchor="middle">Physical Storage Media</text>
      <text x="200" y="270" fill="#94a3b8" font-size="10">HDD platters, SATA, NVMe flash cells</text>
    </g>
  </svg>
</div>
```

* **Application**: Requests file operations using path names (`open("/home/user/notes.txt")`).
* **Logical File**: Exposes the file stream to applications, hiding block offsets.
* **Filesystem**: Translates paths into internal IDs (inodes/MFT records) and maps logical offsets to LBA storage block sectors.
* **Partition / Volume**: Defines the boundaries of a raw disk space allocated to a single logical driver.
* **Block Device Interface**: The operating system subsystem that manages block-oriented command flows.
* **Physical Storage Media**: The actual hardware sectors that store charge states or magnetic orientation.

---

## 3. Raw Storage

At the lowest level, a storage device is a flat array of addressable slots called **Logical Block Addresses (LBAs)**:

```text
RAW STORAGE LBA LIST

[000][001][002][003][004][005][006][007][008]...
```

At this raw layer, files like `notes.txt` or `photo.jpg` do not exist. There are only index numbers. The OS reads or writes data by specifying the exact block index (e.g. *"Read LBA block 120"*). 

The filesystem is the organization layer that compiles these raw addresses into a structured digital workspace.

---

## 4. Formatting / Creating a Filesystem

Creating a filesystem—often referred to as **formatting**—is the step that establishes these directory and index tables on the raw storage media.

```text
RAW DEVICE
    &darr;
Filesystem Creation (Format)
    &darr;
Bookkeeping Tables Initialized (Superblock, Bitmaps, Inodes)
    &darr;
Files / Directories / Free Space Ready
```

Formatting does not necessarily mean overwriting every single sector of the physical disk with zeros (which is a "Full Format"). Instead, a standard format simply initializes the master filesystem index tables, rendering the rest of the block addresses as empty space ready for reuse.

---

## 5. Partitions and Volumes

Before writing a filesystem index, raw disks are usually divided into independent virtual zones called **partitions**:

```html
<div class="svg-container" style="margin: 2.5rem 0; text-align: center;">
  <svg viewBox="0 0 700 120" width="100%" height="auto" style="background: #151d2a; border-radius: 12px; border: 1px solid rgba(148, 163, 184, 0.08); font-family: system-ui, -apple-system, sans-serif;">
    <!-- Raw physical drive container -->
    <rect x="30" y="25" width="640" height="40" rx="6" fill="#111827" stroke="rgba(148, 163, 184, 0.2)" stroke-width="1.5" />
    <text x="350" y="15" fill="#64748b" font-size="10" font-family="monospace" text-anchor="middle" text-transform="uppercase">Physical Drive Allocation Layout</text>

    <!-- Partition 1 -->
    <rect x="35" y="30" width="350" height="30" rx="4" fill="rgba(59, 130, 246, 0.15)" stroke="#3b82f6" />
    <text x="210" y="49" fill="#93c5fd" font-size="11" font-weight="bold" text-anchor="middle">Partition 1 (LBA 00–47)</text>

    <!-- Partition 2 -->
    <rect x="390" y="30" width="180" height="30" rx="4" fill="rgba(16, 185, 129, 0.15)" stroke="#10b981" />
    <text x="480" y="49" fill="#a7f3d0" font-size="11" font-weight="bold" text-anchor="middle">Partition 2 (LBA 48–59)</text>

    <!-- Unallocated space -->
    <rect x="575" y="30" width="90" height="30" rx="4" fill="none" stroke="rgba(148, 163, 184, 0.3)" stroke-dasharray="3,3" />
    <text x="620" y="49" fill="#94a3b8" font-size="10" text-anchor="middle">Unallocated</text>

    <!-- Label explanations -->
    <path d="M 210,65 L 210,85" fill="none" stroke="#3b82f6" stroke-width="1" stroke-dasharray="2,2" />
    <text x="210" y="100" fill="#94a3b8" font-size="9" text-anchor="middle">Ext4 Filesystem (Linux /home)</text>

    <path d="M 480,65 L 480,85" fill="none" stroke="#10b981" stroke-width="1" stroke-dasharray="2,2" />
    <text x="480" y="100" fill="#94a3b8" font-size="9" text-anchor="middle">FAT32 Filesystem (EFI System)</text>
  </svg>
</div>
```

A **partition** represents a designated range of consecutive physical sectors reserved on the disk (e.g. LBA 00 to 47). This boundary allows a single storage drive to host multiple operating systems, separate configurations, or isolate user data from system binaries.

---

## 6. EdgeCase: From Raw Device to Filesystem

Use the simulator below to track how raw blocks are virtualized step-by-step into partitions, initialized with metadata indexes, and layered with file abstractions:

<div id="disk-has-no-files-edgecase" class="edgecase-container"></div>

---

## 7. Important Distinction: Partition vs Filesystem

Understanding the boundary between partitions and filesystems is essential:

* **Partition**: Answers: *Which sectors of the physical media belong to this volume boundary?* It is defined by partition tables (like GPT or MBR) written at the start of the drive.
* **Filesystem**: Answers: *How should the sectors within this partition be structured into directories, metadata tables, and files?*

A partition sets the physical playground limits; a filesystem establishes the rules of the game played inside.

---

## 8. Mounting

To make a filesystem accessible to applications, the operating system must attach it to its logical namespace—a process called **mounting**:

```text
Storage Volume
     &darr;
Filesystem Structures
     &darr;
Mount Point
     &darr;
OS Directory Tree Namespace
     &darr;
Application
```

* **Unix / Linux**: Attach filesystems into a unified directory tree. For example, Partition 1 (`/dev/nvme0n1p1`) might be mounted at `/`, while a USB drive is mounted at `/media/usb`.
* **Windows**: Exposes mounted partitions using drive letters (`C:`, `D:`) or paths.

Mounting takes the self-contained block structures of a filesystem volume and plugs them into the active directory structure.

---

## 9. Real Operating-System Connection

Production kernels use abstraction layers to ensure applications can access different filesystems uniformly:

* **Linux (Virtual File System - VFS)**: VFS acts as a common interface layer. When an application calls `read()`, VFS intercepts it and translates the request into the appropriate filesystem driver call (e.g. ext4, FAT, or NTFS), which in turn requests data blocks from the device driver.
* **Windows (I/O Manager & Filter Drivers)**: A similar stack manages I/O requests, sending them down through filesystem filter drivers to logical volume managers and port drivers.

The layered architecture ensures that application developers write programs targeting files, rather than hardcoding disk sector commands.

---

## 10. HDD vs SSD/NVMe

The physical media underneath the block interface dictates how fast blocks can be read and written:

### Hard Disk Drives (HDDs)
Store data magnetically on spinning platters. Because a mechanical read head must physically travel to specific sector tracks, HDDs suffer from high latency (seek time and rotational delay) and perform sequential accesses much faster than random ones.

### Solid State Drives (SSDs)
Store data in flash memory cells. Since there are no moving parts, random reads are extremely fast. However, writes require erasing blocks before they can be rewritten, which requires internal wear leveling and block relocations.

### NVMe SSDs
Use the high-speed PCI Express (PCIe) bus rather than old SATA controller pathways, allowing thousands of parallel command queues to reduce I/O bottlenecks.

Regardless of the underlying hardware technology, the filesystem presents the same unified file abstraction to the operating system.

---

## 11. The Next Question

We have now crossed the boundary from files and filesystems into the storage device itself.

But storage requests do not all arrive in the same order, and on some devices the physical cost of serving those requests can be enormous.

**When many storage requests are waiting, how should the operating system decide which one to serve first?**
