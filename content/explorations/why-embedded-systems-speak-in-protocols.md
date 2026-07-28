---
id: why-embedded-systems-speak-in-protocols
category: Interaction
series: System Explorations
title: Why Embedded Systems Speak in Protocols
subtitle: Why simple electrical signals evolved into structured conversations.
date: 12th June, 2026
tags: [Protocols, Communication, SPI, I2C, UART, Embedded Systems]
closing_heading: The Language of Silicon
closing_paragraphs:
  - A processor speaking in isolation is only executing calculations. When it learns to follow structured protocols, it joins a larger network of interaction.
  - The choice of protocol defines the parameters of that conversation.
closing_quote: Protocols are not just communication mechanisms; they are the architectural agreements that make distributed systems possible.
footer: Reflections on systems communication - PrajnaEdge.dev
---

## 1. The Limit of Direct Connection

In the early stages of computing design, the challenge is simply getting a CPU to change a physical state. We write a value to a register, voltage appears on a copper pin, and an LED illuminates. This General Purpose Input/Output (GPIO) is the simplest boundary crossing between logic and physical consequence.

But systems do not exist in isolation. A microcontroller must talk to sensors, memory modules, display controllers, and other processors. If we try to scale GPIO to handle this, we quickly run into a physical wall.

To send a single 8-bit integer, we could use eight separate GPIO pins connected by eight physical wires. This parallel approach works, but it consumes valuable pins and turns the PCB routing layout into a dense maze of copper. If we instead use a single wire to send those 8 bits sequentially, we face a new problem: timing. How does the receiver know when to sample the wire? How does it distinguish a string of consecutive '1' bits from a single long '1' bit?

> Without a shared definition of structure, raw electrical signals are indistinguishable from noise.

## 2. Communication as Shared Agreement

Communication requires more than simply pushing electrons down a copper lead. It requires a shared agreement—a protocol. A protocol transitions communication from raw physics to structured grammar.

Every communication protocol establishes three critical boundaries:

1. The Physical Layer: Agreeing on voltage levels. What voltage represents a digital '1' and what represents a '0'? Are we using single-ended voltages or differential signals?

2. The Timing: Agreeing on speed. How long does a single bit of information last?

3. The Framing: Agreeing on structure. How does a transmitter signal that a new message is starting? How does the receiver know when the message has ended, and how does it detect if data was corrupted?

By establishing these rules, we can pack dense information onto a minimal number of physical lines.

## 3. Serial vs. Parallel: The Routing Dilemma

Intuitively, parallel communication seems superior because it transmits multiple bits at the same instant. Early computers relied heavily on parallel buses for printers (LPT ports), hard drives (IDE cables), and internal bus architectures.

However, as timing speeds increased, parallel communication encountered fundamental physical limits:

Skew: Because copper traces on a PCB have slightly different physical lengths and capacitive characteristics, bits traveling in parallel arrive at the destination at slightly different times. At high frequencies, this skew corrupts the data.

Crosstalk: Parallel lines running close to each other generate electromagnetic fields that induce noise on neighboring lines.

PCB Complexity: Routing dozens of high-speed parallel traces requires multi-layer boards and tight spacing constraints, increasing manufacturing costs.

Serial communication solves this by sending bits sequentially over a minimal physical path (often just one or two lines). By focusing on timing alignment on a single line, modern systems can achieve transfer rates orders of magnitude faster than historical parallel buses, using far less physical space.

![GPIO Direct vs Protocol Structured Signaling](Images/protocols_vs_gpio_schematic.png)

*The transition from direct, unstructured GPIO toggling to a structured protocol frame containing synchronization and data payload boundaries.*

## 4. Direction of Flow: Simplex to Full Duplex

Once we move to serial lines, we must decide how devices share the channel to transmit and receive data. This flow is categorized into three modes:

Simplex: One-way communication. A transmitter sends data continuously, and a receiver only listens. There is no feedback loop. This is typical in simple broadcast sensors or debug logs.

Half Duplex: Two-way communication, but only one device can transmit at any given instant. Devices must share the physical line, requiring addressing or turn-taking logic to avoid collisions. I2C and RS-485 are classic examples.

Full Duplex: Simultaneous, bidirectional communication. This is typically achieved by running separate physical lines for transmit (TX) and receive (RX), allowing both devices to speak and listen at the same time without interference. UART and SPI operate in this mode.

## 5. The Synchronization Boundary

The most critical task of any protocol is synchronization—ensuring the receiver samples the wire at the exact moment a bit is stable. This divides serial protocols into two main philosophies:

Synchronous Communication: The transmitter provides a physical clock signal along a dedicated line (e.g., SPI and I2C). The receiver monitors this clock line and samples the data line on the rising or falling clock edge. This is highly reliable and supports variable speeds, but requires an extra physical line.

Asynchronous Communication: No clock signal is transmitted (e.g., UART). Instead, both transmitter and receiver must be configured to use the exact same bit speed (baud rate) beforehand. The receiver detects the start of a transmission by watching for a specific voltage change (the Start Bit) and then uses its local clock to count out intervals and sample the subsequent bits.

> Synchronous protocols share a clock line to guarantee timing. Asynchronous protocols agree on timing beforehand to save a wire.

## 6. From Signals to Conversations

Communication protocols are the grammar of systems. They move us past raw physical toggling into organized logical networks where processors, sensors, and displays negotiate control, exchange status, and build coordinated behavior.

As we explore the interaction layer of the systems tree, we will trace the evolution of these agreements:

UART: The simple, asynchronous point-to-point interface.

SPI: The high-speed, synchronous, register-to-register bus.

I2C: The multi-drop, addressed, two-wire shared conversation.

CAN: The robust, differential, priority-arbitrated network designed for extreme noise environments.

Every protocol is a distinct set of engineering compromises, balancing speed, pin count, distance, and reliability to solve a specific coordination challenge.
