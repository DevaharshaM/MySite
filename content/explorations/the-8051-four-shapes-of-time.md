---
id: the-8051-four-shapes-of-time
category: Controller
series: Controller
title: The 8051 — Four Shapes of Time
subtitle: How the mode bits in TMOD reshape the internal counting silicon of the classic 8051.
date: 28 August 2026
tags: [Controller, 8051, Microcontroller, Timers, TMOD, Mode 0, Mode 1, Mode 2, Mode 3, Auto-Reload, Embedded Systems]
footer: Foundational explorations in microcontroller architecture, 8051 systems, and embedded computing — PrajnaEdge.dev
---

## 1. The Switches We Left Behind

In our previous exploration, we watched time turn into a digital signal.

We saw how Intel's architects took the universal grammar of machine timing and carved it into concrete silicon:

```text
Software establishes the rules in TMOD.
The clock supplies the rhythm.
THx and TLx accumulate counts in silence.
TCON presents the live control levers.
```

By delegating the mechanical accumulation of machine cycles to autonomous hardware, the central processor was freed from the blind spin of software delay loops. Time became an observable hardware event.

Yet in establishing that foundation, we deliberately left two control switches untouched.

Inside the `TMOD` register, tucked neatly into each four-bit control group, sit two mode bits:

```text
TMOD (89H)
  ├── Bit 1, Bit 0  →  M1, M0 for Timer 0
  └── Bit 5, Bit 4  →  M1, M0 for Timer 1
```

![The TMOD Mode Selector and Four Internal Topologies](Images/intel_8051_tmod_mode_bits_overview.svg)

We saw where these bits were located on the machine's control surface. Now we turn them.

In a modern textbook, `M1` and `M0` are usually dismissed in a dry, four-row reference table. The reader memorizes four mode numbers, passes an examination, and moves on without ever realizing what actually occurred.

What actually changes when the mode bits change?

The microcontroller does not possess four separate physical timers. It possesses one shared bank of counting flip-flops and bus gates. When software writes a new bit pattern into `M1` and `M0`, it does not merely select a software setting. It steers internal silicon multiplexers, re-routes carry lines, and reorganizes the physical relationship between `THx` and `TLx`.

One piece of silicon takes four distinct hardware shapes.

---

## 2. Mode 0 — When 16 Bits Become 13

When both mode bits are cleared to zero (`M1 = 0`, `M0 = 0`), the 8051 enters Mode 0.

At first glance, the architecture appears strange:

```text
MODE 0: 13-BIT TIMER / COUNTER
  THx  →  8 bits  (Bits 7..0)
  TLx  →  5 bits  (Bits 4..0 only)
  Total Capacity: 2^13 = 8,192 counts (0000H → 1FFFH)
```

The machine provides two full eight-bit Special Function Registers in the memory map—`THx` at `8CH`/`8DH` and `TLx` at `8AH`/`8BH`. Yet in Mode 0, only thirteen of those sixteen flip-flops participate in the counting chain.

![Mode 0: The 13-Bit Hardware Structure](Images/intel_8051_timer_mode_0_13bit.svg)

Here is how the silicon is wired:

Input pulses (derived either from the internal machine cycle clock `Osc ÷ 12` or an external pin) flow through the `TRx` run switch directly into `TLx`. But they do not count through all eight bits. Only the lower five bits—`D0`, `D1`, `D2`, `D3`, and `D4`—participate.

These five bits form an internal prescaler capable of counting from `0` to `31` (`00H` to `1FH`). The upper three bits of `TLx` (`D5`, `D6`, `D7`) are physically bypassed by the carry chain. Software can read them or write them, but incoming clock ticks never increment them.

When the lower five bits reach `1FH` (31 decimal) and receive the 32nd pulse, bit 4 rolls over to zero. That rollover pulse does not spill into bit 5; instead, internal silicon steers the overflow signal directly into bit 0 of `THx`.

`THx` then behaves as a full eight-bit counter, accumulating counts from `0` to `255`.

When `THx` reaches `FFH` and the five-bit prescaler in `TLx` reaches `1FH`, the total thirteen-bit register pair holds `1FFFH` (8,191 counts). The very next tick causes a complete rollover:

```text
1FFFH  +  1  ───►  0000H  ───►  Hardware asserts TFx = 1
```

Why would Intel build a 13-bit timer into a modern 8-bit microcontroller?

