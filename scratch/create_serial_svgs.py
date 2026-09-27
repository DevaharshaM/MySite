import os
import xml.etree.ElementTree as ET

def validate_svg(filepath):
    try:
        ET.parse(filepath)
        print(f"VALID: {filepath}")
        return True
    except ET.ParseError as e:
        print(f"INVALID: {filepath} -> {e}")
        return False

os.makedirs("Images", exist_ok=True)

# 1. intel_8051_scon_register.svg
svg1 = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 940 390" width="100%" height="100%" style="background:#0B1120; font-family:'DM Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
  <defs>
    <linearGradient id="cardGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1E293B"/>
      <stop offset="100%" stop-color="#0F172A"/>
    </linearGradient>
  </defs>

  <!-- Title -->
  <text x="470" y="36" text-anchor="middle" fill="#F8FAFC" font-size="20" font-weight="700" letter-spacing="0.05em">SCON (98H) &#8212; SERIAL CONTROL REGISTER</text>
  <text x="470" y="60" text-anchor="middle" fill="#94A3B8" font-size="13">The bit-addressable command surface governing the 8051 UART and shift register</text>

  <!-- SCON REGISTER CONTAINER -->
  <g transform="translate(40, 85)">
    <rect width="860" height="115" rx="8" fill="url(#cardGrad)" stroke="#334155" stroke-width="1.5" />
    <rect width="860" height="26" rx="8" fill="#1E293B" />
    <text x="430" y="18" text-anchor="middle" fill="#94A3B8" font-size="11" font-weight="700" letter-spacing="0.05em">SCON (98H) &#8212; SPECIAL FUNCTION REGISTER</text>

    <!-- 8 Bit Cells -->
    <!-- Bit 7: SM0 -->
    <g transform="translate(18, 36)">
      <rect width="96" height="64" rx="4" fill="#0C4A6E" stroke="#38BDF8" stroke-width="1.5" />
      <text x="48" y="17" text-anchor="middle" fill="#7DD3FC" font-size="9" font-weight="600">Bit 7 (9FH)</text>
      <text x="48" y="36" text-anchor="middle" fill="#FFFFFF" font-family="'IBM Plex Mono', monospace" font-size="13" font-weight="700">SM0</text>
      <text x="48" y="52" text-anchor="middle" fill="#BAE6FD" font-size="8">Serial Mode 0</text>
    </g>

    <!-- Bit 6: SM1 -->
    <g transform="translate(122, 36)">
      <rect width="96" height="64" rx="4" fill="#0C4A6E" stroke="#38BDF8" stroke-width="1.5" />
      <text x="48" y="17" text-anchor="middle" fill="#7DD3FC" font-size="9" font-weight="600">Bit 6 (9EH)</text>
      <text x="48" y="36" text-anchor="middle" fill="#FFFFFF" font-family="'IBM Plex Mono', monospace" font-size="13" font-weight="700">SM1</text>
      <text x="48" y="52" text-anchor="middle" fill="#BAE6FD" font-size="8">Serial Mode 1</text>
    </g>

    <!-- Bit 5: SM2 -->
    <g transform="translate(226, 36)">
      <rect width="96" height="64" rx="4" fill="#3B1C54" stroke="#C084FC" stroke-width="1.5" />
      <text x="48" y="17" text-anchor="middle" fill="#E9D5FF" font-size="9" font-weight="600">Bit 5 (9DH)</text>
      <text x="48" y="36" text-anchor="middle" fill="#FFFFFF" font-family="'IBM Plex Mono', monospace" font-size="13" font-weight="700">SM2</text>
      <text x="48" y="52" text-anchor="middle" fill="#DDD6FE" font-size="8">Multiprocessor</text>
    </g>

    <!-- Bit 4: REN -->
    <g transform="translate(330, 36)">
      <rect width="96" height="64" rx="4" fill="#064E3B" stroke="#10B981" stroke-width="1.8" />
      <text x="48" y="17" text-anchor="middle" fill="#6EE7B7" font-size="9" font-weight="700">Bit 4 (9CH)</text>
      <text x="48" y="36" text-anchor="middle" fill="#FFFFFF" font-family="'IBM Plex Mono', monospace" font-size="13" font-weight="700">REN</text>
      <text x="48" y="52" text-anchor="middle" fill="#A7F3D0" font-size="8">Receive Enable</text>
    </g>

    <!-- Bit 3: TB8 -->
    <g transform="translate(434, 36)">
      <rect width="96" height="64" rx="4" fill="#78350F" stroke="#F59E0B" stroke-width="1.5" />
      <text x="48" y="17" text-anchor="middle" fill="#FDE68A" font-size="9" font-weight="600">Bit 3 (9BH)</text>
      <text x="48" y="36" text-anchor="middle" fill="#FFFFFF" font-family="'IBM Plex Mono', monospace" font-size="13" font-weight="700">TB8</text>
      <text x="48" y="52" text-anchor="middle" fill="#FEF08A" font-size="8">Tx 9th Bit</text>
    </g>

    <!-- Bit 2: RB8 -->
    <g transform="translate(538, 36)">
      <rect width="96" height="64" rx="4" fill="#78350F" stroke="#F59E0B" stroke-width="1.5" />
      <text x="48" y="17" text-anchor="middle" fill="#FDE68A" font-size="9" font-weight="600">Bit 2 (9AH)</text>
      <text x="48" y="36" text-anchor="middle" fill="#FFFFFF" font-family="'IBM Plex Mono', monospace" font-size="13" font-weight="700">RB8</text>
      <text x="48" y="52" text-anchor="middle" fill="#FEF08A" font-size="8">Rx 9th Bit</text>
    </g>

    <!-- Bit 1: TI -->
    <g transform="translate(642, 36)">
      <rect width="96" height="64" rx="4" fill="#831843" stroke="#F43F5E" stroke-width="1.8" />
      <text x="48" y="17" text-anchor="middle" fill="#FECDD3" font-size="9" font-weight="700">Bit 1 (99H)</text>
      <text x="48" y="36" text-anchor="middle" fill="#FFFFFF" font-family="'IBM Plex Mono', monospace" font-size="13" font-weight="700">TI</text>
      <text x="48" y="52" text-anchor="middle" fill="#FFE4E6" font-size="8">Tx Int Flag</text>
    </g>

    <!-- Bit 0: RI -->
    <g transform="translate(746, 36)">
      <rect width="96" height="64" rx="4" fill="#831843" stroke="#F43F5E" stroke-width="1.8" />
      <text x="48" y="17" text-anchor="middle" fill="#FECDD3" font-size="9" font-weight="700">Bit 0 (98H)</text>
      <text x="48" y="36" text-anchor="middle" fill="#FFFFFF" font-family="'IBM Plex Mono', monospace" font-size="13" font-weight="700">RI</text>
      <text x="48" y="52" text-anchor="middle" fill="#FFE4E6" font-size="8">Rx Int Flag</text>
    </g>
  </g>

  <!-- FUNCTIONAL GROUP LEGEND CARDS -->
  <g transform="translate(40, 225)">
    <!-- Group 1: Mode Select -->
    <g transform="translate(0, 0)">
      <rect width="200" height="135" rx="6" fill="#1E293B" stroke="#0C4A6E" />
      <rect width="200" height="22" rx="6" fill="#0C4A6E" />
      <text x="100" y="15" text-anchor="middle" fill="#38BDF8" font-size="10" font-weight="700">MODE SELECTION</text>
      <text x="12" y="42" fill="#E2E8F0" font-size="11" font-weight="600">SM0, SM1 (Bits 7..6)</text>
      <text x="12" y="62" fill="#94A3B8" font-size="10">&#8226; 00: Mode 0 (Sync Shift Reg)</text>
      <text x="12" y="80" fill="#94A3B8" font-size="10">&#8226; 01: Mode 1 (8-bit UART Var)</text>
      <text x="12" y="98" fill="#94A3B8" font-size="10">&#8226; 10: Mode 2 (9-bit Fixed)</text>
      <text x="12" y="116" fill="#94A3B8" font-size="10">&#8226; 11: Mode 3 (9-bit Var)</text>
    </g>

    <!-- Group 2: Multiprocessor & Reception -->
    <g transform="translate(220, 0)">
      <rect width="200" height="135" rx="6" fill="#1E293B" stroke="#3B1C54" />
      <rect width="200" height="22" rx="6" fill="#3B1C54" />
      <text x="100" y="15" text-anchor="middle" fill="#C084FC" font-size="10" font-weight="700">MULTIPROCESSOR &amp; RX</text>
      <text x="12" y="42" fill="#E2E8F0" font-size="11" font-weight="600">SM2 (Bit 5) &amp; REN (Bit 4)</text>
      <text x="12" y="62" fill="#94A3B8" font-size="10">&#8226; <tspan fill="#C084FC" font-weight="700">SM2:</tspan> Enables address-only interrupt filtering in Modes 2 &amp; 3.</text>
      <text x="12" y="98" fill="#94A3B8" font-size="10">&#8226; <tspan fill="#10B981" font-weight="700">REN:</tspan> Master receive enable. 1 = Rx on; 0 = Rx locked.</text>
    </g>

    <!-- Group 3: 9th Bit Transport -->
    <g transform="translate(440, 0)">
      <rect width="200" height="135" rx="6" fill="#1E293B" stroke="#78350F" />
      <rect width="200" height="22" rx="6" fill="#78350F" />
      <text x="100" y="15" text-anchor="middle" fill="#F59E0B" font-size="10" font-weight="700">9TH BIT DATA REPOSITORIES</text>
      <text x="12" y="42" fill="#E2E8F0" font-size="11" font-weight="600">TB8 (Bit 3) &amp; RB8 (Bit 2)</text>
      <text x="12" y="62" fill="#94A3B8" font-size="10">&#8226; <tspan fill="#F59E0B" font-weight="700">TB8:</tspan> Holds the 9th bit to transmit in Modes 2 &amp; 3.</text>
      <text x="12" y="98" fill="#94A3B8" font-size="10">&#8226; <tspan fill="#F59E0B" font-weight="700">RB8:</tspan> Captures the 9th received bit (or Stop bit in Mode 1).</text>
    </g>

    <!-- Group 4: Interrupt Flags -->
    <g transform="translate(660, 0)">
      <rect width="200" height="135" rx="6" fill="#1E293B" stroke="#831843" />
      <rect width="200" height="22" rx="6" fill="#831843" />
      <text x="100" y="15" text-anchor="middle" fill="#F43F5E" font-size="10" font-weight="700">INTERRUPT STATUS FLAGS</text>
      <text x="12" y="42" fill="#E2E8F0" font-size="11" font-weight="600">TI (Bit 1) &amp; RI (Bit 0)</text>
      <text x="12" y="62" fill="#94A3B8" font-size="10">&#8226; <tspan fill="#F43F5E" font-weight="700">TI:</tspan> Set by hardware on Tx complete. Must be cleared by software.</text>
      <text x="12" y="98" fill="#94A3B8" font-size="10">&#8226; <tspan fill="#F43F5E" font-weight="700">RI:</tspan> Set by hardware on Rx complete. Must be cleared by software.</text>
    </g>
  </g>
