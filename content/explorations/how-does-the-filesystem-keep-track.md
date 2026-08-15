---
id: how-does-the-filesystem-keep-track
category: "Operating Systems"
series: "Operating Systems"
title: "How Does the Filesystem Keep Track?"
subtitle: "Demystifying persistent directories, metadata bookkeeping, and physical block allocation."
date: "12th August, 2026"
tags: ["Operating Systems", "File Management", "Filesystem", "Allocation", "Metadata"]
---

## 1. Start from the Problem

When an application creates a new file, the operating system must perform a lot of bookkeeping. Suppose your program requests:

```text
notes.txt
```

To manage this file, the operating system cannot simply store a list of active filenames. It must be prepared to answer critical operational questions at any time:

* **What does this file represent?** Is it a regular file, a directory, a symbolic link, or a character device?
* **How large is it?** Where does the file end, and how many bytes are in use?
* **Who owns it and who can access it?** What are the read, write, and execute permissions?
* **When was it changed?** When was the file created, modified, or last opened?
* **Where is its data?** Which physical block sectors on the storage media hold the file's content?
* **Which blocks are free?** Where can the filesystem allocate space when the file expands?
* **How does it survive a power loss?** What happens to the metadata if the machine suddenly shuts down mid-write?

To resolve these questions, the operating system relies on **persistent filesystem structures** written directly onto the storage device.

---

## 2. The Conceptual Filesystem Structures

To organize this information, modern filesystems split their responsibilities among four major conceptual layers:

```html
<div class="svg-container" style="margin: 2.5rem 0; text-align: center;">
  <svg viewBox="0 0 800 250" width="100%" height="auto" style="background: #151d2a; border-radius: 12px; border: 1px solid rgba(148, 163, 184, 0.08); font-family: system-ui, -apple-system, sans-serif;">
    <defs>
      <marker id="arrow-blue" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse">
        <path d="M 0 1 L 10 5 L 0 9 z" fill="#3b82f6" />
      </marker>
      <marker id="arrow-green" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse">
        <path d="M 0 1 L 10 5 L 0 9 z" fill="#10b981" />
      </marker>
    </defs>
    <text x="30" y="30" fill="#64748b" font-size="10" font-family="monospace" text-transform="uppercase" letter-spacing="0.05em">Conceptual Filesystem Architecture</text>
    
    <!-- Top Level: Filesystem -->
    <rect x="320" y="45" width="160" height="35" rx="6" fill="#1e293b" stroke="#3b82f6" stroke-width="1.5" />
    <text x="400" y="67" fill="#fff" font-size="12" font-weight="bold" text-anchor="middle">FILESYSTEM INDEX</text>

    <!-- Mid Level: Directory, Metadata, Free-Space -->
    <!-- Directory Entries -->
    <rect x="60" y="115" width="180" height="45" rx="6" fill="#1e293b" stroke="rgba(148, 163, 184, 0.2)" />
    <text x="150" y="134" fill="#e2e8f0" font-size="11" font-weight="bold" text-anchor="middle">Directory Entries</text>
    <text x="150" y="148" fill="#94a3b8" font-size="9" text-anchor="middle">Maps names to internal IDs</text>

    <!-- File Metadata -->
    <rect x="310" y="115" width="180" height="45" rx="6" fill="#1e293b" stroke="rgba(148, 163, 184, 0.2)" />
    <text x="400" y="134" fill="#e2e8f0" font-size="11" font-weight="bold" text-anchor="middle">File Metadata Records</text>
    <text x="400" y="148" fill="#94a3b8" font-size="9" text-anchor="middle">Stores size, permissions, properties</text>

    <!-- Free Space Tracking -->
    <rect x="560" y="115" width="180" height="45" rx="6" fill="#1e293b" stroke="rgba(148, 163, 184, 0.2)" />
    <text x="650" y="134" fill="#e2e8f0" font-size="11" font-weight="bold" text-anchor="middle">Free-Space Tracking</text>
    <text x="650" y="148" fill="#94a3b8" font-size="9" text-anchor="middle">Tracks available sectors</text>

    <!-- Bottom Level: Data Blocks -->
    <rect x="310" y="195" width="180" height="35" rx="6" fill="#111827" stroke="#10b981" stroke-width="1.5" />
    <text x="400" y="217" fill="#10b981" font-size="11" font-weight="bold" text-anchor="middle">Physical Data Blocks</text>

    <!-- Connectors -->
    <!-- Top Down Arrows -->
    <path d="M 340,80 L 190,112" fill="none" stroke="#3b82f6" stroke-width="1.2" marker-end="url(#arrow-blue)" />
    <path d="M 400,80 L 400,110" fill="none" stroke="#3b82f6" stroke-width="1.2" marker-end="url(#arrow-blue)" />
    <path d="M 460,80 L 610,112" fill="none" stroke="#3b82f6" stroke-width="1.2" marker-end="url(#arrow-blue)" />

    <!-- Directory to Metadata mapping -->
    <path d="M 240,137 L 305,137" fill="none" stroke="#3b82f6" stroke-dasharray="3,3" stroke-width="1.2" marker-end="url(#arrow-blue)" />

    <!-- Metadata & Free Space to Data Blocks -->
    <path d="M 400,160 L 400,190" fill="none" stroke="#10b981" stroke-width="1.2" marker-end="url(#arrow-green)" />
    <path d="M 610,160 L 460,192" fill="none" stroke="#10b981" stroke-width="1.2" marker-end="url(#arrow-green)" />
  </svg>
</div>
```