The answer is historical lineage. Before the 8051 became the industry standard, Intel's dominant microcontroller family was the MCS-48 (the 8048). The 8048 featured a hardware timer built with an internal 5-bit prescaler feeding an 8-bit counter. When developing the 8051, the architects needed to ensure that existing MCS-48 embedded applications could be ported to the new machine with identical timing intervals and minimal rewrite.

Mode 0 is not a technical compromise; it is an architectural bridge to the past. The physical registers exist in full, but the internal routing rewires them to emulate an earlier machine.

---

## 3. Mode 1 — The Full 16-Bit Counter

When the mode bits are set to `M1 = 0` and `M0 = 1`, the timer assumes its cleanest, most natural form: Mode 1.

All sixteen bits are unlocked.

```text
MODE 1: 16-BIT CASCADED COUNTER
  THx (High Byte) : TLx (Low Byte)
  Total Capacity: 2^16 = 65,536 counts (0000H → FFFFH)
```

![Mode 1: The Full 16-Bit Cascaded Counter](Images/intel_8051_timer_mode_1_16bit.svg)

In this mode, all eight bits of `TLx` are active. Incoming pulses increment `TLx` from `00H` up to `FFH` (0 to 255 counts). On the 256th tick, `TLx` rolls over from `FFH` to `00H` and sends a carry pulse directly into bit 0 of `THx`.

`THx` accumulates these carries, incrementing once every 256 input cycles.

Together, `THx` and `TLx` form a unified 16-bit up-counter capable of recording 65,536 continuous states:

```text
0000H  ──►  0001H  ──►  ...  ──►  FFFFH  ──►  0000H (TFx asserted)
```

At a standard crystal frequency of 12 MHz, one machine cycle equals exactly 1 µs. In Mode 1, the timer can measure any duration from 1 µs up to:

```text
65,536 × 1 µs = 65,536 µs = 65.536 ms
```

To measure a specific interval—say, 50,000 µs (50 ms)—software does not start the counter at zero. Instead, it calculates the pre-load offset:

```text
Starting Count = 65,536 − 50,000 = 15,536 = 3CB0H
```

Software writes `3CH` into `TH0` and `B0H` into `TL0`, then sets `TR0 = 1`. The counter increments 50,000 times, arrives at `FFFFH`, rolls over to `0000H`, and immediately raises `TF0 = 1`.

Mode 1 offers the widest dynamic range in the classic 8051 architecture. But it carries a hidden architectural price:

The moment the counter rolls over and raises `TFx`, `THx:TLx` sits at `0000H`. If the application requires a repeating 50 ms tick, software must intervene: an Interrupt Service Routine (ISR) or polling loop must catch the flag, halt the timer, reload `3CB0H` back into the registers, and restart counting.

In high-speed communication or precise frequency synthesis, that software reload delay introduces a fatal flaw: timing jitter. Every instruction the CPU takes to respond to the interrupt pushes the reload later into the future.

The architects knew this. And for that reason, they built a third shape.

---

## 4. Mode 2 — When the Count Comes Back

When the mode bits are set to `M1 = 1` and `M0 = 0`, the timer hardware undergoes its most significant operational transformation: 8-bit Auto-Reload.

In Mode 2, `THx` stops counting entirely.

```text
MODE 2: 8-BIT AUTO-RELOAD
  TLx  →  Active 8-bit Counter (Counts from reload value to FFH)
  THx  →  Static Reload Latch   (Preserves baseline count in silicon)
```

![Mode 2: The 8-Bit Auto-Reload Architecture](Images/intel_8051_timer_mode_2_auto_reload.svg)

The division of labor is radical:

`TLx` is the only register that receives clock pulses. It increments through its eight bits: `00H` up toward `FFH`.

`THx`, meanwhile, is treated by the hardware as an immutable holding pen. Software writes a byte into `THx` during initialization—for instance, `FDH`. Counting pulses do not alter `THx`. It sits silently in the upper data space, holding its value like a physical stencil.

Now observe what happens on overflow.

When `TLx` reaches `FFH` and receives the next tick:

```text
1. TLx rolls over: FFH → 00H
2. Hardware sets the overflow flag: TFx = 1 (in TCON)
3. Dedicated silicon bus lines instantly copy the contents of THx into TLx
```

All three actions happen simultaneously on the exact same clock edge.

```text
       ┌───────────────┐
       │   THx (FDH)   │  ◄── Preserved baseline value
       └───────┬───────┘
               │  Hardware Auto-Reload Path (Instantaneous)
               ▼
       ┌───────────────┐
Pulses │   TLx (FDH)   │ ──► Counts to FFH ──► Rollover ──► Sets TFx
──────►│               │                       │
       └───────────────┘                       │
               ▲                               │
               └───────────────────────────────┘
```

