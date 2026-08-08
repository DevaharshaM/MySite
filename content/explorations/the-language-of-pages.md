---
id: "the-language-of-pages"
category: "Operating Systems"
series: "Operating Systems"
title: "The Language of Pages"
subtitle: "How Virtual Memory and Physical RAM learned to speak the same language."
date: "8th August, 2026"
tags: ["Operating Systems", "Memory Management", "Paging", "Pages", "Frames", "Page Table"]
---

## 1. Why Divide Memory?

The Memory Management Unit (MMU) is incredibly fast, translating addresses on every single CPU cycle. But how does it keep track of where each address belongs?

Imagine if the MMU stored a mapping for every single byte of memory. If a process had a 4 GB address space, the Page Table would need to store 4 billion entries! The map itself would take up many gigabytes of physical RAM, leaving no room for the actual programs.

To solve this, systems divide memory into equal-sized blocks rather than mapping individual bytes. 

*   **Pages**: The equal-sized blocks that partition the **Virtual Address Space** of a process.
*   **Frames**: The equal-sized blocks that partition the **Physical RAM** of the system.

Instead of translating individual byte coordinates, the Page Table simply translates entire **Pages** into **Frames**. 

<div style="text-align: center; margin: 2rem 0; width: 100%;">
  <svg viewBox="0 0 800 320" width="100%" height="auto" style="background: #111827; border: 1px solid rgba(148, 163, 184, 0.12); border-radius: 8px; font-family: 'DM Sans', sans-serif;">
    <rect width="100%" height="100%" fill="url(#grid)" />

    <!-- Virtual Address Space (Pages) -->
    <g transform="translate(40, 30)">
      <rect x="0" y="0" width="180" height="260" rx="8" fill="#1E293B" stroke="#3B82F6" stroke-width="1.5"/>
      <text x="90" y="25" text-anchor="middle" fill="#FFF" font-size="12" font-weight="bold">VIRTUAL ADDRESS SPACE</text>
      
      <rect x="15" y="45" width="150" height="40" rx="4" fill="#0F172A" stroke="rgba(59,130,246,0.3)"/>
      <text x="90" y="70" text-anchor="middle" fill="#3B82F6" font-size="11" font-family="monospace">Page 0</text>
      
      <rect x="15" y="95" width="150" height="40" rx="4" fill="#0F172A" stroke="rgba(59,130,246,0.3)"/>
      <text x="90" y="120" text-anchor="middle" fill="#3B82F6" font-size="11" font-family="monospace">Page 1</text>
      
      <rect x="15" y="145" width="150" height="40" rx="4" fill="#0F172A" stroke="rgba(59,130,246,0.3)"/>
      <text x="90" y="170" text-anchor="middle" fill="#3B82F6" font-size="11" font-family="monospace">Page 2</text>
      
      <rect x="15" y="195" width="150" height="40" rx="4" fill="#0F172A" stroke="rgba(59,130,246,0.3)"/>
      <text x="90" y="220" text-anchor="middle" fill="#3B82F6" font-size="11" font-family="monospace">Page 3</text>
    </g>

    <!-- Page Table (Mapping Gateway) -->
    <g transform="translate(310, 50)">
      <rect x="0" y="0" width="180" height="220" rx="8" fill="#1E293B" stroke="rgba(148,163,184,0.2)" stroke-width="1.5"/>
      <text x="90" y="25" text-anchor="middle" fill="#FFF" font-size="12" font-weight="bold">PAGE TABLE</text>
      
      <rect x="15" y="45" width="150" height="30" rx="4" fill="#0F172A" stroke="rgba(255,255,255,0.05)"/>
      <text x="90" y="64" text-anchor="middle" fill="#E2E8F0" font-size="10" font-family="monospace">Page 0 &rarr; Frame 7</text>

      <rect x="15" y="85" width="150" height="30" rx="4" fill="#0F172A" stroke="rgba(255,255,255,0.05)"/>
      <text x="90" y="104" text-anchor="middle" fill="#E2E8F0" font-size="10" font-family="monospace">Page 1 &rarr; Frame 2</text>

      <rect x="15" y="125" width="150" height="30" rx="4" fill="#0F172A" stroke="rgba(255,255,255,0.05)"/>
      <text x="90" y="144" text-anchor="middle" fill="#E2E8F0" font-size="10" font-family="monospace">Page 2 &rarr; Frame 10</text>

      <rect x="15" y="165" width="150" height="30" rx="4" fill="#0F172A" stroke="rgba(255,255,255,0.05)"/>
      <text x="90" y="184" text-anchor="middle" fill="#E2E8F0" font-size="10" font-family="monospace">Page 3 &rarr; Frame 5</text>
    </g>

    <!-- Physical RAM (Frames) -->
    <g transform="translate(580, 30)">
      <rect x="0" y="0" width="180" height="260" rx="8" fill="#1E293B" stroke="#10B981" stroke-width="1.5"/>
      <text x="90" y="25" text-anchor="middle" fill="#FFF" font-size="12" font-weight="bold">PHYSICAL RAM</text>

      <rect x="15" y="45" width="150" height="30" rx="4" fill="#111B30" stroke="rgba(16,185,129,0.3)"/>
      <text x="90" y="64" text-anchor="middle" fill="#10B981" font-size="10" font-family="monospace">Frame 2</text>

      <rect x="15" y="85" width="150" height="30" rx="4" fill="#111B30" stroke="rgba(16,185,129,0.3)"/>
      <text x="90" y="104" text-anchor="middle" fill="#10B981" font-size="10" font-family="monospace">Frame 5</text>

      <rect x="15" y="125" width="150" height="30" rx="4" fill="#111B30" stroke="rgba(16,185,129,0.3)"/>
      <text x="90" y="144" text-anchor="middle" fill="#10B981" font-size="10" font-family="monospace">Frame 7</text>

      <rect x="15" y="165" width="150" height="30" rx="4" fill="#111B30" stroke="rgba(16,185,129,0.3)"/>
      <text x="90" y="184" text-anchor="middle" fill="#10B981" font-size="10" font-family="monospace">Frame 10</text>

      <text x="90" y="225" text-anchor="middle" fill="#64748B" font-size="9">(Scattered in physical space)</text>
    </g>

    <!-- Connectors -->
    <!-- Page 0 to Frame 7 path -->
    <path d="M 220 95 L 310 115" fill="none" stroke="#3B82F6" stroke-width="1.5" stroke-dasharray="3"/>
    <path d="M 490 115 L 580 170" fill="none" stroke="#10B981" stroke-width="1.5"/>
  </svg>
