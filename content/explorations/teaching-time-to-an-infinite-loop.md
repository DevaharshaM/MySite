---
id: teaching-time-to-an-infinite-loop
category: Bare Metal
series: System Explorations
title: Teaching Time to an Infinite Loop
subtitle: How to schedule multiple tasks at predictable intervals without an operating system.
date: 23rd July, 2026
tags: [Bare Metal, Superloop, Timer, Interrupts, Cooperative Scheduler]
closing_heading: The Division of Time
closing_paragraphs:
  - The infinite loop gave the machine repetition. The timer gave that repetition structure, dividing time into predictable intervals.
  - But to make that repetition useful, the machine must also understand its conditions.
closing_quote: A loop without time is a runaway engine. Time gives it a path; state gives it a purpose.
footer: Analyzing bare-metal timers, flag-based superloops, scheduling latency, and cooperative execution models - PrajnaEdge.dev
---

## 1. The Concept of Time

At the end of our previous journey, we watched the processor enter an infinite loop. It was a structural guarantee that the CPU would never run out of instructions. But we also hit a wall: the loop knows how to repeat, but it does not understand time. Consider this basic superloop:

```c
while (1)
{
    ReadSensor();
    UpdateControl();
    RefreshDisplay();
    SendStatus();
}
```

What if the application dictates that `ReadSensor()` must execute every 10 milliseconds, `UpdateControl()` every 20 milliseconds, `RefreshDisplay()` every 100 milliseconds, and `SendStatus()` every 1000 milliseconds? Neither the CPU instruction pipeline nor the while loop has any concept of a millisecond. If we run this loop as-is, it executes as fast as the system clock allows. The tasks run at arbitrary, hardware-dependent rates. To build a reliable machine, we must teach our software how to measure intervals.

## 2. The Tempting Solution: Delay

The most common initial attempt to solve timing is the blocking delay. We insert waiting routines directly into the execution path:

```c
while (1)
{
    ReadSensor();
    DelayMs(100); // Wait 100 ms
    UpdateDisplay();
}
```

During `DelayMs(100)`, the CPU core spins in a dummy loop, burning power while executing instructions that do nothing. The entire foreground execution path is blocked. If we try to schedule multiple tasks with different intervals using this approach, the timing collapses:

```c
while (1)
{
    ReadSensor();
    DelayMs(10);

    UpdateControl();
    DelayMs(20);

    RefreshDisplay();
    DelayMs(100);

    SendStatus();
    DelayMs(1000);
}
```

These delays do not run independently; they accumulate. The actual period between executions of `ReadSensor()` is not 10 milliseconds. It is the sum of all task execution times plus the sum of all delays—a cycle time exceeding 1130 milliseconds. Blocking delays only mean 'do not progress past this line of code for N milliseconds.' They are not a scheduling architecture.

