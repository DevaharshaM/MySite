---
id: the-file-isnt-open
category: "Operating Systems"
series: "Operating Systems"
title: "The File Isn't Open"
subtitle: "Understanding the system-call boundary and file descriptors."
date: "11th August, 2026"
tags: ["Operating Systems", "File Management", "System Calls", "File Descriptors"]
---

## 1. The Familiar Assumption

When writing code to interact with persistent storage, we often start with a simple command:

```c
open("notes.txt");
```

To a programmer starting out, it is easy to assume a direct, unmediated relationship: the application requests a file, grabs it, and reads or writes its bytes directly from the disk.

```html
<div class="svg-container" style="margin: 2rem 0; text-align: center;">
  <svg viewBox="0 0 800 120" width="100%" height="auto" style="background: #151d2a; border-radius: 12px; border: 1px solid rgba(148, 163, 184, 0.08); font-family: system-ui, -apple-system, sans-serif;">
    <defs>
      <marker id="arrow-blue" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
        <path d="M 0 1 L 10 5 L 0 9 z" fill="#3b82f6" />
      </marker>
    </defs>
    <text x="30" y="30" fill="#64748b" font-size="10" font-family="monospace" text-transform="uppercase" letter-spacing="0.05em">Naive Mental Model (The Illusion)</text>
    
    <rect x="50" y="50" width="160" height="40" rx="6" fill="#1e293b" stroke="rgba(148, 163, 184, 0.2)" />
    <text x="130" y="75" fill="#e2e8f0" font-size="12" font-weight="bold" text-anchor="middle">Application</text>
    
    <line x1="210" y1="70" x2="282" y2="70" stroke="#3b82f6" stroke-width="1.5" stroke-dasharray="4,4" marker-end="url(#arrow-blue)" />
    
    <rect x="290" y="50" width="160" height="40" rx="6" fill="#1e293b" stroke="#3b82f6" stroke-dasharray="4,4" />
    <text x="370" y="75" fill="#3b82f6" font-size="12" font-weight="bold" text-anchor="middle">notes.txt</text>
    
    <line x1="450" y1="70" x2="522" y2="70" stroke="#3b82f6" stroke-width="1.5" stroke-dasharray="4,4" marker-end="url(#arrow-blue)" />
    
    <rect x="530" y="50" width="160" height="40" rx="6" fill="#1e293b" stroke="rgba(148, 163, 184, 0.2)" />
    <text x="610" y="75" fill="#e2e8f0" font-size="12" font-weight="bold" text-anchor="middle">Physical Disk</text>
  </svg>
</div>
```

But this mental model is an illusion. 

An application cannot directly access physical storage devices. The CPU runs program code in a restricted, unprivileged mode (User Mode). In this execution space, program instructions cannot issue raw commands to storage interfaces. If an application could touch storage sectors directly, a single bug or malicious loop in one program could overwrite the partition table, corrupting the entire system.

To interact with a file, the application must cross a strict architectural boundary.

---

## 2. Crossing the Boundary

To access a file, the program must request the operating system kernel to perform the operation on its behalf. It does this by using a set of dedicated functions called **System Calls**.

These calls represent the secure interface through which applications query the kernel:

*   `open()`: Requests access to a file by name.
*   `read()`: Requests bytes from a previously opened file resource.
*   `write()`: Requests bytes into a previously opened file resource.
*   `close()`: Releases the resource.

