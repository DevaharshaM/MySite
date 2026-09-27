import os

def create_address_to_hardware_flow():
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 490" width="100%" height="100%" style="background:#0B1120; font-family:'DM Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
  <defs>
    <linearGradient id="ramGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1E293B"/>
      <stop offset="100%" stop-color="#0F172A"/>
    </linearGradient>
    <linearGradient id="sfrGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1E293B"/>
      <stop offset="100%" stop-color="#172554"/>
    </linearGradient>
    <marker id="arrow-blue" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#38BDF8" />
    </marker>
    <marker id="arrow-emerald" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#10B981" />
    </marker>
    <marker id="arrow-gray" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#64748B" />
    </marker>
  </defs>

  <!-- Title & Subtitle -->
  <text x="450" y="42" text-anchor="middle" fill="#F8FAFC" font-size="20" font-weight="700" letter-spacing="0.05em">DATA MEMORY VS HARDWARE INTERFACE</text>
  <text x="450" y="68" text-anchor="middle" fill="#94A3B8" font-size="13">How the exact same instruction format produces fundamentally different physical consequences</text>

  <!-- LEFT COLUMN: ORDINARY RAM (30H) -->
  <g transform="translate(50, 95)">
    <rect width="375" height="360" rx="10" fill="url(#ramGrad)" stroke="#334155" stroke-width="1.5" />
    <rect x="0" y="0" width="375" height="40" rx="10" fill="#1E293B" stroke="#334155" stroke-width="1.5" />
    <text x="187" y="25" text-anchor="middle" fill="#94A3B8" font-size="13" font-weight="700" letter-spacing="0.05em">STORAGE DESTINATION: ADDRESS 30H</text>

    <!-- Instruction Box -->
    <rect x="25" y="60" width="325" height="46" rx="6" fill="#0F172A" stroke="#475569" stroke-width="1" />
    <text x="40" y="88" fill="#E2E8F0" font-family="'IBM Plex Mono', monospace" font-size="14" font-weight="600">MOV 30H, #55H</text>
    <text x="235" y="88" fill="#64748B" font-family="'IBM Plex Mono', monospace" font-size="11">[0101 0101b]</text>

    <line x1="187" y1="106" x2="187" y2="136" stroke="#64748B" stroke-width="1.5" marker-end="url(#arrow-gray)" />

    <!-- Internal RAM Decoder -->
    <rect x="40" y="136" width="295" height="42" rx="6" fill="#1E293B" stroke="#64748B" stroke-dasharray="3 3" />
    <text x="187" y="162" text-anchor="middle" fill="#CBD5E1" font-size="12">Internal Data Bus &amp; RAM Address Decoder</text>

    <line x1="187" y1="178" x2="187" y2="208" stroke="#64748B" stroke-width="1.5" marker-end="url(#arrow-gray)" />

    <!-- Silicon Flip-Flops -->
    <rect x="35" y="208" width="305" height="54" rx="6" fill="#0F172A" stroke="#38BDF8" stroke-width="1.5" />
    <text x="187" y="231" text-anchor="middle" fill="#38BDF8" font-family="'IBM Plex Mono', monospace" font-size="13" font-weight="600">RAM Location 30H (Scratchpad)</text>
    <text x="187" y="250" text-anchor="middle" fill="#94A3B8" font-size="11">8 Passive Static Latch Cells (Internal Flip-Flops)</text>

    <line x1="187" y1="262" x2="187" y2="292" stroke="#64748B" stroke-width="1.5" marker-end="url(#arrow-gray)" />

    <!-- Result / Consequence -->
    <rect x="25" y="292" width="325" height="54" rx="6" fill="rgba(15, 23, 42, 0.8)" stroke="#475569" />
    <text x="187" y="313" text-anchor="middle" fill="#E2E8F0" font-size="12" font-weight="600">Physical Result: Pure Data Storage</text>
    <text x="187" y="333" text-anchor="middle" fill="#94A3B8" font-size="11">Charge held internally in silicon. External pins untouched.</text>
  </g>

  <!-- RIGHT COLUMN: SFR HARDWARE (90H) -->
  <g transform="translate(475, 95)">
    <rect width="375" height="360" rx="10" fill="url(#sfrGrad)" stroke="#1E3A8A" stroke-width="1.5" />
    <rect x="0" y="0" width="375" height="40" rx="10" fill="#1E3A8A" stroke="#2563EB" stroke-width="1.5" />
    <text x="187" y="25" text-anchor="middle" fill="#60A5FA" font-size="13" font-weight="700" letter-spacing="0.05em">HARDWARE INTERFACE: ADDRESS 90H</text>

    <!-- Instruction Box -->
    <rect x="25" y="60" width="325" height="46" rx="6" fill="#0F172A" stroke="#2563EB" stroke-width="1" />
    <text x="40" y="88" fill="#38BDF8" font-family="'IBM Plex Mono', monospace" font-size="14" font-weight="600">MOV 90H, #55H</text>
    <text x="235" y="88" fill="#60A5FA" font-family="'IBM Plex Mono', monospace" font-size="11">[0101 0101b]</text>

    <line x1="187" y1="106" x2="187" y2="136" stroke="#38BDF8" stroke-width="1.5" marker-end="url(#arrow-blue)" />

    <!-- SFR Decoder -->
    <rect x="40" y="136" width="295" height="42" rx="6" fill="#1E293B" stroke="#38BDF8" stroke-dasharray="3 3" />
    <text x="187" y="162" text-anchor="middle" fill="#93C5FD" font-size="12">SFR Address Decoder (90H Select Strobe)</text>

    <line x1="187" y1="178" x2="187" y2="208" stroke="#38BDF8" stroke-width="1.5" marker-end="url(#arrow-blue)" />

    <!-- P1 SFR & Driver -->
    <rect x="35" y="208" width="305" height="54" rx="6" fill="#0F172A" stroke="#10B981" stroke-width="1.5" />
    <text x="187" y="231" text-anchor="middle" fill="#10B981" font-family="'IBM Plex Mono', monospace" font-size="13" font-weight="600">Port 1 Latch (SFR 90H)</text>
    <text x="187" y="250" text-anchor="middle" fill="#6EE7B7" font-size="11">Latches byte + energizes FET output pin drivers</text>

    <line x1="187" y1="262" x2="187" y2="292" stroke="#10B981" stroke-width="2" marker-end="url(#arrow-emerald)" />

    <!-- Result / Consequence -->
    <rect x="25" y="292" width="325" height="54" rx="6" fill="rgba(6, 78, 59, 0.4)" stroke="#10B981" stroke-width="1" />
    <text x="187" y="313" text-anchor="middle" fill="#34D399" font-size="12" font-weight="700">Physical Result: Pins Change Voltage</text>
    <text x="187" y="333" text-anchor="middle" fill="#A7F3D0" font-size="11">P1.0, P1.2, P1.4, P1.6 = +5V (HIGH); others = 0V (LOW)</text>
  </g>