```html
<div style="background:#0F172A; padding:1.5rem; border:1px solid var(--border); border-radius:8px; display:flex; flex-direction:column; align-items:center; margin:2rem 0;">
  <div style="font-family:'Syne',sans-serif; font-size:0.9rem; font-weight:700; color:#fff; margin-bottom:1rem; text-align:center;">ACCUMULATED LATENCY OF BLOCKING DELAYS</div>
  <svg viewBox="0 0 720 160" style="width:100%; height:auto; max-width:640px; font-family:var(--mono);">
    <line x1="10" y1="50" x2="670" y2="50" stroke="rgba(148,163,184,0.2)" stroke-width="2"/>
    <text x="670" y="45" fill="var(--muted)" font-size="8" text-anchor="end">Time &rarr;</text>

    <rect x="10" y="60" width="80" height="25" rx="3" fill="#1E293B" stroke="#3B82F6"/>
    <text x="50" y="76" fill="#E2E8F0" font-size="8" text-anchor="middle">ReadSensor()</text>
    <text x="50" y="100" fill="var(--muted)" font-size="7" text-anchor="middle">T_exec: 2ms</text>

    <rect x="90" y="60" width="70" height="25" rx="3" fill="rgba(239, 104, 104, 0.05)" stroke="#EF6868" stroke-dasharray="3,3"/>
    <text x="125" y="76" fill="#EF6868" font-size="8" text-anchor="middle">DelayMs(10)</text>

    <rect x="160" y="60" width="80" height="25" rx="3" fill="#1E293B" stroke="#3B82F6"/>
    <text x="200" y="76" fill="#E2E8F0" font-size="8" text-anchor="middle">UpdateControl()</text>
    <text x="200" y="100" fill="var(--muted)" font-size="7" text-anchor="middle">T_exec: 4ms</text>

    <rect x="240" y="60" width="110" height="25" rx="3" fill="rgba(239, 104, 104, 0.05)" stroke="#EF6868" stroke-dasharray="3,3"/>
    <text x="295" y="76" fill="#EF6868" font-size="8" text-anchor="middle">DelayMs(20)</text>

    <rect x="350" y="60" width="90" height="25" rx="3" fill="#1E293B" stroke="#3B82F6"/>
    <text x="395" y="76" fill="#E2E8F0" font-size="8" text-anchor="middle">RefreshDisplay()</text>
    <text x="395" y="100" fill="var(--muted)" font-size="7" text-anchor="middle">T_exec: 12ms</text>

    <rect x="440" y="60" width="220" height="25" rx="3" fill="rgba(239, 104, 104, 0.05)" stroke="#EF6868" stroke-dasharray="3,3"/>
    <text x="550" y="76" fill="#EF6868" font-size="8" text-anchor="middle">DelayMs(100)</text>

    <path d="M 10 120 L 10 130 M 10 125 L 660 125 M 660 120 L 660 130" stroke="#E2E8F0" stroke-width="1"/>
    <text x="335" y="142" fill="#E2E8F0" font-size="9" text-anchor="middle" font-weight="bold">Actual Loop Cycle Time = 148 ms (Expected 100 ms max)</text>
  </svg>
  <div style="font-size:0.75rem; color:var(--muted); font-family:var(--mono); margin-top:0.75rem; text-align:center;">Delays stack sequentially, so the actual period of any task is stretched by all other operations and delay cycles in the loop.</div>
</div>
```

Blocking delays are appropriate only in limited situations: initializing a display chip during boot, letting voltage lines settle, or debugging simple single-task setups. In real runtime environments, they paralyze foreground logic.

## 3. The Machine Already Has a Clock

Instead of wasting CPU instruction cycles, we can delegate timekeeping to hardware peripherals. Microcontrollers contain hardware timers. These modules are independent binary counters on the silicon that increment based on a dedicated clock signal, running in parallel with the CPU's execution pipelines.

```html
<div style="background:#0F172A; padding:1.5rem; border:1px solid var(--border); border-radius:8px; display:flex; flex-direction:column; align-items:center; margin:2rem 0;">
  <div style="font-family:'Syne',sans-serif; font-size:0.9rem; font-weight:700; color:#fff; margin-bottom:1rem; text-align:center;">HARDWARE TIMER PERIPHERAL PIPELINE</div>
  <svg viewBox="0 0 680 180" style="width:100%; height:auto; max-width:600px; font-family:var(--mono);">
    <defs>
      <marker id="arrow-green" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
        <path d="M 0 1 L 10 5 L 0 9 z" fill="#10B981"/>
      </marker>
    </defs>

    <rect x="20" y="50" width="100" height="40" rx="5" fill="#1E293B" stroke="#3B82F6" stroke-width="1.5"/>
    <text x="70" y="70" fill="#FFF" font-size="9" text-anchor="middle" font-weight="bold">CLOCK SOURCE</text>
    <text x="70" y="82" fill="var(--muted)" font-size="7" text-anchor="middle">e.g. 16 MHz</text>

    <path d="M 120 70 L 150 70" stroke="#3B82F6" stroke-width="1.5" marker-end="url(#arrow-green)"/>

    <rect x="150" y="50" width="100" height="40" rx="5" fill="#1E293B" stroke="#3B82F6" stroke-width="1.5"/>
    <text x="200" y="70" fill="#FFF" font-size="9" text-anchor="middle" font-weight="bold">PRESCALER</text>
    <text x="200" y="82" fill="var(--muted)" font-size="7" text-anchor="middle">Divide by N (e.g. 16)</text>

    <path d="M 250 70 L 280 70" stroke="#3B82F6" stroke-width="1.5" marker-end="url(#arrow-green)"/>

    <rect x="280" y="50" width="120" height="40" rx="5" fill="#1E293B" stroke="#10B981" stroke-width="1.5"/>
    <text x="340" y="70" fill="#FFF" font-size="9" text-anchor="middle" font-weight="bold">TIMER COUNTER</text>
    <text x="340" y="82" fill="#10B981" font-size="7" text-anchor="middle">Increments (CNT)</text>

    <path d="M 400 70 L 430 70" stroke="#3B82F6" stroke-width="1.5" marker-end="url(#arrow-green)"/>

    <rect x="430" y="50" width="120" height="40" rx="5" fill="#1E293B" stroke="#3B82F6" stroke-width="1.5"/>
    <text x="490" y="70" fill="#FFF" font-size="9" text-anchor="middle" font-weight="bold">COMPARE REG</text>
    <text x="490" y="82" fill="var(--muted)" font-size="7" text-anchor="middle">Target Value (ARR)</text>

    <path d="M 340 90 L 340 120 L 490 120 L 490 90" fill="none" stroke="#E2E8F0" stroke-width="1" stroke-dasharray="2,2"/>
    <text x="415" y="115" fill="#E2E8F0" font-size="7" text-anchor="middle">Continuous hardware comparison: CNT == ARR?</text>

    <path d="M 550 70 L 580 70" stroke="#10B981" stroke-width="1.5" marker-end="url(#arrow-green)"/>

    <rect x="580" y="45" width="80" height="50" rx="5" fill="#1E293B" stroke="#EF6868" stroke-width="1.5"/>
    <text x="620" y="65" fill="#EF6868" font-size="9" text-anchor="middle" font-weight="bold">INTERRUPT</text>
    <text x="620" y="75" fill="#EF6868" font-size="9" text-anchor="middle" font-weight="bold">EVENT</text>
    <text x="620" y="87" fill="var(--muted)" font-size="6" text-anchor="middle">Triggers ISR</text>
  </svg>
  <div style="font-size:0.75rem; color:var(--muted); font-family:var(--mono); margin-top:0.75rem; text-align:center;">The hardware timer counts clock pulses independently of the CPU core instruction pipeline.</div>
</div>
```

