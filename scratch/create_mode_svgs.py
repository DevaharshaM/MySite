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

# Ensure Images dir exists
os.makedirs("Images", exist_ok=True)

# 1. intel_8051_tmod_mode_bits_overview.svg
svg1 = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 940 430" width="100%" height="100%" style="background:#0B1120; font-family:'DM Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1E293B"/>
      <stop offset="100%" stop-color="#0F172A"/>
    </linearGradient>
    <marker id="arr-sky" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#38BDF8" />
    </marker>
    <marker id="arr-amber" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#F59E0B" />
    </marker>
  </defs>

  <!-- Title -->
  <text x="470" y="36" text-anchor="middle" fill="#F8FAFC" font-size="20" font-weight="700" letter-spacing="0.05em">THE TMOD MODE SELECTOR</text>
  <text x="470" y="60" text-anchor="middle" fill="#94A3B8" font-size="13">Two bits in TMOD determine the internal hardware topology of each timer</text>

  <!-- TMOD REGISTER ROW -->
  <g transform="translate(130, 85)">
    <rect width="680" height="74" rx="8" fill="url(#bgGrad)" stroke="#334155" stroke-width="1.5" />
    <rect width="680" height="24" rx="8" fill="#1E293B" />
    <text x="340" y="17" text-anchor="middle" fill="#94A3B8" font-size="11" font-weight="700" letter-spacing="0.05em">TMOD (89H) &#8212; 8-BIT MODE REGISTER</text>

    <!-- 8 Bit cells: Timer 1 (Bits 7..4) and Timer 0 (Bits 3..0) -->
    <!-- Bit 7: GATE -->
    <rect x="20" y="32" width="75" height="32" rx="4" fill="#0F172A" stroke="#334155" />
    <text x="57" y="47" text-anchor="middle" fill="#64748B" font-size="9" font-weight="600">Bit 7</text>
    <text x="57" y="59" text-anchor="middle" fill="#94A3B8" font-family="'IBM Plex Mono', monospace" font-size="10">GATE</text>

    <!-- Bit 6: C/T -->
    <rect x="100" y="32" width="75" height="32" rx="4" fill="#0F172A" stroke="#334155" />
    <text x="137" y="47" text-anchor="middle" fill="#64748B" font-size="9" font-weight="600">Bit 6</text>
    <text x="137" y="59" text-anchor="middle" fill="#94A3B8" font-family="'IBM Plex Mono', monospace" font-size="10">C/T</text>

    <!-- Bit 5: M1 -->
    <rect x="180" y="32" width="75" height="32" rx="4" fill="#1E1B4B" stroke="#6366F1" stroke-width="1.5" />
    <text x="217" y="47" text-anchor="middle" fill="#A5B4FC" font-size="9" font-weight="700">Bit 5</text>
    <text x="217" y="59" text-anchor="middle" fill="#C7D2FE" font-family="'IBM Plex Mono', monospace" font-size="10" font-weight="700">M1</text>

    <!-- Bit 4: M0 -->
    <rect x="260" y="32" width="75" height="32" rx="4" fill="#1E1B4B" stroke="#6366F1" stroke-width="1.5" />
    <text x="297" y="47" text-anchor="middle" fill="#A5B4FC" font-size="9" font-weight="700">Bit 4</text>
    <text x="297" y="59" text-anchor="middle" fill="#C7D2FE" font-family="'IBM Plex Mono', monospace" font-size="10" font-weight="700">M0</text>

    <!-- Divider -->
    <line x1="345" y1="28" x2="345" y2="70" stroke="#475569" stroke-width="1.5" stroke-dasharray="3,3" />

    <!-- Bit 3: GATE -->
    <rect x="355" y="32" width="75" height="32" rx="4" fill="#0F172A" stroke="#334155" />
    <text x="392" y="47" text-anchor="middle" fill="#64748B" font-size="9" font-weight="600">Bit 3</text>
    <text x="392" y="59" text-anchor="middle" fill="#94A3B8" font-family="'IBM Plex Mono', monospace" font-size="10">GATE</text>

    <!-- Bit 2: C/T -->
    <rect x="435" y="32" width="75" height="32" rx="4" fill="#0F172A" stroke="#334155" />
    <text x="472" y="47" text-anchor="middle" fill="#64748B" font-size="9" font-weight="600">Bit 2</text>
    <text x="472" y="59" text-anchor="middle" fill="#94A3B8" font-family="'IBM Plex Mono', monospace" font-size="10">C/T</text>

    <!-- Bit 1: M1 (Highlighted) -->
    <rect x="515" y="32" width="75" height="32" rx="4" fill="#0C4A6E" stroke="#38BDF8" stroke-width="1.8" />
    <text x="552" y="47" text-anchor="middle" fill="#7DD3FC" font-size="9" font-weight="700">Bit 1</text>
    <text x="552" y="59" text-anchor="middle" fill="#38BDF8" font-family="'IBM Plex Mono', monospace" font-size="11" font-weight="700">M1</text>

    <!-- Bit 0: M0 (Highlighted) -->
    <rect x="595" y="32" width="75" height="32" rx="4" fill="#0C4A6E" stroke="#38BDF8" stroke-width="1.8" />
    <text x="632" y="47" text-anchor="middle" fill="#7DD3FC" font-size="9" font-weight="700">Bit 0</text>
    <text x="632" y="59" text-anchor="middle" fill="#38BDF8" font-family="'IBM Plex Mono', monospace" font-size="11" font-weight="700">M0</text>
  </g>

  <!-- Labels under Timer 1 and Timer 0 groups -->
  <text x="290" y="174" text-anchor="middle" fill="#818CF8" font-size="11" font-weight="600">&#9650; Timer 1 Mode Controls</text>
  <text x="650" y="174" text-anchor="middle" fill="#38BDF8" font-size="11" font-weight="600">&#9650; Timer 0 Mode Controls (Active Focus)</text>

  <!-- BUS STEERING ARROWS TO 4 HARDWARE MODES -->
  <path d="M 590 190 L 590 205 L 125 205 L 125 235" fill="none" stroke="#64748B" stroke-width="1.5" marker-end="url(#arr-sky)" />
  <path d="M 590 190 L 590 205 L 355 205 L 355 235" fill="none" stroke="#64748B" stroke-width="1.5" marker-end="url(#arr-sky)" />
  <path d="M 590 190 L 590 205 L 585 205 L 585 235" fill="none" stroke="#64748B" stroke-width="1.5" marker-end="url(#arr-sky)" />
  <path d="M 590 190 L 590 205 L 815 205 L 815 235" fill="none" stroke="#64748B" stroke-width="1.5" marker-end="url(#arr-sky)" />

  <!-- 4 MODE CARDS -->
  <!-- CARD 0: Mode 0 (13-bit) -->
  <g transform="translate(25, 245)">
    <rect width="200" height="155" rx="8" fill="url(#bgGrad)" stroke="#334155" stroke-width="1.5" />
    <rect width="200" height="30" rx="8" fill="#1E293B" />
    <text x="100" y="20" text-anchor="middle" fill="#F8FAFC" font-size="12" font-weight="700">MODE 0 (0 0)</text>
    <text x="100" y="55" text-anchor="middle" fill="#38BDF8" font-size="13" font-weight="600">13-Bit Counter</text>
    <text x="100" y="78" text-anchor="middle" fill="#94A3B8" font-family="'IBM Plex Mono', monospace" font-size="11">THx (8b) + TLx (5b)</text>
    <text x="100" y="102" text-anchor="middle" fill="#E2E8F0" font-size="11">0000H &#8594; 1FFFH</text>
    <text x="100" y="122" text-anchor="middle" fill="#64748B" font-size="10">8,192 max counts</text>
    <rect x="25" y="132" width="150" height="15" rx="3" fill="#0F172A" />
    <text x="100" y="143" text-anchor="middle" fill="#94A3B8" font-size="9">MCS-48 Compatibility</text>
  </g>

  <!-- CARD 1: Mode 1 (16-bit) -->
  <g transform="translate(255, 245)">
    <rect width="200" height="155" rx="8" fill="url(#bgGrad)" stroke="#38BDF8" stroke-width="1.8" />
    <rect width="200" height="30" rx="8" fill="#0C4A6E" />
    <text x="100" y="20" text-anchor="middle" fill="#7DD3FC" font-size="12" font-weight="700">MODE 1 (0 1)</text>
    <text x="100" y="55" text-anchor="middle" fill="#38BDF8" font-size="13" font-weight="600">16-Bit Counter</text>
    <text x="100" y="78" text-anchor="middle" fill="#94A3B8" font-family="'IBM Plex Mono', monospace" font-size="11">THx (8b) : TLx (8b)</text>
    <text x="100" y="102" text-anchor="middle" fill="#E2E8F0" font-size="11">0000H &#8594; FFFFH</text>
    <text x="100" y="122" text-anchor="middle" fill="#64748B" font-size="10">65,536 max counts</text>
    <rect x="25" y="132" width="150" height="15" rx="3" fill="#0F172A" />
    <text x="100" y="143" text-anchor="middle" fill="#38BDF8" font-size="9">General Purpose Timing</text>
  </g>

  <!-- CARD 2: Mode 2 (8-bit Auto-reload) -->
  <g transform="translate(485, 245)">
    <rect width="200" height="155" rx="8" fill="url(#bgGrad)" stroke="#10B981" stroke-width="1.8" />
    <rect width="200" height="30" rx="8" fill="#064E3B" />
    <text x="100" y="20" text-anchor="middle" fill="#6EE7B7" font-size="12" font-weight="700">MODE 2 (1 0)</text>
    <text x="100" y="55" text-anchor="middle" fill="#34D399" font-size="13" font-weight="600">8-Bit Auto-Reload</text>
    <text x="100" y="78" text-anchor="middle" fill="#94A3B8" font-family="'IBM Plex Mono', monospace" font-size="11">TLx counts &#8226; THx reloads</text>
    <text x="100" y="102" text-anchor="middle" fill="#E2E8F0" font-size="11">TLx &#8592; THx on overflow</text>
    <text x="100" y="122" text-anchor="middle" fill="#64748B" font-size="10">1 to 256 exact ticks</text>
    <rect x="25" y="132" width="150" height="15" rx="3" fill="#0F172A" />
    <text x="100" y="143" text-anchor="middle" fill="#34D399" font-size="9">Baud Rates &amp; PWM</text>
  </g>

  <!-- CARD 3: Mode 3 (Split Timer) -->
  <g transform="translate(715, 245)">
    <rect width="200" height="155" rx="8" fill="url(#bgGrad)" stroke="#F59E0B" stroke-width="1.8" />
    <rect width="200" height="30" rx="8" fill="#78350F" />
    <text x="100" y="20" text-anchor="middle" fill="#FDE68A" font-size="12" font-weight="700">MODE 3 (1 1)</text>
    <text x="100" y="55" text-anchor="middle" fill="#FBBF24" font-size="13" font-weight="600">Split Timer 0</text>
    <text x="100" y="78" text-anchor="middle" fill="#94A3B8" font-family="'IBM Plex Mono', monospace" font-size="11">Two 8-Bit Timers</text>
    <text x="100" y="102" text-anchor="middle" fill="#E2E8F0" font-size="11">TL0 (TR0) + TH0 (TR1)</text>
    <text x="100" y="122" text-anchor="middle" fill="#64748B" font-size="10">Timer 1 runs uninhibited</text>
    <rect x="25" y="132" width="150" height="15" rx="3" fill="#0F172A" />
    <text x="100" y="143" text-anchor="middle" fill="#FBBF24" font-size="9">Extra Timer + Baud Gen</text>
  </g>