### Directory Entries
The namespace is the human-facing interface of the filesystem. The directory structure answers: **What name refers to which filesystem object?**

Directory records are lookups mapping filenames to internal system identifiers:
```text
notes.txt &rarr; File Identity #7182
photo.jpg &rarr; File Identity #8221
```

### File Metadata
Once the filename maps to an internal ID, the operating system accesses the metadata record. It answers: **What is this file?**

The metadata block contains everything about the file except its name or its raw data:
* File size (in bytes or sectors).
* Owner and group membership.
* Access permissions (Read/Write/Execute constraints).
* Timestamps (creation, modification, access).
* File type (regular, folder, link, etc.).
* Link count (number of directory entry references).
* Data location offsets (pointing to where the data blocks are located).

### Data Allocation Information
To read or write the actual data payload, the OS consults the location map stored in the file's metadata. It answers: **Where are the contents of this file stored?**

Conceptually:
```text
File #7182
   &darr;
Block 209
Block 310
Block 311
```
The exact indexing mechanisms vary, ranging from sequential block indexes to extent maps (which reference a starting block and a run length).

### Free-Space Tracking
When files grow or new files are created, the filesystem needs to know: **Which storage blocks are available for new data?**

Conceptually, the filesystem maintains a map of the drive:
```text
[USED] [USED] [FREE] [USED] [FREE] [FREE] [USED]
```
The OS reads this structure to find free space quickly and update its markers as sectors are assigned.

---

## 3. The Key Realization

A filesystem is not just a bucket where you store files.

> **A filesystem is a collection of metadata and data structures that allow the operating system to find, describe, allocate, modify, and delete those files.**

Without these background structures, the storage drive is merely a flat, raw string of addressable sectors. The filesystem is the translation machinery that converts raw sectors into a structured digital workspace.

---

## 4. EdgeCase: The Lifecycle of a File

Use the simulator below to trace how the operating system coordinates directories, metadata tables, space trackers, and storage sectors during the lifecycle of a file:

<div id="filesystem-tracker-edgecase" class="edgecase-container"></div>

---

## 5. Important Conceptual Distinction

When you click "Delete" in the simulator above, notice that the physical data blocks are not wiped. 

When a file is deleted, the operating system typically does not overwrite the physical sectors with zeros immediately. Instead, it:
1. Removes the name mapping from the directory.
2. Releases the metadata record (making its ID available for new files).
3. Marks the data blocks as "free" in the space tracker.

The old data remains physically readable on the drive sectors until it is overwritten by a subsequent write operation.

---

## 6. Real Operating-System Connection

While the concepts remain uniform, different operating systems organize their directories and metadata structures in unique ways:

### Unix / Linux (ext4, XFS)
Linux filesystems separate names from properties using index nodes (**inodes**). Directory entry records map name strings directly to inode numbers. Each inode stands as a self-contained record pointing to the file metadata and data block pointers.

### Windows (NTFS)
NTFS stores all file data and properties in a database called the **Master File Table (MFT)**. MFT records contain the attributes of a file, such as its name, security permissions, and either the data itself (for very small files) or references to external data clusters.

### macOS (APFS)
APFS uses a b-tree object map, dynamically scaling metadata nodes to manage file snapshots, space sharing, and quick lookups without hardcoded layout layouts.

Regardless of the on-disk implementation details, every operating system must provide matching mechanisms for directory names, metadata properties, data tracking, and free-space bookkeeping.

---

## 7. The Next Question

We now understand how the filesystem keeps track of files.

**But what actually happens underneath the filesystem when it asks the storage device to read or write those blocks?**
