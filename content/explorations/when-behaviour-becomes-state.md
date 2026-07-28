---
id: when-behaviour-becomes-state
category: Bare Metal
series: System Explorations
title: When Behaviour Becomes State
subtitle: How to design predictable firmware states without operating system schedulers.
date: 23rd July, 2026
tags: [Bare Metal, State Machine, Firmware Design, Superloop, Timing]
closing_heading: The Limits of the Simple Model
closing_paragraphs:
  - This simple timed superloop and state machine architecture can support highly sophisticated products—from medical devices to aerospace sensor nodes. It operates directly on the silicon with zero kernel overhead, minimal memory foot print, and complete predictability.
  - But as system complexity continues to scale, this cooperative model reaches a boundary. What happens when multiple tasks must block for external events, or task execution times collide? When sequential cooperation is no longer enough, a new way of organizing execution is waiting.
closing_quote: The superloop keeps running, ticking millisecond by millisecond, waiting for the next path to awaken.
footer: Analyzing bare-metal state machines, transition lifecycles, and integrated timing models - PrajnaEdge.dev
---

## 1. Same Input, Different Behaviour

Our previous explorations built a sequential superloop and taught it to coordinate tasks at precise intervals using hardware timers. The machine now has heartbeat and timing structure. But a critical question remains: even if the system knows exactly when to run a task, how does it decide what behaviour is appropriate at this exact millisecond?

Consider a motor-driven industrial system. It receives a single input: a `Start` button press. If the system is idle, pressing Start should engage the power relays and initiate a startup sequence. If the motor is already running, pressing Start should be ignored. If the system is in a fault state due to an overcurrent trigger, pressing Start must be rejected for safety.

The physical input is identical in all three cases. Yet, the required software reaction is entirely different. This is because input alone does not determine behaviour. Behaviour is a function of both the current input and the historical context of the system. We call this context the system's State.

> Embedded software cannot exist as a pure function of its inputs. It must remember its past to govern its future.

## 2. The Hidden Memory Inside Behaviour

In poorly structured firmware, state is often stored in scattered boolean flags: `bool is_running = false;`, `bool has_fault = false;`, `bool is_starting = false;`. As features grow, these flags multiply. Contradictory states accidentally become possible: what happens if both `is_running` and `has_fault` are true? The code enters an undefined territory.

To avoid this complexity, we define mutually exclusive modes of operation using an explicit enumeration:

```c
typedef enum
{
    STATE_IDLE,
    STATE_STARTING,
    STATE_RUNNING,
    STATE_FAULT
} SystemState;

SystemState current_state = STATE_IDLE;
```

By declaring a single `current_state` variable, we guarantee that the firmware can occupy exactly one state at any given moment. This is the foundation of a Finite State Machine.

## 3. The First State Machine

The most common bare-metal state machine pattern utilizes a switch statement inside a periodic superloop task:

```c
switch (current_state)
{
    case STATE_IDLE:
        HandleIdle();
        break;

    case STATE_STARTING:
        HandleStarting();
        break;

    case STATE_RUNNING:
        HandleRunning();
        break;

    case STATE_FAULT:
        HandleFault();
        break;

    default:
        current_state = STATE_FAULT; // Fail-safe default
        break;
}
```

This switch-case structure maps our states, events, and transitions. It organizes code into modular, isolated blocks, preventing feature additions from degrading into a tangle of conditional statements.