</svg>'''

with open("Images/intel_8051_tmod_mode_bits_overview.svg", "w", encoding="utf-8") as f:
    f.write(svg1)
validate_svg("Images/intel_8051_tmod_mode_bits_overview.svg")

# 2. intel_8051_timer_mode_0_13bit.svg
svg2 = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 940 380" width="100%" height="100%" style="background:#0B1120; font-family:'DM Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
  <defs>
    <linearGradient id="cardGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1E293B"/>
      <stop offset="100%" stop-color="#0F172A"/>
    </linearGradient>
    <marker id="m-arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#38BDF8" />
    </marker>
    <marker id="m-overflow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#F59E0B" />
    </marker>
  </defs>

  <!-- Title -->
  <text x="470" y="36" text-anchor="middle" fill="#F8FAFC" font-size="20" font-weight="700" letter-spacing="0.05em">MODE 0 &#8212; THE 13-BIT HARDWARE STRUCTURE</text>
  <text x="470" y="60" text-anchor="middle" fill="#94A3B8" font-size="13">8 bits of THx cascaded with the lower 5 bits of TLx (MCS-48 compatibility architecture)</text>

  <!-- HARDWARE FLOW ROW -->
  <g transform="translate(40, 95)">
    <!-- 1. INPUT SOURCE -->
    <g transform="translate(0, 30)">
      <rect width="130" height="120" rx="8" fill="url(#cardGrad)" stroke="#334155" stroke-width="1.5" />
      <rect width="130" height="26" rx="8" fill="#1E293B" />
      <text x="65" y="18" text-anchor="middle" fill="#94A3B8" font-size="10" font-weight="700">INPUT SOURCE</text>
      <text x="65" y="55" text-anchor="middle" fill="#38BDF8" font-size="11" font-weight="600">Osc &#247; 12</text>
      <text x="65" y="70" text-anchor="middle" fill="#64748B" font-size="10">or Pin Tx</text>
      <!-- Gate -->
      <circle cx="65" cy="98" r="10" fill="#0F172A" stroke="#10B981" stroke-width="1.5" />
      <text x="65" y="102" text-anchor="middle" fill="#10B981" font-family="'IBM Plex Mono', monospace" font-size="8">TRx</text>
      <text x="65" y="122" text-anchor="middle" fill="#64748B" font-size="8">Run Switch</text>
    </g>

    <!-- Arrow 1 -->
    <line x1="135" y1="90" x2="165" y2="90" stroke="#38BDF8" stroke-width="2" marker-end="url(#m-arrow)" />

    <!-- 2. TLx REGISTER (8 BITS: 5 ACTIVE, 3 DISCONNECTED) -->
    <g transform="translate(170, 10)">
      <rect width="320" height="160" rx="8" fill="url(#cardGrad)" stroke="#38BDF8" stroke-width="1.5" />
      <rect width="320" height="26" rx="8" fill="#0C4A6E" />
      <text x="160" y="18" text-anchor="middle" fill="#7DD3FC" font-size="11" font-weight="700">TLx REGISTER (LOW BYTE)</text>

      <!-- 8 Bit Cells -->
      <g transform="translate(15, 38)">
        <!-- Bit 7 Unused -->
        <rect x="0" y="0" width="34" height="42" rx="3" fill="#1E293B" stroke="#475569" stroke-dasharray="2,2" />
        <text x="17" y="16" text-anchor="middle" fill="#64748B" font-size="9">D7</text>
        <text x="17" y="32" text-anchor="middle" fill="#475569" font-family="'IBM Plex Mono', monospace" font-size="11">&#8212;</text>

        <!-- Bit 6 Unused -->
        <rect x="37" y="0" width="34" height="42" rx="3" fill="#1E293B" stroke="#475569" stroke-dasharray="2,2" />
        <text x="54" y="16" text-anchor="middle" fill="#64748B" font-size="9">D6</text>
        <text x="54" y="32" text-anchor="middle" fill="#475569" font-family="'IBM Plex Mono', monospace" font-size="11">&#8212;</text>

        <!-- Bit 5 Unused -->
        <rect x="74" y="0" width="34" height="42" rx="3" fill="#1E293B" stroke="#475569" stroke-dasharray="2,2" />
        <text x="91" y="16" text-anchor="middle" fill="#64748B" font-size="9">D5</text>
        <text x="91" y="32" text-anchor="middle" fill="#475569" font-family="'IBM Plex Mono', monospace" font-size="11">&#8212;</text>

        <!-- Bit 4 Active -->
        <rect x="111" y="0" width="34" height="42" rx="3" fill="#064E3B" stroke="#10B981" stroke-width="1.5" />
        <text x="128" y="16" text-anchor="middle" fill="#6EE7B7" font-size="9" font-weight="700">D4</text>
        <text x="128" y="32" text-anchor="middle" fill="#34D399" font-family="'IBM Plex Mono', monospace" font-size="11">b4</text>

        <!-- Bit 3 Active -->
        <rect x="148" y="0" width="34" height="42" rx="3" fill="#064E3B" stroke="#10B981" stroke-width="1.5" />
        <text x="165" y="16" text-anchor="middle" fill="#6EE7B7" font-size="9" font-weight="700">D3</text>
        <text x="165" y="32" text-anchor="middle" fill="#34D399" font-family="'IBM Plex Mono', monospace" font-size="11">b3</text>

        <!-- Bit 2 Active -->
        <rect x="185" y="0" width="34" height="42" rx="3" fill="#064E3B" stroke="#10B981" stroke-width="1.5" />
        <text x="202" y="16" text-anchor="middle" fill="#6EE7B7" font-size="9" font-weight="700">D2</text>
        <text x="202" y="32" text-anchor="middle" fill="#34D399" font-family="'IBM Plex Mono', monospace" font-size="11">b2</text>

        <!-- Bit 1 Active -->
        <rect x="222" y="0" width="34" height="42" rx="3" fill="#064E3B" stroke="#10B981" stroke-width="1.5" />
        <text x="239" y="16" text-anchor="middle" fill="#6EE7B7" font-size="9" font-weight="700">D1</text>
        <text x="239" y="32" text-anchor="middle" fill="#34D399" font-family="'IBM Plex Mono', monospace" font-size="11">b1</text>

        <!-- Bit 0 Active -->
        <rect x="259" y="0" width="34" height="42" rx="3" fill="#064E3B" stroke="#10B981" stroke-width="1.5" />
        <text x="276" y="16" text-anchor="middle" fill="#6EE7B7" font-size="9" font-weight="700">D0</text>
        <text x="276" y="32" text-anchor="middle" fill="#34D399" font-family="'IBM Plex Mono', monospace" font-size="11">b0</text>
      </g>

      <!-- Annotations for TLx -->
      <text x="60" y="98" text-anchor="middle" fill="#64748B" font-size="9">&#9650; Upper 3 bits ignored</text>
      <text x="210" y="98" text-anchor="middle" fill="#34D399" font-size="10" font-weight="600">&#9650; 5-Bit Prescaler Counter (0 to 31 counts)</text>
      <rect x="15" y="112" width="290" height="34" rx="4" fill="#0F172A" />
      <text x="160" y="126" text-anchor="middle" fill="#94A3B8" font-size="10">Rolls over every 32 input ticks (1FH &#8594; 00H)</text>
      <text x="160" y="139" text-anchor="middle" fill="#38BDF8" font-size="10" font-weight="600">Bit 4 overflow cascades directly into THx</text>
    </g>

    <!-- Cascade Arrow from TLx.D4 to THx -->
    <path d="M 495 90 L 530 90" fill="none" stroke="#10B981" stroke-width="2" marker-end="url(#m-arrow)" />
    <text x="512" y="80" text-anchor="middle" fill="#10B981" font-size="9" font-weight="700">&#247; 32</text>

    <!-- 3. THx REGISTER (8 BITS: FULL COUNTER) -->
    <g transform="translate(535, 10)">
      <rect width="230" height="160" rx="8" fill="url(#cardGrad)" stroke="#10B981" stroke-width="1.5" />
      <rect width="230" height="26" rx="8" fill="#064E3B" />
      <text x="115" y="18" text-anchor="middle" fill="#6EE7B7" font-size="11" font-weight="700">THx REGISTER (HIGH BYTE)</text>

      <g transform="translate(15, 38)">
        <rect width="200" height="42" rx="4" fill="#064E3B" stroke="#10B981" stroke-width="1.5" />
        <text x="100" y="22" text-anchor="middle" fill="#E2E8F0" font-size="11" font-weight="700">Full 8-Bit Counter (D7..D0)</text>
        <text x="100" y="36" text-anchor="middle" fill="#6EE7B7" font-family="'IBM Plex Mono', monospace" font-size="10">Increments 0 to 255</text>
      </g>

      <rect x="15" y="94" width="200" height="52" rx="4" fill="#0F172A" />
      <text x="115" y="112" text-anchor="middle" fill="#94A3B8" font-size="10">Combines with 5-bit TLx</text>
      <text x="115" y="126" text-anchor="middle" fill="#F8FAFC" font-family="'IBM Plex Mono', monospace" font-size="11" font-weight="600">Total = 13 Bits (8,192)</text>
      <text x="115" y="139" text-anchor="middle" fill="#34D399" font-size="9">Count range: 0000H &#8594; 1FFFH</text>
    </g>

    <!-- Overflow Arrow from THx to TFx -->
    <line x1="770" y1="90" x2="800" y2="90" stroke="#F59E0B" stroke-width="2" marker-end="url(#m-overflow)" />

    <!-- 4. OVERFLOW FLAG TFx -->
    <g transform="translate(805, 30)">
      <rect width="90" height="120" rx="8" fill="url(#cardGrad)" stroke="#F59E0B" stroke-width="1.5" />
      <rect width="90" height="26" rx="8" fill="#78350F" />
      <text x="45" y="18" text-anchor="middle" fill="#FDE68A" font-size="10" font-weight="700">OVERFLOW</text>
      <text x="45" y="58" text-anchor="middle" fill="#F59E0B" font-size="14" font-weight="700">TFx = 1</text>
      <text x="45" y="78" text-anchor="middle" fill="#94A3B8" font-size="9">in TCON</text>
      <rect x="10" y="88" width="70" height="22" rx="3" fill="#0F172A" />
      <text x="45" y="102" text-anchor="middle" fill="#CBD5E1" font-size="8">At 1FFFH &#8594; 0</text>
    </g>
  </g>

  <!-- Bottom Explanatory Banner -->
  <g transform="translate(40, 290)">
    <rect width="860" height="60" rx="6" fill="#1E293B" stroke="#334155" />
    <text x="25" y="24" fill="#38BDF8" font-size="11" font-weight="700">ARCHITECTURAL CONTEXT &#8212; WHY 13 BITS?</text>
    <text x="25" y="44" fill="#CBD5E1" font-size="11">The predecessor MCS-48 (8048) microcontroller featured an internal 5-bit prescaler followed by an 8-bit timer. Mode 0 in the 8051 replicates this identical 13-bit hardware behavior, ensuring legacy timing loops and control routines could be ported without modification.</text>
  </g>
</svg>'''

