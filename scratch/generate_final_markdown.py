# -*- coding: utf-8 -*-

markdown_text = r"""---
id: the-8051-when-time-becomes-a-signal
category: Controller
series: Controller
title: The 8051 — When Time Becomes a Signal
subtitle: How the classic 8051 specializes the architecture of hardware timing through its Special Function Registers.
date: 28 August 2026
tags: [Controller, 8051, Microcontroller, Timers, Counters, Hardware Timing, TCON, TMOD, EdgeCase, Embedded Systems]
footer: Foundational explorations in microcontroller architecture, 8051 systems, and embedded computing — PrajnaEdge.dev
---

## 1. The Doors We Left Unopened

In our exploration of the 8051 Special Function Register map, we walked through the upper data space above `7FH`.

We saw how Intel's architects mapped the entire machine—CPU registers, parallel I/O ports, serial communications, and interrupt controls—into a unified control surface. And right in the middle of that map, six registers appeared under a single heading:

```text
TIMERS & COUNTERS
  │
  ├── TCON (88H)  →  Timer / Counter Control Register (Bit-Addressable)
  ├── TMOD (89H)  →  Timer / Counter Mode Register    (Byte-Only)
  │
  ├── TL0  (8AH)  →  Timer 0 Low Byte
  ├── TL1  (8BH)  →  Timer 1 Low Byte
  ├── TH0  (8CH)  →  Timer 0 High Byte
  └── TH1  (8DH)  →  Timer 1 High Byte
```

In that previous exploration, these registers were only addresses—quiet names on a silicon layout, closed doorways sitting on the machine's control surface.

Now we can open them.

---

## 2. Concrete Silicon, Not Abstract Theory

In the Coordination node of the PrajnaEdge Tree, our exploration [The Architecture of Time](/explorations/the-architecture-of-time/) established the universal grammar of machine timing:

```text
Clock Source  ───►  Counter  ───►  Overflow  ───►  Event
```

We saw that to break free from the trap of CPU software delay loops—where the processor burns millions of cycles spinning in empty decrement loops, blind to the outside world—a machine must delegate time to autonomous digital counting circuits.

![Software Delay Loop vs Autonomous Hardware Timer](Images/intel_8051_software_delay_vs_hardware_timer.svg)

That was the universal concept.

But abstract concepts do not execute on circuit boards. Real silicon does.

Now let us step out of theory and look into one actual, historical machine. How does the classic Intel 8051 actually implement this timing architecture?

In the 8051, there are no generic auto-reload registers, no multichannel capture-compare complexes, and no complex bus arbitration layers. Instead, the 8051 gives the universal timing model a lean, concrete form:

```text
8051 Oscillator / 12  ───►  Timer 0 / 1  ───►  THx:TLx  ───►  TFx Flag  ───►  CPU / ISR Action
```

The entire mechanism is operated through the six Special Function Registers we met in the memory map.

---

## 3. The Clock Is Already Moving

Where does an 8051 get its time?

It does not generate time out of nothing. The moment power is applied to the chip, an external quartz crystal begins oscillating—traditionally at 12 MHz.

Inside the chip, frequency divider circuits partition this oscillation into **machine cycles**. In the classic 8051, exactly 12 oscillator periods form one machine cycle:

$$\text{Machine Cycle Frequency} = \frac{12\text{ MHz}}{12} = 1\text{ MHz}$$

$$1\text{ Machine Cycle} = 1\ \mu\text{s}$$

This rhythm is *already flowing*. Every instruction fetch, every memory cycle, and every bus operation beats to this steady, relentless 1-microsecond pulse train.

![The 8051 Clock-to-Overflow Pipeline](Images/intel_8051_timer_clock_to_overflow.svg)

The 8051 timer does not create a new clock. It simply taps into this preexisting stream of machine cycles, passes it through a software-controlled run gate (`TR0`), and feeds it into an autonomous 16-bit counting register (`TH0:TL0`).

While software executes instructions elsewhere, the counter increments on every cycle in silence.

---

## 4. Timer or Counter? The $C/\overline{T}$ Decision

Here we arrive at an essential architectural realization.

What is the fundamental difference between measuring time and counting external events?

To a programmer, they feel like two completely different tasks:
- Measuring time means waiting for 50 milliseconds to elapse.
- Counting events means tallying revolutions of an optical motor encoder or recording sensor pulses on a factory belt.

Yet to digital hardware, **both operations are identical**:

```text
Pulses Arrive  ───►  Counter Register Increments by 1
```

The 8051 does not duplicate silicon by building two separate subsystems for timers and counters. It uses the **exact same 16-bit counting hardware** for both.

All that changes is where the pulses come from:

1. **Timer Mode ($C/\overline{T} = 0$):**
   The counter is fed by the internal machine cycle clock (Oscillator / 12). Because pulses arrive at regular, predictable intervals, the accumulated count directly represents elapsed time.

2. **Counter Mode ($C/\overline{T} = 1$):**
   The counter is disconnected from the internal clock and connected directly to an external chip pin:
   - **Pin P3.4 (T0)** for Timer 0
   - **Pin P3.5 (T1)** for Timer 1

   Whenever a 1-to-0 negative electrical transition occurs on the pin, the hardware increments the register. The counter is now counting physical happenings in the outside world.

![Timer or Counter? The Pulse Source](Images/intel_8051_timer_vs_counter_sources.svg)

The selector switch between these two modes is a single bit in silicon: the **$C/\overline{T}$ bit** in **`TMOD (89H)`**.

---

## 5. Two Timers, One Architectural Pattern

The 8051 contains two identical, independent timing blocks: **Timer 0** and **Timer 1**.

Let us observe how their physical counting registers are paired in hardware:

### The 16-Bit Counter Pairings

A classic 8051 CPU operates on an 8-bit internal data bus. To count up to 65,535, each 16-bit timer is split across two separate 8-bit Special Function Registers:

<!-- Timer 0 16-bit Register Diagram -->
<div style="margin: 1.5rem 0; overflow-x: auto; -webkit-overflow-scrolling: touch;">
  <div style="min-width: 520px; background: #0F172A; border: 1.5px solid #10B981; border-radius: 8px; padding: 1rem; box-shadow: 0 4px 20px rgba(0,0,0,0.3);">
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.75rem; border-bottom:1px solid #1E293B; padding-bottom:0.4rem;">
      <span style="font-family:'IBM Plex Mono', monospace; font-size:0.85rem; font-weight:700; color:#34D399;">TIMER 0 &mdash; 16-BIT HARDWARE COUNTER</span>
      <span style="font-size:0.7rem; color:#94A3B8; background:#064E3B; padding:0.15rem 0.5rem; border-radius:4px; font-family:'IBM Plex Mono', monospace;">Max: 65,535 (FFFFH)</span>
    </div>

    <!-- 16-Bit Register Grid -->
    <div style="display:grid; grid-template-columns: 1fr 1fr; border: 1.5px solid #059669; border-radius: 6px; overflow: hidden; background: #020617;">
      <!-- TH0 -->
      <div style="border-right: 1.5px solid #059669; padding: 0.8rem 0.5rem; text-align: center; background: rgba(16, 185, 129, 0.08);">
        <div style="font-family:'IBM Plex Mono', monospace; font-size: 1.05rem; font-weight: 700; color: #34D399;">TH0 (8CH)</div>
        <div style="font-size: 0.72rem; color: #94A3B8; margin-top: 0.2rem;">High Byte &bull; Bits 15..8</div>
      </div>
      <!-- TL0 -->
      <div style="padding: 0.8rem 0.5rem; text-align: center; background: rgba(16, 185, 129, 0.08);">
        <div style="font-family:'IBM Plex Mono', monospace; font-size: 1.05rem; font-weight: 700; color: #34D399;">TL0 (8AH)</div>
        <div style="font-size: 0.72rem; color: #94A3B8; margin-top: 0.2rem;">Low Byte &bull; Bits 7..0</div>
      </div>
    </div>

    <div style="display:flex; justify-content:space-between; margin-top:0.4rem; font-family:'IBM Plex Mono', monospace; font-size:0.7rem; color:#64748B;">
      <span>Bit 15</span>
      <span style="color:#10B981; font-weight:600;">&larr; Cascading 16-bit Count Range &rarr;</span>
      <span>Bit 0</span>
    </div>
  </div>
</div>

<!-- Timer 1 16-bit Register Diagram -->
<div style="margin: 1.5rem 0; overflow-x: auto; -webkit-overflow-scrolling: touch;">
  <div style="min-width: 520px; background: #0F172A; border: 1.5px solid #6366F1; border-radius: 8px; padding: 1rem; box-shadow: 0 4px 20px rgba(0,0,0,0.3);">
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.75rem; border-bottom:1px solid #1E293B; padding-bottom:0.4rem;">
      <span style="font-family:'IBM Plex Mono', monospace; font-size:0.85rem; font-weight:700; color:#818CF8;">TIMER 1 &mdash; 16-BIT HARDWARE COUNTER</span>
      <span style="font-size:0.7rem; color:#94A3B8; background:#312E81; padding:0.15rem 0.5rem; border-radius:4px; font-family:'IBM Plex Mono', monospace;">Max: 65,535 (FFFFH)</span>
    </div>

    <!-- 16-Bit Register Grid -->
    <div style="display:grid; grid-template-columns: 1fr 1fr; border: 1.5px solid #4F46E5; border-radius: 6px; overflow: hidden; background: #020617;">
      <!-- TH1 -->
      <div style="border-right: 1.5px solid #4F46E5; padding: 0.8rem 0.5rem; text-align: center; background: rgba(99, 102, 241, 0.08);">
        <div style="font-family:'IBM Plex Mono', monospace; font-size: 1.05rem; font-weight: 700; color: #818CF8;">TH1 (8DH)</div>
        <div style="font-size: 0.72rem; color: #94A3B8; margin-top: 0.2rem;">High Byte &bull; Bits 15..8</div>
      </div>
      <!-- TL1 -->
      <div style="padding: 0.8rem 0.5rem; text-align: center; background: rgba(99, 102, 241, 0.08);">
        <div style="font-family:'IBM Plex Mono', monospace; font-size: 1.05rem; font-weight: 700; color: #818CF8;">TL1 (8BH)</div>
        <div style="font-size: 0.72rem; color: #94A3B8; margin-top: 0.2rem;">Low Byte &bull; Bits 7..0</div>
      </div>
    </div>

    <div style="display:flex; justify-content:space-between; margin-top:0.4rem; font-family:'IBM Plex Mono', monospace; font-size:0.7rem; color:#64748B;">
      <span>Bit 15</span>
      <span style="color:#818CF8; font-weight:600;">&larr; Cascading 16-bit Count Range &rarr;</span>
      <span>Bit 0</span>
    </div>
  </div>
</div>

Notice the pairing in the SFR address space:
- The low bytes are placed adjacent at `8AH (TL0)` and `8BH (TL1)`.
- The high bytes are placed adjacent at `8CH (TH0)` and `8DH (TH1)`.

Together, `TL0` and `TH0` form a 16-bit digital register capable of counting from `0000H` up to `FFFFH` (65,535 counts). `TL1` and `TH1` form an identical 16-bit register for Timer 1.

![Two Timers, One Architectural Pattern](Images/intel_8051_two_timers_architecture.svg)

Both timers operate completely independently, yet both are supervised through two shared registers: **`TMOD`** and **`TCON`**.

---

## 6. The Control Panel: TMOD vs TCON

Why did Intel's architects split timer control across two separate registers instead of one?

Recall the bit-addressable rule from *The 8051 — Where Software Touches Hardware*:

> An SFR is bit-addressable if and only if its address ends in `0H` or `8H`.

This rule reveals the profound architectural divide between **setting rules** and **pulling live levers**:

### TMOD (89H): Setting the Rules Once
Address `89H` does *not* end in `0H` or `8H`. It is **byte-only**.

`TMOD` is configured during system boot to establish operating policies:
- Is Timer 0 operating as a Timer ($C/\overline{T} = 0$) or Counter ($C/\overline{T} = 1$)?
- What is its counting structure ($M1, M0$): 13-bit Mode 0, 16-bit Mode 1, or 8-bit Auto-Reload Mode 2?
- What are the corresponding policies for Timer 1?

Because configuration is written once during setup, bit-by-bit manipulation is unnecessary. Here is how `TMOD` is organized in silicon:

<!-- TMOD Register Frame Diagram -->
<div style="margin: 1.5rem 0; overflow-x: auto; -webkit-overflow-scrolling: touch;">
  <div style="min-width: 580px; background: #0F172A; border: 1.5px solid #38BDF8; border-radius: 8px; padding: 1.25rem; box-shadow: 0 4px 24px rgba(0,0,0,0.4);">
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.75rem; border-bottom:1px solid #1E293B; padding-bottom:0.5rem;">
      <span style="font-family:'IBM Plex Mono', monospace; font-size:0.85rem; font-weight:700; color:#38BDF8;">TMOD (89H) &mdash; TIMER / COUNTER MODE REGISTER</span>
      <span style="font-size:0.7rem; color:#94A3B8; background:#1E293B; padding:0.2rem 0.5rem; border-radius:4px; font-family:'IBM Plex Mono', monospace;">BYTE-ONLY &bull; RESET: 00H</span>
    </div>

    <!-- 8-Bit Cell Grid -->
    <div style="display:grid; grid-template-columns: repeat(8, 1fr); border: 2px solid #334155; border-radius: 6px; overflow: hidden; background: #020617;">
      <!-- Bit 7: GATE (T1) -->
      <div style="border-right: 1px solid #1E293B; padding: 0.65rem 0.2rem; text-align: center; background: rgba(99, 102, 241, 0.08);">
        <div style="font-family:'IBM Plex Mono', monospace; font-size: 0.85rem; font-weight: 700; color: #A5B4FC;">GATE</div>
        <div style="font-size: 0.62rem; color: #64748B; font-family:'IBM Plex Mono', monospace;">T1</div>
      </div>
      <!-- Bit 6: C/T (T1) -->
      <div style="border-right: 1px solid #1E293B; padding: 0.65rem 0.2rem; text-align: center; background: rgba(99, 102, 241, 0.08);">
        <div style="font-family:'IBM Plex Mono', monospace; font-size: 0.85rem; font-weight: 700; color: #A5B4FC;">C/T</div>
        <div style="font-size: 0.62rem; color: #64748B; font-family:'IBM Plex Mono', monospace;">T1</div>
      </div>
      <!-- Bit 5: M1 (T1) -->
      <div style="border-right: 1px solid #1E293B; padding: 0.65rem 0.2rem; text-align: center; background: rgba(99, 102, 241, 0.08);">
        <div style="font-family:'IBM Plex Mono', monospace; font-size: 0.85rem; font-weight: 700; color: #A5B4FC;">M1</div>
        <div style="font-size: 0.62rem; color: #64748B; font-family:'IBM Plex Mono', monospace;">T1</div>
      </div>
      <!-- Bit 4: M0 (T1) -->
      <div style="border-right: 2px solid #475569; padding: 0.65rem 0.2rem; text-align: center; background: rgba(99, 102, 241, 0.08);">
        <div style="font-family:'IBM Plex Mono', monospace; font-size: 0.85rem; font-weight: 700; color: #A5B4FC;">M0</div>
        <div style="font-size: 0.62rem; color: #64748B; font-family:'IBM Plex Mono', monospace;">T1</div>
      </div>
      <!-- Bit 3: GATE (T0) -->
      <div style="border-right: 1px solid #1E293B; padding: 0.65rem 0.2rem; text-align: center; background: rgba(16, 185, 129, 0.08);">
        <div style="font-family:'IBM Plex Mono', monospace; font-size: 0.85rem; font-weight: 700; color: #34D399;">GATE</div>
        <div style="font-size: 0.62rem; color: #64748B; font-family:'IBM Plex Mono', monospace;">T0</div>
      </div>
      <!-- Bit 2: C/T (T0) -->
      <div style="border-right: 1px solid #1E293B; padding: 0.65rem 0.2rem; text-align: center; background: rgba(16, 185, 129, 0.08);">
        <div style="font-family:'IBM Plex Mono', monospace; font-size: 0.85rem; font-weight: 700; color: #34D399;">C/T</div>
        <div style="font-size: 0.62rem; color: #64748B; font-family:'IBM Plex Mono', monospace;">T0</div>
      </div>
      <!-- Bit 1: M1 (T0) -->
      <div style="border-right: 1px solid #1E293B; padding: 0.65rem 0.2rem; text-align: center; background: rgba(16, 185, 129, 0.08);">
        <div style="font-family:'IBM Plex Mono', monospace; font-size: 0.85rem; font-weight: 700; color: #34D399;">M1</div>
        <div style="font-size: 0.62rem; color: #64748B; font-family:'IBM Plex Mono', monospace;">T0</div>
      </div>
      <!-- Bit 0: M0 (T0) -->
      <div style="padding: 0.65rem 0.2rem; text-align: center; background: rgba(16, 185, 129, 0.08);">
        <div style="font-family:'IBM Plex Mono', monospace; font-size: 0.85rem; font-weight: 700; color: #34D399;">M0</div>
        <div style="font-size: 0.62rem; color: #64748B; font-family:'IBM Plex Mono', monospace;">T0</div>
      </div>
    </div>

    <!-- Bit numbers row -->
    <div style="display:grid; grid-template-columns: repeat(8, 1fr); text-align: center; margin-top: 0.4rem; font-family:'IBM Plex Mono', monospace; font-size: 0.72rem; color: #64748B;">
      <span>Bit 7</span><span>Bit 6</span><span>Bit 5</span><span>Bit 4</span><span>Bit 3</span><span>Bit 2</span><span>Bit 1</span><span>Bit 0</span>
    </div>

    <!-- Grouping Banners -->
    <div style="display:grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-top: 0.75rem; font-size: 0.72rem; text-align: center; font-weight: 600;">
      <div style="background: rgba(99, 102, 241, 0.12); border: 1px solid #4F46E5; color: #A5B4FC; padding: 0.35rem; border-radius: 4px;">
        &larr; TIMER 1 CONFIGURATION (Bits 7..4) &rarr;
      </div>
      <div style="background: rgba(16, 185, 129, 0.12); border: 1px solid #059669; color: #6EE7B7; padding: 0.35rem; border-radius: 4px;">
        &larr; TIMER 0 CONFIGURATION (Bits 3..0) &rarr;
      </div>
    </div>
  </div>
</div>

Software writes the whole byte during initialization:

```text
MOV TMOD, #01H    ; Timer 0 in 16-bit Timer Mode (C/T = 0, Mode 1)
```

### TCON (88H): The Live Operational Levers
Address `88H` ends in `8H`. It is **bit-addressable**!

`TCON` contains the live runtime switches and status flags that software must touch constantly:

<!-- TCON Register Frame Diagram -->
<div style="margin: 1.5rem 0; overflow-x: auto; -webkit-overflow-scrolling: touch;">
  <div style="min-width: 580px; background: #0F172A; border: 1.5px solid #10B981; border-radius: 8px; padding: 1.25rem; box-shadow: 0 4px 24px rgba(0,0,0,0.4);">
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.75rem; border-bottom:1px solid #1E293B; padding-bottom:0.5rem;">
      <span style="font-family:'IBM Plex Mono', monospace; font-size:0.85rem; font-weight:700; color:#34D399;">TCON (88H) &mdash; TIMER / COUNTER CONTROL REGISTER</span>
      <span style="font-size:0.7rem; color:#94A3B8; background:#064E3B; padding:0.2rem 0.5rem; border-radius:4px; font-family:'IBM Plex Mono', monospace;">BIT-ADDRESSABLE &bull; RESET: 00H</span>
    </div>

    <!-- 8-Bit Cell Grid -->
    <div style="display:grid; grid-template-columns: repeat(8, 1fr); border: 2px solid #334155; border-radius: 6px; overflow: hidden; background: #020617;">
      <!-- Bit 7: TF1 -->
      <div style="border-right: 1px solid #1E293B; padding: 0.65rem 0.2rem; text-align: center; background: rgba(99, 102, 241, 0.12);">
        <div style="font-family:'IBM Plex Mono', monospace; font-size: 0.85rem; font-weight: 700; color: #F59E0B;">TF1</div>
        <div style="font-size: 0.62rem; color: #818CF8; font-family:'IBM Plex Mono', monospace;">8FH</div>
      </div>
      <!-- Bit 6: TR1 -->
      <div style="border-right: 1.5px solid #475569; padding: 0.65rem 0.2rem; text-align: center; background: rgba(99, 102, 241, 0.12);">
        <div style="font-family:'IBM Plex Mono', monospace; font-size: 0.85rem; font-weight: 700; color: #38BDF8;">TR1</div>
        <div style="font-size: 0.62rem; color: #818CF8; font-family:'IBM Plex Mono', monospace;">8EH</div>
      </div>
      <!-- Bit 5: TF0 -->
      <div style="border-right: 1px solid #1E293B; padding: 0.65rem 0.2rem; text-align: center; background: rgba(16, 185, 129, 0.12);">
        <div style="font-family:'IBM Plex Mono', monospace; font-size: 0.85rem; font-weight: 700; color: #F59E0B;">TF0</div>
        <div style="font-size: 0.62rem; color: #34D399; font-family:'IBM Plex Mono', monospace;">8DH</div>
      </div>
      <!-- Bit 4: TR0 -->
      <div style="border-right: 2px solid #475569; padding: 0.65rem 0.2rem; text-align: center; background: rgba(16, 185, 129, 0.12);">
        <div style="font-family:'IBM Plex Mono', monospace; font-size: 0.85rem; font-weight: 700; color: #38BDF8;">TR0</div>
        <div style="font-size: 0.62rem; color: #34D399; font-family:'IBM Plex Mono', monospace;">8CH</div>
      </div>
      <!-- Bit 3: IE1 -->
      <div style="border-right: 1px solid #1E293B; padding: 0.65rem 0.2rem; text-align: center;">
        <div style="font-family:'IBM Plex Mono', monospace; font-size: 0.85rem; font-weight: 600; color: #94A3B8;">IE1</div>
        <div style="font-size: 0.62rem; color: #64748B; font-family:'IBM Plex Mono', monospace;">8BH</div>
      </div>
      <!-- Bit 2: IT1 -->
      <div style="border-right: 1px solid #1E293B; padding: 0.65rem 0.2rem; text-align: center;">
        <div style="font-family:'IBM Plex Mono', monospace; font-size: 0.85rem; font-weight: 600; color: #94A3B8;">IT1</div>
        <div style="font-size: 0.62rem; color: #64748B; font-family:'IBM Plex Mono', monospace;">8AH</div>
      </div>
      <!-- Bit 1: IE0 -->
      <div style="border-right: 1px solid #1E293B; padding: 0.65rem 0.2rem; text-align: center;">
        <div style="font-family:'IBM Plex Mono', monospace; font-size: 0.85rem; font-weight: 600; color: #94A3B8;">IE0</div>
        <div style="font-size: 0.62rem; color: #64748B; font-family:'IBM Plex Mono', monospace;">89H</div>
      </div>
      <!-- Bit 0: IT0 -->
      <div style="padding: 0.65rem 0.2rem; text-align: center;">
        <div style="font-family:'IBM Plex Mono', monospace; font-size: 0.85rem; font-weight: 600; color: #94A3B8;">IT0</div>
        <div style="font-size: 0.62rem; color: #64748B; font-family:'IBM Plex Mono', monospace;">88H</div>
      </div>
    </div>

    <!-- Bit numbers row -->
    <div style="display:grid; grid-template-columns: repeat(8, 1fr); text-align: center; margin-top: 0.4rem; font-family:'IBM Plex Mono', monospace; font-size: 0.72rem; color: #64748B;">
      <span>Bit 7</span><span>Bit 6</span><span>Bit 5</span><span>Bit 4</span><span>Bit 3</span><span>Bit 2</span><span>Bit 1</span><span>Bit 0</span>
    </div>

    <!-- Functional split banners -->
    <div style="display:grid; grid-template-columns: 2fr 2fr 4fr; gap: 6px; margin-top: 0.75rem; font-size: 0.7rem; text-align: center; font-weight: 600;">
      <div style="background: rgba(99, 102, 241, 0.15); border: 1px solid #6366F1; color: #A5B4FC; padding: 0.3rem; border-radius: 4px;">
        TIMER 1 (TF1, TR1)
      </div>
      <div style="background: rgba(16, 185, 129, 0.15); border: 1px solid #10B981; color: #6EE7B7; padding: 0.3rem; border-radius: 4px;">
        TIMER 0 (TF0, TR0)
      </div>
      <div style="background: #1E293B; border: 1px solid #334155; color: #94A3B8; padding: 0.3rem; border-radius: 4px;">
        EXTERNAL INTERRUPTS (INT1, INT0)
      </div>
    </div>
  </div>
</div>

- **`TR0 (8CH)` / `TR1 (8EH)` — Timer Run Bits:**
  The run gates. When `TR0 = 0`, pulses are blocked and the counter freezes. When `TR0 = 1`, pulses flow into the counter. Because `TCON` is bit-addressable, software starts or stops counting with a single atomic instruction:
  ```text
  SETB TR0    ; Open gate: Timer 0 begins counting
  CLR  TR0    ; Close gate: Timer 0 halts immediately
  ```

- **`TF0 (8DH)` / `TF1 (8FH)` — Timer Overflow Flags:**
  The alert signals. When the counter rolls over from its limit back to `0000H`, the hardware automatically sets `TF0 = 1`. This flag announces to the CPU that the allotted time or pulse tally has completed.

---

## 7. The Causal Chain: Hardware to Software to Physical World

Here we must be precise about the boundary between silicon and software.

On a classic 8051, **timer overflow does NOT directly toggle arbitrary I/O pins.**

There is no internal copper wire connecting Timer 0 overflow directly to Pin P1.0. Instead, the 8051 operates on a strict three-tier causal chain:

```text
[1. AUTONOMOUS HARDWARE]
Clock pulses increment TH0:TL0 in silicon
        ↓
Counter rolls over: FFFFH → 0000H (Mode 1) or FFH → Reload (Mode 2)
        ↓
Hardware asserts overflow flag: TF0 = 1 (TCON.5)

[2. CPU / SOFTWARE RESPONSE]
CPU detects TF0 = 1 (via polling loop or Interrupt Service Routine)
        ↓
Software executes purposeful instruction:
CPL P1.0    ; Invert state of Port 1 Pin 0
CLR TF0     ; Clear overflow flag to acknowledge

[3. PHYSICAL WORLD CONSEQUENCE]
Pin P1.0 voltage switches state: 0V ↔ +5V
        ↓
An electrical square wave emerges across external copper wires!
```

This separation is deliberate.

Hardware does what hardware does best: precise, deterministic, relentless counting without spending CPU cycles.

Software does what software does best: interpreting the event and deciding how the physical system should respond.

---

## 8. EdgeCase — The Configuration Experiment

In this interactive workbench, you do not merely watch a counter count. You configure the 8051 timer hardware and observe the direct architectural consequences in silicon.

### Configure Your Hardware

Select the pulse source, choose which timer to inspect, and select the operating mode:

<div id="edgecase-workbench-root" style="background:#0F172A; border:1px solid #1E293B; border-radius:10px; padding:1.25rem; margin:2rem 0; font-family:'DM Sans', sans-serif;">
  <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #1E293B; padding-bottom:0.75rem; margin-bottom:1rem;">
    <div>
      <span style="font-family:'IBM Plex Mono', monospace; font-size:0.75rem; font-weight:700; color:#38BDF8; letter-spacing:0.05em;">CONFIGURATION EXPERIMENT</span>
      <h3 style="margin:0.2rem 0 0 0; color:#F8FAFC; font-size:1.15rem; font-weight:700;">8051 Timer / Counter Hardware Path</h3>
    </div>
    <span id="tsim-reg-mode-tag" style="font-size:0.75rem; color:#A5B4FC; font-family:'IBM Plex Mono', monospace; background:#1E1B4B; padding:0.25rem 0.6rem; border-radius:4px; border:1px solid #4338CA;">Mode 1: 16-Bit Cascading Counter</span>
  </div>

  <!-- THREE CONFIGURATION CONTROLS -->
  <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap:0.75rem; margin-bottom:1rem;">
    <!-- 1. SOURCE SELECT -->
    <div style="background:#0B1120; border:1px solid #334155; border-radius:6px; padding:0.6rem 0.8rem;">
      <div style="font-size:0.7rem; color:#94A3B8; font-weight:700; margin-bottom:0.4rem; font-family:'IBM Plex Mono', monospace;">1. PULSE SOURCE (C/T bit)</div>
      <div style="display:flex; gap:4px;">
        <button id="tsim-cfg-src-timer" onclick="edgeCaseAction('set_source', 'timer')" style="flex:1; background:#0C4A6E; border:1px solid #38BDF8; color:#fff; font-size:0.75rem; font-family:'IBM Plex Mono', monospace; padding:0.35rem 0.4rem; border-radius:4px; cursor:pointer;">TIMER (Osc/12)</button>
        <button id="tsim-cfg-src-counter" onclick="edgeCaseAction('set_source', 'counter')" style="flex:1; background:#1E293B; border:1px solid #475569; color:#94A3B8; font-size:0.75rem; font-family:'IBM Plex Mono', monospace; padding:0.35rem 0.4rem; border-radius:4px; cursor:pointer;">COUNTER (Pin)</button>
      </div>
    </div>

    <!-- 2. TIMER SELECT -->
    <div style="background:#0B1120; border:1px solid #334155; border-radius:6px; padding:0.6rem 0.8rem;">
      <div style="font-size:0.7rem; color:#94A3B8; font-weight:700; margin-bottom:0.4rem; font-family:'IBM Plex Mono', monospace;">2. TIMER SELECT</div>
      <div style="display:flex; gap:4px;">
        <button id="tsim-cfg-timer-0" onclick="edgeCaseAction('set_timer', 0)" style="flex:1; background:#064E3B; border:1px solid #10B981; color:#fff; font-size:0.75rem; font-family:'IBM Plex Mono', monospace; padding:0.35rem 0.4rem; border-radius:4px; cursor:pointer;">TIMER 0 (T0)</button>
        <button id="tsim-cfg-timer-1" onclick="edgeCaseAction('set_timer', 1)" style="flex:1; background:#1E293B; border:1px solid #475569; color:#94A3B8; font-size:0.75rem; font-family:'IBM Plex Mono', monospace; padding:0.35rem 0.4rem; border-radius:4px; cursor:pointer;">TIMER 1 (T1)</button>
      </div>
    </div>

    <!-- 3. MODE SELECT -->
    <div style="background:#0B1120; border:1px solid #334155; border-radius:6px; padding:0.6rem 0.8rem;">
      <div style="font-size:0.7rem; color:#94A3B8; font-weight:700; margin-bottom:0.4rem; font-family:'IBM Plex Mono', monospace;">3. OPERATING MODE (M1 M0)</div>
      <div style="display:flex; gap:4px;">
        <button id="tsim-cfg-mode-1" onclick="edgeCaseAction('set_mode', 1)" style="flex:1; background:#1E3A8A; border:1px solid #60A5FA; color:#fff; font-size:0.75rem; font-family:'IBM Plex Mono', monospace; padding:0.35rem 0.4rem; border-radius:4px; cursor:pointer;">MODE 1 (16-Bit)</button>
        <button id="tsim-cfg-mode-2" onclick="edgeCaseAction('set_mode', 2)" style="flex:1; background:#1E293B; border:1px solid #475569; color:#94A3B8; font-size:0.75rem; font-family:'IBM Plex Mono', monospace; padding:0.35rem 0.4rem; border-radius:4px; cursor:pointer;">MODE 2 (Auto-Reload)</button>
      </div>
    </div>
  </div>

  <!-- ACTIVE HARDWARE PATH SCHEMATIC BANNER -->
  <div style="background:#0B1120; border-left:3px solid #38BDF8; border-radius:0 6px 6px 0; padding:0.65rem 0.9rem; margin-bottom:1rem; font-family:'IBM Plex Mono', monospace; font-size:0.78rem;">
    <div id="tsim-active-path-label" style="color:#CBD5E1; line-height:1.4;">
      <span style="color:#38BDF8;">INTERNAL CLOCK:</span> 12 MHz Crystal / 12 &rarr; TR0 Run Gate &rarr; TH0:TL0 (16-bit) &rarr; TF0 Overflow &rarr; CPU
    </div>
  </div>

  <!-- ACTION BUTTONS ROW -->
  <div style="display:flex; flex-wrap:wrap; gap:0.5rem; align-items:center; margin-bottom:1.25rem;">
    <button onclick="edgeCaseAction('toggle_run')" id="tsim-btn-run" style="background:#10B981; border:none; color:#0F172A; font-weight:700; padding:0.5rem 1.1rem; border-radius:6px; font-family:'IBM Plex Mono', monospace; font-size:0.85rem; cursor:pointer; transition:all 0.2s;">&#9654; RUN</button>
    <button onclick="edgeCaseAction('step')" id="tsim-btn-step" style="background:#1E293B; border:1px solid #475569; color:#CBD5E1; padding:0.5rem 0.9rem; border-radius:6px; font-family:'IBM Plex Mono', monospace; font-size:0.85rem; cursor:pointer;">⏭ STEP (+1)</button>
    <button onclick="edgeCaseAction('reset')" style="background:#1E293B; border:1px solid #475569; color:#CBD5E1; padding:0.5rem 0.9rem; border-radius:6px; font-family:'IBM Plex Mono', monospace; font-size:0.85rem; cursor:pointer;">↺ RESET</button>
    
    <!-- External Pulse Generator (Active in Counter Mode) -->
    <button onclick="edgeCaseAction('pulse_pin')" id="tsim-btn-ext-pulse" style="display:none; background:#78350F; border:1px solid #F59E0B; color:#FDE68A; font-weight:700; padding:0.5rem 1rem; border-radius:6px; font-family:'IBM Plex Mono', monospace; font-size:0.85rem; cursor:pointer; box-shadow:0 0 10px rgba(245,158,11,0.25);">
      &#9889; PULSE EXTERNAL PIN P3.4 (T0)
    </button>

    <!-- Presets -->
    <div style="display:flex; gap:4px; margin-left:auto;">
      <span style="font-size:0.75rem; color:#64748B; align-self:center; margin-right:4px;">Presets:</span>
      <button onclick="edgeCaseAction('preset_overflow')" style="background:#1E293B; border:1px solid #38BDF8; color:#38BDF8; padding:0.4rem 0.6rem; border-radius:4px; font-family:'IBM Plex Mono', monospace; font-size:0.75rem; cursor:pointer;">Near Overflow</button>
      <button onclick="edgeCaseAction('preset_mid')" style="background:#1E293B; border:1px solid #475569; color:#94A3B8; padding:0.4rem 0.6rem; border-radius:4px; font-family:'IBM Plex Mono', monospace; font-size:0.75rem; cursor:pointer;">Mid-Scale</button>
    </div>
  </div>

  <!-- 3-STAGE PIPELINE CARDS -->
  <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(260px, 1fr)); gap:1rem; margin-bottom:1.25rem;">
    
    <!-- STAGE 1: HARDWARE COUNTING REGISTERS -->
    <div style="background:#0B1120; border:1.5px solid #10B981; border-radius:8px; padding:1rem;">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.5rem;">
        <span style="font-family:'IBM Plex Mono', monospace; font-size:0.75rem; font-weight:700; color:#34D399;">[1. HARDWARE COUNTER]</span>
        <div id="tsim-pulse-led" style="width:10px; height:10px; border-radius:50%; background:#334155; transition:all 0.1s;"></div>
      </div>

      <!-- Registers display -->
      <div style="display:flex; gap:8px; margin-bottom:0.6rem;">
        <div style="flex:1; background:#0F172A; border:1px solid #1E293B; border-radius:4px; padding:0.4rem; text-align:center;">
          <div id="tsim-lbl-th" style="font-size:0.65rem; color:#94A3B8;">TH0 (8CH) [HIGH BYTE]</div>
          <div id="tsim-val-th" style="font-family:'IBM Plex Mono', monospace; font-size:1.15rem; color:#38BDF8; font-weight:700;">00H</div>
        </div>
        <div style="flex:1; background:#0F172A; border:1px solid #1E293B; border-radius:4px; padding:0.4rem; text-align:center;">
          <div id="tsim-lbl-tl" style="font-size:0.65rem; color:#94A3B8;">TL0 (8AH) [LOW BYTE]</div>
          <div id="tsim-val-tl" style="font-family:'IBM Plex Mono', monospace; font-size:1.15rem; color:#34D399; font-weight:700;">00H</div>
        </div>
      </div>

      <!-- Progress bar -->
      <div style="background:#1E293B; height:6px; border-radius:3px; overflow:hidden;">
        <div id="tsim-prog-bar" style="background:#10B981; width:0%; height:100%; transition:width 0.1s;"></div>
      </div>
      <div style="display:flex; justify-content:space-between; font-size:0.65rem; color:#64748B; margin-top:0.3rem;">
        <span id="tsim-count-display" style="font-family:'IBM Plex Mono', monospace; color:#F8FAFC; font-weight:600;">0000H (0 / 65535)</span>
        <span>OVERFLOW</span>
      </div>

      <div style="margin-top:0.75rem; padding-top:0.5rem; border-top:1px solid #1E293B; display:flex; justify-content:space-between; align-items:center;">
        <span style="font-size:0.7rem; color:#94A3B8;">Overflow Flag:</span>
        <span id="tsim-tf-badge" style="font-family:'IBM Plex Mono', monospace; font-size:0.75rem; font-weight:700; color:#64748B; padding:0.15rem 0.5rem; border-radius:4px; background:#0F172A;">TF0 = 0 (IDLE)</span>
      </div>
    </div>

    <!-- STAGE 2: CPU / SOFTWARE RESPONSE -->
    <div style="background:#0B1120; border:1.5px solid #F59E0B; border-radius:8px; padding:1rem; display:flex; flex-direction:column; justify-content:space-between;">
      <div>
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.5rem;">
          <span style="font-family:'IBM Plex Mono', monospace; font-size:0.75rem; font-weight:700; color:#FCD34D;">[2. CPU / SOFTWARE]</span>
          <span style="font-size:0.65rem; color:#F59E0B; background:#451A03; padding:0.15rem 0.4rem; border-radius:3px; font-weight:600;">CAUSAL BRIDGE</span>
        </div>
        
        <div style="font-size:0.75rem; color:#94A3B8; margin-bottom:0.75rem;">
          Classic 8051 timers do not directly alter GPIO pins. Software detects <code style="color:#F59E0B;">TFx = 1</code> and executes response code.
        </div>

        <div style="background:#0F172A; border:1px solid #334155; border-radius:4px; padding:0.6rem; margin-bottom:0.75rem;">
          <div style="font-size:0.65rem; color:#64748B; margin-bottom:0.25rem;">SIMULATED CPU / ISR ACTION:</div>
          <div id="tsim-cpu-action" style="font-family:'IBM Plex Mono', monospace; font-size:0.78rem; color:#CBD5E1; line-height:1.4;">
            Hardware idle. Press RUN or STEP.
          </div>
        </div>
      </div>

      <div style="font-size:0.7rem; color:#64748B; border-top:1px solid #1E293B; padding-top:0.4rem;">
        Atomic Instructions: <code style="color:#38BDF8;">CPL P1.0</code> | <code style="color:#34D399;">CLR TFx</code>
      </div>
    </div>

    <!-- STAGE 3: PHYSICAL WORLD & WAVEFORM -->
    <div style="background:#0B1120; border:1.5px solid #38BDF8; border-radius:8px; padding:1rem; display:flex; flex-direction:column; justify-content:space-between;">
      <div>
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.5rem;">
          <span style="font-family:'IBM Plex Mono', monospace; font-size:0.75rem; font-weight:700; color:#7DD3FC;">[3. PHYSICAL WORLD]</span>
          <span id="tsim-pin-badge" style="font-family:'IBM Plex Mono', monospace; font-size:0.8rem; font-weight:700; color:#38BDF8;">LOW (0V)</span>
        </div>

        <div style="font-size:0.75rem; color:#94A3B8; margin-bottom:0.5rem;">
          Port 1 Pin 0 Electrical Potential (5V TTL):
        </div>

        <!-- Mini Live Waveform Display -->
        <div style="background:#0F172A; border:1px solid #1E293B; border-radius:4px; height:42px; position:relative; overflow:hidden; display:flex; align-items:center; padding:0 6px;">
          <svg id="tsim-waveform-svg" viewBox="0 0 200 30" width="100%" height="30" preserveAspectRatio="none">
            <polyline id="tsim-wave-line" fill="none" stroke="#10B981" stroke-width="2" points="0,24 200,24" />
          </svg>
        </div>
      </div>

      <div style="font-size:0.7rem; color:#64748B; margin-top:0.5rem;">
        Time has crossed into physical electrical consequence.
      </div>
    </div>

  </div>

  <!-- Narrative Trace -->
  <div id="tsim-narrative" style="background:rgba(15, 23, 42, 0.9); border-left:3px solid #38BDF8; padding:0.8rem 1rem; border-radius:0 6px 6px 0; font-size:0.85rem; color:#CBD5E1; line-height:1.5;">
    <strong style="color:#38BDF8;">EXPERIMENT READY:</strong> Select your configuration choices above, then press <strong>RUN</strong> or <strong>STEP</strong> to watch the hardware path execute.
  </div>
</div>

---

## 9. When Counting Becomes a Waveform

Look closely at what happens when this cycle repeats periodically.

Suppose we configure Timer 0 to overflow every 500 microseconds ($500\ \mu\text{s}$).

Each time `TF0` fires, the CPU service routine inverts Pin P1.0:

```text
First Overflow  (500 µs)   →  CPL P1.0  →  Pin goes HIGH (+5V)
Second Overflow (1000 µs)  →  CPL P1.0  →  Pin goes LOW  (0V)
Third Overflow  (1500 µs)  →  CPL P1.0  →  Pin goes HIGH (+5V)
Fourth Overflow (2000 µs)  →  CPL P1.0  →  Pin goes LOW  (0V)
```

The pin stays HIGH for $500\ \mu\text{s}$ and LOW for $500\ \mu\text{s}$.

The total repetition period is $1000\ \mu\text{s} = 1\text{ millisecond}$.

One millisecond per period equals a frequency of exactly **1,000 Hertz (1 kHz)**.

![From Overflow Event to Physical Waveform](Images/intel_8051_timer_to_waveform.svg)

If you connect an oscilloscope probe to Pin P1.0, you see a pristine square wave.

If you connect that pin to a small piezo speaker, you hear a clean acoustic musical tone.

Think about what has occurred:

Inside silicon, a digital register was quietly incrementing binary numbers on each machine cycle. But through the causal chain of hardware overflow and purposeful software response, that invisible internal counting has become a physical, vibrating electrical wave that radiates into the physical universe.

Time has become a signal.

---

## 10. The Deeper Realization

In [The Architecture of Time](/explorations/the-architecture-of-time/), we saw that time coordination is the foundation of intelligent action. Without a structured clock, a machine is merely reactive; with one, it becomes purposeful.

Here in the 8051, we see how that architecture was made physical.

A timer is not the CPU watching a clock.

It is a piece of hardware that moves on its own.

Software does not count the seconds, microseconds, or machine cycles. Software simply establishes the rules in `TMOD`, loads the starting values into `THx:TLx`, and raises the run gate in `TCON`.

From that instant onward, the machine cycle clock carries the count forward in silence.

And when that quiet internal counting rolls over to alert the CPU and toggle a physical pin, something fundamental has taken place:

An invisible rhythm inside silicon has become a physical signal the outside world can see, hear, and respond to.
"""

target = 'content/explorations/the-8051-when-time-becomes-a-signal.md'
with open(target, 'w', encoding='utf-8') as f:
    f.write(markdown_text)

print("Updated content/explorations/the-8051-when-time-becomes-a-signal.md successfully!")