</div>

---

## 2. Why Equal Sizes?

If we partition memory into blocks, a crucial rule emerges: **Pages and Frames must be exactly the same size.**

Why? Because the MMU never modifies the entire address sequence. It only replaces the Page Number with the physical Frame Number. The rest of the address—the Offset—remains completely untouched.

*   **Page Number**: Represents *which* block in the virtual address space is being accessed.
*   **Frame Number**: Represents *which* physical block in the RAM chip is being targeted.
*   **Offset**: Represents the specific byte offset *within* that block.

Because the offset is identical on both sides, the index of the byte inside the Page is exactly the same as the index of the byte inside the Frame. If the sizes differed, the offset would point to a completely different byte, scrambling data structure alignments.

<div style="text-align: center; margin: 2rem 0; width: 100%;">
  <svg viewBox="0 0 800 260" width="100%" height="auto" style="background: #111827; border: 1px solid rgba(148, 163, 184, 0.12); border-radius: 8px; font-family: 'DM Sans', sans-serif;">
    <rect width="100%" height="100%" fill="url(#grid)" />

    <!-- CPU Generating Address -->
    <rect x="40" y="80" width="160" height="90" rx="6" fill="#1E293B" stroke="#3B82F6" stroke-width="1.5"/>
    <text x="120" y="110" text-anchor="middle" fill="#FFF" font-size="12" font-weight="bold">CPU ADDRESS</text>
    <rect x="55" y="125" width="130" height="30" rx="3" fill="#0F172A" stroke="rgba(59,130,246,0.3)"/>
    <text x="120" y="144" text-anchor="middle" fill="#3B82F6" font-size="11" font-family="monospace">0x1234</text>

    <!-- Page / Offset Split -->
    <g transform="translate(250, 40)">
      <rect x="0" y="0" width="120" height="60" rx="4" fill="#1E293B" stroke="#3B82F6"/>
      <text x="60" y="20" text-anchor="middle" fill="#64748B" font-size="10">PAGE NUMBER</text>
      <text x="60" y="45" text-anchor="middle" fill="#3B82F6" font-size="14" font-family="monospace" font-weight="bold">0x12</text>
    </g>

    <g transform="translate(250, 150)">
      <rect x="0" y="0" width="120" height="60" rx="4" fill="#1E293B" stroke="#F59E0B" stroke-dasharray="3"/>
      <text x="60" y="20" text-anchor="middle" fill="#64748B" font-size="10">OFFSET</text>
      <text x="60" y="45" text-anchor="middle" fill="#F59E0B" font-size="14" font-family="monospace" font-weight="bold">0x34</text>
    </g>

    <!-- Page Table Translation Box -->
    <rect x="420" y="40" width="120" height="60" rx="4" fill="#111B30" stroke="#10B981" stroke-width="1.5"/>
    <text x="480" y="65" text-anchor="middle" fill="#10B981" font-size="11" font-weight="bold">Frame: 0x8A</text>
    <text x="480" y="85" text-anchor="middle" fill="#64748B" font-size="9">(Page Table Translation)</text>

    <!-- Reassembled Physical Address -->
    <rect x="590" y="80" width="170" height="90" rx="6" fill="#1E293B" stroke="#10B981" stroke-width="1.5"/>
    <text x="675" y="110" text-anchor="middle" fill="#FFF" font-size="12" font-weight="bold">PHYSICAL RAM TARGET</text>
    <rect x="605" y="125" width="140" height="30" rx="3" fill="#0F172A" stroke="rgba(16,185,129,0.3)"/>
    <text x="675" y="144" text-anchor="middle" fill="#10B981" font-size="11" font-family="monospace">
      0x8A<tspan fill="#F59E0B">34</tspan>
    </text>

    <!-- Flow paths -->
    <path d="M 200 125 L 250 70" fill="none" stroke="#3B82F6" stroke-width="1.5"/>
    <path d="M 200 125 L 250 180" fill="none" stroke="#F59E0B" stroke-width="1.5"/>
    
    <path d="M 370 70 L 420 70" fill="none" stroke="#3B82F6" stroke-width="1.5"/>
    <path d="M 540 70 L 590 125" fill="none" stroke="#10B981" stroke-width="1.5"/>
    <path d="M 370 180 L 590 125" fill="none" stroke="#F59E0B" stroke-width="1.5" stroke-dasharray="4"/>
  </svg>