with open("Images/intel_8051_timer_mode_0_13bit.svg", "w", encoding="utf-8") as f:
    f.write(svg2)
validate_svg("Images/intel_8051_timer_mode_0_13bit.svg")

# 3. intel_8051_timer_mode_1_16bit.svg
svg3 = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 940 380" width="100%" height="100%" style="background:#0B1120; font-family:'DM Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
  <defs>
    <linearGradient id="cardGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1E293B"/>
      <stop offset="100%" stop-color="#0F172A"/>
    </linearGradient>
    <marker id="m1-arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#38BDF8" />
    </marker>
    <marker id="m1-overflow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#F59E0B" />
    </marker>
  </defs>

  <!-- Title -->
  <text x="470" y="36" text-anchor="middle" fill="#F8FAFC" font-size="20" font-weight="700" letter-spacing="0.05em">MODE 1 &#8212; THE FULL 16-BIT CASCADED COUNTER</text>
  <text x="470" y="60" text-anchor="middle" fill="#94A3B8" font-size="13">All 8 bits of TLx cascaded into all 8 bits of THx for a total of 65,536 counting states</text>

  <!-- HARDWARE FLOW ROW -->
  <g transform="translate(40, 95)">
    <!-- 1. INPUT SOURCE -->
    <g transform="translate(0, 30)">
      <rect width="130" height="120" rx="8" fill="url(#cardGrad)" stroke="#334155" stroke-width="1.5" />
      <rect width="130" height="26" rx="8" fill="#1E293B" />
      <text x="65" y="18" text-anchor="middle" fill="#94A3B8" font-size="10" font-weight="700">INPUT SOURCE</text>
      <text x="65" y="55" text-anchor="middle" fill="#38BDF8" font-size="11" font-weight="600">Osc &#247; 12</text>
      <text x="65" y="70" text-anchor="middle" fill="#64748B" font-size="10">or Pin Tx</text>
      <!-- Gate -->
      <circle cx="65" cy="98" r="10" fill="#0F172A" stroke="#10B981" stroke-width="1.5" />
      <text x="65" y="102" text-anchor="middle" fill="#10B981" font-family="'IBM Plex Mono', monospace" font-size="8">TRx</text>
      <text x="65" y="122" text-anchor="middle" fill="#64748B" font-size="8">Run Switch</text>
    </g>

    <!-- Arrow 1 -->
    <line x1="135" y1="90" x2="175" y2="90" stroke="#38BDF8" stroke-width="2" marker-end="url(#m1-arrow)" />

    <!-- 2. TLx REGISTER (FULL 8 BITS) -->
    <g transform="translate(180, 10)">
      <rect width="260" height="160" rx="8" fill="url(#cardGrad)" stroke="#38BDF8" stroke-width="1.5" />
      <rect width="260" height="26" rx="8" fill="#0C4A6E" />
      <text x="130" y="18" text-anchor="middle" fill="#7DD3FC" font-size="11" font-weight="700">TLx REGISTER (BITS 0..7)</text>

      <g transform="translate(15, 38)">
        <rect width="230" height="42" rx="4" fill="#0369A1" stroke="#38BDF8" stroke-width="1.5" />
        <text x="115" y="22" text-anchor="middle" fill="#FFFFFF" font-size="11" font-weight="700">Low Byte Counter (00H &#8594; FFH)</text>
        <text x="115" y="36" text-anchor="middle" fill="#BAE6FD" font-family="'IBM Plex Mono', monospace" font-size="10">Increments every 1 &#181;s tick</text>
      </g>

      <rect x="15" y="94" width="230" height="52" rx="4" fill="#0F172A" />
      <text x="115" y="112" text-anchor="middle" fill="#94A3B8" font-size="10">On rollover: FFH &#8594; 00H</text>
      <text x="115" y="126" text-anchor="middle" fill="#38BDF8" font-size="11" font-weight="600">Sends 1 pulse to THx</text>
      <text x="115" y="139" text-anchor="middle" fill="#64748B" font-size="9">Exact frequency: Input &#247; 256</text>
    </g>

    <!-- Cascade Arrow from TLx to THx -->
    <path d="M 445 90 L 485 90" fill="none" stroke="#38BDF8" stroke-width="2" marker-end="url(#m1-arrow)" />
    <text x="465" y="80" text-anchor="middle" fill="#38BDF8" font-size="9" font-weight="700">&#247; 256</text>

    <!-- 3. THx REGISTER (FULL 8 BITS) -->
    <g transform="translate(490, 10)">
      <rect width="260" height="160" rx="8" fill="url(#cardGrad)" stroke="#10B981" stroke-width="1.5" />
      <rect width="260" height="26" rx="8" fill="#064E3B" />
      <text x="130" y="18" text-anchor="middle" fill="#6EE7B7" font-size="11" font-weight="700">THx REGISTER (BITS 8..15)</text>

      <g transform="translate(15, 38)">
        <rect width="230" height="42" rx="4" fill="#064E3B" stroke="#10B981" stroke-width="1.5" />
        <text x="115" y="22" text-anchor="middle" fill="#FFFFFF" font-size="11" font-weight="700">High Byte Counter (00H &#8594; FFH)</text>
        <text x="115" y="36" text-anchor="middle" fill="#A7F3D0" font-family="'IBM Plex Mono', monospace" font-size="10">Increments every 256 &#181;s</text>
      </g>

      <rect x="15" y="94" width="230" height="52" rx="4" fill="#0F172A" />
      <text x="115" y="112" text-anchor="middle" fill="#94A3B8" font-size="10">Combined 16-bit register pair</text>
      <text x="115" y="126" text-anchor="middle" fill="#F8FAFC" font-family="'IBM Plex Mono', monospace" font-size="11" font-weight="600">0000H &#8594; FFFFH (65,536)</text>
      <text x="115" y="139" text-anchor="middle" fill="#34D399" font-size="9">Max interval: 65,536 &#181;s = 65.536 ms</text>
    </g>

    <!-- Overflow Arrow from THx to TFx -->
    <line x1="755" y1="90" x2="795" y2="90" stroke="#F59E0B" stroke-width="2" marker-end="url(#m1-overflow)" />

    <!-- 4. OVERFLOW FLAG TFx -->
    <g transform="translate(800, 30)">
      <rect width="95" height="120" rx="8" fill="url(#cardGrad)" stroke="#F59E0B" stroke-width="1.5" />
      <rect width="95" height="26" rx="8" fill="#78350F" />
      <text x="47" y="18" text-anchor="middle" fill="#FDE68A" font-size="10" font-weight="700">OVERFLOW</text>
      <text x="47" y="58" text-anchor="middle" fill="#F59E0B" font-size="14" font-weight="700">TFx = 1</text>
      <text x="47" y="78" text-anchor="middle" fill="#94A3B8" font-size="9">in TCON</text>
      <rect x="10" y="88" width="75" height="22" rx="3" fill="#0F172A" />
      <text x="47" y="102" text-anchor="middle" fill="#CBD5E1" font-size="8">At FFFFH &#8594; 0000H</text>
    </g>
  </g>

  <!-- Bottom Explanatory Banner -->
  <g transform="translate(40, 290)">
    <rect width="860" height="60" rx="6" fill="#1E293B" stroke="#334155" />
    <text x="25" y="24" fill="#38BDF8" font-size="11" font-weight="700">ARCHITECTURAL REALIZATION &#8212; PRE-LOADING THE COUNTER</text>
    <text x="25" y="44" fill="#CBD5E1" font-size="11">To measure an exact interval of N counts, software loads the 16-bit registers with (65536 &#8722; N). The counter counts up towards FFFFH, and the moment it ticks past the ceiling, TFx alerts software. After overflow, software must manually reload THx and TLx for the next cycle.</text>
  </g>
</svg>'''

with open("Images/intel_8051_timer_mode_1_16bit.svg", "w", encoding="utf-8") as f:
    f.write(svg3)
validate_svg("Images/intel_8051_timer_mode_1_16bit.svg")

# 4. intel_8051_timer_mode_2_auto_reload.svg
svg4 = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 940 410" width="100%" height="100%" style="background:#0B1120; font-family:'DM Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
  <defs>
    <linearGradient id="cardGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1E293B"/>
      <stop offset="100%" stop-color="#0F172A"/>
    </linearGradient>
    <marker id="m2-arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#38BDF8" />
    </marker>
    <marker id="m2-reload" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#10B981" />
    </marker>
    <marker id="m2-overflow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#F59E0B" />
    </marker>
  </defs>

  <!-- Title -->
  <text x="470" y="36" text-anchor="middle" fill="#F8FAFC" font-size="20" font-weight="700" letter-spacing="0.05em">MODE 2 &#8212; THE 8-BIT AUTO-RELOAD ARCHITECTURE</text>
  <text x="470" y="60" text-anchor="middle" fill="#94A3B8" font-size="13">TLx acts as the active counter while THx holds the permanent reload value in silicon</text>

  <!-- ARCHITECTURE DIAGRAM -->
  <g transform="translate(60, 85)">
    <!-- 1. THx RELOAD VALUE HOLDER (UPPER BLOCK) -->
    <g transform="translate(230, 10)">
      <rect width="320" height="95" rx="8" fill="url(#cardGrad)" stroke="#10B981" stroke-width="1.8" />
      <rect width="320" height="26" rx="8" fill="#064E3B" />
      <text x="160" y="18" text-anchor="middle" fill="#6EE7B7" font-size="11" font-weight="700">THx REGISTER &#8212; PRESERVED RELOAD VALUE</text>

      <rect x="25" y="38" width="270" height="42" rx="4" fill="#064E3B" stroke="#10B981" />
      <text x="160" y="55" text-anchor="middle" fill="#FFFFFF" font-size="11" font-weight="700">Static Storage Latch (Unchanged by Counting)</text>
      <text x="160" y="70" text-anchor="middle" fill="#A7F3D0" font-family="'IBM Plex Mono', monospace" font-size="10">E.g., TH1 = FDH (for 9600 Baud at 11.0592 MHz)</text>
    </g>

    <!-- 2. INPUT SOURCE & TRx GATE -->
    <g transform="translate(0, 155)">
      <rect width="140" height="110" rx="8" fill="url(#cardGrad)" stroke="#334155" stroke-width="1.5" />
      <rect width="140" height="26" rx="8" fill="#1E293B" />
      <text x="70" y="18" text-anchor="middle" fill="#94A3B8" font-size="10" font-weight="700">INPUT SOURCE</text>
      <text x="70" y="52" text-anchor="middle" fill="#38BDF8" font-size="11" font-weight="600">Osc &#247; 12</text>
      <text x="70" y="66" text-anchor="middle" fill="#64748B" font-size="10">or Pin Tx Pulses</text>
      <circle cx="70" cy="88" r="9" fill="#0F172A" stroke="#10B981" stroke-width="1.5" />
      <text x="70" y="91" text-anchor="middle" fill="#10B981" font-family="'IBM Plex Mono', monospace" font-size="7">TRx</text>
    </g>

    <!-- Arrow from Input to TLx -->
    <line x1="145" y1="210" x2="220" y2="210" stroke="#38BDF8" stroke-width="2" marker-end="url(#m2-arrow)" />

    <!-- 3. TLx LIVE COUNTING REGISTER (LOWER BLOCK) -->
    <g transform="translate(230, 155)">
      <rect width="320" height="110" rx="8" fill="url(#cardGrad)" stroke="#38BDF8" stroke-width="1.8" />
      <rect width="320" height="26" rx="8" fill="#0C4A6E" />
      <text x="160" y="18" text-anchor="middle" fill="#7DD3FC" font-size="11" font-weight="700">TLx REGISTER &#8212; ACTIVE 8-BIT COUNTER</text>

      <g transform="translate(25, 38)">
        <rect width="270" height="42" rx="4" fill="#0369A1" stroke="#38BDF8" stroke-width="1.5" />
        <text x="135" y="22" text-anchor="middle" fill="#FFFFFF" font-size="11" font-weight="700">Live Counter: Increments [THx Value] &#8594; FFH</text>
        <text x="135" y="36" text-anchor="middle" fill="#BAE6FD" font-family="'IBM Plex Mono', monospace" font-size="10">Reaches ceiling at FFH &#8594; rolls to 00H</text>
      </g>
      <text x="160" y="98" text-anchor="middle" fill="#94A3B8" font-size="10">Capacity: 1 to 256 clock machine cycles</text>
    </g>

    <!-- 4. HARDWARE AUTO-RELOAD PATH (DOWNWARD ARROW FROM THx TO TLx) -->
    <path d="M 390 110 L 390 145" fill="none" stroke="#10B981" stroke-width="2.5" marker-end="url(#m2-reload)" />
    <rect x="290" y="118" width="200" height="20" rx="3" fill="#064E3B" stroke="#10B981" />
    <text x="390" y="132" text-anchor="middle" fill="#A7F3D0" font-size="9" font-weight="700">SILICON AUTO-RELOAD (TLx &#8592; THx)</text>

    <!-- 5. OVERFLOW OUTPUT PATH (TO TFx AND OUTSIDE) -->
    <path d="M 555 210 L 650 210" fill="none" stroke="#F59E0B" stroke-width="2" marker-end="url(#m2-overflow)" />
    <text x="600" y="200" text-anchor="middle" fill="#F59E0B" font-size="9" font-weight="700">FFH &#8594; 00H</text>

    <!-- 6. OVERFLOW FLAG TFx -->
    <g transform="translate(660, 155)">
      <rect width="160" height="110" rx="8" fill="url(#cardGrad)" stroke="#F59E0B" stroke-width="1.5" />
      <rect width="160" height="26" rx="8" fill="#78350F" />
      <text x="80" y="18" text-anchor="middle" fill="#FDE68A" font-size="10" font-weight="700">TFx FLAG (TCON)</text>

      <text x="80" y="55" text-anchor="middle" fill="#F59E0B" font-size="14" font-weight="700">TFx = 1</text>
      <text x="80" y="72" text-anchor="middle" fill="#CBD5E1" font-size="10">Alerts CPU / ISR</text>
      <rect x="15" y="82" width="130" height="20" rx="3" fill="#0F172A" />
      <text x="80" y="96" text-anchor="middle" fill="#94A3B8" font-size="9">Or Drives Serial Clock</text>
    </g>
  </g>

  <!-- Bottom Explanatory Banner -->
  <g transform="translate(40, 335)">
    <rect width="860" height="60" rx="6" fill="#1E293B" stroke="#334155" />
    <text x="25" y="24" fill="#34D399" font-size="11" font-weight="700">THE ESSENCE OF AUTO-RELOAD &#8212; ZERO JITTER, ZERO CPU OVERHEAD</text>
    <text x="25" y="44" fill="#CBD5E1" font-size="11">In Mode 1, software had to reload THx:TLx after every overflow, introducing interrupt latency and timing jitter. In Mode 2, dedicated silicon transfers the THx value into TLx on the exact clock edge of the overflow. The timer never stops, never misses a cycle, and never stutters.</text>
  </g>
</svg>'''

with open("Images/intel_8051_timer_mode_2_auto_reload.svg", "w", encoding="utf-8") as f:
    f.write(svg4)
validate_svg("Images/intel_8051_timer_mode_2_auto_reload.svg")

# 5. intel_8051_timer_mode_3_split.svg
svg5 = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 450" width="100%" height="100%" style="background:#0B1120; font-family:'DM Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
  <defs>
    <linearGradient id="cardGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1E293B"/>
      <stop offset="100%" stop-color="#0F172A"/>
    </linearGradient>
    <marker id="m3-sky" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#38BDF8" />
    </marker>
    <marker id="m3-purple" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#A855F7" />
    </marker>
    <marker id="m3-amber" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#F59E0B" />
    </marker>
  </defs>

  <!-- Title -->
  <text x="480" y="36" text-anchor="middle" fill="#F8FAFC" font-size="20" font-weight="700" letter-spacing="0.05em">MODE 3 &#8212; WHEN TIMER 0 SPLITS INTO TWO INDEPENDENT COUNTERS</text>
  <text x="480" y="60" text-anchor="middle" fill="#94A3B8" font-size="13">TL0 and TH0 operate as two distinct 8-bit timers by borrowing Timer 1's control and flag bits</text>

  <!-- SPLIT TIMERS ROW -->
  <g transform="translate(40, 85)">
    <!-- LEFT PANEL: TL0 (Timer 0 Section 1) -->
    <g transform="translate(0, 0)">
      <rect width="425" height="205" rx="8" fill="url(#cardGrad)" stroke="#38BDF8" stroke-width="1.8" />
      <rect width="425" height="28" rx="8" fill="#0C4A6E" />
      <text x="212" y="19" text-anchor="middle" fill="#7DD3FC" font-size="12" font-weight="700">TL0 &#8212; 8-BIT TIMER / COUNTER</text>

      <!-- Source input -->
      <g transform="translate(20, 42)">
        <rect width="105" height="60" rx="4" fill="#0F172A" stroke="#334155" />
        <text x="52" y="16" text-anchor="middle" fill="#94A3B8" font-size="9">Selectable via C/T</text>
        <text x="52" y="32" text-anchor="middle" fill="#38BDF8" font-size="10" font-weight="600">Osc &#247; 12</text>
        <text x="52" y="47" text-anchor="middle" fill="#64748B" font-size="9">or Pin T0 (P3.4)</text>
      </g>

      <!-- Gate switch TR0 -->
      <g transform="translate(145, 52)">
        <circle cx="20" cy="20" r="14" fill="#0F172A" stroke="#10B981" stroke-width="1.5" />
        <text x="20" y="24" text-anchor="middle" fill="#10B981" font-family="'IBM Plex Mono', monospace" font-size="9" font-weight="700">TR0</text>
        <text x="20" y="45" text-anchor="middle" fill="#94A3B8" font-size="8">TCON.4</text>
      </g>

      <!-- Connecting line to TL0 counter -->
      <line x1="125" y1="72" x2="140" y2="72" stroke="#38BDF8" stroke-width="1.5" />
      <line x1="165" y1="72" x2="195" y2="72" stroke="#38BDF8" stroke-width="1.5" marker-end="url(#m3-sky)" />

      <!-- TL0 8-bit counter block -->
      <g transform="translate(200, 42)">
        <rect width="115" height="60" rx="4" fill="#0369A1" stroke="#38BDF8" stroke-width="1.5" />
        <text x="57" y="20" text-anchor="middle" fill="#FFFFFF" font-size="11" font-weight="700">TL0 Register</text>
        <text x="57" y="36" text-anchor="middle" fill="#BAE6FD" font-family="'IBM Plex Mono', monospace" font-size="10">8-Bit (00..FFH)</text>
        <text x="57" y="50" text-anchor="middle" fill="#7DD3FC" font-size="8">256 Max Counts</text>
      </g>

      <!-- Overflow to TF0 -->
      <line x1="315" y1="72" x2="340" y2="72" stroke="#F59E0B" stroke-width="1.5" marker-end="url(#m3-amber)" />

      <g transform="translate(345, 42)">
        <rect width="65" height="60" rx="4" fill="#78350F" stroke="#F59E0B" stroke-width="1.5" />
        <text x="32" y="20" text-anchor="middle" fill="#FDE68A" font-size="10" font-weight="700">TF0</text>
        <text x="32" y="36" text-anchor="middle" fill="#F59E0B" font-size="11" font-weight="700">= 1</text>
        <text x="32" y="50" text-anchor="middle" fill="#CBD5E1" font-size="8">TCON.5</text>
      </g>

      <!-- Summary box -->
      <rect x="20" y="118" width="385" height="72" rx="4" fill="#0F172A" stroke="#334155" />
      <text x="35" y="137" fill="#38BDF8" font-size="10" font-weight="700">&#8226; Uses Normal Timer 0 Controls:</text>
      <text x="45" y="153" fill="#CBD5E1" font-size="10">&#8212; Run control: TR0 (TCON.4) and GATE0 (TMOD.3)</text>
      <text x="45" y="168" fill="#CBD5E1" font-size="10">&#8212; Input selector: C/T0 (TMOD.2) selects Timer or Counter mode</text>
      <text x="45" y="183" fill="#CBD5E1" font-size="10">&#8212; Overflow interrupt: TF0 (TCON.5, vector at 000BH)</text>
    </g>

    <!-- RIGHT PANEL: TH0 (Timer 0 Section 2 - Borrowing Timer 1 controls) -->
    <g transform="translate(455, 0)">
      <rect width="425" height="205" rx="8" fill="url(#cardGrad)" stroke="#A855F7" stroke-width="1.8" />
      <rect width="425" height="28" rx="8" fill="#581C87" />
      <text x="212" y="19" text-anchor="middle" fill="#E9D5FF" font-size="12" font-weight="700">TH0 &#8212; 8-BIT TIMER (BORROWS TIMER 1 BITS)</text>

      <!-- Source input (Machine cycle ONLY) -->
      <g transform="translate(20, 42)">
        <rect width="105" height="60" rx="4" fill="#0F172A" stroke="#334155" />
        <text x="52" y="16" text-anchor="middle" fill="#94A3B8" font-size="9">Fixed Internal Source</text>
        <text x="52" y="32" text-anchor="middle" fill="#A855F7" font-size="10" font-weight="600">Osc &#247; 12</text>
        <text x="52" y="47" text-anchor="middle" fill="#64748B" font-size="8">(Timer mode ONLY)</text>
      </g>

      <!-- Gate switch TR1 (Borrowed!) -->
      <g transform="translate(145, 52)">
        <circle cx="20" cy="20" r="14" fill="#0F172A" stroke="#A855F7" stroke-width="1.8" />
        <text x="20" y="24" text-anchor="middle" fill="#C084FC" font-family="'IBM Plex Mono', monospace" font-size="9" font-weight="700">TR1</text>
        <text x="20" y="45" text-anchor="middle" fill="#E9D5FF" font-size="8">BORROWED</text>
      </g>

      <!-- Connecting line to TH0 counter -->
      <line x1="125" y1="72" x2="140" y2="72" stroke="#A855F7" stroke-width="1.5" />
      <line x1="165" y1="72" x2="195" y2="72" stroke="#A855F7" stroke-width="1.5" marker-end="url(#m3-purple)" />

      <!-- TH0 8-bit counter block -->
      <g transform="translate(200, 42)">
        <rect width="115" height="60" rx="4" fill="#6B21A8" stroke="#A855F7" stroke-width="1.5" />
        <text x="57" y="20" text-anchor="middle" fill="#FFFFFF" font-size="11" font-weight="700">TH0 Register</text>
        <text x="57" y="36" text-anchor="middle" fill="#F3E8FF" font-family="'IBM Plex Mono', monospace" font-size="10">8-Bit (00..FFH)</text>
        <text x="57" y="50" text-anchor="middle" fill="#D8B4FE" font-size="8">256 Max Counts</text>
      </g>

      <!-- Overflow to TF1 (Borrowed!) -->
      <line x1="315" y1="72" x2="340" y2="72" stroke="#F59E0B" stroke-width="1.5" marker-end="url(#m3-amber)" />

      <g transform="translate(345, 42)">
        <rect width="65" height="60" rx="4" fill="#78350F" stroke="#F59E0B" stroke-width="1.5" />
        <text x="32" y="20" text-anchor="middle" fill="#FDE68A" font-size="10" font-weight="700">TF1</text>
        <text x="32" y="36" text-anchor="middle" fill="#F59E0B" font-size="11" font-weight="700">= 1</text>
        <text x="32" y="50" text-anchor="middle" fill="#CBD5E1" font-size="8">BORROWED</text>
      </g>

      <!-- Summary box -->
      <rect x="20" y="118" width="385" height="72" rx="4" fill="#0F172A" stroke="#334155" />
      <text x="35" y="137" fill="#C084FC" font-size="10" font-weight="700">&#8226; Commandeers Timer 1 Resources:</text>
      <text x="45" y="153" fill="#CBD5E1" font-size="10">&#8212; Run control: TR1 (TCON.6) now turns TH0 on and off!</text>
      <text x="45" y="168" fill="#CBD5E1" font-size="10">&#8212; Input source: Strictly internal timer (Osc &#247; 12)</text>
      <text x="45" y="183" fill="#CBD5E1" font-size="10">&#8212; Overflow interrupt: TF1 (TCON.7, vector at 001BH)</text>
    </g>
  </g>

  <!-- LOWER PANEL: WHAT HAPPENS TO TIMER 1? -->
  <g transform="translate(40, 310)">
    <rect width="880" height="115" rx="8" fill="#1E293B" stroke="#475569" stroke-width="1.5" />
    <rect width="880" height="26" rx="8" fill="#334155" />
    <text x="440" y="18" text-anchor="middle" fill="#F8FAFC" font-size="11" font-weight="700">CONSEQUENCE: WHAT HAPPENS TO TIMER 1 IN MODE 3?</text>

    <g transform="translate(25, 38)">
      <text x="0" y="15" fill="#34D399" font-size="11" font-weight="700">&#8226; Timer 1 loses its control bit (TR1) and its interrupt flag (TF1).</text>
      <text x="0" y="32" fill="#CBD5E1" font-size="11">&#8226; Can Timer 1 still count? <tspan fill="#38BDF8" font-weight="600">Yes.</tspan> Timer 1 can still be placed in Mode 0, Mode 1, or Mode 2. It turns on automatically when switched into any mode other than Mode 3.</text>
      <text x="0" y="49" fill="#CBD5E1" font-size="11">&#8226; Because it has no overflow flag (TF1) to trigger interrupts, Timer 1 cannot service periodic software tasks.</text>
      <text x="0" y="66" fill="#FBBF24" font-size="11" font-weight="600">&#8226; The Perfect Partnership: Timer 1 runs continuously in Mode 2 as the autonomous Baud Rate Generator for the UART, freeing TH0 &amp; TL0 for application timing!</text>
    </g>
  </g>
</svg>'''

with open("Images/intel_8051_timer_mode_3_split.svg", "w", encoding="utf-8") as f:
    f.write(svg5)
validate_svg("Images/intel_8051_timer_mode_3_split.svg")

# 6. intel_8051_four_modes_comparison.svg
svg6 = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 480" width="100%" height="100%" style="background:#0B1120; font-family:'DM Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
  <defs>
    <linearGradient id="rowGrad0" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1E293B"/>
      <stop offset="100%" stop-color="#0F172A"/>
    </linearGradient>
  </defs>

  <!-- Title -->
  <text x="480" y="36" text-anchor="middle" fill="#F8FAFC" font-size="20" font-weight="700" letter-spacing="0.05em">ONE PIECE OF SILICON &#8212; FOUR INTERNAL TOPOLOGIES</text>
  <text x="480" y="60" text-anchor="middle" fill="#94A3B8" font-size="13">How the M1, M0 control bits re-route the internal data paths of the 8051 timer hardware</text>

  <!-- 4 ROWS -->
  <!-- ROW 0: MODE 0 -->
  <g transform="translate(40, 85)">
    <rect width="880" height="75" rx="6" fill="url(#rowGrad0)" stroke="#334155" stroke-width="1.5" />
    <!-- Mode Badge -->
    <rect x="15" y="15" width="110" height="45" rx="4" fill="#0F172A" stroke="#64748B" />
    <text x="70" y="34" text-anchor="middle" fill="#F8FAFC" font-size="11" font-weight="700">MODE 0</text>
    <text x="70" y="50" text-anchor="middle" fill="#94A3B8" font-family="'IBM Plex Mono', monospace" font-size="11">M1=0  M0=0</text>

    <!-- Architecture Visual -->
    <g transform="translate(145, 15)">
      <rect width="180" height="45" rx="4" fill="#1E293B" stroke="#475569" />
      <text x="90" y="24" text-anchor="middle" fill="#CBD5E1" font-size="11" font-weight="600">THx (8b) + TLx (5b)</text>
      <text x="90" y="40" text-anchor="middle" fill="#64748B" font-size="9">Upper 3 bits of TLx unused</text>
    </g>

    <!-- Details -->
    <g transform="translate(345, 18)">
      <text x="0" y="16" fill="#38BDF8" font-size="11" font-weight="600">13-Bit Counter</text>
      <text x="0" y="34" fill="#94A3B8" font-size="10">Counts 0000H &#8594; 1FFFH (8,192 states). Rollover sets TFx.</text>
    </g>

    <!-- Application / Significance -->
    <g transform="translate(640, 18)">
      <rect width="220" height="38" rx="4" fill="#0F172A" />
      <text x="110" y="16" text-anchor="middle" fill="#E2E8F0" font-size="10" font-weight="600">MCS-48 Backward Compatibility</text>
      <text x="110" y="30" text-anchor="middle" fill="#64748B" font-size="9">Legacy compatibility with 8048 code</text>
    </g>
  </g>

  <!-- ROW 1: MODE 1 -->
  <g transform="translate(40, 175)">
    <rect width="880" height="75" rx="6" fill="url(#rowGrad0)" stroke="#38BDF8" stroke-width="1.5" />
    <!-- Mode Badge -->
    <rect x="15" y="15" width="110" height="45" rx="4" fill="#0C4A6E" stroke="#38BDF8" />
    <text x="70" y="34" text-anchor="middle" fill="#7DD3FC" font-size="11" font-weight="700">MODE 1</text>
    <text x="70" y="50" text-anchor="middle" fill="#38BDF8" font-family="'IBM Plex Mono', monospace" font-size="11">M1=0  M0=1</text>

    <!-- Architecture Visual -->
    <g transform="translate(145, 15)">
      <rect width="180" height="45" rx="4" fill="#0C4A6E" stroke="#38BDF8" />
      <text x="90" y="24" text-anchor="middle" fill="#FFFFFF" font-size="11" font-weight="700">THx (8b) : TLx (8b)</text>
      <text x="90" y="40" text-anchor="middle" fill="#7DD3FC" font-size="9">Full 16-bit unified cascade</text>
    </g>

    <!-- Details -->
    <g transform="translate(345, 18)">
      <text x="0" y="16" fill="#38BDF8" font-size="11" font-weight="600">16-Bit Counter</text>
      <text x="0" y="34" fill="#94A3B8" font-size="10">Counts 0000H &#8594; FFFFH (65,536 states). Rollover sets TFx.</text>
    </g>

    <!-- Application / Significance -->
    <g transform="translate(640, 18)">
      <rect width="220" height="38" rx="4" fill="#0F172A" />
      <text x="110" y="16" text-anchor="middle" fill="#38BDF8" font-size="10" font-weight="600">Longest Time Delays</text>
      <text x="110" y="30" text-anchor="middle" fill="#94A3B8" font-size="9">Up to 65.536 ms intervals (at 12 MHz)</text>
    </g>
  </g>

  <!-- ROW 2: MODE 2 -->
  <g transform="translate(40, 265)">
    <rect width="880" height="75" rx="6" fill="url(#rowGrad0)" stroke="#10B981" stroke-width="1.5" />
    <!-- Mode Badge -->
    <rect x="15" y="15" width="110" height="45" rx="4" fill="#064E3B" stroke="#10B981" />
    <text x="70" y="34" text-anchor="middle" fill="#6EE7B7" font-size="11" font-weight="700">MODE 2</text>
    <text x="70" y="50" text-anchor="middle" fill="#34D399" font-family="'IBM Plex Mono', monospace" font-size="11">M1=1  M0=0</text>

    <!-- Architecture Visual -->
    <g transform="translate(145, 15)">
      <rect width="180" height="45" rx="4" fill="#064E3B" stroke="#10B981" />
      <text x="90" y="24" text-anchor="middle" fill="#FFFFFF" font-size="11" font-weight="700">TLx (Count) &#8592; THx (Reload)</text>
      <text x="90" y="40" text-anchor="middle" fill="#6EE7B7" font-size="9">Silicon auto-reload on overflow</text>
    </g>

    <!-- Details -->
    <g transform="translate(345, 18)">
      <text x="0" y="16" fill="#34D399" font-size="11" font-weight="600">8-Bit Auto-Reload</text>
      <text x="0" y="34" fill="#94A3B8" font-size="10">Counts [THx] &#8594; FFH (1 to 256 ticks). Never stops or drifts.</text>
    </g>

    <!-- Application / Significance -->
    <g transform="translate(640, 18)">
      <rect width="220" height="38" rx="4" fill="#0F172A" />
      <text x="110" y="16" text-anchor="middle" fill="#34D399" font-size="10" font-weight="600">UART Baud Rates &amp; Clean Pulses</text>
      <text x="110" y="30" text-anchor="middle" fill="#94A3B8" font-size="9">Zero jitter, zero software reload latency</text>
    </g>
  </g>

  <!-- ROW 3: MODE 3 -->
  <g transform="translate(40, 355)">
    <rect width="880" height="75" rx="6" fill="url(#rowGrad0)" stroke="#F59E0B" stroke-width="1.5" />
    <!-- Mode Badge -->
    <rect x="15" y="15" width="110" height="45" rx="4" fill="#78350F" stroke="#F59E0B" />
    <text x="70" y="34" text-anchor="middle" fill="#FDE68A" font-size="11" font-weight="700">MODE 3</text>
    <text x="70" y="50" text-anchor="middle" fill="#FBBF24" font-family="'IBM Plex Mono', monospace" font-size="11">M1=1  M0=1</text>

    <!-- Architecture Visual -->
    <g transform="translate(145, 15)">
      <rect width="180" height="45" rx="4" fill="#78350F" stroke="#F59E0B" />
      <text x="90" y="24" text-anchor="middle" fill="#FFFFFF" font-size="11" font-weight="700">TL0 (TR0) + TH0 (TR1)</text>
      <text x="90" y="40" text-anchor="middle" fill="#FDE68A" font-size="9">Split Timer 0 dual operation</text>
    </g>

    <!-- Details -->
    <g transform="translate(345, 18)">
      <text x="0" y="16" fill="#FBBF24" font-size="11" font-weight="600">Split Timer 0 (Two 8-Bit Timers)</text>
      <text x="0" y="34" fill="#94A3B8" font-size="10">TH0 borrows TR1 &amp; TF1. Timer 1 runs free for UART baud rate.</text>
    </g>

    <!-- Application / Significance -->
    <g transform="translate(640, 18)">
      <rect width="220" height="38" rx="4" fill="#0F172A" />
      <text x="110" y="16" text-anchor="middle" fill="#FBBF24" font-size="10" font-weight="600">Extra Timer Channel</text>
      <text x="110" y="30" text-anchor="middle" fill="#94A3B8" font-size="9">Baud generator + 2 timing intervals</text>
    </g>
  </g>

  <!-- Bottom Realization -->
  <text x="480" y="460" text-anchor="middle" fill="#64748B" font-size="11" font-weight="500">Same physical registers &#8212; different silicon connections steered purely by software configuration.</text>
</svg>'''

with open("Images/intel_8051_four_modes_comparison.svg", "w", encoding="utf-8") as f:
    f.write(svg6)
validate_svg("Images/intel_8051_four_modes_comparison.svg")
print("All 6 SVGs generated and validated successfully!")