The timer does not wait for the CPU. It does not generate an interrupt and beg software to reload its starting number. The silicon hardware reloads itself.

Because the reload occurs in hardware without executing a single instruction, the period between successive overflows is mathematically exact:

```text
Reload Value FDH (253 decimal)
Capacity = 256 − 253 = 3 machine cycles
Every 3 µs, like clockwork, TFx pulses and TLx reloads.
```

There is zero software latency. Zero timing jitter. Even if the CPU is locked in a long multiplication instruction or servicing an unrelated high-priority interrupt, the timer continues to pulse with crystal precision.

This is why Mode 2 is the beating heart of serial communications in the 8051. When the serial port (UART) needs to transmit bits at exactly 9600 baud, Timer 1 is configured in Mode 2. Its overflow pulses drive the baud rate clock automatically, perfectly synchronized, day after day, without the CPU ever writing to `TL1` again.

Hardware remembers the count so software doesn't have to.

---

## 5. Mode 3 — When One Timer Becomes Two

Mode 3 (`M1 = 1`, `M0 = 1`) is the most surprising architectural shape in the microcontroller.

In Mode 3, the timer does not merely change its bit width or enable a reload latch. Timer 0 physically splits into two completely separate eight-bit timers.

```text
MODE 3: SPLIT TIMER 0
  TL0  →  Independent 8-bit Timer / Counter
  TH0  →  Independent 8-bit Timer (Machine Cycles only)
```

![Mode 3: Split Timer 0 Architecture](Images/intel_8051_timer_mode_3_split.svg)

Consider the physical problem Intel's engineers faced:

An 8051 chip has only two hardware timers: Timer 0 and Timer 1. Suppose a design requires Timer 1 to run continuously as a baud rate generator for the serial port. That leaves the engineer with only one timer—Timer 0—to handle all application intervals, debounce delays, periodic sensor sampling, and waveforms. If the application needs two independent periodic events, the system would run out of timers.

Mode 3 solves this by splitting Timer 0 in two:

### 1. The Lower Half: TL0
`TL0` becomes an independent 8-bit timer/counter (`00H` to `FFH`, 256 counts). It retains all of Timer 0's normal control mechanisms:
- Clock source can be internal machine cycles or external pin `T0` (selected by `C/T0` in `TMOD`).
- Gating is controlled by `GATE0` and pin `INT0`.
- Running is controlled by `TR0` (`TCON.4`).
- Overflow raises `TF0` (`TCON.5`), vectoring to the standard Timer 0 interrupt vector at `000BH`.

### 2. The Upper Half: TH0
`TH0` also becomes an independent 8-bit timer (`00H` to `FFH`, 256 counts). But notice: `TH0` is an 8-bit register that now needs its own run switch and its own overflow flag. Where does it get them?

It commandeers them from Timer 1!

In Mode 3, `TH0` borrows:
- `TR1` (`TCON.6`) as its run switch. Setting `TR1 = 1` starts `TH0`; clearing `TR1 = 0` stops `TH0`.
- `TF1` (`TCON.7`) as its overflow flag. When `TH0` rolls over from `FFH` to `00H`, it asserts `TF1 = 1`, vectoring to the Timer 1 interrupt vector at `001BH`.

`TH0` is strictly an internal timer—its counting pulses come exclusively from the machine cycle clock (`Osc ÷ 12`). It cannot count external pin pulses.

### What Happens to Timer 1?
Because `TH0` has hijacked `TR1` and `TF1`, what happens to Timer 1?

Timer 1 has lost its run bit and its interrupt flag. But its counting registers—`TH1` and `TL1`—are still fully alive!

Timer 1 can still be configured in Mode 0, Mode 1, or Mode 2 via `TMOD`. It turns on and begins counting the moment it is switched into any mode other than Mode 3. However, because it has no `TF1` flag to generate interrupts, it cannot alert the CPU when it overflows.

And that turns out to be an ingenious design pairing:

Timer 1 does not need interrupts when serving as the serial port's baud rate generator! In serial communication, Timer 1's overflow output is wired internally to the UART shift clock. It never needs to interrupt the CPU.