Consider a simple configuration: an input clock of 1 MHz. If we set the timer's prescaler to 1, the counter increments every 1 microsecond. If we set a target compare register value of 1000, a comparator on the silicon triggers a compare match event exactly every 1000 counts—representing a precise 1 millisecond interval.

## 4. The Hidden Connection: The Architecture of Time

<span style="display:inline-block; border-left: 2px solid var(--blue); padding-left: 0.75rem; margin: 0.5rem 0; font-style: italic; color: var(--muted);">We have encountered this hardware before. In [The Architecture of Time](the-architecture-of-time), we explored what happens when timers themselves reach their limits — overflow, wraparound, and the edge cases hidden inside measuring time. Here, we are looking at the same hardware from another direction. Not how time can fail, but how time can organize software.</span>

## 5. Creating a System Tick

By configuring a hardware timer to assert an interrupt line at a periodic rate, we establish a software timebase—a system tick. Every tick, the CPU jumps to the interrupt vector to increment a global counter:

```c
volatile uint32_t system_ticks = 0;

void Timer_IRQHandler(void)
{
    system_ticks++;
}
```

If the timer is configured to interrupt every 1 millisecond, then `system_ticks` increments 1000 times a second. An elapsed tick count of 10 corresponds to 10 milliseconds, and 1000 ticks represents 1 second. This global tick is the heartbeat of the system.

## 6. Avoid ISR Bloat

Since we have a periodic timer interrupt, it is tempting to run our task logic directly inside the ISR:

```c
void Timer_IRQHandler(void)
{
    ReadSensor();
    UpdateControl();
    RefreshDisplay();
    SendStatus();
}
```

This is a dangerous anti-pattern. While this code runs at precise intervals, it executes inside the high-priority interrupt context. If the display refresh or status transmission takes longer than 1 millisecond, the ISR will not complete before the next timer interrupt triggers. The system crashes or locks up. Foreground execution is starved, other interrupts are blocked, and real-time promises fail.

## 7. Flags: Turning Time Into Events

To keep the interrupt context lean, we use flags. The background ISR handles the timing calculations, sets boolean indicators when tasks become due, and yields control immediately. The heavy application execution is performed inside the foreground superloop:

```c
volatile bool task_10ms = false;
volatile bool task_100ms = false;
volatile bool task_1000ms = false;

void Timer_IRQHandler(void)
{
    static uint32_t tick = 0;
    tick++;

    if ((tick % 10) == 0)   task_10ms = true;
    if ((tick % 100) == 0)  task_100ms = true;
    if ((tick % 1000) == 0) task_1000ms = true;
}

int main(void)
{
    Initialize();

    while (1)
    {
        if (task_10ms)
        {
            task_10ms = false;
            ReadSensor();
        }
        if (task_100ms)
        {
            task_100ms = false;
            RefreshDisplay();
        }
        if (task_1000ms)
        {
            task_1000ms = false;
            SendStatus();
        }
    }
}
```

```html
<div style="background:#0F172A; padding:1.5rem; border:1px solid var(--border); border-radius:8px; display:flex; flex-direction:column; align-items:center; margin:2rem 0;">
  <div style="font-family:'Syne',sans-serif; font-size:0.9rem; font-weight:700; color:#fff; margin-bottom:1rem; text-align:center;">TIMER TICK & FLAG-BASED SUPERLOOP DISPATCH</div>
  <svg viewBox="0 0 680 260" style="width:100%; height:auto; max-width:600px; font-family:var(--mono);">
    <defs>
      <marker id="arrow-blue" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
        <path d="M 0 1 L 10 5 L 0 9 z" fill="#3B82F6"/>
      </marker>
    </defs>

    <rect x="260" y="10" width="160" height="30" rx="4" fill="#1E293B" stroke="#10B981"/>
    <text x="340" y="28" fill="#FFF" font-size="9" text-anchor="middle" font-weight="bold">HARDWARE TIMER (1 ms Period)</text>

    <path d="M 340 40 L 340 70" stroke="#10B981" stroke-width="1.5" marker-end="url(#arrow-blue)"/>
    <text x="350" y="58" fill="#10B981" font-size="8">Interrupt Request (IRQ)</text>

    <rect x="220" y="70" width="240" height="50" rx="4" fill="#1E293B" stroke="#EF6868"/>
    <text x="340" y="85" fill="#EF6868" font-size="9" text-anchor="middle" font-weight="bold">Timer_IRQHandler() [Background]</text>
    <text x="340" y="98" fill="var(--muted)" font-size="8" text-anchor="middle">Increments tick, sets flags if due</text>
    <text x="340" y="110" fill="var(--muted)" font-size="7" text-anchor="middle">e.g. if (tick % 10 == 0) task_10ms = true</text>

    <path d="M 280 120 L 160 160" stroke="#EF6868" stroke-width="1.5" marker-end="url(#arrow-blue)"/>
    <path d="M 340 120 L 340 160" stroke="#EF6868" stroke-width="1.5" marker-end="url(#arrow-blue)"/>
    <path d="M 400 120 L 520 160" stroke="#EF6868" stroke-width="1.5" marker-end="url(#arrow-blue)"/>

    <rect x="100" y="160" width="120" height="25" rx="3" fill="#1E293B" stroke="#3B82F6"/>
    <text x="160" y="175" fill="#E2E8F0" font-size="8" text-anchor="middle">task_10ms = true</text>

    <rect x="280" y="160" width="120" height="25" rx="3" fill="#1E293B" stroke="#3B82F6"/>
    <text x="340" y="175" fill="#E2E8F0" font-size="8" text-anchor="middle">task_100ms = true</text>

    <rect x="460" y="160" width="120" height="25" rx="3" fill="#1E293B" stroke="#3B82F6"/>
    <text x="520" y="175" fill="#E2E8F0" font-size="8" text-anchor="middle">task_1000ms = true</text>

    <path d="M 160 185 L 160 215" stroke="rgba(148,163,184,0.3)" stroke-width="1.5" marker-end="url(#arrow-blue)"/>
    <path d="M 340 185 L 340 215" stroke="rgba(148,163,184,0.3)" stroke-width="1.5" marker-end="url(#arrow-blue)"/>
    <path d="M 520 185 L 520 215" stroke="rgba(148,163,184,0.3)" stroke-width="1.5" marker-end="url(#arrow-blue)"/>

    <rect x="80" y="215" width="520" height="35" rx="4" fill="rgba(59, 130, 246, 0.04)" stroke="#3B82F6" stroke-width="1.5"/>
    <text x="340" y="236" fill="#FFF" font-size="9" text-anchor="middle" font-weight="bold">FOREGROUND SUPERLOOP (Checks flags, runs tasks, resets flags)</text>
  </svg>
  <div style="font-size:0.75rem; color:var(--muted); font-family:var(--mono); margin-top:0.75rem; text-align:center;">The background ISR triggers at a precise frequency to raise flags, which the foreground superloop checks and processes cooperatively.</div>
</div>
```