```html
<div style="background:#0F172A; padding:1.5rem; border:1px solid var(--border); border-radius:8px; display:flex; flex-direction:column; align-items:center; margin:2rem 0;">
  <div style="font-family:'Syne',sans-serif; font-size:0.9rem; font-weight:700; color:#fff; margin-bottom:1rem; text-align:center;">SYSTEM STATE TRANSITION DIAGRAM</div>
  <svg viewBox="0 0 600 320" style="width:100%; height:auto; max-width:500px; font-family:var(--mono);">
    <defs>
      <marker id="arrow-blue" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
        <path d="M 0 1 L 10 5 L 0 9 z" fill="#3B82F6"/>
      </marker>
      <marker id="arrow-red" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
        <path d="M 0 1 L 10 5 L 0 9 z" fill="#EF6868"/>
      </marker>
    </defs>

    <rect x="50" y="40" width="100" height="40" rx="6" fill="#1E293B" stroke="#3B82F6" stroke-width="1.5"/>
    <text x="100" y="65" fill="#FFF" font-size="9" font-weight="bold" text-anchor="middle">STATE_IDLE</text>

    <path d="M 150 60 L 290 60" stroke="#3B82F6" stroke-width="1.5" marker-end="url(#arrow-blue)"/>
    <text x="220" y="52" fill="#3B82F6" font-size="8" text-anchor="middle">Start command</text>

    <rect x="300" y="40" width="100" height="40" rx="6" fill="#1E293B" stroke="#3B82F6" stroke-width="1.5"/>
    <text x="350" y="65" fill="#FFF" font-size="9" font-weight="bold" text-anchor="middle">STATE_STARTING</text>

    <path d="M 350 80 L 350 170" stroke="#3B82F6" stroke-width="1.5" marker-end="url(#arrow-blue)"/>
    <text x="360" y="130" fill="#3B82F6" font-size="8" text-anchor="start">Startup complete</text>

    <rect x="300" y="180" width="100" height="40" rx="6" fill="#1E293B" stroke="#10B981" stroke-width="1.5"/>
    <text x="350" y="205" fill="#FFF" font-size="9" font-weight="bold" text-anchor="middle">STATE_RUNNING</text>

    <path d="M 300 200 L 150 200" stroke="#EF6868" stroke-width="1.5" marker-end="url(#arrow-red)"/>
    <text x="225" y="192" fill="#EF6868" font-size="8" text-anchor="middle">Fault detected</text>

    <rect x="50" y="180" width="100" height="40" rx="6" fill="#1E293B" stroke="#EF6868" stroke-width="1.5"/>
    <text x="100" y="205" fill="#FFF" font-size="9" font-weight="bold" text-anchor="middle">STATE_FAULT</text>

    <path d="M 100 180 L 100 90" stroke="#3B82F6" stroke-width="1.5" marker-end="url(#arrow-blue)"/>
    <text x="90" y="140" fill="#3B82F6" font-size="8" text-anchor="end">Reset / Fault cleared</text>

    <path d="M 300 70 C 200 90, 150 120, 120 170" fill="none" stroke="#EF6868" stroke-width="1.5" stroke-dasharray="3,3" marker-end="url(#arrow-red)"/>
    <text x="180" y="115" fill="#EF6868" font-size="8" text-anchor="middle">Fault during boot</text>
  </svg>
  <div style="font-size:0.75rem; color:var(--muted); font-family:var(--mono); margin-top:0.75rem; text-align:center;">Mutually exclusive enums form deterministic paths where inputs trigger state transitions and execution modes.</div>
</div>
```

## 4. Transitions: When Behaviour Changes

A state transition is the act of switching from one state to another. In our motor example, transitions are conditional:

```c
case STATE_IDLE:
    if (start_requested)
    {
        current_state = STATE_STARTING;
    }
    break;
```

By validating transitions only within specific states, we ensure that out-of-order events (such as pressing Start while the machine is already running or faulted) are ignored, maintaining safety and operational constraints.

## 5. Entry, Run, and Exit Actions

Transitioning to a state often requires one-time configurations. For example, entering `STATE_STARTING` requires enabling a motor relay, clearing a fault log, and setting a boot timer. If we place this logic inside the state handler:

```c
case STATE_STARTING:
    EnableMotorRelay();
    ResetBootTimer();
    break;
```

These routines execute repeatedly on every iteration of the superloop. This wastes execution cycles and resets timers continuously, preventing the system from progressing. We must divide state actions into distinct phases:

1. **On Entry**: Runs exactly once when entering the state.
2. **While Active (Run)**: Runs repeatedly while the state remains active.
3. **On Exit**: Runs exactly once when leaving the state.

