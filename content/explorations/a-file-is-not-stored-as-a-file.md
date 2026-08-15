---
id: a-file-is-not-stored-as-a-file
category: "Operating Systems"
series: "Operating Systems"
title: "A File Is Not Stored as a File"
subtitle: "Understanding block translation layers, allocation strategies, and logical-to-physical address mapping."
date: "12th August, 2026"
tags: ["Operating Systems", "Storage Management", "Filesystem", "Allocation", "Fragmentation"]
---

## 1. Start with the Familiar File

When you browse your storage, you see files organized neatly into folders:

```text
notes.txt
```

A user or an application interacts with a file as a single, continuous stream of bytes. You open the file, write some text, read it back, and close it.

But this continuity is a software abstraction. The underlying physical storage device has no concept of a "file," a "name," or a "directory." It does not know where `notes.txt` begins or ends. 

Instead, storage devices operate purely in terms of fixed-size data blocks.

```html
<div style="margin: 2rem 0; text-align: center;">
  <svg viewBox="0 0 700 80" width="100%" height="auto" style="background: #151d2a; border-radius: 8px; border: 1px solid rgba(148, 163, 184, 0.08); font-family: monospace;">
    <!-- Flow diagram: App -> File -> FS -> Blocks -> Device -->
    <rect x="20" y="25" width="100" height="30" rx="4" fill="#1e293b" stroke="#3b82f6" />
    <text x="70" y="44" fill="#fff" font-size="11" text-anchor="middle">Application</text>
    
    <text x="140" y="44" fill="#64748b" font-size="14" text-anchor="middle">&rarr;</text>
    
    <rect x="160" y="25" width="80" height="30" rx="4" fill="#1e293b" stroke="#3b82f6" />
    <text x="200" y="44" fill="#fff" font-size="11" text-anchor="middle">File</text>
    
    <text x="260" y="44" fill="#64748b" font-size="14" text-anchor="middle">&rarr;</text>

    <rect x="280" y="25" width="100" height="30" rx="4" fill="#1e293b" stroke="#3b82f6" />
    <text x="330" y="44" fill="#fff" font-size="11" text-anchor="middle">Filesystem</text>
    
    <text x="400" y="44" fill="#64748b" font-size="14" text-anchor="middle">&rarr;</text>

    <rect x="420" y="25" width="110" height="30" rx="4" fill="#1e293b" stroke="#10b981" />
    <text x="475" y="44" fill="#10b981" font-size="11" text-anchor="middle">Storage Blocks</text>
    
    <text x="550" y="44" fill="#64748b" font-size="14" text-anchor="middle">&rarr;</text>

    <rect x="570" y="25" width="110" height="30" rx="4" fill="#111827" stroke="#10b981" />
    <text x="625" y="44" fill="#10b981" font-size="11" text-anchor="middle">Physical Device</text>
  </svg>
</div>
```

The key realization is simple:
> **A file is a logical object managed by the operating system. Storage hardware works entirely with blocks.**

---

## 2. From File to Blocks

When a file is written to storage, the filesystem must divide the continuous file bytes into discrete, block-sized chunks.

Suppose `notes.txt` is exactly **10 KB** in size, and the filesystem organizes storage into **4 KB blocks**. The filesystem splits the file as follows:

* **Block 1**: Bytes 0 to 4,095 (4 KB) &rarr; Storage Block 120
* **Block 2**: Bytes 4,096 to 8,191 (4 KB) &rarr; Storage Block 121
* **Block 3**: Bytes 8,192 to 10,239 (2 KB used) &rarr; Storage Block 122

Notice that the final block (Block 122) contains only 2 KB of file content, but it still consumes a full 4 KB block on disk. The remaining 2 KB of that block cannot be allocated to another file, resulting in **internal fragmentation**. 

This block-based translation is handled entirely by the operating system's filesystem driver.

---

## 3. A File's Blocks Do Not Have to Be Physically Adjacent

Because the filesystem maps logical segments to storage blocks through an index, a file's blocks do not need to sit next to each other on the physical drive.

A file could easily be scattered across the storage medium:
```text
notes.txt
   &darr;
Logical Block 0 &rarr; Storage Block 120
Logical Block 1 &rarr; Storage Block 121
Logical Block 2 &rarr; Storage Block 245
```