</svg>'''

with open("Images/intel_8051_scon_register.svg", "w", encoding="utf-8") as f:
    f.write(svg1)
validate_svg("Images/intel_8051_scon_register.svg")

# 2. intel_8051_sbuf_dual_architecture.svg
svg2 = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 940 400" width="100%" height="100%" style="background:#0B1120; font-family:'DM Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
  <defs>
    <linearGradient id="cardGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1E293B"/>
      <stop offset="100%" stop-color="#0F172A"/>
    </linearGradient>
    <marker id="sbuf-arr" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#38BDF8" />
    </marker>
    <marker id="sbuf-arr-amber" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#F59E0B" />
    </marker>
    <marker id="sbuf-arr-emerald" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#10B981" />
    </marker>
  </defs>

  <!-- Title -->
  <text x="470" y="36" text-anchor="middle" fill="#F8FAFC" font-size="20" font-weight="700" letter-spacing="0.05em">SBUF (99H) &#8212; ONE ADDRESS, TWO PHYSICAL PATHS</text>
  <text x="470" y="60" text-anchor="middle" fill="#94A3B8" font-size="13">Software sees a single register; silicon routes writes to transmission and reads from reception</text>

  <!-- CENTRAL SOFTWARE PORTAL (SBUF) -->
  <g transform="translate(320, 85)">
    <rect width="300" height="60" rx="8" fill="url(#cardGrad)" stroke="#38BDF8" stroke-width="2" />
    <text x="150" y="26" text-anchor="middle" fill="#F8FAFC" font-family="'IBM Plex Mono', monospace" font-size="14" font-weight="700">SBUF (SFR 99H)</text>
    <text x="150" y="44" text-anchor="middle" fill="#94A3B8" font-size="10">Internal CPU Bus Software Interface</text>
  </g>

  <!-- LEFT BRANCH: TRANSMIT PATH (WRITE ONLY) -->
  <g transform="translate(60, 185)">
    <rect width="360" height="150" rx="8" fill="#1E293B" stroke="#F59E0B" stroke-width="1.5" />
    <rect width="360" height="26" rx="8" fill="#78350F" />
    <text x="180" y="18" text-anchor="middle" fill="#FDE68A" font-size="11" font-weight="700">TRANSMISSION PATH (WRITE BUS)</text>

    <!-- Transmit Buffer Box -->
    <rect x="25" y="42" width="310" height="42" rx="4" fill="#0F172A" stroke="#B45309" stroke-width="1.2" />
    <text x="180" y="61" text-anchor="middle" fill="#FFFFFF" font-family="'IBM Plex Mono', monospace" font-size="11" font-weight="600">Transmit Buffer &amp; Shift Register</text>
    <text x="180" y="75" text-anchor="middle" fill="#FDE68A" font-size="9">Loaded when CPU executes: MOV SBUF, A</text>

    <!-- Transmit Pin Output -->
    <g transform="translate(100, 100)">
      <line x1="80" y1="0" x2="80" y2="25" stroke="#F59E0B" stroke-width="2" marker-end="url(#sbuf-arr-amber)" />
      <rect x="30" y="25" width="100" height="20" rx="3" fill="#0C4A6E" stroke="#38BDF8" />
      <text x="80" y="38" text-anchor="middle" fill="#7DD3FC" font-family="'IBM Plex Mono', monospace" font-size="9" font-weight="700">TXD (P3.1)</text>
    </g>
  </g>

  <!-- RIGHT BRANCH: RECEIVE PATH (READ ONLY) -->
  <g transform="translate(520, 185)">
    <rect width="360" height="150" rx="8" fill="#1E293B" stroke="#10B981" stroke-width="1.5" />
    <rect width="360" height="26" rx="8" fill="#064E3B" />
    <text x="180" y="18" text-anchor="middle" fill="#A7F3D0" font-size="11" font-weight="700">RECEPTION PATH (READ BUS)</text>

    <!-- Receive Buffer Box -->
    <rect x="25" y="42" width="310" height="42" rx="4" fill="#0F172A" stroke="#047857" stroke-width="1.2" />
    <text x="180" y="61" text-anchor="middle" fill="#FFFFFF" font-family="'IBM Plex Mono', monospace" font-size="11" font-weight="600">Receive Shift Register &amp; Latch</text>
    <text x="180" y="75" text-anchor="middle" fill="#A7F3D0" font-size="9">Read when CPU executes: MOV A, SBUF</text>

    <!-- Receive Pin Input -->
    <g transform="translate(100, 100)">
      <rect x="30" y="25" width="100" height="20" rx="3" fill="#0C4A6E" stroke="#38BDF8" />
      <text x="80" y="38" text-anchor="middle" fill="#7DD3FC" font-family="'IBM Plex Mono', monospace" font-size="9" font-weight="700">RXD (P3.0)</text>
      <line x1="80" y1="25" x2="80" y2="0" stroke="#10B981" stroke-width="2" marker-end="url(#sbuf-arr-emerald)" />
    </g>
  </g>

  <!-- Connectors from SBUF to Paths -->
  <!-- Write Arrow: SBUF to Transmit -->
  <path d="M 370 145 L 370 165 L 240 165 L 240 185" fill="none" stroke="#F59E0B" stroke-width="2" marker-end="url(#sbuf-arr-amber)" />
  <rect x="260" y="152" width="100" height="18" rx="2" fill="#0F172A" stroke="#F59E0B" />
  <text x="310" y="164" text-anchor="middle" fill="#FDE68A" font-size="8" font-weight="700">WRITE: MOV SBUF, A</text>

  <!-- Read Arrow: Receive to SBUF -->
  <path d="M 700 185 L 700 165 L 570 165 L 570 145" fill="none" stroke="#10B981" stroke-width="2" marker-end="url(#sbuf-arr-emerald)" />
  <rect x="580" y="152" width="100" height="18" rx="2" fill="#0F172A" stroke="#10B981" />
  <text x="630" y="164" text-anchor="middle" fill="#A7F3D0" font-size="8" font-weight="700">READ: MOV A, SBUF</text>

  <!-- Full Duplex Architectural Realization Footer -->
  <g transform="translate(60, 350)">
    <rect width="820" height="34" rx="4" fill="#0F172A" stroke="#334155" />
    <text x="410" y="16" text-anchor="middle" fill="#CBD5E1" font-size="10">
      <tspan fill="#38BDF8" font-weight="700">Full-Duplex Architecture:</tspan> Because transmit and receive hardware registers are physically separate, the 8051 can transmit and receive simultaneously without collision.
    </text>
    <text x="410" y="28" text-anchor="middle" fill="#64748B" font-size="9">Writing SBUF never overwrites unread received bytes; reading SBUF never corrupts an active transmission.</text>
  </g>
</svg>'''