## 8. Why Flags Are Not Time

This split design keeps interrupts fast. However, it introduces a new variable: scheduling latency. A flag setting does not mean the task executes exactly at the due timestamp; it means the task is released for execution. The actual run begins when the foreground loop reaches the task's check block.

```html
<div style="background:#0F172A; padding:1.5rem; border:1px solid var(--border); border-radius:8px; display:flex; flex-direction:column; align-items:center; margin:2rem 0;">
  <div style="font-family:'Syne',sans-serif; font-size:0.9rem; font-weight:700; color:#fff; margin-bottom:1rem; text-align:center;">SCHEDULING LATENCY EFFECT</div>
  <svg viewBox="0 0 700 180" style="width:100%; height:auto; max-width:600px; font-family:var(--mono);">
    <line x1="10" y1="50" x2="650" y2="50" stroke="rgba(148,163,184,0.2)" stroke-width="2"/>
    <text x="650" y="45" fill="var(--muted)" font-size="8" text-anchor="end">Time &rarr;</text>

    <rect x="10" y="60" width="220" height="25" rx="3" fill="#1E293B" stroke="#3B82F6"/>
    <text x="120" y="76" fill="#E2E8F0" font-size="8" text-anchor="middle">Foreground busy: RunHeavyMath()</text>

    <line x1="150" y1="120" x2="150" y2="60" stroke="#EF6868" stroke-width="1.5" stroke-dasharray="2,2"/>
    <circle cx="150" cy="120" r="4" fill="#EF6868"/>
    <text x="150" y="135" fill="#EF6868" font-size="8" text-anchor="middle" font-weight="bold">Flag set (Due Time)</text>
    <text x="150" y="145" fill="var(--muted)" font-size="7" text-anchor="middle">task_10ms = true</text>

    <path d="M 150 155 L 150 165 M 150 160 L 230 160 M 230 155 L 230 165" stroke="#EF6868" stroke-width="1"/>
    <text x="190" y="175" fill="#EF6868" font-size="8" text-anchor="middle" font-weight="bold">Scheduling Latency</text>

    <rect x="230" y="60" width="100" height="25" rx="3" fill="#1E293B" stroke="#10B981"/>
    <text x="280" y="76" fill="#FFF" font-size="8" text-anchor="middle" font-weight="bold">ReadSensor()</text>
    <text x="280" y="100" fill="var(--muted)" font-size="7" text-anchor="middle">Actual Execution</text>
  </svg>
  <div style="font-size:0.75rem; color:var(--muted); font-family:var(--mono); margin-top:0.75rem; text-align:center;">The difference between a task's release trigger and its actual execution start is the scheduling latency.</div>
</div>
```

If the superloop is currently busy executing a 25 ms calculation when the 10 ms flag is raised, the task experiences 25 ms of scheduling latency. The execution time of the background tasks limits the timing accuracy of the foreground loop.

## 9. When a Boolean Flag Loses Information

What happens if the scheduling latency is longer than the period of the task itself? Suppose the foreground loop is blocked for 35 milliseconds. During this block, the background timer interrupt fires three times at 10 ms, 20 ms, and 30 ms.

With a simple boolean flag: `task_10ms = true`. The flag switches from false to true on the first tick, and remains true on the second and third ticks. When the foreground loop finally unblocks and checks the flag, it sees a single `true` event. Two occurrences have collapsed, causing data loss. If our task is to refresh a screen, this is acceptable; we simply paint the latest frame. If the task is to sample a sensor, we have lost two critical packets of information.

To resolve this, systems rely on event counters, timestamp registers, ring buffers, or hardware-managed DMA paths to capture data autonomously without depending on loop response times.

## 10. Timestamp-Based Periodic Execution

An alternative scheduling architecture checks elapsed timestamps directly in the superloop without setting flags in the ISR. Instead of blocking the loop using delays, we check system ticks continuously:

```c
uint32_t last_sensor_time = 0;

while (1)
{
    uint32_t now = system_ticks;

    if ((uint32_t)(now - last_sensor_time) >= 10U)
    {
        last_sensor_time = now;
        ReadSensor();
    }
    
    // Other non-blocking checks can run here
}
```