This establishes an important separation of concerns:

1. **Logical File Order**: A continuous byte sequence starting at 0 and running to 10,239.
2. **Physical Block Locations**: Scattered blocks (120, 121, 245) residing wherever space was available when the write occurred.

The storage hardware does not know these blocks are related; it simply reads and writes individual blocks as commanded.

---

## 4. Classic Storage Allocation Strategies

How does the filesystem keep track of which blocks belong to which files? Historically, three classic allocation strategies were designed to solve this mapping problem:

```html
<div class="svg-container" style="margin: 2.5rem 0; text-align: center;">
  <svg viewBox="0 0 800 240" width="100%" height="auto" style="background: #151d2a; border-radius: 12px; border: 1px solid rgba(148, 163, 184, 0.08); font-family: system-ui, -apple-system, sans-serif;">
    <defs>
      <marker id="arrow-blue" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="4" markerHeight="4" orient="auto-start-reverse">
        <path d="M 0 1 L 10 5 L 0 9 z" fill="#3b82f6" />
      </marker>
    </defs>

    <!-- SECTION 1: CONTIGUOUS ALLOCATION -->
    <text x="140" y="30" fill="#fff" font-size="12" font-weight="bold" text-anchor="middle">Contiguous Allocation</text>
    
    <!-- Directory entry -->
    <rect x="30" y="50" width="220" height="35" rx="4" fill="#1e293b" stroke="rgba(148, 163, 184, 0.15)" />
    <text x="40" y="72" fill="#94a3b8" font-size="10" font-family="monospace">File A: Start 120, Length 3</text>
    
    <!-- Block layout -->
    <g transform="translate(30, 110)">
      <rect x="0" y="0" width="60" height="30" rx="3" fill="rgba(59,130,246,0.15)" stroke="#3b82f6" />
      <text x="30" y="19" fill="#93c5fd" font-size="10" font-family="monospace" text-anchor="middle">Block 120</text>
      
      <rect x="70" y="0" width="60" height="30" rx="3" fill="rgba(59,130,246,0.15)" stroke="#3b82f6" />
      <text x="100" y="19" fill="#93c5fd" font-size="10" font-family="monospace" text-anchor="middle">Block 121</text>
      
      <rect x="140" y="0" width="60" height="30" rx="3" fill="rgba(59,130,246,0.15)" stroke="#3b82f6" />
      <text x="170" y="19" fill="#93c5fd" font-size="10" font-family="monospace" text-anchor="middle">Block 122</text>
      
      <!-- Connective flow -->
      <line x1="60" y1="15" x2="70" y2="15" stroke="#3b82f6" stroke-width="1" />
      <line x1="130" y1="15" x2="140" y2="15" stroke="#3b82f6" stroke-width="1" />
    </g>
    <text x="140" y="175" fill="#94a3b8" font-size="9" text-anchor="middle">Sequential, but prone to fragmentation</text>

    <!-- Divider Line -->
    <line x1="270" y1="20" x2="270" y2="220" stroke="rgba(148, 163, 184, 0.1)" stroke-width="1" />

    <!-- SECTION 2: LINKED ALLOCATION -->
    <text x="400" y="30" fill="#fff" font-size="12" font-weight="bold" text-anchor="middle">Linked Allocation</text>

    <!-- Directory entry -->
    <rect x="290" y="50" width="220" height="35" rx="4" fill="#1e293b" stroke="rgba(148, 163, 184, 0.15)" />
    <text x="300" y="72" fill="#94a3b8" font-size="10" font-family="monospace">File B: Start 120</text>

    <!-- Block layout -->
    <g transform="translate(290, 110)">
      <rect x="0" y="0" width="60" height="30" rx="3" fill="rgba(16,185,129,0.1)" stroke="#10b981" />
      <text x="30" y="15" fill="#a7f3d0" font-size="10" font-family="monospace" text-anchor="middle">Block 120</text>
      <text x="30" y="25" fill="#64748b" font-size="7" font-family="monospace" text-anchor="middle">ptr: 245</text>
      
      <rect x="80" y="0" width="60" height="30" rx="3" fill="rgba(16,185,129,0.1)" stroke="#10b981" />
      <text x="110" y="15" fill="#a7f3d0" font-size="10" font-family="monospace" text-anchor="middle">Block 245</text>
      <text x="110" y="25" fill="#64748b" font-size="7" font-family="monospace" text-anchor="middle">ptr: 91</text>
      
      <rect x="160" y="0" width="60" height="30" rx="3" fill="rgba(16,185,129,0.1)" stroke="#10b981" />
      <text x="190" y="15" fill="#a7f3d0" font-size="10" font-family="monospace" text-anchor="middle">Block 91</text>
      <text x="190" y="25" fill="#ef4444" font-size="7" font-family="monospace" text-anchor="middle">ptr: NULL</text>
      
      <!-- Connective arrows -->
      <path d="M 60,15 L 75,15" fill="none" stroke="#10b981" stroke-dasharray="2,2" stroke-width="1.2" marker-end="url(#arrow-blue)" />
      <path d="M 140,15 L 155,15" fill="none" stroke="#10b981" stroke-dasharray="2,2" stroke-width="1.2" marker-end="url(#arrow-blue)" />
    </g>
    <text x="400" y="175" fill="#94a3b8" font-size="9" text-anchor="middle">Non-contiguous, but random access is poor</text>

    <!-- Divider Line -->
    <line x1="530" y1="20" x2="530" y2="220" stroke="rgba(148, 163, 184, 0.1)" stroke-width="1" />

    <!-- SECTION 3: INDEXED ALLOCATION -->
    <text x="660" y="30" fill="#fff" font-size="12" font-weight="bold" text-anchor="middle">Indexed Allocation</text>

    <!-- Directory entry -->
    <rect x="550" y="50" width="220" height="35" rx="4" fill="#1e293b" stroke="rgba(148, 163, 184, 0.15)" />
    <text x="560" y="72" fill="#94a3b8" font-size="10" font-family="monospace">File C: Index Block 150</text>

    <!-- Block layout -->
    <g transform="translate(550, 100)">
      <!-- Index block -->
      <rect x="0" y="10" width="70" height="70" rx="3" fill="#1f2937" stroke="#60a5fa" stroke-width="1.5" />
      <text x="35" y="22" fill="#fff" font-size="8" font-weight="bold" text-anchor="middle">Index [150]</text>
      <text x="35" y="36" fill="#93c5fd" font-size="8" font-family="monospace" text-anchor="middle">0: 120</text>
      <text x="35" y="48" fill="#93c5fd" font-size="8" font-family="monospace" text-anchor="middle">1: 245</text>
      <text x="35" y="60" fill="#93c5fd" font-size="8" font-family="monospace" text-anchor="middle">2: 91</text>
      
      <!-- Data Blocks -->
      <rect x="140" y="0" width="60" height="22" rx="2" fill="rgba(96,165,250,0.1)" stroke="rgba(96,165,250,0.4)" />
      <text x="170" y="14" fill="#93c5fd" font-size="8" font-family="monospace" text-anchor="middle">Block 120</text>

      <rect x="140" y="34" width="60" height="22" rx="2" fill="rgba(96,165,250,0.1)" stroke="rgba(96,165,250,0.4)" />
      <text x="170" y="48" fill="#93c5fd" font-size="8" font-family="monospace" text-anchor="middle">Block 245</text>

      <rect x="140" y="68" width="60" height="22" rx="2" fill="rgba(96,165,250,0.1)" stroke="rgba(96,165,250,0.4)" />
      <text x="170" y="82" fill="#93c5fd" font-size="8" font-family="monospace" text-anchor="middle">Block 91</text>

      <!-- Connectors from index to data blocks -->
      <path d="M 70,30 L 135,11" fill="none" stroke="#60a5fa" stroke-width="1" marker-end="url(#arrow-blue)" />
      <path d="M 70,45 L 135,45" fill="none" stroke="#60a5fa" stroke-width="1" marker-end="url(#arrow-blue)" />
      <path d="M 70,60 L 135,79" fill="none" stroke="#60a5fa" stroke-width="1" marker-end="url(#arrow-blue)" />
    </g>
    <text x="660" y="195" fill="#94a3b8" font-size="9" text-anchor="middle">Efficient indexes, handles large files</text>
  </svg>
</div>
```