with open("Images/intel_8051_sbuf_dual_architecture.svg", "w", encoding="utf-8") as f:
    f.write(svg2)
validate_svg("Images/intel_8051_sbuf_dual_architecture.svg")

# 3. intel_8051_serial_four_modes.svg
svg3 = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 940 430" width="100%" height="100%" style="background:#0B1120; font-family:'DM Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
  <defs>
    <linearGradient id="cardGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1E293B"/>
      <stop offset="100%" stop-color="#0F172A"/>
    </linearGradient>
  </defs>

  <!-- Title -->
  <text x="470" y="36" text-anchor="middle" fill="#F8FAFC" font-size="20" font-weight="700" letter-spacing="0.05em">FOUR MODES, FOUR PERSONALITIES</text>
  <text x="470" y="60" text-anchor="middle" fill="#94A3B8" font-size="13">Configured by SM0 and SM1 in SCON &#8212; from synchronous I/O expansion to multi-drop networking</text>

  <!-- 4 MODE CARDS IN A 2x2 GRID -->
  <!-- MODE 0 -->
  <g transform="translate(40, 85)">
    <rect width="410" height="150" rx="8" fill="url(#cardGrad)" stroke="#38BDF8" stroke-width="1.5" />
    <rect width="410" height="26" rx="8" fill="#0C4A6E" />
    <text x="15" y="17" fill="#FFFFFF" font-family="'IBM Plex Mono', monospace" font-size="11" font-weight="700">MODE 0 (SM0=0, SM1=0)</text>
    <text x="395" y="17" text-anchor="end" fill="#7DD3FC" font-size="10" font-weight="600">Synchronous Shift Register</text>

    <g transform="translate(15, 38)">
      <text x="0" y="15" fill="#38BDF8" font-size="11" font-weight="700">&#8226; Framing &amp; Data:</text>
      <text x="110" y="15" fill="#CBD5E1" font-size="11">8-bit data only. No start bit, no stop bit.</text>

      <text x="0" y="35" fill="#38BDF8" font-size="11" font-weight="700">&#8226; Pin Roles:</text>
      <text x="80" y="35" fill="#CBD5E1" font-size="11">RXD = Bidirectional Data; TXD = Shift Clock pulses.</text>

      <text x="0" y="55" fill="#38BDF8" font-size="11" font-weight="700">&#8226; Baud Rate:</text>
      <text x="85" y="55" fill="#CBD5E1" font-size="11">Fixed at Oscillator &#247; 12 (1 MHz at 12 MHz clock).</text>

      <text x="0" y="75" fill="#38BDF8" font-size="11" font-weight="700">&#8226; Primary Role:</text>
      <text x="95" y="75" fill="#94A3B8" font-size="10">High-speed I/O pin expansion using external shift registers.</text>
    </g>
  </g>

  <!-- MODE 1 -->
  <g transform="translate(490, 85)">
    <rect width="410" height="150" rx="8" fill="url(#cardGrad)" stroke="#10B981" stroke-width="1.8" />
    <rect width="410" height="26" rx="8" fill="#064E3B" />
    <text x="15" y="17" fill="#FFFFFF" font-family="'IBM Plex Mono', monospace" font-size="11" font-weight="700">MODE 1 (SM0=0, SM1=1)</text>
    <text x="395" y="17" text-anchor="end" fill="#6EE7B7" font-size="10" font-weight="700">Standard 8-Bit UART</text>

    <g transform="translate(15, 38)">
      <text x="0" y="15" fill="#10B981" font-size="11" font-weight="700">&#8226; Framing &amp; Data:</text>
      <text x="110" y="15" fill="#CBD5E1" font-size="11">10-bit frame (1 Start + 8 Data + 1 Stop bit).</text>

      <text x="0" y="35" fill="#10B981" font-size="11" font-weight="700">&#8226; Pin Roles:</text>
      <text x="80" y="35" fill="#CBD5E1" font-size="11">TXD = Serial Out; RXD = Serial In (Asynchronous).</text>

      <text x="0" y="55" fill="#10B981" font-size="11" font-weight="700">&#8226; Baud Rate:</text>
      <text x="85" y="55" fill="#CBD5E1" font-size="11">Variable &#8212; generated by Timer 1 overflows.</text>

      <text x="0" y="75" fill="#10B981" font-size="11" font-weight="700">&#8226; Primary Role:</text>
      <text x="95" y="75" fill="#94A3B8" font-size="10">Standard PC, terminal, modem, and peripheral communication.</text>
    </g>
  </g>

  <!-- MODE 2 -->
  <g transform="translate(40, 255)">
    <rect width="410" height="150" rx="8" fill="url(#cardGrad)" stroke="#F59E0B" stroke-width="1.5" />
    <rect width="410" height="26" rx="8" fill="#78350F" />
    <text x="15" y="17" fill="#FFFFFF" font-family="'IBM Plex Mono', monospace" font-size="11" font-weight="700">MODE 2 (SM0=1, SM1=0)</text>
    <text x="395" y="17" text-anchor="end" fill="#FDE68A" font-size="10" font-weight="600">9-Bit UART (Fixed Baud)</text>

    <g transform="translate(15, 38)">
      <text x="0" y="15" fill="#F59E0B" font-size="11" font-weight="700">&#8226; Framing &amp; Data:</text>
      <text x="110" y="15" fill="#CBD5E1" font-size="11">11-bit frame (1 Start + 8 Data + 9th Bit + 1 Stop).</text>

      <text x="0" y="35" fill="#F59E0B" font-size="11" font-weight="700">&#8226; 9th Bit Source:</text>
      <text x="105" y="35" fill="#CBD5E1" font-size="11">TB8 for Transmit; captured into RB8 on Receive.</text>

      <text x="0" y="55" fill="#F59E0B" font-size="11" font-weight="700">&#8226; Baud Rate:</text>
      <text x="85" y="55" fill="#CBD5E1" font-size="11">Fixed at Oscillator &#247; 64 (or &#247; 32 if SMOD=1).</text>

      <text x="0" y="75" fill="#F59E0B" font-size="11" font-weight="700">&#8226; Primary Role:</text>
      <text x="95" y="75" fill="#94A3B8" font-size="10">Long-distance multiprocessor networking with zero timer overhead.</text>
    </g>
  </g>

  <!-- MODE 3 -->
  <g transform="translate(490, 255)">
    <rect width="410" height="150" rx="8" fill="url(#cardGrad)" stroke="#C084FC" stroke-width="1.5" />
    <rect width="410" height="26" rx="8" fill="#3B1C54" />
    <text x="15" y="17" fill="#FFFFFF" font-family="'IBM Plex Mono', monospace" font-size="11" font-weight="700">MODE 3 (SM0=1, SM1=1)</text>
    <text x="395" y="17" text-anchor="end" fill="#E9D5FF" font-size="10" font-weight="600">9-Bit UART (Variable Baud)</text>

    <g transform="translate(15, 38)">
      <text x="0" y="15" fill="#C084FC" font-size="11" font-weight="700">&#8226; Framing &amp; Data:</text>
      <text x="110" y="15" fill="#CBD5E1" font-size="11">11-bit frame (1 Start + 8 Data + 9th Bit + 1 Stop).</text>

      <text x="0" y="35" fill="#C084FC" font-size="11" font-weight="700">&#8226; 9th Bit Source:</text>
      <text x="105" y="35" fill="#CBD5E1" font-size="11">TB8 for Transmit; captured into RB8 on Receive.</text>

      <text x="0" y="55" fill="#C084FC" font-size="11" font-weight="700">&#8226; Baud Rate:</text>
      <text x="85" y="55" fill="#CBD5E1" font-size="11">Variable &#8212; generated by Timer 1 overflows.</text>

      <text x="0" y="75" fill="#C084FC" font-size="11" font-weight="700">&#8226; Primary Role:</text>
      <text x="95" y="75" fill="#94A3B8" font-size="10">Multi-controller bus networks running at flexible standard baud rates.</text>
    </g>
  </g>