</svg>'''
    with open('Images/intel_8051_address_to_hardware_flow.svg', 'w', encoding='utf-8') as f:
        f.write(svg)
    print("Created Images/intel_8051_address_to_hardware_flow.svg")

def create_bit_addressable_sfr_rule():
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 500" width="100%" height="100%" style="background:#0B1120; font-family:'DM Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
  <defs>
    <linearGradient id="headerGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1E293B"/>
      <stop offset="100%" stop-color="#0F172A"/>
    </linearGradient>
  </defs>

  <!-- Title & Subtitle -->
  <text x="450" y="38" text-anchor="middle" fill="#F8FAFC" font-size="20" font-weight="700" letter-spacing="0.05em">THE 8051 BIT-ADDRESSABLE SFR RULE</text>
  <text x="450" y="64" text-anchor="middle" fill="#94A3B8" font-size="13">Only SFR addresses whose least significant hex digit is 0H or 8H are bit-addressable</text>

  <!-- RULE BADGE -->
  <rect x="250" y="85" width="400" height="36" rx="18" fill="rgba(56, 189, 248, 0.1)" stroke="#38BDF8" stroke-width="1.5" />
  <text x="450" y="108" text-anchor="middle" fill="#38BDF8" font-family="'IBM Plex Mono', monospace" font-size="13" font-weight="600">RULE: Address MOD 8 == 0 (Ends in 0H or 8H)</text>

  <!-- LEFT: BIT-ADDRESSABLE TABLE (11 REGISTERS) -->
  <g transform="translate(45, 140)">
    <rect width="470" height="330" rx="8" fill="#0F172A" stroke="#10B981" stroke-width="1.5" />
    <rect x="0" y="0" width="470" height="34" rx="8" fill="#064E3B" stroke="#10B981" stroke-width="1.5" />
    <text x="18" y="22" fill="#34D399" font-size="12" font-weight="700" letter-spacing="0.05em">BIT-ADDRESSABLE SFRS (11 REGISTERS · 88 INDIVIDUAL BITS)</text>

    <!-- Table Header -->
    <text x="25" y="54" fill="#64748B" font-family="'IBM Plex Mono', monospace" font-size="11" font-weight="600">ADDR</text>
    <text x="85" y="54" fill="#64748B" font-family="'IBM Plex Mono', monospace" font-size="11" font-weight="600">SFR</text>
    <text x="150" y="54" fill="#64748B" font-family="'IBM Plex Mono', monospace" font-size="11" font-weight="600">BIT RANGE</text>
    <text x="270" y="54" fill="#64748B" font-size="11" font-weight="600">FUNCTION / TARGET</text>

    <line x1="15" y1="62" x2="455" y2="62" stroke="#1E293B" stroke-width="1" />

    <!-- Rows -->
    <!-- 80H P0 -->
    <text x="25" y="83" fill="#38BDF8" font-family="'IBM Plex Mono', monospace" font-size="11">80H</text>
    <text x="85" y="83" fill="#E2E8F0" font-family="'IBM Plex Mono', monospace" font-size="11" font-weight="600">P0</text>
    <text x="150" y="83" fill="#94A3B8" font-family="'IBM Plex Mono', monospace" font-size="11">80H – 87H</text>
    <text x="270" y="83" fill="#CBD5E1" font-size="11">Port 0 Latch Pins</text>

    <!-- 88H TCON -->
    <text x="25" y="107" fill="#38BDF8" font-family="'IBM Plex Mono', monospace" font-size="11">88H</text>
    <text x="85" y="107" fill="#E2E8F0" font-family="'IBM Plex Mono', monospace" font-size="11" font-weight="600">TCON</text>
    <text x="150" y="107" fill="#94A3B8" font-family="'IBM Plex Mono', monospace" font-size="11">88H – 8FH</text>
    <text x="270" y="107" fill="#CBD5E1" font-size="11">Timer &amp; Interrupt Control Flags</text>

    <!-- 90H P1 -->
    <text x="25" y="131" fill="#38BDF8" font-family="'IBM Plex Mono', monospace" font-size="11">90H</text>
    <text x="85" y="131" fill="#E2E8F0" font-family="'IBM Plex Mono', monospace" font-size="11" font-weight="600">P1</text>
    <text x="150" y="131" fill="#94A3B8" font-family="'IBM Plex Mono', monospace" font-size="11">90H – 97H</text>
    <text x="270" y="131" fill="#CBD5E1" font-size="11">Port 1 Latch Pins</text>

    <!-- 98H SCON -->
    <text x="25" y="155" fill="#38BDF8" font-family="'IBM Plex Mono', monospace" font-size="11">98H</text>
    <text x="85" y="155" fill="#E2E8F0" font-family="'IBM Plex Mono', monospace" font-size="11" font-weight="600">SCON</text>
    <text x="150" y="155" fill="#94A3B8" font-family="'IBM Plex Mono', monospace" font-size="11">98H – 9FH</text>
    <text x="270" y="155" fill="#CBD5E1" font-size="11">Serial Port Control &amp; Flags (TI, RI)</text>

    <!-- A0H P2 -->
    <text x="25" y="179" fill="#38BDF8" font-family="'IBM Plex Mono', monospace" font-size="11">A0H</text>
    <text x="85" y="179" fill="#E2E8F0" font-family="'IBM Plex Mono', monospace" font-size="11" font-weight="600">P2</text>
    <text x="150" y="179" fill="#94A3B8" font-family="'IBM Plex Mono', monospace" font-size="11">A0H – A7H</text>
    <text x="270" y="179" fill="#CBD5E1" font-size="11">Port 2 Latch Pins</text>

    <!-- A8H IE -->
    <text x="25" y="203" fill="#38BDF8" font-family="'IBM Plex Mono', monospace" font-size="11">A8H</text>
    <text x="85" y="203" fill="#E2E8F0" font-family="'IBM Plex Mono', monospace" font-size="11" font-weight="600">IE</text>
    <text x="150" y="203" fill="#94A3B8" font-family="'IBM Plex Mono', monospace" font-size="11">A8H – AFH</text>
    <text x="270" y="203" fill="#CBD5E1" font-size="11">Interrupt Enable Mask Bits</text>

    <!-- B0H P3 -->
    <text x="25" y="227" fill="#38BDF8" font-family="'IBM Plex Mono', monospace" font-size="11">B0H</text>
    <text x="85" y="227" fill="#E2E8F0" font-family="'IBM Plex Mono', monospace" font-size="11" font-weight="600">P3</text>
    <text x="150" y="227" fill="#94A3B8" font-family="'IBM Plex Mono', monospace" font-size="11">B0H – B7H</text>
    <text x="270" y="227" fill="#CBD5E1" font-size="11">Port 3 Latch Pins</text>

    <!-- B8H IP -->
    <text x="25" y="251" fill="#38BDF8" font-family="'IBM Plex Mono', monospace" font-size="11">B8H</text>
    <text x="85" y="251" fill="#E2E8F0" font-family="'IBM Plex Mono', monospace" font-size="11" font-weight="600">IP</text>
    <text x="150" y="251" fill="#94A3B8" font-family="'IBM Plex Mono', monospace" font-size="11">B8H – BFH</text>
    <text x="270" y="251" fill="#CBD5E1" font-size="11">Interrupt Priority Selection Bits</text>

    <!-- D0H PSW -->
    <text x="25" y="275" fill="#38BDF8" font-family="'IBM Plex Mono', monospace" font-size="11">D0H</text>
    <text x="85" y="275" fill="#E2E8F0" font-family="'IBM Plex Mono', monospace" font-size="11" font-weight="600">PSW</text>
    <text x="150" y="275" fill="#94A3B8" font-family="'IBM Plex Mono', monospace" font-size="11">D0H – D7H</text>
    <text x="270" y="275" fill="#CBD5E1" font-size="11">ALU Status Flags &amp; Bank Select (RS1/RS0)</text>

    <!-- E0H ACC -->
    <text x="25" y="299" fill="#38BDF8" font-family="'IBM Plex Mono', monospace" font-size="11">E0H</text>
    <text x="85" y="299" fill="#E2E8F0" font-family="'IBM Plex Mono', monospace" font-size="11" font-weight="600">ACC</text>
    <text x="150" y="299" fill="#94A3B8" font-family="'IBM Plex Mono', monospace" font-size="11">E0H – E7H</text>
    <text x="270" y="299" fill="#CBD5E1" font-size="11">Accumulator Working Bits</text>

    <!-- F0H B -->
    <text x="25" y="323" fill="#38BDF8" font-family="'IBM Plex Mono', monospace" font-size="11">F0H</text>
    <text x="85" y="323" fill="#E2E8F0" font-family="'IBM Plex Mono', monospace" font-size="11" font-weight="600">B</text>
    <text x="150" y="323" fill="#94A3B8" font-family="'IBM Plex Mono', monospace" font-size="11">F0H – F7H</text>
    <text x="270" y="323" fill="#CBD5E1" font-size="11">B Register Math Bits</text>
  </g>

  <!-- RIGHT: CONTRAST & PRACTICAL SIGNIFICANCE -->
  <g transform="translate(540, 140)">
    <!-- NON-BIT-ADDRESSABLE BOX -->
    <rect width="315" height="150" rx="8" fill="#0F172A" stroke="#475569" stroke-width="1.5" />
    <rect x="0" y="0" width="315" height="34" rx="8" fill="#1E293B" stroke="#475569" stroke-width="1.5" />
    <text x="15" y="22" fill="#94A3B8" font-size="12" font-weight="700" letter-spacing="0.05em">BYTE-ONLY SFRS (NOT BIT-ADDRESSABLE)</text>
    
    <text x="20" y="60" fill="#EF4444" font-family="'IBM Plex Mono', monospace" font-size="11" font-weight="600">CANNOT BE ADDRESSED BY BIT:</text>
    <text x="20" y="85" fill="#E2E8F0" font-family="'IBM Plex Mono', monospace" font-size="11">SP (81H), DPL (82H), DPH (83H)</text>
    <text x="20" y="105" fill="#E2E8F0" font-family="'IBM Plex Mono', monospace" font-size="11">PCON (87H), TMOD (89H)</text>
    <text x="20" y="125" fill="#E2E8F0" font-family="'IBM Plex Mono', monospace" font-size="11">TL0 (8AH), TH0 (8BH), TL1 (8CH), TH1 (8DH), SBUF (99H)</text>

    <!-- DIRECT INSTRUCTION EXAMPLE -->
    <rect y="170" width="315" height="160" rx="8" fill="#0F172A" stroke="#38BDF8" stroke-width="1.5" />
    <rect y="170" width="315" height="34" rx="8" fill="#0C4A6E" stroke="#38BDF8" stroke-width="1.5" />
    <text x="15" y="192" fill="#38BDF8" font-size="12" font-weight="700" letter-spacing="0.05em">THE EMBEDDED ADVANTAGE</text>

    <text x="20" y="225" fill="#10B981" font-family="'IBM Plex Mono', monospace" font-size="12" font-weight="600">SETB P1.0</text>
    <text x="110" y="225" fill="#94A3B8" font-size="11">; 1 instruction (turn pin on)</text>

    <text x="20" y="248" fill="#EF4444" font-family="'IBM Plex Mono', monospace" font-size="12" font-weight="600">CLR  TR0</text>
    <text x="110" y="248" fill="#94A3B8" font-size="11">; 1 instruction (stop timer)</text>

    <text x="20" y="275" fill="#CBD5E1" font-size="11">No software masking, no shifts, no temporary registers, zero side effects on neighbor bits.</text>
    <text x="20" y="310" fill="#38BDF8" font-family="'IBM Plex Mono', monospace" font-size="10">Direct bit manipulation at machine cycle speed.</text>
  </g>
</svg>'''
    with open('Images/intel_8051_bit_addressable_sfr_rule.svg', 'w', encoding='utf-8') as f:
        f.write(svg)
    print("Created Images/intel_8051_bit_addressable_sfr_rule.svg")