```html
<div style="background:#0F172A; padding:1.5rem; border:1px solid var(--border); border-radius:8px; display:flex; flex-direction:column; align-items:center; margin:2rem 0;">
  <div style="font-family:'Syne',sans-serif; font-size:0.9rem; font-weight:700; color:#fff; margin-bottom:1rem; text-align:center;">STATE TRANSITION LIFECYCLE (ENTRY / RUN / EXIT)</div>
  <svg viewBox="0 0 680 180" style="width:100%; height:auto; max-width:600px; font-family:var(--mono);">
    <defs>
      <marker id="arrow-green" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
        <path d="M 0 1 L 10 5 L 0 9 z" fill="#10B981"/>
      </marker>
    </defs>

    <rect x="20" y="50" width="160" height="50" rx="5" fill="#1E293B" stroke="#3B82F6" stroke-width="1.5"/>
    <text x="100" y="72" fill="#3B82F6" font-size="9" text-anchor="middle" font-weight="bold">ON ENTRY (Once)</text>
    <text x="100" y="87" fill="var(--muted)" font-size="7" text-anchor="middle">Configure registers / reset timers</text>

    <path d="M 180 75 L 240 75" stroke="#3B82F6" stroke-width="1.5" marker-end="url(#arrow-green)"/>

    <rect x="240" y="40" width="200" height="70" rx="5" fill="#1E293B" stroke="#10B981" stroke-width="1.5"/>
    <text x="340" y="65" fill="#10B981" font-size="9" text-anchor="middle" font-weight="bold">WHILE IN STATE (Every Loop)</text>
    <text x="340" y="80" fill="var(--muted)" font-size="7" text-anchor="middle">Run continuous task behavior</text>
    <text x="340" y="93" fill="var(--muted)" font-size="7" text-anchor="middle">Check transition conditions</text>

    <path d="M 440 75 L 500 75" stroke="#3B82F6" stroke-width="1.5" marker-end="url(#arrow-green)"/>

    <rect x="500" y="50" width="160" height="50" rx="5" fill="#1E293B" stroke="#EF6868" stroke-width="1.5"/>
    <text x="580" y="72" fill="#EF6868" font-size="9" text-anchor="middle" font-weight="bold">ON EXIT (Once)</text>
    <text x="580" y="87" fill="var(--muted)" font-size="7" text-anchor="middle">Release hardware / clear flags</text>
  </svg>
  <div style="font-size:0.75rem; color:var(--muted); font-family:var(--mono); margin-top:0.75rem; text-align:center;">Explicit boundaries ensure setup and teardown routines execute exactly once during transitions.</div>
</div>
```

In modular systems, transitions are routed through a dedicated state-setter function that enforces this lifecycle:

```c
void SetState(SystemState new_state)
{
    if (new_state == current_state)
        return;

    ExitState(current_state);       // Trigger exit logic
    current_state = new_state;
    EnterState(current_state);     // Trigger entry logic
}
```

## 6. Integrating Time: Non-Blocking State Waits

Let's connect this state model with the timing engine we built in our previous exploration. Suppose our startup process must wait in `STATE_STARTING` for exactly 500 milliseconds before transitioning to `STATE_RUNNING`. The naive approach uses blocking delay:

```c
case STATE_STARTING:
    EnableMotorRelay();
    DelayMs(500); // Blocks the entire system
    current_state = STATE_RUNNING;
    break;
```

This delay freezes the superloop. The CPU cannot check sensors, handle communications, or evaluate safety limits for half a second, exposing the machine to catastrophic failure modes if a fault occurs during boot.

Instead of blocking, we integrate state with our non-blocking tick counter: On entering `STATE_STARTING`, we record the start timestamp: `startup_begin_time = system_ticks;`. Then, inside the active state checks, we evaluate the duration:

```c
case STATE_STARTING:
    if ((uint32_t)(system_ticks - startup_begin_time) >= 500U)
    {
        SetState(STATE_RUNNING); // Transition safely
    }
    break;
```

By checking elapsed time instead of waiting passively, the processor is released. The loop continues to run, keeping communication layers flowing and safety interrupts fully armed while the startup period progresses. The machine doesn't wait; it remembers.

## 7. Putting It Inside the Superloop

We can now examine how the entire bare-metal architecture comes together inside our main application loop:

```c
int main(void)
{
    Initialize();

    while (1)
    {
        ProcessInputs();
        ProcessCommunication();

        if (control_task_due)
        {
            control_task_due = false;
            RunStateMachine(); // Executes periodic control logic
        }

        ProcessBackgroundWork();
    }
}
```