By placing Timer 0 in Mode 3 and Timer 1 in Mode 2, the engineer effectively extracts **three hardware timing resources** out of two physical timers:
1. `TL0`: An independent 8-bit timer or event counter with interrupt `TF0`.
2. `TH0`: A second independent 8-bit timer with interrupt `TF1`.
3. `Timer 1`: An autonomous baud-rate clock generator running silently in the background.

What if Timer 1 itself is placed into Mode 3?

In classic 8051 hardware, setting Timer 1's mode bits to `M1 = 1, M0 = 1` simply halts Timer 1. Its clock input is disconnected, and the registers hold their values frozen. Mode 3 is a specialized capability belonging fundamentally to Timer 0.

---

## 6. One Piece of Silicon, Four Internal Topologies

Now we can look at the complete architecture as a single coherent system.

The mode bits `M1` and `M0` are not software flags checked by a firmware interpreter. They are electrical control lines routed straight to silicon switches inside the timer block.

![One Silicon Register Pair, Four Internal Topologies](Images/intel_8051_four_modes_comparison.svg)

The physical silicon contains sixteen flip-flops for Timer 0 and sixteen flip-flops for Timer 1. But depending on two bits in `TMOD`, those thirty-two flip-flops re-wire themselves into an MCS-48 emulator, a wide-range 16-bit accumulator, an unassisted periodic oscillator, or a partitioned dual-timer complex.

---

## 7. EdgeCase — Turn the Hardware Switches

Here we can open the timer and observe how the silicon transforms in real time.

In the interactive workbench below, you are not running a software delay loop. You are directly manipulating the configuration switches of the 8051 timer architecture.

Choose the **Timer** (`Timer 0` or `Timer 1`), select the **Pulse Source** (`Internal Timer` via `Osc ÷ 12` or `External Counter` via pins `T0`/`T1`), and select the **Internal Mode** (`Mode 0`, `Mode 1`, `Mode 2`, or `Mode 3`).

Notice how the live `TMOD` byte updates, how the internal signal path changes, and how the register flip-flops respond when pulses arrive.