### Contiguous Allocation
The filesystem places the entire file's blocks in consecutive sequence on the storage device.
* **Advantage**: Extremely fast sequential access, as the device read heads (in HDDs) or controller logic (in SSDs) do not need to jump addresses.
* **Disadvantage**: Prone to external fragmentation. As files are created and deleted, finding consecutive blocks large enough for new files becomes increasingly difficult.

### Linked Allocation
Each block contains a small pointer to the next block, forming a chain.
* **Advantage**: No block space is wasted due to external fragmentation; any free block can join the chain.
* **Disadvantage**: Poor random access performance. To read Block 50, the OS must read Blocks 1 through 49 first to follow the pointers.

### Indexed Allocation
All data block pointers are collected together in a single dedicated index block.
* **Advantage**: Supports fast direct/random access to any block without reading preceding data.
* **Disadvantage**: Overhead. Even tiny files consume an entire extra block just to hold the index mapping.

---

## 5. Important Clarification

Modern operating system filesystems rarely implement these classic models in their raw textbook form. Instead, they use advanced adaptations:

* **Extents**: Rather than indexing every block individually, modern filesystems allocate ranges of consecutive blocks. An extent is simply a `(Start Block, Run Length)` pair. For example: *"Start at Block 120 and read the next 8 blocks."*
* **B-Trees / Extent Trees**: Large files index their extents inside tree structures, allowing quick lookups and scaling to petabytes of data.