</svg>'''

with open("Images/intel_8051_serial_four_modes.svg", "w", encoding="utf-8") as f:
    f.write(svg3)
validate_svg("Images/intel_8051_serial_four_modes.svg")

# 4. intel_8051_multiprocessor_sm2_flow.svg
svg4 = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 940 380" width="100%" height="100%" style="background:#0B1120; font-family:'DM Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
  <defs>
    <linearGradient id="cardGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1E293B"/>
      <stop offset="100%" stop-color="#0F172A"/>
    </linearGradient>
    <marker id="bus-arr" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#38BDF8" />
    </marker>
  </defs>

  <!-- Title -->
  <text x="470" y="36" text-anchor="middle" fill="#F8FAFC" font-size="20" font-weight="700" letter-spacing="0.05em">THE 9TH BIT &amp; MULTIPROCESSOR FILTERING (SM2)</text>
  <text x="470" y="60" text-anchor="middle" fill="#94A3B8" font-size="13">Hardware filters out unaddressed traffic, saving thousands of wasted CPU interrupt cycles</text>

  <!-- MASTER CONTROLLER TRANSMITTER -->
  <g transform="translate(40, 85)">
    <rect width="240" height="150" rx="8" fill="url(#cardGrad)" stroke="#38BDF8" stroke-width="1.8" />
    <rect width="240" height="26" rx="8" fill="#0C4A6E" />
    <text x="120" y="17" text-anchor="middle" fill="#FFFFFF" font-size="11" font-weight="700">MASTER CONTROLLER</text>

    <g transform="translate(15, 38)">
      <rect x="0" y="0" width="210" height="42" rx="4" fill="#0F172A" stroke="#38BDF8" />
      <text x="105" y="18" text-anchor="middle" fill="#7DD3FC" font-size="10" font-weight="700">SENDING ADDRESS FRAME</text>
      <text x="105" y="32" text-anchor="middle" fill="#F8FAFC" font-family="'IBM Plex Mono', monospace" font-size="9">TB8 = 1 (Address Byte)</text>

      <rect x="0" y="52" width="210" height="42" rx="4" fill="#0F172A" stroke="#64748B" />
      <text x="105" y="70" text-anchor="middle" fill="#94A3B8" font-size="10" font-weight="700">SENDING DATA FRAME</text>
      <text x="105" y="84" text-anchor="middle" fill="#CBD5E1" font-family="'IBM Plex Mono', monospace" font-size="9">TB8 = 0 (Payload Byte)</text>
    </g>
  </g>

  <!-- SHARED SERIAL BUS LINE -->
  <line x1="280" y1="160" x2="360" y2="160" stroke="#38BDF8" stroke-width="3" />
  <line x1="360" y1="100" x2="360" y2="280" stroke="#38BDF8" stroke-width="3" />

  <!-- SLAVE 1: ADDRESSED SLAVE (MATCH!) -->
  <g transform="translate(420, 85)">
    <line x1="-60" y1="35" x2="0" y2="35" stroke="#10B981" stroke-width="2" marker-end="url(#bus-arr)" />
    <rect width="480" height="105" rx="8" fill="url(#cardGrad)" stroke="#10B981" stroke-width="1.8" />
    <rect width="480" height="24" rx="8" fill="#064E3B" />
    <text x="15" y="16" fill="#FFFFFF" font-family="'IBM Plex Mono', monospace" font-size="11" font-weight="700">SLAVE 1 (TARGET ADDRESS MATCH)</text>
    <text x="465" y="16" text-anchor="end" fill="#6EE7B7" font-size="10" font-weight="700">&#10004; WAKES UP</text>

    <g transform="translate(15, 35)">
      <text x="0" y="15" fill="#A7F3D0" font-size="10">1. Address arrives with <tspan font-family="'IBM Plex Mono', monospace" font-weight="700">RB8 = 1</tspan>. Because <tspan font-family="'IBM Plex Mono', monospace">SM2 = 1</tspan>, hardware asserts <tspan font-family="'IBM Plex Mono', monospace" font-weight="700">RI = 1</tspan>!</text>
      <text x="0" y="32" fill="#CBD5E1" font-size="10">2. ISR reads SBUF, matches its unique node address, and clears <tspan font-family="'IBM Plex Mono', monospace" font-weight="700" fill="#FDE68A">SM2 = 0</tspan>.</text>
      <text x="0" y="49" fill="#F8FAFC" font-size="10" font-weight="600">3. Now receives all subsequent data bytes (<tspan font-family="'IBM Plex Mono', monospace">RB8 = 0</tspan>) normally until packet ends!</text>
    </g>
  </g>

  <!-- SLAVE 2: UNADDRESSED SLAVE (IGNORED!) -->
  <g transform="translate(420, 215)">
    <line x1="-60" y1="35" x2="0" y2="35" stroke="#64748B" stroke-width="2" marker-end="url(#bus-arr)" />
    <rect width="480" height="105" rx="8" fill="url(#cardGrad)" stroke="#475569" stroke-width="1.2" />
    <rect width="480" height="24" rx="8" fill="#1E293B" />
    <text x="15" y="16" fill="#94A3B8" font-family="'IBM Plex Mono', monospace" font-size="11" font-weight="700">SLAVE 2 (OTHER SLAVE ON BUS)</text>
    <text x="465" y="16" text-anchor="end" fill="#F87171" font-size="10" font-weight="700">&#128564; STAYS ASLEEP</text>

    <g transform="translate(15, 35)">
      <text x="0" y="15" fill="#94A3B8" font-size="10">1. Address arrives with <tspan font-family="'IBM Plex Mono', monospace">RB8 = 1</tspan>. ISR reads SBUF: address belongs to Slave 1!</text>
      <text x="0" y="32" fill="#FCA5A5" font-size="10">2. Slave 2 leaves <tspan font-family="'IBM Plex Mono', monospace" font-weight="700">SM2 = 1</tspan> enabled in SCON.</text>
      <text x="0" y="49" fill="#CBD5E1" font-size="10">3. As Master streams data (<tspan font-family="'IBM Plex Mono', monospace">RB8 = 0</tspan>), Slave 2 hardware <tspan fill="#F87171" font-weight="700">NEVER asserts RI</tspan>. Zero CPU interrupts!</text>
    </g>
  </g>

  <!-- FOOTER NOTE -->
  <g transform="translate(40, 335)">
    <rect width="860" height="32" rx="4" fill="#0F172A" stroke="#334155" />
    <text x="430" y="16" text-anchor="middle" fill="#CBD5E1" font-size="10">
      <tspan fill="#C084FC" font-weight="700">Silicon Efficiency:</tspan> With SM2 = 1, thousands of data bytes destined for Slave 1 pass across the bus without stealing a single clock cycle from Slave 2.
    </text>
  </g>
</svg>'''