def create_sfr_synthesis_flow():
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 480" width="100%" height="100%" style="background:#0B1120; font-family:'DM Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
  <defs>
    <marker id="synth-arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#38BDF8" />
    </marker>
  </defs>

  <!-- Title & Subtitle -->
  <text x="450" y="42" text-anchor="middle" fill="#F8FAFC" font-size="20" font-weight="700" letter-spacing="0.05em">WHERE SOFTWARE TOUCHES HARDWARE</text>
  <text x="450" y="68" text-anchor="middle" fill="#94A3B8" font-size="13">The unbroken chain of causality connecting abstract code to physical reality</text>

  <!-- HORIZONTAL 6-STAGE CHAIN -->
  <!-- STAGE 1: SOFTWARE -->
  <g transform="translate(40, 110)">
    <rect width="115" height="180" rx="8" fill="#1E293B" stroke="#475569" stroke-width="1.5" />
    <rect width="115" height="30" rx="8" fill="#334155" />
    <text x="57" y="20" text-anchor="middle" fill="#F8FAFC" font-size="11" font-weight="700">1. SOFTWARE</text>
    <text x="57" y="65" text-anchor="middle" fill="#38BDF8" font-size="12" font-weight="600">Firmware Logic</text>
    <text x="57" y="90" text-anchor="middle" fill="#94A3B8" font-size="10">High-level intent</text>
    <text x="57" y="110" text-anchor="middle" fill="#94A3B8" font-size="10">Control loop</text>
    <text x="57" y="130" text-anchor="middle" fill="#94A3B8" font-size="10">State machine</text>
    <text x="57" y="160" text-anchor="middle" fill="#64748B" font-family="'IBM Plex Mono', monospace" font-size="10">"Turn on LED"</text>
  </g>

  <!-- ARROW 1 -->
  <line x1="160" y1="200" x2="185" y2="200" stroke="#38BDF8" stroke-width="2" marker-end="url(#synth-arrow)" />

  <!-- STAGE 2: INSTRUCTION -->
  <g transform="translate(190, 110)">
    <rect width="115" height="180" rx="8" fill="#1E293B" stroke="#475569" stroke-width="1.5" />
    <rect width="115" height="30" rx="8" fill="#334155" />
    <text x="57" y="20" text-anchor="middle" fill="#F8FAFC" font-size="11" font-weight="700">2. INSTRUCTION</text>
    <text x="57" y="65" text-anchor="middle" fill="#38BDF8" font-size="12" font-weight="600">Opcode Exec</text>
    <text x="57" y="95" text-anchor="middle" fill="#CBD5E1" font-family="'IBM Plex Mono', monospace" font-size="11" font-weight="600">MOV 90H, #01H</text>
    <text x="57" y="125" text-anchor="middle" fill="#94A3B8" font-size="10">Decoded by</text>
    <text x="57" y="142" text-anchor="middle" fill="#94A3B8" font-size="10">instruction register</text>
    <text x="57" y="160" text-anchor="middle" fill="#64748B" font-size="10">&amp; CPU sequencer</text>
  </g>

  <!-- ARROW 2 -->
  <line x1="310" y1="200" x2="335" y2="200" stroke="#38BDF8" stroke-width="2" marker-end="url(#synth-arrow)" />

  <!-- STAGE 3: ADDRESS / BUS -->
  <g transform="translate(340, 110)">
    <rect width="115" height="180" rx="8" fill="#1E293B" stroke="#475569" stroke-width="1.5" />
    <rect width="115" height="30" rx="8" fill="#334155" />
    <text x="57" y="20" text-anchor="middle" fill="#F8FAFC" font-size="11" font-weight="700">3. ADDRESS</text>
    <text x="57" y="65" text-anchor="middle" fill="#38BDF8" font-size="12" font-weight="600">Bus Strobe</text>
    <text x="57" y="95" text-anchor="middle" fill="#F59E0B" font-family="'IBM Plex Mono', monospace" font-size="13" font-weight="700">90H</text>
    <text x="57" y="125" text-anchor="middle" fill="#94A3B8" font-size="10">Address decoder</text>
    <text x="57" y="142" text-anchor="middle" fill="#94A3B8" font-size="10">asserts specific</text>
    <text x="57" y="160" text-anchor="middle" fill="#94A3B8" font-size="10">SFR write line</text>
  </g>

  <!-- ARROW 3 -->
  <line x1="460" y1="200" x2="485" y2="200" stroke="#38BDF8" stroke-width="2" marker-end="url(#synth-arrow)" />

  <!-- STAGE 4: SFR -->
  <g transform="translate(490, 110)">
    <rect width="115" height="180" rx="8" fill="#1E293B" stroke="#2563EB" stroke-width="1.5" />
    <rect width="115" height="30" rx="8" fill="#1D4ED8" />
    <text x="57" y="20" text-anchor="middle" fill="#F8FAFC" font-size="11" font-weight="700">4. SFR</text>
    <text x="57" y="65" text-anchor="middle" fill="#60A5FA" font-size="12" font-weight="600">Control Latch</text>
    <text x="57" y="95" text-anchor="middle" fill="#93C5FD" font-family="'IBM Plex Mono', monospace" font-size="12" font-weight="700">P1 (PORT 1)</text>
    <text x="57" y="125" text-anchor="middle" fill="#94A3B8" font-size="10">Latches data byte</text>
    <text x="57" y="142" text-anchor="middle" fill="#94A3B8" font-size="10">0000 0001b into</text>
    <text x="57" y="160" text-anchor="middle" fill="#94A3B8" font-size="10">hardware flip-flops</text>
  </g>

  <!-- ARROW 4 -->
  <line x1="610" y1="200" x2="635" y2="200" stroke="#38BDF8" stroke-width="2" marker-end="url(#synth-arrow)" />

  <!-- STAGE 5: HARDWARE -->
  <g transform="translate(640, 110)">
    <rect width="115" height="180" rx="8" fill="#1E293B" stroke="#059669" stroke-width="1.5" />
    <rect width="115" height="30" rx="8" fill="#047857" />
    <text x="57" y="20" text-anchor="middle" fill="#F8FAFC" font-size="11" font-weight="700">5. HARDWARE</text>
    <text x="57" y="65" text-anchor="middle" fill="#34D399" font-size="12" font-weight="600">Pin Drivers</text>
    <text x="57" y="95" text-anchor="middle" fill="#6EE7B7" font-size="11" font-weight="600">FET Transistors</text>
    <text x="57" y="125" text-anchor="middle" fill="#94A3B8" font-size="10">Switches pull-up</text>
    <text x="57" y="142" text-anchor="middle" fill="#94A3B8" font-size="10">FET network on</text>
    <text x="57" y="160" text-anchor="middle" fill="#94A3B8" font-size="10">Pin 1 (P1.0)</text>
  </g>

  <!-- ARROW 5 -->
  <line x1="760" y1="200" x2="785" y2="200" stroke="#38BDF8" stroke-width="2" marker-end="url(#synth-arrow)" />

  <!-- STAGE 6: PHYSICAL WORLD -->
  <g transform="translate(790, 110)">
    <rect width="90" height="180" rx="8" fill="#064E3B" stroke="#10B981" stroke-width="1.5" />
    <rect width="90" height="30" rx="8" fill="#059669" />
    <text x="45" y="20" text-anchor="middle" fill="#F8FAFC" font-size="10" font-weight="700">6. WORLD</text>
    <text x="45" y="65" text-anchor="middle" fill="#A7F3D0" font-size="12" font-weight="700">Reality</text>
    <text x="45" y="95" text-anchor="middle" fill="#34D399" font-family="'IBM Plex Mono', monospace" font-size="13" font-weight="700">+5V</text>
    <text x="45" y="125" text-anchor="middle" fill="#A7F3D0" font-size="10">Current flows</text>
    <text x="45" y="142" text-anchor="middle" fill="#A7F3D0" font-size="10">LED turns ON</text>
    <text x="45" y="160" text-anchor="middle" fill="#A7F3D0" font-size="10">Physics responds</text>
  </g>

  <!-- BOTTOM SUMMARY CARD -->
  <g transform="translate(40, 325)">
    <rect width="840" height="115" rx="8" fill="rgba(15, 23, 42, 0.7)" stroke="#334155" stroke-width="1" />
    <text x="420" y="32" text-anchor="middle" fill="#E2E8F0" font-size="13" font-weight="700">THE ESSENCE OF SPECIAL FUNCTION REGISTERS</text>
    <text x="420" y="60" text-anchor="middle" fill="#94A3B8" font-size="12">An address in the 8051 is not simply an abstract number for storing and fetching variables.</text>
    <text x="420" y="82" text-anchor="middle" fill="#38BDF8" font-size="12" font-weight="600">The architecture gives addresses meaning — transforming numerical byte transfers into physical action.</text>
  </g>
</svg>'''
    with open('Images/intel_8051_sfr_synthesis_flow.svg', 'w', encoding='utf-8') as f:
        f.write(svg)
    print("Created Images/intel_8051_sfr_synthesis_flow.svg")

if __name__ == '__main__':
    create_address_to_hardware_flow()
    create_bit_addressable_sfr_rule()
    create_sfr_synthesis_flow()