```html
<div id="four-shapes-edgecase-root" style="background:#0F172A; border:1px solid #334155; border-radius:10px; padding:1.5rem; margin:2rem 0; color:#E2E8F0; font-family:'DM Sans', sans-serif;">
  
  <!-- WORKBENCH HEADER -->
  <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:1rem; border-bottom:1px solid #334155; padding-bottom:1rem; margin-bottom:1.5rem;">
    <div>
      <div style="font-family:'Syne', sans-serif; font-size:1.15rem; font-weight:700; color:#F8FAFC; letter-spacing:0.02em;">
        EDGECASE: TURN THE HARDWARE SWITCHES
      </div>
      <div style="font-size:0.85rem; color:#94A3B8; margin-top:0.25rem;">
        Interactive 8051 Silicon Topologies &bull; Live Register Wiring Simulator
      </div>
    </div>
    <div style="display:flex; align-items:center; gap:0.5rem; background:#1E293B; padding:0.4rem 0.8rem; border-radius:6px; border:1px solid #475569;">
      <span style="font-size:0.75rem; color:#94A3B8; font-weight:600;">ACTIVE TMOD:</span>
      <span id="tsim-tmod-hex" style="font-family:'IBM Plex Mono', monospace; font-size:0.95rem; font-weight:700; color:#38BDF8;">01H</span>
    </div>
  </div>

  <!-- CONTROL DECK -->
  <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(260px, 1fr)); gap:1rem; margin-bottom:1.5rem;">
    
    <!-- 1. TIMER SELECTION -->
    <div style="background:#1E293B; padding:0.85rem; border-radius:8px; border:1px solid #334155;">
      <div style="font-size:0.75rem; font-weight:700; color:#94A3B8; letter-spacing:0.05em; margin-bottom:0.5rem;">1. SELECT TIMER PERIPHERAL</div>
      <div style="display:flex; gap:0.5rem;">
        <button id="tsim-btn-timer-0" onclick="window.edgeCaseAction('set_timer', 0)" style="flex:1; padding:0.5rem; font-size:0.8rem; font-weight:600; border-radius:6px; cursor:pointer; background:#064E3B; border:1.5px solid #10B981; color:#FFFFFF; transition:all 0.2s;">
          Timer 0 (TL0/TH0)
        </button>
        <button id="tsim-btn-timer-1" onclick="window.edgeCaseAction('set_timer', 1)" style="flex:1; padding:0.5rem; font-size:0.8rem; font-weight:600; border-radius:6px; cursor:pointer; background:#1E293B; border:1.5px solid #475569; color:#94A3B8; transition:all 0.2s;">
          Timer 1 (TL1/TH1)
        </button>
      </div>
    </div>

    <!-- 2. SOURCE SELECTION (C/T Bit) -->
    <div style="background:#1E293B; padding:0.85rem; border-radius:8px; border:1px solid #334155;">
      <div style="font-size:0.75rem; font-weight:700; color:#94A3B8; letter-spacing:0.05em; margin-bottom:0.5rem;">2. CLOCK SOURCE (C/T BIT)</div>
      <div style="display:flex; gap:0.5rem;">
        <button id="tsim-btn-src-timer" onclick="window.edgeCaseAction('set_source', 'timer')" style="flex:1; padding:0.5rem; font-size:0.8rem; font-weight:600; border-radius:6px; cursor:pointer; background:#0C4A6E; border:1.5px solid #38BDF8; color:#FFFFFF; transition:all 0.2s;">
          Timer (Osc &divide; 12)
        </button>
        <button id="tsim-btn-src-counter" onclick="window.edgeCaseAction('set_source', 'counter')" style="flex:1; padding:0.5rem; font-size:0.8rem; font-weight:600; border-radius:6px; cursor:pointer; background:#1E293B; border:1.5px solid #475569; color:#94A3B8; transition:all 0.2s;">
          Counter (Pin T0/T1)
        </button>
      </div>
    </div>

  </div>

  <!-- 3. MODE SELECTION (M1, M0 Bits) -->
  <div style="background:#1E293B; padding:0.85rem; border-radius:8px; border:1px solid #334155; margin-bottom:1.5rem;">
    <div style="font-size:0.75rem; font-weight:700; color:#94A3B8; letter-spacing:0.05em; margin-bottom:0.5rem;">3. INTERNAL TOPOLOGY (M1, M0 BITS IN TMOD)</div>
    <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(180px, 1fr)); gap:0.5rem;">
      <button id="tsim-btn-mode-0" onclick="window.edgeCaseAction('set_mode', 0)" style="padding:0.6rem 0.4rem; font-size:0.8rem; font-weight:600; border-radius:6px; cursor:pointer; background:#1E293B; border:1.5px solid #475569; color:#94A3B8; transition:all 0.2s; text-align:center;">
        <div>Mode 0 (0 0)</div>
        <div style="font-size:0.7rem; font-weight:normal; opacity:0.8; margin-top:2px;">13-Bit Counter</div>
      </button>
      <button id="tsim-btn-mode-1" onclick="window.edgeCaseAction('set_mode', 1)" style="padding:0.6rem 0.4rem; font-size:0.8rem; font-weight:600; border-radius:6px; cursor:pointer; background:#1E3A8A; border:1.5px solid #60A5FA; color:#FFFFFF; transition:all 0.2s; text-align:center;">
        <div>Mode 1 (0 1)</div>
        <div style="font-size:0.7rem; font-weight:normal; opacity:0.8; margin-top:2px;">16-Bit Cascaded</div>
      </button>
      <button id="tsim-btn-mode-2" onclick="window.edgeCaseAction('set_mode', 2)" style="padding:0.6rem 0.4rem; font-size:0.8rem; font-weight:600; border-radius:6px; cursor:pointer; background:#1E293B; border:1.5px solid #475569; color:#94A3B8; transition:all 0.2s; text-align:center;">
        <div>Mode 2 (1 0)</div>
        <div style="font-size:0.7rem; font-weight:normal; opacity:0.8; margin-top:2px;">8-Bit Auto-Reload</div>
      </button>
      <button id="tsim-btn-mode-3" onclick="window.edgeCaseAction('set_mode', 3)" style="padding:0.6rem 0.4rem; font-size:0.8rem; font-weight:600; border-radius:6px; cursor:pointer; background:#1E293B; border:1.5px solid #475569; color:#94A3B8; transition:all 0.2s; text-align:center;">
        <div>Mode 3 (1 1)</div>
        <div style="font-size:0.7rem; font-weight:normal; opacity:0.8; margin-top:2px;">Split Timer</div>
      </button>
    </div>
  </div>

  <!-- LIVE TMOD BITFIELD BAR -->
  <div style="background:#0B1120; border:1px solid #334155; border-radius:8px; padding:0.8rem 1rem; margin-bottom:1.5rem;">
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.5rem; font-size:0.75rem; color:#94A3B8;">
      <span>TMOD REGISTER BITS (89H)</span>
      <span id="tsim-tmod-summary" style="font-family:'IBM Plex Mono', monospace; color:#38BDF8;">Timer 0: Mode 1 (16-bit) &bull; C/T=0</span>
    </div>
    <div style="display:grid; grid-template-columns:repeat(8, 1fr); gap:4px; text-align:center; font-family:'IBM Plex Mono', monospace;">
      <!-- Timer 1 Nibble (Bits 7..4) -->
      <div id="tmod-bit-7" style="background:#1E293B; padding:4px; border-radius:4px; border:1px solid #334155;"><div style="font-size:0.65rem; color:#64748B;">GATE1</div><div style="font-size:0.85rem; font-weight:700; color:#94A3B8;">0</div></div>
      <div id="tmod-bit-6" style="background:#1E293B; padding:4px; border-radius:4px; border:1px solid #334155;"><div style="font-size:0.65rem; color:#64748B;">C/T1</div><div style="font-size:0.85rem; font-weight:700; color:#94A3B8;">0</div></div>
      <div id="tmod-bit-5" style="background:#1E293B; padding:4px; border-radius:4px; border:1px solid #334155;"><div style="font-size:0.65rem; color:#64748B;">M1</div><div style="font-size:0.85rem; font-weight:700; color:#94A3B8;">0</div></div>
      <div id="tmod-bit-4" style="background:#1E293B; padding:4px; border-radius:4px; border:1px solid #334155;"><div style="font-size:0.65rem; color:#64748B;">M0</div><div style="font-size:0.85rem; font-weight:700; color:#94A3B8;">0</div></div>
      <!-- Timer 0 Nibble (Bits 3..0) -->
      <div id="tmod-bit-3" style="background:#1E293B; padding:4px; border-radius:4px; border:1px solid #334155;"><div style="font-size:0.65rem; color:#64748B;">GATE0</div><div style="font-size:0.85rem; font-weight:700; color:#94A3B8;">0</div></div>
      <div id="tmod-bit-2" style="background:#1E293B; padding:4px; border-radius:4px; border:1px solid #334155;"><div style="font-size:0.65rem; color:#64748B;">C/T0</div><div id="val-tmod-ct0" style="font-size:0.85rem; font-weight:700; color:#38BDF8;">0</div></div>
      <div id="tmod-bit-1" style="background:#0C4A6E; padding:4px; border-radius:4px; border:1.5px solid #38BDF8;"><div style="font-size:0.65rem; color:#7DD3FC;">M1</div><div id="val-tmod-m1" style="font-size:0.85rem; font-weight:700; color:#38BDF8;">0</div></div>
      <div id="tmod-bit-0" style="background:#0C4A6E; padding:4px; border-radius:4px; border:1.5px solid #38BDF8;"><div style="font-size:0.65rem; color:#7DD3FC;">M0</div><div id="val-tmod-m0" style="font-size:0.85rem; font-weight:700; color:#38BDF8;">1</div></div>
    </div>
  </div>

  <!-- DYNAMIC SILICON TOPOLOGY DIAGRAM -->
  <div style="background:#0B1120; border:1.5px solid #38BDF8; border-radius:8px; padding:1.25rem; margin-bottom:1.5rem;">
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.75rem;">
      <span style="font-size:0.75rem; font-weight:700; color:#38BDF8; letter-spacing:0.05em;">ACTIVE SILICON SIGNAL FLOW</span>
      <span id="tsim-pulse-indicator" style="display:inline-flex; align-items:center; gap:6px; font-size:0.75rem; color:#94A3B8;">
        <span id="tsim-pulse-led" style="display:inline-block; width:8px; height:8px; border-radius:50%; background:#334155; transition:background 0.08s;"></span>
        PULSE TICK
      </span>
    </div>
    
    <div id="tsim-topology-view" style="min-height:90px; display:flex; align-items:center; justify-content:center;">
      <!-- Dynamic SVG or DOM Topology injected by script -->
    </div>

    <!-- Active Hardware Path Label -->
    <div id="tsim-path-description" style="margin-top:0.75rem; font-size:0.8rem; color:#CBD5E1; line-height:1.5; text-align:center; padding:0.4rem; background:#1E293B; border-radius:4px;">
      Loading silicon pathway...
    </div>
  </div>

  <!-- REGISTER READOUTS & HARDWARE STATUS -->
  <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(220px, 1fr)); gap:1rem; margin-bottom:1.5rem;">
    
    <!-- HIGH BYTE / RELOAD REGISTER -->
    <div style="background:#1E293B; padding:1rem; border-radius:8px; border:1px solid #334155; position:relative;">
      <div id="tsim-th-label" style="font-size:0.75rem; font-weight:700; color:#94A3B8; margin-bottom:0.25rem;">TH0 REGISTER (8CH)</div>
      <div id="tsim-th-role" style="font-size:0.7rem; color:#60A5FA; margin-bottom:0.5rem;">Cascaded High Byte (Bits 15..8)</div>
      <div style="display:flex; align-items:baseline; justify-content:space-between;">
        <span id="tsim-th-hex" style="font-family:'IBM Plex Mono', monospace; font-size:1.75rem; font-weight:700; color:#F8FAFC;">00H</span>
        <span id="tsim-th-dec" style="font-family:'IBM Plex Mono', monospace; font-size:0.85rem; color:#94A3B8;">Dec: 0</span>
      </div>
    </div>

    <!-- LOW BYTE / ACTIVE COUNTER REGISTER -->
    <div style="background:#1E293B; padding:1rem; border-radius:8px; border:1px solid #334155; position:relative;">
      <div id="tsim-tl-label" style="font-size:0.75rem; font-weight:700; color:#94A3B8; margin-bottom:0.25rem;">TL0 REGISTER (8AH)</div>
      <div id="tsim-tl-role" style="font-size:0.7rem; color:#34D399; margin-bottom:0.5rem;">Active Low Counter (Bits 7..0)</div>
      <div style="display:flex; align-items:baseline; justify-content:space-between;">
        <span id="tsim-tl-hex" style="font-family:'IBM Plex Mono', monospace; font-size:1.75rem; font-weight:700; color:#34D399;">00H</span>
        <span id="tsim-tl-dec" style="font-family:'IBM Plex Mono', monospace; font-size:0.85rem; color:#94A3B8;">Dec: 0</span>
      </div>
    </div>

    <!-- COUNTER PROGRESS & TCON FLAGS -->
    <div style="background:#1E293B; padding:1rem; border-radius:8px; border:1px solid #334155;">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.5rem;">
        <span style="font-size:0.75rem; font-weight:700; color:#94A3B8;">ACCUMULATED STATE</span>
        <span id="tsim-count-state" style="font-family:'IBM Plex Mono', monospace; font-size:0.8rem; font-weight:700; color:#38BDF8;">0 / 65535</span>
      </div>
      <!-- Progress Track -->
      <div style="height:6px; background:#0F172A; border-radius:3px; overflow:hidden; margin-bottom:0.75rem;">
        <div id="tsim-progress-bar" style="width:0%; height:100%; background:linear-gradient(90deg, #38BDF8, #10B981); transition:width 0.1s;"></div>
      </div>
      <!-- TCON Levers -->
      <div style="display:flex; gap:0.5rem; justify-content:space-between;">
        <div id="tsim-tr-flag" style="flex:1; background:#0F172A; padding:4px 6px; border-radius:4px; font-size:0.7rem; text-align:center; color:#64748B;">
          TR0 = 0 (HALTED)
        </div>
        <div id="tsim-tf-flag" style="flex:1; background:#0F172A; padding:4px 6px; border-radius:4px; font-size:0.7rem; text-align:center; color:#64748B; font-weight:600;">
          TF0 = 0 (NO OVERFLOW)
        </div>
      </div>
    </div>

  </div>

  <!-- ACTION CONTROLS -->
  <div style="display:flex; flex-wrap:wrap; gap:0.6rem; margin-bottom:1.5rem;">
    <button id="tsim-btn-run" onclick="window.edgeCaseAction('toggle_run')" style="padding:0.6rem 1.25rem; font-size:0.85rem; font-weight:700; border-radius:6px; cursor:pointer; background:#10B981; border:none; color:#0F172A; transition:all 0.2s;">
      &#9654; RUN CLOCK
    </button>
    <button onclick="window.edgeCaseAction('step')" style="padding:0.6rem 1rem; font-size:0.85rem; font-weight:600; border-radius:6px; cursor:pointer; background:#1E293B; border:1px solid #475569; color:#E2E8F0; transition:all 0.2s;">
      &#9197; STEP 1 TICK
    </button>
    <button id="tsim-btn-ext-pulse" onclick="window.edgeCaseAction('pulse_pin')" style="display:none; padding:0.6rem 1.25rem; font-size:0.85rem; font-weight:700; border-radius:6px; cursor:pointer; background:#D97706; border:1px solid #F59E0B; color:#FFFFFF; transition:all 0.2s;">
      &#9889; TICK EXTERNAL PIN (T0)
    </button>
    <button onclick="window.edgeCaseAction('pulse_burst')" style="padding:0.6rem 1rem; font-size:0.85rem; font-weight:600; border-radius:6px; cursor:pointer; background:#1E293B; border:1px solid #475569; color:#A5B4FC; transition:all 0.2s;">
      &#128640; FAST TICK (+10)
    </button>
    <button onclick="window.edgeCaseAction('preset_overflow')" style="padding:0.6rem 1rem; font-size:0.85rem; font-weight:600; border-radius:6px; cursor:pointer; background:#1E293B; border:1px solid #F59E0B; color:#FBBF24; transition:all 0.2s;">
      &#9193; PRESET NEAR OVERFLOW
    </button>
    <button onclick="window.edgeCaseAction('reset')" style="padding:0.6rem 1rem; font-size:0.85rem; font-weight:600; border-radius:6px; cursor:pointer; background:#1E293B; border:1px solid #475569; color:#94A3B8; margin-left:auto; transition:all 0.2s;">
      &#8634; RESET
    </button>
  </div>

  <!-- HARDWARE REALITY TRACE CONSOLE -->
  <div style="background:#060A13; border:1px solid #1E293B; border-radius:6px; padding:0.85rem 1rem; font-family:'IBM Plex Mono', monospace; font-size:0.8rem; line-height:1.6; color:#94A3B8;">
    <div style="font-size:0.7rem; font-weight:700; color:#64748B; letter-spacing:0.05em; margin-bottom:0.25rem;">HARDWARE SILICON TRACE</div>
    <div id="tsim-trace-log">
      Timer initialized in Mode 1 (16-bit). Machine cycle clock ready. Press <span style="color:#10B981;">RUN CLOCK</span> or <span style="color:#F8FAFC;">STEP 1 TICK</span> to observe register accumulation.
    </div>
  </div>

</div>
```