Instead of waiting, the CPU evaluates the condition. If 10 milliseconds have not elapsed, it falls through to check other tasks. This transition from blocking waits to non-blocking timestamp comparisons keeps the loop flowing. Furthermore, by utilizing unsigned subtraction (`now - last_sensor_time`), the comparison remains completely wrap-safe when the 32-bit counter overflows and wraps back to zero.

## 11. Period Versus Execution Time

Regardless of whether we use flags, timestamps, or operating system schedulers, there is an absolute physical constraint. Suppose a task must run every 10 milliseconds, but the task itself requires 15 milliseconds of CPU execution time. No scheduling technique can resolve this. The task overflows its time budget, causing a scheduling overrun:

```html
<div style="background:#0F172A; padding:1.5rem; border:1px solid var(--border); border-radius:8px; display:flex; flex-direction:column; align-items:center; margin:2rem 0;">
  <div style="font-family:'Syne',sans-serif; font-size:0.9rem; font-weight:700; color:#fff; margin-bottom:1rem; text-align:center;">THE TIME BUDGET COLLAPSE (OVERRUN)</div>
  <svg viewBox="0 0 700 180" style="width:100%; height:auto; max-width:600px; font-family:var(--mono);">
    <line x1="10" y1="50" x2="650" y2="50" stroke="rgba(148,163,184,0.2)" stroke-width="2"/>
    <text x="650" y="45" fill="var(--muted)" font-size="8" text-anchor="end">Time &rarr;</text>

    <path d="M 10 25 L 10 35 M 10 30 L 250 30 M 250 25 L 250 35" stroke="#3B82F6" stroke-width="1.5"/>
    <text x="130" y="22" fill="#3B82F6" font-size="9" text-anchor="middle" font-weight="bold">Required Period: 10 ms</text>

    <path d="M 250 25 L 250 35 M 250 30 L 490 30 M 490 25 L 490 35" stroke="#3B82F6" stroke-width="1.5"/>
    <text x="370" y="22" fill="#3B82F6" font-size="9" text-anchor="middle" font-weight="bold">Period 2: 10 ms</text>

    <rect x="10" y="60" width="360" height="25" rx="3" fill="rgba(239, 104, 104, 0.05)" stroke="#EF6868"/>
    <text x="190" y="76" fill="#EF6868" font-size="8" text-anchor="middle" font-weight="bold">Task execution: 15 ms</text>

    <line x1="250" y1="40" x2="250" y2="100" stroke="#EF6868" stroke-width="1.5" stroke-dasharray="3,3"/>
    <polygon points="250,105 245,95 255,95" fill="#EF6868"/>
    <text x="250" y="118" fill="#EF6868" font-size="8" text-anchor="middle" font-weight="bold">Missed Deadline / Overrun</text>
  </svg>
  <div style="font-size:0.75rem; color:var(--muted); font-family:var(--mono); margin-top:0.75rem; text-align:center;">If execution time exceeds the required period, the system cannot meet its timing goals, regardless of the scheduler used.</div>
</div>
```

To avoid timing collapses, the total processor utilization—the sum of all task execution times divided by their periods—must remain safely below 100%. If utilization exceeds this boundary, the workload must be reduced, optimized, or distributed across multiple cores.

## 12. A Simple Cooperative Scheduler

By organizing tasks inside non-blocking time checks, we have constructed a basic Cooperative Scheduler directly on the bare metal:

```c
while (1)
{
    if (TaskDue_10ms())   RunFastTask();
    if (TaskDue_100ms())  RunMediumTask();
    if (TaskDue_1000ms()) RunSlowTask();
}
```

Because there is no RTOS kernel managing preemptive context switches, every task runs to completion. This system works because each task cooperates by completing its work quickly and returning control to the superloop. It is simple, highly efficient, and predictable—but it requires discipline to avoid any blocking calls.

## 13. The Timer Solved 'When', But Not 'What'

We have structured our loop, bringing order and timing to our tasks. The microcontroller now executes routines at predictable frequencies.

But knowing when to run is only half of firmware behavior. A system must also know what to do at that moment. A motor controller running every 10 milliseconds must act differently if it is starting up, spinning at target speed, braking, or indicating a fault. Time tells the system when to reconsider its state. We must now explore how behavior shifts as the machine transitions across conditions.
