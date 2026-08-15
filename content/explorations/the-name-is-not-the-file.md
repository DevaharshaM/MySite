---
id: the-name-is-not-the-file
category: "Operating Systems"
series: "Operating Systems"
title: "The Name Is Not the File"
subtitle: "Understanding directories, path resolution, and filesystem identity."
date: "11th August, 2026"
tags: ["Operating Systems", "File Management", "Path Resolution", "Directories", "Hard Links"]
---

## 1. Start with the Familiar Name

When we interact with persistent storage, we locate and open files using names:

```text
notes.txt
```

To a user or a programmer, it is natural to assume that the name *is* the file itself.

But this assumption is incorrect.

A filename is merely a string used to identify an object. It is not the underlying file object, nor is it the physical container of the data. A filename is a name used for lookup within a namespace. The physical data blocks on disk and the metadata describing them have an entirely separate identity.

This separation becomes more apparent when we construct a sequence of names to identify a file—a **Path**:

```text
/home/dev/projects/notes.txt
```

A path is not a single physical string stored on disk that points directly to a sector. Instead, a path is a map. It represents a route that the operating system must navigate component by component to find the target object.

---

## 2. From Path to File

To resolve the path `/home/dev/projects/notes.txt`, the filesystem must step through each component of the directory hierarchy:

```html
<div class="svg-container" style="margin: 2rem 0; text-align: center;">
  <svg viewBox="0 0 800 130" width="100%" height="auto" style="background: #151d2a; border-radius: 12px; border: 1px solid rgba(148, 163, 184, 0.08); font-family: system-ui, -apple-system, sans-serif;">
    <defs>
      <marker id="arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
        <path d="M 0 1 L 10 5 L 0 9 z" fill="#3b82f6" />
      </marker>
    </defs>
    <text x="30" y="30" fill="#64748b" font-size="10" font-family="monospace" text-transform="uppercase" letter-spacing="0.05em">Path Resolution Sequence</text>
    
    <rect x="40" y="55" width="40" height="30" rx="4" fill="#1e293b" stroke="#3b82f6" />
    <text x="60" y="74" fill="#fff" font-size="11" font-weight="bold" font-family="monospace" text-anchor="middle">/</text>
    <line x1="80" y1="70" x2="112" y2="70" stroke="#3b82f6" stroke-width="1.5" marker-end="url(#arrow)" />
    
    <rect x="120" y="55" width="70" height="30" rx="4" fill="#1e293b" stroke="rgba(148, 163, 184, 0.2)" />
    <text x="155" y="74" fill="#e2e8f0" font-size="11" text-anchor="middle">home</text>
    <line x1="190" y1="70" x2="222" y2="70" stroke="#3b82f6" stroke-width="1.5" marker-end="url(#arrow)" />

    <rect x="230" y="55" width="70" height="30" rx="4" fill="#1e293b" stroke="rgba(148, 163, 184, 0.2)" />
    <text x="265" y="74" fill="#e2e8f0" font-size="11" text-anchor="middle">dev</text>
    <line x1="300" y1="70" x2="332" y2="70" stroke="#3b82f6" stroke-width="1.5" marker-end="url(#arrow)" />

    <rect x="340" y="55" width="85" height="30" rx="4" fill="#1e293b" stroke="rgba(148, 163, 184, 0.2)" />
    <text x="382" y="74" fill="#e2e8f0" font-size="11" text-anchor="middle">projects</text>
    <line x1="425" y1="70" x2="457" y2="70" stroke="#3b82f6" stroke-width="1.5" marker-end="url(#arrow)" />

    <rect x="465" y="55" width="85" height="30" rx="4" fill="#1e293b" stroke="#3b82f6" stroke-dasharray="3,2" />
    <text x="507" y="74" fill="#3b82f6" font-size="11" font-weight="bold" text-anchor="middle">notes.txt</text>
    <line x1="550" y1="70" x2="592" y2="70" stroke="#10b981" stroke-width="1.5" marker-end="url(#arrow)" />

    <rect x="600" y="55" width="140" height="30" rx="4" fill="#111827" stroke="#10b981" stroke-width="1.5" />
    <text x="670" y="74" fill="#10b981" font-size="11" font-weight="bold" text-anchor="middle">File Identity (Inode)</text>
  </svg>
</div>
```