```html
<div style="background:#0F172A; padding:1.5rem; border:1px solid var(--border); border-radius:8px; display:flex; flex-direction:column; align-items:center; margin:2rem 0;">
  <div style="font-family:'Syne',sans-serif; font-size:0.9rem; font-weight:700; color:#fff; margin-bottom:1rem; text-align:center;">THE COOPERATIVE TIMED STATE ARCHITECTURE</div>
  <svg viewBox="0 0 680 280" style="width:100%; height:auto; max-width:600px; font-family:var(--mono);">
    <defs>
      <marker id="arrow-blue" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
        <path d="M 0 1 L 10 5 L 0 9 z" fill="#3B82F6"/>
      </marker>
    </defs>

    <rect x="250" y="10" width="180" height="30" rx="4" fill="#1E293B" stroke="#10B981"/>
    <text x="340" y="28" fill="#FFF" font-size="9" text-anchor="middle" font-weight="bold">1. HARDWARE TIMER (ticks)</text>

    <path d="M 340 40 L 340 75" stroke="#10B981" stroke-width="1.5" marker-end="url(#arrow-blue)"/>

    <rect x="200" y="75" width="280" height="45" rx="4" fill="#1E293B" stroke="#EF6868"/>
    <text x="340" y="92" fill="#EF6868" font-size="9" text-anchor="middle" font-weight="bold">2. BACKGROUND TIMER ISR / SYSTEM TICKS</text>
    <text x="340" y="107" fill="var(--muted)" font-size="7" text-anchor="middle">Increments counter, flags periodic control windows</text>

    <path d="M 340 120 L 340 155" stroke="#EF6868" stroke-width="1.5" marker-end="url(#arrow-blue)"/>

    <rect x="150" y="155" width="380" height="45" rx="4" fill="#1E293B" stroke="#3B82F6"/>
    <text x="340" y="172" fill="#3B82F6" font-size="9" text-anchor="middle" font-weight="bold">3. FOREGROUND SUPERLOOP DISPATCHER</text>
    <text x="340" y="187" fill="var(--muted)" font-size="7" text-anchor="middle">Evaluates non-blocking time window tasks</text>

    <path d="M 340 200 L 340 235" stroke="#3B82F6" stroke-width="1.5" marker-end="url(#arrow-blue)"/>

    <rect x="180" y="235" width="320" height="35" rx="4" fill="rgba(59, 130, 246, 0.04)" stroke="#3B82F6" stroke-width="1.5"/>
    <text x="340" y="256" fill="#FFF" font-size="9" text-anchor="middle" font-weight="bold">4. STATE MACHINE (Determines current behavior)</text>
  </svg>
  <div style="font-size:0.75rem; color:var(--muted); font-family:var(--mono); margin-top:0.75rem; text-align:center;">Hardware timers tick background registers; superloop filters dispatch; state enums direct actual instruction blocks.</div>
</div>
```

## 8. Events Can Come from Many Places

State transitions can be driven by a variety of asynchronous event sources:
- **Hardware Input Events**: Button presses, optical sensor triggers, limit switch closures.
- **Timer Expired Events**: Software timeout completions (like our non-blocking 500 ms wait).
- **Sensor Thresholds**: Temperature crossing safety ranges.
- **Communication Messages**: Host system packet arrivals.
- **Interrupt Signals**: Critical peripheral hardware updates.

In a clean cooperative architecture, background interrupts capture and queue these events, leaving the foreground logic to evaluate and execute the state transitions at a safe, unified execution level. This limits context-switch issues and race conditions.

## 9. State Explosion

State machines are a powerful structuring tool, but they have a scaling bottleneck: state explosion. A basic application starts with 4 states. As features are added, you introduce new states: `STOPPING`, `CALIBRATING`, `DIAGNOSTIC`, `UPDATE_FW`, `LOW_POWER`. The number of states grows, and the paths between them multiply exponentially.

If transition paths are modified from multiple locations in the file without clear boundaries, states can trigger unexpectedly, causing hidden bugs. Designing state machines requires caution: keep state counts bounded, keep state modification unified, and enforce strict ownership of state-variable updates.

## 10. A State Machine Is Not the Machine

A state machine is a conceptual model used to organize code, not a representation of the entire system. Real-world systems also contain continuous physical processes, asynchronous hardware registers, packet streams, and interrupt lines. Trying to model every single variable and condition as a state will make the code unmanageable. State should be reserved for representing the system's primary operating modes.

## 11. The Complete Bare Metal Picture

We have reached the end of our foundational path. Our bare-metal machine now possesses a complete execution architecture, built step-by-step across four key stages:

1. **Before main()**: How silicon boots, configures vectors, migrates memory segments, and constructs the C environment.
2. **The Infinite Loop That Runs a Machine**: How the core commits to perpetual execution, performing background and foreground cycles.
3. **Teaching Time to an Infinite Loop**: How independent counters and timer interrupts segment execution, scheduling tasks periodically.
4. **When Behaviour Becomes State**: How explicit enums and transitions organize behaviors, ensuring the machine reacts safely to inputs.