with open("Images/intel_8051_multiprocessor_sm2_flow.svg", "w", encoding="utf-8") as f:
    f.write(svg4)
validate_svg("Images/intel_8051_multiprocessor_sm2_flow.svg")

# 5. intel_8051_timer1_baud_rate_clock.svg
svg5 = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 940 370" width="100%" height="100%" style="background:#0B1120; font-family:'DM Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
  <defs>
    <linearGradient id="cardGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1E293B"/>
      <stop offset="100%" stop-color="#0F172A"/>
    </linearGradient>
    <marker id="clk-arr" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#38BDF8" />
    </marker>
  </defs>

  <!-- Title -->
  <text x="470" y="36" text-anchor="middle" fill="#F8FAFC" font-size="20" font-weight="700" letter-spacing="0.05em">WHEN THE TIMER BECOMES THE CLOCK</text>
  <text x="470" y="60" text-anchor="middle" fill="#94A3B8" font-size="13">The silicon heartbeat: How Timer 1 overflows and PCON.SMOD govern serial baud rate</text>

  <!-- PIPELINE CARDS HORIZONTAL -->
  <g transform="translate(30, 95)">
    <!-- 1. Crystal Oscillator -->
    <g transform="translate(0, 0)">
      <rect width="140" height="105" rx="6" fill="url(#cardGrad)" stroke="#64748B" stroke-width="1.5" />
      <rect width="140" height="24" rx="6" fill="#1E293B" />
      <text x="70" y="17" text-anchor="middle" fill="#94A3B8" font-size="10" font-weight="700">1. OSCILLATOR</text>
      <text x="70" y="52" text-anchor="middle" fill="#F8FAFC" font-family="'IBM Plex Mono', monospace" font-size="13" font-weight="700">11.0592 MHz</text>
      <text x="70" y="70" text-anchor="middle" fill="#64748B" font-size="9">Crystal Frequency</text>
      <text x="70" y="88" text-anchor="middle" fill="#38BDF8" font-size="9">&#247; 12 Internal Clock</text>
    </g>

    <!-- Arrow 1 -->
    <line x1="145" y1="52" x2="175" y2="52" stroke="#38BDF8" stroke-width="2" marker-end="url(#clk-arr)" />

    <!-- 2. Timer 1 in Mode 2 -->
    <g transform="translate(180, 0)">
      <rect width="180" height="105" rx="6" fill="url(#cardGrad)" stroke="#38BDF8" stroke-width="1.8" />
      <rect width="180" height="24" rx="6" fill="#0C4A6E" />
      <text x="90" y="17" text-anchor="middle" fill="#7DD3FC" font-size="10" font-weight="700">2. TIMER 1 (MODE 2)</text>
      <text x="90" y="48" text-anchor="middle" fill="#FFFFFF" font-family="'IBM Plex Mono', monospace" font-size="12" font-weight="700">TH1 Auto-Reload</text>
      <text x="90" y="66" text-anchor="middle" fill="#BAE6FD" font-size="9">Overﬂows every (256 &#8722; TH1)</text>
      <text x="90" y="84" text-anchor="middle" fill="#38BDF8" font-size="9">Machine Cycles</text>
    </g>

    <!-- Arrow 2 -->
    <line x1="365" y1="52" x2="395" y2="52" stroke="#38BDF8" stroke-width="2" marker-end="url(#clk-arr)" />

    <!-- 3. PCON.SMOD Prescaler -->
    <g transform="translate(400, 0)">
      <rect width="180" height="105" rx="6" fill="url(#cardGrad)" stroke="#F59E0B" stroke-width="1.8" />
      <rect width="180" height="24" rx="6" fill="#78350F" />
      <text x="90" y="17" text-anchor="middle" fill="#FDE68A" font-size="10" font-weight="700">3. BAUD RATE MULTIPLIER</text>
      <text x="90" y="48" text-anchor="middle" fill="#FFFFFF" font-family="'IBM Plex Mono', monospace" font-size="12" font-weight="700">PCON (87H) . SMOD</text>
      <text x="90" y="66" text-anchor="middle" fill="#FDE68A" font-size="9">SMOD=0 &#8594; &#247; 32 Divisor</text>
      <text x="90" y="84" text-anchor="middle" fill="#FBBF24" font-size="9">SMOD=1 &#8594; &#247; 16 (Doubles Baud!)</text>
    </g>

    <!-- Arrow 3 -->
    <line x1="585" y1="52" x2="615" y2="52" stroke="#38BDF8" stroke-width="2" marker-end="url(#clk-arr)" />

    <!-- 4. Serial Baud Clock -->
    <g transform="translate(620, 0)">
      <rect width="260" height="105" rx="6" fill="url(#cardGrad)" stroke="#10B981" stroke-width="1.8" />
      <rect width="260" height="24" rx="6" fill="#064E3B" />
      <text x="130" y="17" text-anchor="middle" fill="#6EE7B7" font-size="10" font-weight="700">4. SERIAL BAUD RATE</text>
      <text x="130" y="48" text-anchor="middle" fill="#FFFFFF" font-family="'IBM Plex Mono', monospace" font-size="12" font-weight="700">TXD &amp; RXD BIT CLOCK</text>
      <text x="130" y="66" text-anchor="middle" fill="#A7F3D0" font-size="9">Standard Baud: 9600, 4800, 2400</text>
      <text x="130" y="84" text-anchor="middle" fill="#34D399" font-size="9">Sampled at 16&#215; Bit Rate on Rx</text>
    </g>
  </g>

  <!-- ARCHITECTURAL PAYOFF BOX -->
  <g transform="translate(50, 230)">
    <rect width="840" height="105" rx="8" fill="#1E293B" stroke="#38BDF8" stroke-width="1.5" />
    <rect width="840" height="24" rx="8" fill="#0C4A6E" />
    <text x="420" y="17" text-anchor="middle" fill="#7DD3FC" font-size="11" font-weight="700">WHY 11.0592 MHz CRYSTAL DOMINATES 8051 DESIGNS</text>

    <g transform="translate(25, 36)">
      <text x="0" y="16" fill="#F8FAFC" font-size="11">At 12 MHz, Timer 1 reload math produces fractional errors (e.g. 8.51%), causing framing bit slippage.</text>
      <text x="0" y="36" fill="#7DD3FC" font-size="11">At <tspan fill="#FFFFFF" font-weight="700">11.0592 MHz</tspan>, machine cycle clock is exactly 921,600 Hz &#8212; dividing evenly into 9600, 4800, 2400, and 1200 baud with <tspan fill="#10B981" font-weight="700">0.00% error!</tspan></text>
      <text x="0" y="54" fill="#94A3B8" font-size="10">Example: Setting TH1 = FDH with SMOD = 0 yields exactly 9600 baud.</text>
    </g>
  </g>
</svg>'''

with open("Images/intel_8051_timer1_baud_rate_clock.svg", "w", encoding="utf-8") as f:
    f.write(svg5)
validate_svg("Images/intel_8051_timer1_baud_rate_clock.svg")

# 6. intel_8051_serial_interrupt_dispatch.svg
svg6 = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 940 370" width="100%" height="100%" style="background:#0B1120; font-family:'DM Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
  <defs>
    <linearGradient id="cardGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1E293B"/>
      <stop offset="100%" stop-color="#0F172A"/>
    </linearGradient>
    <marker id="irq-arr" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#F43F5E" />
    </marker>
    <marker id="irq-arr-blue" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#38BDF8" />
    </marker>
  </defs>

  <!-- Title -->
  <text x="470" y="36" text-anchor="middle" fill="#F8FAFC" font-size="20" font-weight="700" letter-spacing="0.05em">THE SERIAL INTERRUPT PATHWAY</text>
  <text x="470" y="60" text-anchor="middle" fill="#94A3B8" font-size="13">Two distinct hardware events converge onto one single vector at 0023H</text>

  <!-- CONVERGENCE FLOW -->
  <g transform="translate(40, 85)">
    <!-- Event A: Transmission Complete (TI) -->
    <g transform="translate(0, 0)">
      <rect width="230" height="65" rx="6" fill="url(#cardGrad)" stroke="#F43F5E" stroke-width="1.5" />
      <text x="115" y="24" text-anchor="middle" fill="#FECDD3" font-size="11" font-weight="700">TRANSMIT COMPLETE</text>
      <text x="115" y="44" text-anchor="middle" fill="#FFFFFF" font-family="'IBM Plex Mono', monospace" font-size="12" font-weight="700">TI = 1 (SCON.1)</text>
    </g>

    <!-- Event B: Reception Complete (RI) -->
    <g transform="translate(0, 85)">
      <rect width="230" height="65" rx="6" fill="url(#cardGrad)" stroke="#F43F5E" stroke-width="1.5" />
      <text x="115" y="24" text-anchor="middle" fill="#FECDD3" font-size="11" font-weight="700">RECEPTION COMPLETE</text>
      <text x="115" y="44" text-anchor="middle" fill="#FFFFFF" font-family="'IBM Plex Mono', monospace" font-size="12" font-weight="700">RI = 1 (SCON.0)</text>
    </g>

    <!-- Converging OR Gate -->
    <path d="M 235 32 L 285 32 L 285 75" fill="none" stroke="#F43F5E" stroke-width="2" />
    <path d="M 235 118 L 285 118 L 285 75" fill="none" stroke="#F43F5E" stroke-width="2" />
    <line x1="285" y1="75" x2="330" y2="75" stroke="#F43F5E" stroke-width="2" marker-end="url(#irq-arr)" />

    <!-- OR Gate Box -->
    <g transform="translate(335, 45)">
      <rect width="110" height="60" rx="6" fill="#1E293B" stroke="#F43F5E" stroke-width="1.5" />
      <text x="55" y="26" text-anchor="middle" fill="#FECDD3" font-size="10" font-weight="700">INTERNAL</text>
      <text x="55" y="44" text-anchor="middle" fill="#FFFFFF" font-size="12" font-weight="700">OR GATE</text>
    </g>

    <!-- Arrow from OR Gate to IE Gating -->
    <line x1="450" y1="75" x2="490" y2="75" stroke="#F43F5E" stroke-width="2" marker-end="url(#irq-arr)" />

    <!-- IE Gating Stage -->
    <g transform="translate(495, 40)">
      <rect width="150" height="70" rx="6" fill="url(#cardGrad)" stroke="#38BDF8" stroke-width="1.5" />
      <text x="75" y="22" text-anchor="middle" fill="#7DD3FC" font-size="10" font-weight="700">IE GATING (A8H)</text>
      <text x="75" y="42" text-anchor="middle" fill="#FFFFFF" font-family="'IBM Plex Mono', monospace" font-size="11">ES = 1 (Bit 4)</text>
      <text x="75" y="58" text-anchor="middle" fill="#FFFFFF" font-family="'IBM Plex Mono', monospace" font-size="11">EA = 1 (Bit 7)</text>
    </g>

    <!-- Arrow to Vector Table -->
    <line x1="650" y1="75" x2="690" y2="75" stroke="#38BDF8" stroke-width="2" marker-end="url(#irq-arr-blue)" />

    <!-- Vector Address Target -->
    <g transform="translate(695, 35)">
      <rect width="165" height="80" rx="6" fill="#064E3B" stroke="#10B981" stroke-width="2" />
      <text x="82" y="24" text-anchor="middle" fill="#A7F3D0" font-size="10" font-weight="700">FIXED ROM VECTOR</text>
      <text x="82" y="48" text-anchor="middle" fill="#FFFFFF" font-family="'IBM Plex Mono', monospace" font-size="15" font-weight="700">0023H</text>
      <text x="82" y="66" text-anchor="middle" fill="#6EE7B7" font-size="9">LJMP SERIAL_ISR</text>
    </g>
  </g>

  <!-- ISR INSTRUCTIONS EXPLANATION -->
  <g transform="translate(40, 255)">
    <rect width="860" height="95" rx="8" fill="#1E293B" stroke="#F43F5E" stroke-width="1.2" />
    <rect width="860" height="24" rx="8" fill="#831843" />
    <text x="430" y="16" text-anchor="middle" fill="#FFE4E6" font-size="11" font-weight="700">THE SERIAL EXCEPTION: WHY SOFTWARE MUST CLEAR TI AND RI</text>

    <g transform="translate(20, 34)">
      <text x="0" y="16" fill="#CBD5E1" font-size="11">Unlike Timer 0/1 where hardware clears the flag upon branching, the 8051 <tspan fill="#F87171" font-weight="700">NEVER clears TI or RI automatically</tspan>.</text>
      <text x="0" y="34" fill="#CBD5E1" font-size="11">The ISR must test <tspan font-family="'IBM Plex Mono', monospace" fill="#FDE68A">JNB TI</tspan> or <tspan font-family="'IBM Plex Mono', monospace" fill="#FDE68A">JNB RI</tspan> to determine the source, and execute <tspan font-family="'IBM Plex Mono', monospace" fill="#10B981">CLR TI</tspan> or <tspan font-family="'IBM Plex Mono', monospace" fill="#10B981">CLR RI</tspan> before returning with <tspan font-family="'IBM Plex Mono', monospace" fill="#7DD3FC">RETI</tspan>.</text>
      <text x="0" y="50" fill="#94A3B8" font-size="10">If software forgets to clear the flag, the CPU will re-enter the ISR continuously in an unbreakable loop!</text>
    </g>
  </g>
</svg>'''

with open("Images/intel_8051_serial_interrupt_dispatch.svg", "w", encoding="utf-8") as f:
    f.write(svg6)
validate_svg("Images/intel_8051_serial_interrupt_dispatch.svg")

# 7. intel_8051_complete_serial_architecture.svg
svg7 = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 940 450" width="100%" height="100%" style="background:#0B1120; font-family:'DM Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
  <defs>
    <linearGradient id="cardGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1E293B"/>
      <stop offset="100%" stop-color="#0F172A"/>
    </linearGradient>
    <marker id="all-arr" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#38BDF8" />
    </marker>
  </defs>

  <!-- Title -->
  <text x="470" y="32" text-anchor="middle" fill="#F8FAFC" font-size="18" font-weight="700" letter-spacing="0.05em">THE COMPLETE 8051 SERIAL CONVERSATION</text>
  <text x="470" y="52" text-anchor="middle" fill="#94A3B8" font-size="12">How SCON, SBUF, Timer 1, PCON, and the Interrupt Controller orchestrate serial computing</text>

  <!-- SYSTEM TOPOLOGY GRID -->
  <!-- 1. SOFTWARE APPLICATION LAYER -->
  <g transform="translate(340, 70)">
    <rect width="260" height="42" rx="6" fill="#1E293B" stroke="#64748B" stroke-width="1.5" />
    <text x="130" y="20" text-anchor="middle" fill="#F8FAFC" font-size="11" font-weight="700">SOFTWARE APPLICATION</text>
    <text x="130" y="34" text-anchor="middle" fill="#94A3B8" font-family="'IBM Plex Mono', monospace" font-size="9">MOV SBUF, A  |  MOV A, SBUF</text>
  </g>

  <!-- Line down to SBUF -->
  <line x1="470" y1="112" x2="470" y2="135" stroke="#38BDF8" stroke-width="2" marker-end="url(#all-arr)" />

  <!-- 2. SBUF DUAL REGISTER -->
  <g transform="translate(320, 138)">
    <rect width="300" height="60" rx="8" fill="url(#cardGrad)" stroke="#38BDF8" stroke-width="1.8" />
    <rect width="145" height="42" x="8" y="9" rx="4" fill="#0F172A" stroke="#F59E0B" />
    <text x="80" y="27" text-anchor="middle" fill="#FDE68A" font-size="10" font-weight="700">Tx Buffer</text>
    <text x="80" y="42" text-anchor="middle" fill="#CBD5E1" font-size="8">Shift Out</text>

    <rect width="145" height="42" x="147" y="9" rx="4" fill="#0F172A" stroke="#10B981" />
    <text x="220" y="27" text-anchor="middle" fill="#A7F3D0" font-size="10" font-weight="700">Rx Latch</text>
    <text x="220" y="42" text-anchor="middle" fill="#CBD5E1" font-size="8">Shift In</text>
  </g>

  <!-- LEFT: CLOCK / TIMING SYSTEM -->
  <g transform="translate(30, 130)">
    <rect width="240" height="150" rx="8" fill="url(#cardGrad)" stroke="#38BDF8" stroke-width="1.5" />
    <rect width="240" height="24" rx="8" fill="#0C4A6E" />
    <text x="120" y="17" text-anchor="middle" fill="#7DD3FC" font-size="10" font-weight="700">BAUD TIMING GENERATOR</text>

    <g transform="translate(15, 34)">
      <text x="0" y="16" fill="#F8FAFC" font-size="10" font-weight="600">Oscillator (11.0592 MHz)</text>
      <text x="0" y="32" fill="#38BDF8" font-size="10">&#8595; &#247; 12 Machine Cycle</text>
      <text x="0" y="50" fill="#FFFFFF" font-family="'IBM Plex Mono', monospace" font-size="10" font-weight="700">Timer 1 (TH1 Mode 2)</text>
      <text x="0" y="68" fill="#F59E0B" font-size="10">&#8595; PCON.SMOD (&#247; 32 / &#247; 16)</text>
      <text x="0" y="86" fill="#10B981" font-size="10" font-weight="700">Serial Bit Clock Output</text>
    </g>
  </g>

  <!-- Line from Timer to SBUF Serial Hardware -->
  <line x1="270" y1="210" x2="340" y2="210" stroke="#38BDF8" stroke-width="2" marker-end="url(#all-arr)" />

  <!-- RIGHT: SCON CONTROL REGISTER -->
  <g transform="translate(670, 130)">
    <rect width="240" height="150" rx="8" fill="url(#cardGrad)" stroke="#C084FC" stroke-width="1.5" />
    <rect width="240" height="24" rx="8" fill="#3B1C54" />
    <text x="120" y="17" text-anchor="middle" fill="#E9D5FF" font-size="10" font-weight="700">SCON (98H) CONFIGURATION</text>

    <g transform="translate(15, 34)">
      <text x="0" y="16" fill="#CBD5E1" font-size="10">&#8226; <tspan fill="#38BDF8" font-weight="700">SM0, SM1:</tspan> Modes 0, 1, 2, 3</text>
      <text x="0" y="34" fill="#CBD5E1" font-size="10">&#8226; <tspan fill="#C084FC" font-weight="700">SM2:</tspan> Multiprocessor Filter</text>
      <text x="0" y="52" fill="#CBD5E1" font-size="10">&#8226; <tspan fill="#10B981" font-weight="700">REN:</tspan> Receive Gate (1 = ON)</text>
      <text x="0" y="70" fill="#CBD5E1" font-size="10">&#8226; <tspan fill="#F59E0B" font-weight="700">TB8 / RB8:</tspan> 9th Bit Store</text>
      <text x="0" y="88" fill="#CBD5E1" font-size="10">&#8226; <tspan fill="#F43F5E" font-weight="700">TI / RI:</tspan> Interrupt Triggers</text>
    </g>
  </g>

  <!-- Line from SCON to SBUF Hardware -->
  <line x1="670" y1="210" x2="600" y2="210" stroke="#C084FC" stroke-width="2" marker-end="url(#all-arr)" />

  <!-- BOTTOM: PHYSICAL PINS & INTERRUPT PATH -->
  <!-- Physical Pins -->
  <g transform="translate(340, 240)">
    <rect width="260" height="65" rx="6" fill="#1E293B" stroke="#F59E0B" stroke-width="1.5" />
    <text x="130" y="20" text-anchor="middle" fill="#FDE68A" font-size="11" font-weight="700">PHYSICAL PORT 3 PINS</text>
    <text x="65" y="44" text-anchor="middle" fill="#38BDF8" font-family="'IBM Plex Mono', monospace" font-size="10" font-weight="700">TXD (P3.1)</text>
    <text x="195" y="44" text-anchor="middle" fill="#10B981" font-family="'IBM Plex Mono', monospace" font-size="10" font-weight="700">RXD (P3.0)</text>
  </g>

  <!-- Interrupt Pathway Bottom -->
  <g transform="translate(180, 335)">
    <rect width="580" height="95" rx="8" fill="#1E293B" stroke="#F43F5E" stroke-width="1.5" />
    <rect width="580" height="24" rx="8" fill="#831843" />
    <text x="290" y="16" text-anchor="middle" fill="#FFE4E6" font-size="11" font-weight="700">INTERRUPT SUBSYSTEM INTEGRATION</text>

    <g transform="translate(20, 36)">
      <text x="0" y="16" fill="#CBD5E1" font-size="11">Hardware asserts <tspan fill="#F43F5E" font-weight="700">TI</tspan> or <tspan fill="#F43F5E" font-weight="700">RI</tspan> &#8594; Gated by <tspan fill="#38BDF8" font-weight="700">IE.ES</tspan> &amp; <tspan fill="#38BDF8" font-weight="700">IE.EA</tspan> &#8594; Vectors to <tspan fill="#10B981" font-weight="700">0023H</tspan></text>
      <text x="0" y="38" fill="#94A3B8" font-size="10">Software ISR services buffer, clears TI/RI in software, and executes RETI to restore normal flow.</text>
    </g>
  </g>
</svg>'''

with open("Images/intel_8051_complete_serial_architecture.svg", "w", encoding="utf-8") as f:
    f.write(svg7)
validate_svg("Images/intel_8051_complete_serial_architecture.svg")

print("All 7 Serial SVGs created and validated successfully!")