The process begins at the absolute root of the filesystem namespace. The operating system looks up the root node, retrieves its contents, finds the mapping for `home`, and traverses downward. It repeats this matching step for `dev` and `projects` until it gets the entry for `notes.txt`.

A path is not a pointer to data. **A path is a set of instructions for navigating a hierarchical namespace.**

---

## 3. Directories Are Not Folders

In graphical user interfaces, directories are styled as "folders"—visual bins that contain physical files. 

Conceptually, however, a directory is a mapping table. It is an organizational structure that translates human-readable name strings into unique filesystem internal identities.

```html
<div class="svg-container" style="margin: 2rem 0; text-align: center;">
  <svg viewBox="0 0 800 200" width="100%" height="auto" style="background: #151d2a; border-radius: 12px; border: 1px solid rgba(148, 163, 184, 0.08); font-family: system-ui, -apple-system, sans-serif;">
    <defs>
      <marker id="arrow-green" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
        <path d="M 0 1 L 10 5 L 0 9 z" fill="#10b981" />
      </marker>
    </defs>
    <text x="30" y="30" fill="#64748b" font-size="10" font-family="monospace" text-transform="uppercase" letter-spacing="0.05em">Conceptual Directory Structure</text>
    
    <rect x="50" y="50" width="220" height="120" rx="8" fill="#1e293b" stroke="rgba(148, 163, 184, 0.2)" />
    <text x="70" y="75" fill="#fff" font-size="12" font-weight="bold">Directory Entries Table</text>
    <line x1="70" y1="85" x2="250" y2="85" stroke="rgba(148, 163, 184, 0.1)" />
    <text x="70" y="105" fill="#a5f3fc" font-size="10" font-family="monospace">📄 notes.txt</text>
    <text x="70" y="125" fill="#a5f3fc" font-size="10" font-family="monospace">🖼️ photo.jpg</text>
    <text x="70" y="145" fill="#f59e0b" font-size="10" font-family="monospace">📁 projects/</text>
    
    <path d="M 270,100 L 372,80" fill="none" stroke="#10b981" stroke-width="1.5" marker-end="url(#arrow-green)" />
    <path d="M 270,120 L 372,120" fill="none" stroke="#10b981" stroke-width="1.5" marker-end="url(#arrow-green)" />
    <path d="M 270,140 L 372,160" fill="none" stroke="#10b981" stroke-width="1.5" marker-end="url(#arrow-green)" />
    
    <rect x="380" y="60" width="220" height="36" rx="4" fill="#111827" stroke="rgba(148, 163, 184, 0.15)" />
    <text x="400" y="82" fill="#e2e8f0" font-size="11">File: 'notes.txt' Metadata and Inode #7182</text>
    
    <rect x="380" y="102" width="220" height="36" rx="4" fill="#111827" stroke="rgba(148, 163, 184, 0.15)" />
    <text x="400" y="124" fill="#e2e8f0" font-size="11">File: 'photo.jpg' Metadata and Inode #8221</text>
    
    <rect x="380" y="144" width="220" height="36" rx="4" fill="#1e293b" stroke="#f59e0b" stroke-width="1.5" />
    <text x="400" y="166" fill="#f59e0b" font-size="11" font-weight="bold">Directory Object: Inode #1204</text>
  </svg>
</div>
```

A directory provides mappings from names to filesystem objects. When we look up `notes.txt` inside a directory table, we receive the internal index key. By nesting directory objects inside other directory tables, the filesystem builds the entire hierarchical directory tree.

---

## 4. EdgeCase: Path Resolution