```html
<div class="svg-container" style="margin: 2.5rem 0; text-align: center;">
  <svg viewBox="0 0 800 360" width="100%" height="auto" style="background: #151d2a; border-radius: 12px; border: 1px solid rgba(148, 163, 184, 0.08); font-family: system-ui, -apple-system, sans-serif;">
    <defs>
      <marker id="arrow-green" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
        <path d="M 0 1 L 10 5 L 0 9 z" fill="#10b981" />
      </marker>
      <marker id="arrow-gray" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
        <path d="M 0 1 L 10 5 L 0 9 z" fill="#94a3b8" />
      </marker>
    </defs>
    
    <text x="30" y="35" fill="#ffffff" font-size="14" font-weight="bold">Crossing the User-Kernel Boundary</text>
    
    <text x="30" y="80" fill="#64748b" font-size="10" font-family="monospace" text-transform="uppercase" letter-spacing="0.05em">User Space (Unprivileged Mode)</text>
    
    <rect x="250" y="60" width="300" height="40" rx="6" fill="#1e293b" stroke="rgba(148, 163, 184, 0.2)" />
    <text x="400" y="85" fill="#e2e8f0" font-size="12" font-weight="bold" text-anchor="middle">Application: open("notes.txt")</text>
    
    <line x1="30" y1="130" x2="770" y2="130" stroke="#ef4444" stroke-dasharray="6,4" stroke-width="1.5" />
    <rect x="310" y="120" width="180" height="20" rx="4" fill="#ef4444" opacity="0.1" />
    <text x="400" y="134" fill="#ef4444" font-size="9" font-family="monospace" font-weight="bold" text-anchor="middle" text-transform="uppercase" letter-spacing="0.1em">User-Kernel Boundary</text>
    
    <line x1="400" y1="100" x2="400" y2="154" stroke="#94a3b8" stroke-width="1.5" marker-end="url(#arrow-gray)" />
    
    <text x="30" y="170" fill="#64748b" font-size="10" font-family="monospace" text-transform="uppercase" letter-spacing="0.05em">Kernel Space (Privileged Mode)</text>
    
    <rect x="250" y="160" width="300" height="40" rx="6" fill="#1e293b" stroke="#3b82f6" stroke-width="1.5" />
    <text x="400" y="185" fill="#e2e8f0" font-size="12" font-family="monospace" text-anchor="middle">Syscall Entry: sys_open()</text>
    
    <line x1="400" y1="200" x2="400" y2="224" stroke="#94a3b8" stroke-width="1.5" marker-end="url(#arrow-gray)" />
    
    <rect x="250" y="230" width="300" height="40" rx="6" fill="#1e293b" stroke="#10b981" stroke-width="1.5" />
    <text x="400" y="255" fill="#e2e8f0" font-size="12" font-weight="bold" text-anchor="middle">Filesystem Driver (ext4 / NTFS)</text>
    
    <line x1="400" y1="270" x2="400" y2="294" stroke="#94a3b8" stroke-width="1.5" marker-end="url(#arrow-gray)" />
    
    <rect x="250" y="300" width="300" height="40" rx="6" fill="#1e293b" stroke="#a855f7" stroke-width="1" />
    <text x="400" y="325" fill="#e2e8f0" font-size="12" font-weight="bold" text-anchor="middle">Physical Storage Driver &amp; Disk</text>
  </svg>
</div>
```

It is important to make a conceptual distinction: **these system calls are not File Management itself**. They are simply the API—the doors in the wall. File Management is the massive, complex infrastructure running inside the kernel that handles access verification, data buffering, filesystem block mapping, and storage scheduling behind those doors.

---

## 3. The File Descriptor: A Digital Ticket

When an application invokes `open("notes.txt")`, the kernel does not send the physical file data to the application. Instead, if the request is valid, the kernel returns a simple integer:

```c
int fd = open("notes.txt", O_RDONLY);
// Returns: fd = 3
```

This integer is a **File Descriptor** (often abbreviated as `fd`).

The application does not receive a pointer to raw storage or the filesystem structures. It receives a reference index. When the application needs to read data, it passes this index back to the kernel:

```c
read(fd, buffer, 100);  // Read 100 bytes using descriptor reference "fd"
write(fd, data, 50);    // Write 50 bytes using descriptor reference "fd"
close(fd);              // Release the reference
```

Conceptually, we must separate three distinct ideas:

*   **The File**: The persistent resource resting on storage (defined by its metadata/inode and data blocks).
*   **The Open File (Description)**: The temporary tracking state allocated by the kernel when a file is opened (storing the current read/write cursor offset, access flags, and links to the file metadata).
*   **The File Descriptor**: The process-specific integer index that references the kernel's open-file table.

The application holds only the descriptor index. The operating system retains complete control over the file state.

---

## 4. EdgeCase: The Open File Lifecycle

Watch the interactive sequence below to see how execution transitions across the system-call boundary, how descriptors are mapped in the process table, and how the kernel tracks file offsets:

<div id="file-open-edgecase" class="edgecase-container"></div>

---

## 5. Multiple Processes and Shared Files

Because descriptors are private indexes mapped inside a process's file descriptor table, different processes have separate descriptor namespaces. 

If Process A and Process B both open `"notes.txt"` independently, they do not automatically share the same open file state:

```html
<div class="svg-container" style="margin: 2.5rem 0; text-align: center;">
  <svg viewBox="0 0 800 240" width="100%" height="auto" style="background: #151d2a; border-radius: 12px; border: 1px solid rgba(148, 163, 184, 0.08); font-family: system-ui, -apple-system, sans-serif;">
    <defs>
      <marker id="arrow-blue" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
        <path d="M 0 1 L 10 5 L 0 9 z" fill="#3b82f6" />
      </marker>
      <marker id="arrow-purple" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
        <path d="M 0 1 L 10 5 L 0 9 z" fill="#a855f7" />
      </marker>
    </defs>
    
    <text x="30" y="35" fill="#ffffff" font-size="14" font-weight="bold">Independent Open States for a Shared File</text>
    
    <rect x="50" y="60" width="180" height="60" rx="6" fill="#1e293b" stroke="rgba(148, 163, 184, 0.2)" />
    <text x="60" y="80" fill="#e2e8f0" font-size="11" font-weight="bold">Process A Space</text>
    <text x="60" y="100" fill="#3b82f6" font-size="10" font-family="monospace">File Descriptor: fd = 3</text>
    
    <rect x="50" y="150" width="180" height="60" rx="6" fill="#1e293b" stroke="rgba(148, 163, 184, 0.2)" />
    <text x="60" y="170" fill="#e2e8f0" font-size="11" font-weight="bold">Process B Space</text>
    <text x="60" y="190" fill="#3b82f6" font-size="10" font-family="monospace">File Descriptor: fd = 3</text>
    
    <line x1="230" y1="90" x2="282" y2="90" stroke="#3b82f6" stroke-width="1.5" marker-end="url(#arrow-blue)" />
    <line x1="230" y1="180" x2="282" y2="180" stroke="#3b82f6" stroke-width="1.5" marker-end="url(#arrow-blue)" />
    
    <rect x="290" y="60" width="220" height="60" rx="6" fill="#1e293b" stroke="rgba(148, 163, 184, 0.2)" />
    <text x="300" y="80" fill="#f59e0b" font-size="10" font-weight="bold" font-family="monospace">Open File Entry A</text>
    <text x="300" y="98" fill="#CBD5E1" font-size="10" font-family="monospace">Cursor Offset: 0</text>
    
    <rect x="290" y="150" width="220" height="60" rx="6" fill="#1e293b" stroke="rgba(148, 163, 184, 0.2)" />
    <text x="300" y="170" fill="#f59e0b" font-size="10" font-weight="bold" font-family="monospace">Open File Entry B</text>
    <text x="300" y="188" fill="#CBD5E1" font-size="10" font-family="monospace">Cursor Offset: 0</text>
    
    <path d="M 510,90 L 582,120" fill="none" stroke="#a855f7" stroke-width="1.5" marker-end="url(#arrow-purple)" />
    <path d="M 510,180 L 582,130" fill="none" stroke="#a855f7" stroke-width="1.5" marker-end="url(#arrow-purple)" />
    
    <rect x="590" y="95" width="160" height="60" rx="6" fill="#1e293b" stroke="#a855f7" stroke-width="1.5" />
    <text x="670" y="120" fill="#e2e8f0" font-size="11" font-weight="bold" text-anchor="middle">notes.txt Inode</text>
    <text x="670" y="140" fill="#64748b" font-size="9" font-family="monospace" text-anchor="middle">Shared Metadata &amp; Sectors</text>
  </svg>
</div>
```

Each process receives its own descriptor (which might happen to be the same integer, e.g. `3`) mapping to a separate Open File entry in the kernel's global table. Each entry maintains its own read/write cursor offset. If Process A reads 10 bytes, its offset advances to 10, while Process B's offset remains at 0.

However, in certain scenarios (such as when a process forks or passes descriptor references through IPC), different processes *can* share the exact same kernel-managed open file state. In that case, an offset advance by one process directly affects where the other process will read or write next.

File descriptors belong to individual processes, but open-file states and files are distinct kernel-wide resources.

---

## 6. Diverse Handles, Uniform Concept

The exact names and mechanisms for this reference system differ across operating systems, but the underlying architectural pattern is identical:

*   **Unix / Linux / POSIX**: Relies on integer-based **File Descriptors**. Standard streams are pre-allocated: `0` (stdin), `1` (stdout), and `2` (stderr).
*   **Windows**: Applications invoke APIs like `CreateFile()` and receive a **HANDLE** (a pointer-sized opaque reference) rather than a small integer.

In both paradigms, the application receives a reference token. The process never interacts with the storage driver directly; it requests operations using the token, and the operating system handles the translation.

---

## 7. The Name-to-Identity Mapping

We now understand that an application does not directly hold the physical file. It uses a file descriptor or reference index to ask the operating system to perform operations on the file. The kernel maintains the open file state and delegates block lookup to the filesystem.

But this relies on the file already being identified by name. 

When the application requests:

`/usr/local/bin/prog`

**How does the filesystem find the file that this name refers to?**