</div>

The offset **never changes**. Page `0x12` translates into Frame `0x8A`, but offset `0x34` maps directly to offset `0x34` inside the destination frame.

---

## 3. The Page Table

So, what is the Page Table?

It is simply an array indexed by the **Page Number**. Each entry in the Page Table (often called a Page Table Entry, or PTE) contains the corresponding **Frame Number** where that page is physically loaded.

| Virtual Page Number | Valid Bit | Physical Frame Number |
| :--- | :--- | :--- |
| **0x00** | 1 | 0x07 |
| **0x01** | 1 | 0x02 |
| **0x02** | 1 | 0x0A |
| **0x03** | 1 | 0x05 |

If the CPU wants to access Virtual Address `0x011A` (Page `0x01`, Offset `0x1A`), the MMU queries index `0x01` of the Page Table. The table returns Frame Number `0x02`. The MMU then targets Physical Address `0x021A`.

No math, no search loops. Just a direct index lookup.

---

## 4. EdgeCase: One Page Finds Its Frame

Let's watch a single Virtual Address complete the translation pipeline.

#### 4.2.1 EdgeCase: Page-to-Frame Pipeline

<div id="one-page-finds-its-frame-edgecase" class="edgecase-container"></div>

---

## 5. Reflection

We now know the language of memory: Page sizes match Frame sizes, letting us translate coordinates by simply swapping the block headers while leaving the internal offset untouched.

But a structural bottleneck exists:

The Physical RAM chip contains only a limited number of Frame slots. What happens when a process attempts to read a Page that isn't currently loaded into any of those physical frames?

The operating system must make room. But how does it decide which page to evict, and how does the hardware handle this missing memory link?