Watch the interactive sequence below to trace how the operating system resolves `/home/dev/projects/notes.txt` from the root node through nested directories, retrieving directory entry tables along the path:

<div id="path-resolution-edgecase" class="edgecase-container"></div>

---

## 5. The Surprising Part: Name ≠ Identity

Because directories only link names to identities, the name of a file is decoupled from the file itself. This means **multiple names can point to the same underlying file identity**.

This relationship is known as a **Hard Link**:

```html
<div class="svg-container" style="margin: 2rem 0; text-align: center;">
  <svg viewBox="0 0 800 180" width="100%" height="auto" style="background: #151d2a; border-radius: 12px; border: 1px solid rgba(148, 163, 184, 0.08); font-family: system-ui, -apple-system, sans-serif;">
    <defs>
      <marker id="arrow-green" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
        <path d="M 0 1 L 10 5 L 0 9 z" fill="#10b981" />
      </marker>
    </defs>
    <text x="30" y="30" fill="#64748b" font-size="10" font-family="monospace" text-transform="uppercase" letter-spacing="0.05em">Hard Link Architecture</text>
    
    <rect x="50" y="50" width="220" height="100" rx="8" fill="#1e293b" stroke="rgba(148, 163, 184, 0.2)" />
    <text x="70" y="75" fill="#fff" font-size="11" font-weight="bold">Directory Entries Map</text>
    <line x1="70" y1="83" x2="230" y2="83" stroke="rgba(148, 163, 184, 0.1)" />
    
    <rect x="70" y="93" width="180" height="20" rx="3" fill="rgba(255,255,255,0.02)" stroke="rgba(148, 163, 184, 0.1)" />
    <text x="80" y="107" fill="#e2e8f0" font-size="10" font-family="monospace">📄 report.txt</text>
    
    <rect x="70" y="120" width="180" height="20" rx="3" fill="rgba(255,255,255,0.02)" stroke="rgba(148, 163, 184, 0.1)" />
    <text x="80" y="134" fill="#e2e8f0" font-size="10" font-family="monospace">📄 backup.txt</text>

    <path d="M 250,103 L 392,100" fill="none" stroke="#10b981" stroke-width="1.5" marker-end="url(#arrow-green)" />
    <path d="M 250,130 L 392,110" fill="none" stroke="#10b981" stroke-width="1.5" marker-end="url(#arrow-green)" />

    <rect x="400" y="65" width="260" height="70" rx="6" fill="#111827" stroke="#10b981" stroke-width="2" />
    <text x="420" y="90" fill="#10b981" font-size="12" font-weight="bold">Inode #7182 (Single File Identity)</text>
    <text x="420" y="108" fill="#94a3b8" font-size="10">Link Count: 2</text>
    <text x="420" y="123" fill="#64748b" font-size="9" font-family="monospace">Data blocks: #41902, #41903</text>
  </svg>
</div>
```