The fundamental goal, however, remains the same: **translating a single logical file stream into a set of mapped storage block addresses.**

---

## 6. EdgeCase: From File to Blocks

Use the simulator below to visualize how the filesystem translates a 10 KB file into logical blocks, maps them to physical sectors, and services a read request from the middle of the file:

<div id="file-to-blocks-edgecase" class="edgecase-container"></div>

---

## 7. Do Not Overclaim Physical Placement

While the filesystem maps files to "Storage Blocks," it is important to realize that these storage blocks are still logical representations.

On modern Solid State Drives (SSDs) and NVMe drives, there is another translation layer inside the device itself. When the filesystem requests **Logical Block Address (LBA) 120**, the SSD controller's **Flash Translation Layer (FTL)** intercepts the request and maps it to a physical flash memory cell. 

The SSD controller does this to balance wear across its silicon gates, handle bad blocks, and optimize write performance. The operating system filesystem manages logical block layouts, while the storage drive controller manages the actual physical hardware mapping.

---

## 8. Real Operating-System Connection

Most production operating systems rely heavily on **extent-based allocation** instead of raw block mapping:

* **Linux (ext4)**: Uses extent trees to store metadata. A single extent can represent up to 128 MB of contiguous space on a 4 KB block filesystem, reducing metadata overhead significantly.
* **Windows (NTFS)**: Refers to extents as *data runs*. The MFT record describes files as a series of runs mapping logical clusters to physical storage clusters.
* **macOS (APFS)**: Employs dynamic extent allocation paired with copy-on-write clones, letting multiple directory entries reference the same extents until a write is made.

---

## 9. Connection to Fragmentation

In the Memory Management branch, we saw how memory becomes fragmented as pages are allocated and freed. The same phenomenon occurs in storage.

When a file's blocks are scattered far apart on physical storage, the file is **fragmented**:
* **On Hard Disk Drives (HDDs)**: Fragmentation is highly destructive to performance. The mechanical drive head must physically rotate and seek to jump between distant sectors, causing noticeable delays.
* **On Solid State Drives (SSDs)**: There are no moving heads, so mechanical seek delays do not apply. However, extreme fragmentation still imposes CPU overhead on the filesystem driver (which must manage massive mapping tables) and limits the drive controller's ability to run parallel block operations.

---

## 10. The Next Question

We now know that a file is a logical object whose data is mapped onto storage blocks.

But those blocks do not exist in isolation.

**What exactly is the layer between the filesystem and the storage device — and how do partitions, volumes and filesystems turn a raw device into something the OS can actually use?**