### The Bits We Haven’t Opened Yet

Look once more at the `TMOD` register.

At the highest bit of each four-bit group—bit 3 for Timer 0, and bit 7 for Timer 1—sits one last control switch: `GATE`.

```text
TMOD (89H)
  ├── Bit 3  →  GATE for Timer 0
  └── Bit 7  →  GATE for Timer 1
```

Until now, starting and stopping the counter seemed to belong entirely to software. When `GATE = 0`, the timer behaves normally: software sets `TRx = 1` to begin counting, and clears `TRx = 0` to halt it. The processor holds the switch.

When `GATE = 1`, however, the architecture introduces a second condition.

The timer is no longer allowed to run merely because software set `TRx = 1`. In hardware, the run signal is routed through an internal AND gate that combines the software enable bit with an external physical pin:

```text
Timer 0 Clock Gate  =  TR0  AND  INT0 (P3.2)
Timer 1 Clock Gate  =  TR1  AND  INT1 (P3.3)
```

The timer can advance only when **both** conditions are true at the same physical instant:
- `TRx = 1` in software, and
- The corresponding external pin—`INT0` (`P3.2`) for Timer 0, or `INT1` (`P3.3`) for Timer 1—is held **HIGH**.

If the external pin falls `LOW`, the clock input disconnects immediately, freezing the count regardless of the state of `TRx`.

This is a fundamental shift in authority. By setting `GATE = 1`, software does not retain sole control over time. It delegates the gating of the clock to the physical world outside the chip. Software can prime the timer and walk away; the arrival of an external voltage pulse starts the count, and the falling edge stops it.

The machine has turned its timer into an autonomous hardware stopwatch—measuring the exact width of an external electrical pulse down to the microsecond, without the CPU ever having to poll a pin.

---

## 8. The Deeper Realization

The classic 8051 did not build four separate timers onto its silicon die.

It did not duplicate flip-flops, add redundant adder circuits, or consume precious wafer area with four competing timing mechanisms.

Instead, its architects designed a single, adaptable piece of digital hardware whose internal data paths could be steered by two configuration bits.

Writing to `TMOD` is not an abstract software exercise. When software writes to `M1` and `M0`, it directly controls silicon multiplexers that connect, disconnect, and re-route registers. Two bits decide whether time is measured through thirteen bits, sixteen bits, an automatically reloading eight-bit loop, or two independent partitioned timers.

The machine does not merely execute instructions to count time.

It reshapes how counting happens.