In this system, both `report.txt` and `backup.txt` entries are registered inside a directory pointing to the exact same file metadata entry (Inode #7182). 

This is not a copy. Both names refer to the exact same file. If a program writes to `report.txt` and updates its content, a subsequent read of `backup.txt` immediately reveals those updates. The file remains alive until all names pointing to its inode reference are deleted (reducing the link count to 0).

---

## 6. Symbolic Links

Another way to map names is through a **Symbolic Link** (often called a symlink or shortcut). 

Unlike a hard link, which points directly to the file identity, a symbolic link is a separate file that stores a path string referencing another name:

```html
<div class="svg-container" style="margin: 2rem 0; text-align: center;">
  <svg viewBox="0 0 800 200" width="100%" height="auto" style="background: #151d2a; border-radius: 12px; border: 1px solid rgba(148, 163, 184, 0.08); font-family: system-ui, -apple-system, sans-serif;">
    <defs>
      <marker id="arrow-blue" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
        <path d="M 0 1 L 10 5 L 0 9 z" fill="#3b82f6" />
      </marker>
      <marker id="arrow-purple" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
        <path d="M 0 1 L 10 5 L 0 9 z" fill="#a855f7" />
      </marker>
    </defs>
    <text x="30" y="30" fill="#64748b" font-size="10" font-family="monospace" text-transform="uppercase" letter-spacing="0.05em">Symbolic Link (Shortcut) Pathing</text>
    
    <rect x="50" y="50" width="220" height="120" rx="8" fill="#1e293b" stroke="rgba(148, 163, 184, 0.2)" />
    <text x="70" y="72" fill="#fff" font-size="11" font-weight="bold">Directory Entry Table</text>
    <line x1="70" y1="80" x2="230" y2="80" stroke="rgba(148, 163, 184, 0.1)" />

    <rect x="65" y="88" width="190" height="26" rx="3" fill="rgba(59,130,246,0.1)" stroke="#3b82f6" />
    <text x="75" y="104" fill="#3b82f6" font-size="10" font-family="monospace" font-weight="bold">🔗 latest.txt</text>

    <rect x="65" y="124" width="190" height="26" rx="3" fill="rgba(16,185,129,0.05)" stroke="rgba(148, 163, 184, 0.15)" />
    <text x="75" y="140" fill="#e2e8f0" font-size="10" font-family="monospace">📄 report.txt</text>

    <path d="M 255,101 L 372,85" fill="none" stroke="#3b82f6" stroke-width="1.5" marker-end="url(#arrow-blue)" />
    <path d="M 470,110 L 268,135" fill="none" stroke="#3b82f6" stroke-dasharray="3,3" stroke-width="1.5" marker-end="url(#arrow-blue)" />
    <path d="M 255,137 L 592,137" fill="none" stroke="#a855f7" stroke-width="1.5" marker-end="url(#arrow-purple)" />

    <rect x="380" y="60" width="180" height="50" rx="5" fill="#1e293b" stroke="#3b82f6" stroke-dasharray="4,4" />
    <text x="390" y="78" fill="#94a3b8" font-size="9" font-family="monospace">Symlink Inode #8012</text>
    <text x="390" y="94" fill="#3b82f6" font-size="9" font-family="monospace" font-weight="bold">Contents: 'report.txt'</text>

    <rect x="600" y="107" width="160" height="50" rx="5" fill="#111827" stroke="#a855f7" stroke-width="1.5" />
    <text x="610" y="128" fill="#e2e8f0" font-size="10" font-weight="bold">Inode #7182</text>
    <text x="610" y="144" fill="#64748b" font-size="9" font-family="monospace">Real Data Blocks</text>
  </svg>
</div>
```

The difference between the two configurations is fundamental:
* **Hard Link**: A direct path from multiple names to the *same target inode*.
* **Symbolic Link**: A path from a name to a *new file object* whose data payload contains the text string of another path.

If the target name `report.txt` is deleted, the symlink `latest.txt` remains behind but becomes a "broken link," resolving to a path that no longer exists.

---

## 7. Relative vs. Absolute Paths

Paths can be specified in two formats:

* **Absolute**: Starts from the root token (`/`), e.g., `/home/dev/projects/notes.txt`. Resolution always begins at root.
* **Relative**: Does not start from root, e.g., `projects/notes.txt`. Resolution begins from a contextual environment—typically the process's **Current Working Directory** (CWD).

This context means the same relative path can resolve to different physical files depending on which folder the application is executed from.

---

## 8. Real Operating-System Connection

While disk format structures vary across operating systems, the core programming interface remains uniform. 

For instance, Linux filesystems (like ext4) implement directory entries as tables mapping name strings to numerical index nodes (**inodes**). The inode contains all metadata and block addresses, but has no knowledge of the name itself. Regardless of the underlying operating system—be it Windows, macOS, or Linux—the OS presents the exact same unified namespace abstraction (names, paths, directories, and file objects) to user application processes.

---

## 9. The Next Question

How does the filesystem keep track of all this information — the file's metadata, its directory entries, its data blocks, and the free space around them?
