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

# 1. intel_8051_tcon_interrupt_bits.svg
svg1 = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 940 390" width="100%" height="100%" style="background:#0B1120; font-family:'DM Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
  <defs>
    <linearGradient id="cardGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1E293B"/>
      <stop offset="100%" stop-color="#0F172A"/>
    </linearGradient>
  </defs>

  <!-- Title -->
  <text x="470" y="36" text-anchor="middle" fill="#F8FAFC" font-size="20" font-weight="700" letter-spacing="0.05em">TCON (88H) &#8212; THE DUAL-NATURE REGISTER</text>
  <text x="470" y="60" text-anchor="middle" fill="#94A3B8" font-size="13">Where hardware timing controls meet external interrupt triggers on the 8051 surface</text>

  <!-- TCON REGISTER CONTAINER -->
  <g transform="translate(60, 85)">
    <rect width="820" height="110" rx="8" fill="url(#cardGrad)" stroke="#334155" stroke-width="1.5" />
    <rect width="820" height="26" rx="8" fill="#1E293B" />
    <text x="410" y="18" text-anchor="middle" fill="#94A3B8" font-size="11" font-weight="700" letter-spacing="0.05em">TCON (88H) &#8212; BIT-ADDRESSABLE SPECIAL FUNCTION REGISTER</text>

    <!-- 8 Bit Cells -->
    <!-- Bit 7: TF1 -->
    <g transform="translate(20, 36)">
      <rect width="90" height="60" rx="4" fill="#0C4A6E" stroke="#38BDF8" stroke-width="1.5" />
      <text x="45" y="16" text-anchor="middle" fill="#7DD3FC" font-size="9" font-weight="600">Bit 7 (8FH)</text>
      <text x="45" y="34" text-anchor="middle" fill="#FFFFFF" font-family="'IBM Plex Mono', monospace" font-size="13" font-weight="700">TF1</text>
      <text x="45" y="50" text-anchor="middle" fill="#BAE6FD" font-size="8">Timer 1 Flag</text>
    </g>

    <!-- Bit 6: TR1 -->
    <g transform="translate(118, 36)">
      <rect width="90" height="60" rx="4" fill="#0C4A6E" stroke="#38BDF8" stroke-width="1.5" />
      <text x="45" y="16" text-anchor="middle" fill="#7DD3FC" font-size="9" font-weight="600">Bit 6 (8EH)</text>
      <text x="45" y="34" text-anchor="middle" fill="#FFFFFF" font-family="'IBM Plex Mono', monospace" font-size="13" font-weight="700">TR1</text>
      <text x="45" y="50" text-anchor="middle" fill="#BAE6FD" font-size="8">Timer 1 Run</text>
    </g>

    <!-- Bit 5: TF0 -->
    <g transform="translate(216, 36)">
      <rect width="90" height="60" rx="4" fill="#0C4A6E" stroke="#38BDF8" stroke-width="1.5" />
      <text x="45" y="16" text-anchor="middle" fill="#7DD3FC" font-size="9" font-weight="600">Bit 5 (8DH)</text>
      <text x="45" y="34" text-anchor="middle" fill="#FFFFFF" font-family="'IBM Plex Mono', monospace" font-size="13" font-weight="700">TF0</text>
      <text x="45" y="50" text-anchor="middle" fill="#BAE6FD" font-size="8">Timer 0 Flag</text>
    </g>

    <!-- Bit 4: TR0 -->
    <g transform="translate(314, 36)">
      <rect width="90" height="60" rx="4" fill="#0C4A6E" stroke="#38BDF8" stroke-width="1.5" />
      <text x="45" y="16" text-anchor="middle" fill="#7DD3FC" font-size="9" font-weight="600">Bit 4 (8CH)</text>
      <text x="45" y="34" text-anchor="middle" fill="#FFFFFF" font-family="'IBM Plex Mono', monospace" font-size="13" font-weight="700">TR0</text>
      <text x="45" y="50" text-anchor="middle" fill="#BAE6FD" font-size="8">Timer 0 Run</text>
    </g>

    <!-- Boundary Divider -->
    <line x1="410" y1="30" x2="410" y2="102" stroke="#F59E0B" stroke-width="2" stroke-dasharray="4,4" />

    <!-- Bit 3: IE1 -->
    <g transform="translate(416, 36)">
      <rect width="90" height="60" rx="4" fill="#78350F" stroke="#F59E0B" stroke-width="1.8" />
      <text x="45" y="16" text-anchor="middle" fill="#FDE68A" font-size="9" font-weight="700">Bit 3 (8BH)</text>
      <text x="45" y="34" text-anchor="middle" fill="#FFFFFF" font-family="'IBM Plex Mono', monospace" font-size="13" font-weight="700">IE1</text>
      <text x="45" y="50" text-anchor="middle" fill="#FEF08A" font-size="8">Ext Int 1 Flag</text>
    </g>

    <!-- Bit 2: IT1 -->
    <g transform="translate(514, 36)">
      <rect width="90" height="60" rx="4" fill="#78350F" stroke="#F59E0B" stroke-width="1.8" />
      <text x="45" y="16" text-anchor="middle" fill="#FDE68A" font-size="9" font-weight="700">Bit 2 (8AH)</text>
      <text x="45" y="34" text-anchor="middle" fill="#FFFFFF" font-family="'IBM Plex Mono', monospace" font-size="13" font-weight="700">IT1</text>
      <text x="45" y="50" text-anchor="middle" fill="#FEF08A" font-size="8">Type 1 Select</text>
    </g>

    <!-- Bit 1: IE0 -->
    <g transform="translate(612, 36)">
      <rect width="90" height="60" rx="4" fill="#064E3B" stroke="#10B981" stroke-width="1.8" />
      <text x="45" y="16" text-anchor="middle" fill="#6EE7B7" font-size="9" font-weight="700">Bit 1 (89H)</text>
      <text x="45" y="34" text-anchor="middle" fill="#FFFFFF" font-family="'IBM Plex Mono', monospace" font-size="13" font-weight="700">IE0</text>
      <text x="45" y="50" text-anchor="middle" fill="#A7F3D0" font-size="8">Ext Int 0 Flag</text>
    </g>

    <!-- Bit 0: IT0 -->
    <g transform="translate(710, 36)">
      <rect width="90" height="60" rx="4" fill="#064E3B" stroke="#10B981" stroke-width="1.8" />
      <text x="45" y="16" text-anchor="middle" fill="#6EE7B7" font-size="9" font-weight="700">Bit 0 (88H)</text>
      <text x="45" y="34" text-anchor="middle" fill="#FFFFFF" font-family="'IBM Plex Mono', monospace" font-size="13" font-weight="700">IT0</text>
      <text x="45" y="50" text-anchor="middle" fill="#A7F3D0" font-size="8">Type 0 Select</text>
    </g>
  </g>

  <!-- ANNOTATIONS BELOW -->
  <g transform="translate(60, 215)">
    <!-- Left: Timers -->
    <g transform="translate(0, 0)">
      <rect width="385" height="135" rx="6" fill="#1E293B" stroke="#38BDF8" stroke-width="1" />
      <text x="20" y="24" fill="#38BDF8" font-size="11" font-weight="700">&#9650; UPPER NIBBLE: TIMERS (BITS 7..4)</text>
      <text x="20" y="46" fill="#CBD5E1" font-size="11">&#8226; <tspan fill="#38BDF8" font-weight="600">TR0, TR1:</tspan> Software run gates that start/stop counting.</text>
      <text x="20" y="68" fill="#CBD5E1" font-size="11">&#8226; <tspan fill="#38BDF8" font-weight="600">TF0, TF1:</tspan> Hardware overflow flags raised on rollover.</text>
      <text x="20" y="90" fill="#94A3B8" font-size="10">Explored thoroughly in previous chapters as the heartbeat of machine timing.</text>
      <rect x="20" y="102" width="345" height="20" rx="3" fill="#0F172A" />
      <text x="192" y="116" text-anchor="middle" fill="#38BDF8" font-size="9">Auto-cleared by CPU when branching to timer ISR</text>
    </g>

    <!-- Right: External Interrupts -->
    <g transform="translate(435, 0)">
      <rect width="385" height="135" rx="6" fill="#1E293B" stroke="#F59E0B" stroke-width="1" />
      <text x="20" y="24" fill="#FBBF24" font-size="11" font-weight="700">&#9650; LOWER NIBBLE: EXTERNAL INTERRUPTS (BITS 3..0)</text>
      <text x="20" y="46" fill="#CBD5E1" font-size="11">&#8226; <tspan fill="#F59E0B" font-weight="600">IT0, IT1:</tspan> Trigger Mode. 0 = Low-Level, 1 = Falling-Edge.</text>
      <text x="20" y="68" fill="#CBD5E1" font-size="11">&#8226; <tspan fill="#F59E0B" font-weight="600">IE0, IE1:</tspan> External Interrupt Flags (Pin INT0/INT1 state).</text>
      <text x="20" y="90" fill="#94A3B8" font-size="10">The mystery revealed: TCON also serves as the external interrupt latch.</text>
      <rect x="20" y="102" width="345" height="20" rx="3" fill="#0F172A" />
      <text x="192" y="116" text-anchor="middle" fill="#FBBF24" font-size="9">In edge mode, hardware auto-clears IEx upon vectoring</text>
    </g>
  </g>
</svg>'''

with open("Images/intel_8051_tcon_interrupt_bits.svg", "w", encoding="utf-8") as f:
    f.write(svg1)
validate_svg("Images/intel_8051_tcon_interrupt_bits.svg")

# 2. intel_8051_five_interrupt_sources.svg
svg2 = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 940 400" width="100%" height="100%" style="background:#0B1120; font-family:'DM Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
  <defs>
    <linearGradient id="hubGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1E293B"/>
      <stop offset="100%" stop-color="#0F172A"/>
    </linearGradient>
    <marker id="src-arr" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#38BDF8" />
    </marker>
    <marker id="src-amber" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#F59E0B" />
    </marker>
  </defs>

  <!-- Title -->
  <text x="470" y="36" text-anchor="middle" fill="#F8FAFC" font-size="20" font-weight="700" letter-spacing="0.05em">THE FIVE VOICES OF THE 8051</text>
  <text x="470" y="60" text-anchor="middle" fill="#94A3B8" font-size="13">Hardware channels that demand processor attention in the classic architecture</text>

  <!-- 5 SOURCE CARDS (LEFT) -->
  <g transform="translate(40, 85)">
    <!-- 1. INT0 -->
    <g transform="translate(0, 0)">
      <rect width="260" height="48" rx="6" fill="#1E293B" stroke="#10B981" stroke-width="1.5" />
      <text x="15" y="22" fill="#6EE7B7" font-size="11" font-weight="700">1. EXTERNAL PIN INT0 (P3.2)</text>
      <text x="15" y="38" fill="#94A3B8" font-size="9">Pin transition or low level &#8594; Latch IE0</text>
      <line x1="265" y1="24" x2="350" y2="135" stroke="#10B981" stroke-width="1.5" marker-end="url(#src-arr)" />
    </g>

    <!-- 2. TF0 -->
    <g transform="translate(0, 60)">
      <rect width="260" height="48" rx="6" fill="#1E293B" stroke="#38BDF8" stroke-width="1.5" />
      <text x="15" y="22" fill="#7DD3FC" font-size="11" font-weight="700">2. TIMER 0 OVERFLOW (TF0)</text>
      <text x="15" y="38" fill="#94A3B8" font-size="9">TH0:TL0 rollover (FFFFH &#8594; 0000H)</text>
      <line x1="265" y1="24" x2="350" y2="140" stroke="#38BDF8" stroke-width="1.5" marker-end="url(#src-arr)" />
    </g>

    <!-- 3. INT1 -->
    <g transform="translate(0, 120)">
      <rect width="260" height="48" rx="6" fill="#1E293B" stroke="#10B981" stroke-width="1.5" />
      <text x="15" y="22" fill="#6EE7B7" font-size="11" font-weight="700">3. EXTERNAL PIN INT1 (P3.3)</text>
      <text x="15" y="38" fill="#94A3B8" font-size="9">Pin transition or low level &#8594; Latch IE1</text>
      <line x1="265" y1="24" x2="350" y2="145" stroke="#10B981" stroke-width="1.5" marker-end="url(#src-arr)" />
    </g>

    <!-- 4. TF1 -->
    <g transform="translate(0, 180)">
      <rect width="260" height="48" rx="6" fill="#1E293B" stroke="#38BDF8" stroke-width="1.5" />
      <text x="15" y="22" fill="#7DD3FC" font-size="11" font-weight="700">4. TIMER 1 OVERFLOW (TF1)</text>
      <text x="15" y="38" fill="#94A3B8" font-size="9">TH1:TL1 rollover (FFFFH &#8594; 0000H)</text>
      <line x1="265" y1="24" x2="350" y2="150" stroke="#38BDF8" stroke-width="1.5" marker-end="url(#src-arr)" />
    </g>

    <!-- 5. SERIAL UART -->
    <g transform="translate(0, 240)">
      <rect width="260" height="48" rx="6" fill="#1E293B" stroke="#A855F7" stroke-width="1.5" />
      <text x="15" y="22" fill="#D8B4FE" font-size="11" font-weight="700">5. SERIAL UART (RI / TI)</text>
      <text x="15" y="38" fill="#94A3B8" font-size="9">Byte received (RI) OR byte transmitted (TI)</text>
      <line x1="265" y1="24" x2="350" y2="155" stroke="#A855F7" stroke-width="1.5" marker-end="url(#src-arr)" />
    </g>
  </g>

  <!-- CENTRAL ARBITRATION HUB -->
  <g transform="translate(400, 140)">
    <rect width="230" height="180" rx="8" fill="url(#hubGrad)" stroke="#38BDF8" stroke-width="2" />
    <rect width="230" height="28" rx="8" fill="#0C4A6E" />
    <text x="115" y="19" text-anchor="middle" fill="#7DD3FC" font-size="11" font-weight="700">INTERRUPT ENGINE</text>

    <g transform="translate(15, 40)">
      <rect width="200" height="34" rx="4" fill="#0F172A" stroke="#334155" />
      <text x="100" y="16" text-anchor="middle" fill="#CBD5E1" font-size="9" font-weight="600">1. Gating Check (IE Register)</text>
      <text x="100" y="28" text-anchor="middle" fill="#64748B" font-size="8">Is EA=1 and Bit Enabled?</text>

      <rect y="42" width="200" height="34" rx="4" fill="#0F172A" stroke="#334155" />
      <text x="100" y="58" text-anchor="middle" fill="#CBD5E1" font-size="9" font-weight="600">2. Priority Check (IP Register)</text>
      <text x="100" y="70" text-anchor="middle" fill="#64748B" font-size="8">High Priority or Low Priority?</text>

      <rect y="84" width="200" height="34" rx="4" fill="#0F172A" stroke="#334155" />
      <text x="100" y="100" text-anchor="middle" fill="#CBD5E1" font-size="9" font-weight="600">3. Polling Tie-Breaker</text>
      <text x="100" y="112" text-anchor="middle" fill="#64748B" font-size="8">Hardware order resolves ties</text>
    </g>
  </g>

  <!-- ARROW TO CPU -->
  <line x1="635" y1="230" x2="695" y2="230" stroke="#F59E0B" stroke-width="2.5" marker-end="url(#src-amber)" />

  <!-- CPU DESTINATION (RIGHT) -->
  <g transform="translate(705, 140)">
    <rect width="190" height="180" rx="8" fill="url(#hubGrad)" stroke="#F59E0B" stroke-width="1.8" />
    <rect width="190" height="28" rx="8" fill="#78350F" />
    <text x="95" y="19" text-anchor="middle" fill="#FDE68A" font-size="11" font-weight="700">CPU EXECUTION</text>

    <g transform="translate(15, 45)">
      <circle cx="80" cy="18" r="14" fill="#0F172A" stroke="#F59E0B" stroke-width="1.5" />
      <text x="80" y="22" text-anchor="middle" fill="#F59E0B" font-size="10" font-weight="700">PC</text>

      <text x="80" y="52" text-anchor="middle" fill="#FFFFFF" font-size="11" font-weight="700">Vector Redirection</text>
      <text x="80" y="68" text-anchor="middle" fill="#CBD5E1" font-size="9">Push return PC to stack</text>
      <text x="80" y="82" text-anchor="middle" fill="#CBD5E1" font-size="9">Branch to ISR Vector</text>

      <rect y="92" width="160" height="24" rx="3" fill="#0F172A" />
      <text x="80" y="108" text-anchor="middle" fill="#34D399" font-family="'IBM Plex Mono', monospace" font-size="9" font-weight="600">RETI ends handler</text>
    </g>
  </g>
</svg>'''

with open("Images/intel_8051_five_interrupt_sources.svg", "w", encoding="utf-8") as f:
    f.write(svg2)
validate_svg("Images/intel_8051_five_interrupt_sources.svg")

# 3. intel_8051_ie_register_two_stage_gating.svg
svg3 = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 940 380" width="100%" height="100%" style="background:#0B1120; font-family:'DM Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
  <defs>
    <linearGradient id="cardGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1E293B"/>
      <stop offset="100%" stop-color="#0F172A"/>
    </linearGradient>
    <marker id="ie-arr" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#38BDF8" />
    </marker>
    <marker id="ie-green" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#10B981" />
    </marker>
  </defs>

  <!-- Title -->
  <text x="470" y="36" text-anchor="middle" fill="#F8FAFC" font-size="20" font-weight="700" letter-spacing="0.05em">IE (A8H) &#8212; TWO-STAGE GATING ARCHITECTURE</text>
  <text x="470" y="60" text-anchor="middle" fill="#94A3B8" font-size="13">Individual source permissions governed by the EA master circuit breaker</text>

  <!-- IE REGISTER ROW -->
  <g transform="translate(60, 85)">
    <rect width="820" height="95" rx="8" fill="url(#cardGrad)" stroke="#38BDF8" stroke-width="1.5" />
    <rect width="820" height="26" rx="8" fill="#0C4A6E" />
    <text x="410" y="18" text-anchor="middle" fill="#7DD3FC" font-size="11" font-weight="700" letter-spacing="0.05em">IE REGISTER (A8H) &#8212; BIT-ADDRESSABLE</text>

    <!-- 8 Bit Cells -->
    <!-- Bit 7: EA -->
    <g transform="translate(20, 34)">
      <rect width="90" height="50" rx="4" fill="#064E3B" stroke="#10B981" stroke-width="1.8" />
      <text x="45" y="15" text-anchor="middle" fill="#6EE7B7" font-size="8" font-weight="700">Bit 7 (AFH)</text>
      <text x="45" y="32" text-anchor="middle" fill="#FFFFFF" font-family="'IBM Plex Mono', monospace" font-size="13" font-weight="700">EA</text>
      <text x="45" y="44" text-anchor="middle" fill="#A7F3D0" font-size="7">Global Enable</text>
    </g>

    <!-- Bit 6: Unimplemented -->
    <g transform="translate(118, 34)">
      <rect width="90" height="50" rx="4" fill="#1E293B" stroke="#475569" stroke-dasharray="2,2" />
      <text x="45" y="15" text-anchor="middle" fill="#64748B" font-size="8">Bit 6</text>
      <text x="45" y="32" text-anchor="middle" fill="#475569" font-family="'IBM Plex Mono', monospace" font-size="13">&#8212;</text>
      <text x="45" y="44" text-anchor="middle" fill="#64748B" font-size="7">Reserved</text>
    </g>

    <!-- Bit 5: Unimplemented -->
    <g transform="translate(216, 34)">
      <rect width="90" height="50" rx="4" fill="#1E293B" stroke="#475569" stroke-dasharray="2,2" />
      <text x="45" y="15" text-anchor="middle" fill="#64748B" font-size="8">Bit 5</text>
      <text x="45" y="32" text-anchor="middle" fill="#475569" font-family="'IBM Plex Mono', monospace" font-size="13">&#8212;</text>
      <text x="45" y="44" text-anchor="middle" fill="#64748B" font-size="7">Reserved</text>
    </g>

    <!-- Bit 4: ES -->
    <g transform="translate(314, 34)">
      <rect width="90" height="50" rx="4" fill="#0C4A6E" stroke="#38BDF8" stroke-width="1.5" />
      <text x="45" y="15" text-anchor="middle" fill="#7DD3FC" font-size="8" font-weight="600">Bit 4 (ACH)</text>
      <text x="45" y="32" text-anchor="middle" fill="#FFFFFF" font-family="'IBM Plex Mono', monospace" font-size="13" font-weight="700">ES</text>
      <text x="45" y="44" text-anchor="middle" fill="#BAE6FD" font-size="7">Serial Enable</text>
    </g>

    <!-- Bit 3: ET1 -->
    <g transform="translate(412, 34)">
      <rect width="90" height="50" rx="4" fill="#0C4A6E" stroke="#38BDF8" stroke-width="1.5" />
      <text x="45" y="15" text-anchor="middle" fill="#7DD3FC" font-size="8" font-weight="600">Bit 3 (ABH)</text>
      <text x="45" y="32" text-anchor="middle" fill="#FFFFFF" font-family="'IBM Plex Mono', monospace" font-size="13" font-weight="700">ET1</text>
      <text x="45" y="44" text-anchor="middle" fill="#BAE6FD" font-size="7">Timer 1 Enable</text>
    </g>

    <!-- Bit 2: EX1 -->
    <g transform="translate(510, 34)">
      <rect width="90" height="50" rx="4" fill="#0C4A6E" stroke="#38BDF8" stroke-width="1.5" />
      <text x="45" y="15" text-anchor="middle" fill="#7DD3FC" font-size="8" font-weight="600">Bit 2 (AAH)</text>
      <text x="45" y="32" text-anchor="middle" fill="#FFFFFF" font-family="'IBM Plex Mono', monospace" font-size="13" font-weight="700">EX1</text>
      <text x="45" y="44" text-anchor="middle" fill="#BAE6FD" font-size="7">Ext Int 1 Enable</text>
    </g>

    <!-- Bit 1: ET0 -->
    <g transform="translate(608, 34)">
      <rect width="90" height="50" rx="4" fill="#0C4A6E" stroke="#38BDF8" stroke-width="1.5" />
      <text x="45" y="15" text-anchor="middle" fill="#7DD3FC" font-size="8" font-weight="600">Bit 1 (A9H)</text>
      <text x="45" y="32" text-anchor="middle" fill="#FFFFFF" font-family="'IBM Plex Mono', monospace" font-size="13" font-weight="700">ET0</text>
      <text x="45" y="44" text-anchor="middle" fill="#BAE6FD" font-size="7">Timer 0 Enable</text>
    </g>

    <!-- Bit 0: EX0 -->
    <g transform="translate(706, 34)">
      <rect width="90" height="50" rx="4" fill="#0C4A6E" stroke="#38BDF8" stroke-width="1.5" />
      <text x="45" y="15" text-anchor="middle" fill="#7DD3FC" font-size="8" font-weight="600">Bit 0 (A8H)</text>
      <text x="45" y="32" text-anchor="middle" fill="#FFFFFF" font-family="'IBM Plex Mono', monospace" font-size="13" font-weight="700">EX0</text>
      <text x="45" y="44" text-anchor="middle" fill="#BAE6FD" font-size="7">Ext Int 0 Enable</text>
    </g>
  </g>

  <!-- TWO-STAGE GATING SCHEMATIC -->
  <g transform="translate(60, 205)">
    <rect width="820" height="150" rx="8" fill="#1E293B" stroke="#334155" />

    <!-- Stage 1 Label -->
    <text x="25" y="24" fill="#38BDF8" font-size="11" font-weight="700">STAGE 1: INDIVIDUAL LOCAL SWITCHES</text>
    <text x="25" y="42" fill="#94A3B8" font-size="10">Each peripheral channel must be explicitly authorized by its dedicated enable bit:</text>

    <g transform="translate(25, 55)">
      <!-- Channel EX0 -->
      <rect width="130" height="34" rx="4" fill="#0F172A" stroke="#334155" />
      <text x="65" y="16" text-anchor="middle" fill="#CBD5E1" font-size="9">EX0 = 1</text>
      <text x="65" y="28" text-anchor="middle" fill="#64748B" font-size="8">Allows INT0</text>

      <!-- Channel ET0 -->
      <rect x="145" y="0" width="130" height="34" rx="4" fill="#0F172A" stroke="#334155" />
      <text x="210" y="16" text-anchor="middle" fill="#CBD5E1" font-size="9">ET0 = 1</text>
      <text x="210" y="28" text-anchor="middle" fill="#64748B" font-size="8">Allows Timer 0</text>

      <!-- Channel EX1 -->
      <rect x="290" y="0" width="130" height="34" rx="4" fill="#0F172A" stroke="#334155" />
      <text x="355" y="16" text-anchor="middle" fill="#CBD5E1" font-size="9">EX1 = 1</text>
      <text x="355" y="28" text-anchor="middle" fill="#64748B" font-size="8">Allows INT1</text>

      <!-- Channel ET1 -->
      <rect x="435" y="0" width="130" height="34" rx="4" fill="#0F172A" stroke="#334155" />
      <text x="500" y="16" text-anchor="middle" fill="#CBD5E1" font-size="9">ET1 = 1</text>
      <text x="500" y="28" text-anchor="middle" fill="#64748B" font-size="8">Allows Timer 1</text>

      <!-- Channel ES -->
      <rect x="580" y="0" width="130" height="34" rx="4" fill="#0F172A" stroke="#334155" />
      <text x="645" y="16" text-anchor="middle" fill="#CBD5E1" font-size="9">ES = 1</text>
      <text x="645" y="28" text-anchor="middle" fill="#64748B" font-size="8">Allows Serial</text>
    </g>

    <!-- Arrow down to Stage 2 -->
    <path d="M 390 100 L 390 115" stroke="#38BDF8" stroke-width="2" marker-end="url(#ie-arr)" />

    <!-- Stage 2 Master Switch -->
    <g transform="translate(25, 110)">
      <rect width="770" height="30" rx="4" fill="#064E3B" stroke="#10B981" stroke-width="1.2" />
      <text x="385" y="20" text-anchor="middle" fill="#A7F3D0" font-size="11" font-weight="700">STAGE 2 MASTER GATE: EA = 1 (SETB EA) MUST BE CLOSED FOR ANY INTERRUPT TO REACH CPU</text>
    </g>
  </g>
</svg>'''

with open("Images/intel_8051_ie_register_two_stage_gating.svg", "w", encoding="utf-8") as f:
    f.write(svg3)
validate_svg("Images/intel_8051_ie_register_two_stage_gating.svg")

# 4. intel_8051_ip_register_priority_levels.svg
svg4 = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 940 370" width="100%" height="100%" style="background:#0B1120; font-family:'DM Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
  <defs>
    <linearGradient id="cardGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1E293B"/>
      <stop offset="100%" stop-color="#0F172A"/>
    </linearGradient>
  </defs>

  <!-- Title -->
  <text x="470" y="36" text-anchor="middle" fill="#F8FAFC" font-size="20" font-weight="700" letter-spacing="0.05em">IP (B8H) &#8212; TWO-LEVEL PRIORITY CONTROL</text>
  <text x="470" y="60" text-anchor="middle" fill="#94A3B8" font-size="13">Assigning 0 (Low Priority) or 1 (High Priority) to each interrupt source</text>

  <!-- IP REGISTER ROW -->
  <g transform="translate(60, 85)">
    <rect width="820" height="95" rx="8" fill="url(#cardGrad)" stroke="#A855F7" stroke-width="1.5" />
    <rect width="820" height="26" rx="8" fill="#581C87" />
    <text x="410" y="18" text-anchor="middle" fill="#E9D5FF" font-size="11" font-weight="700" letter-spacing="0.05em">IP REGISTER (B8H) &#8212; BIT-ADDRESSABLE</text>

    <!-- 8 Bit Cells -->
    <g transform="translate(20, 34)">
      <rect width="90" height="50" rx="4" fill="#1E293B" stroke="#475569" stroke-dasharray="2,2" />
      <text x="45" y="15" text-anchor="middle" fill="#64748B" font-size="8">Bit 7</text>
      <text x="45" y="32" text-anchor="middle" fill="#475569" font-family="'IBM Plex Mono', monospace" font-size="13">&#8212;</text>
      <text x="45" y="44" text-anchor="middle" fill="#64748B" font-size="7">Reserved</text>
    </g>

    <g transform="translate(118, 34)">
      <rect width="90" height="50" rx="4" fill="#1E293B" stroke="#475569" stroke-dasharray="2,2" />
      <text x="45" y="15" text-anchor="middle" fill="#64748B" font-size="8">Bit 6</text>
      <text x="45" y="32" text-anchor="middle" fill="#475569" font-family="'IBM Plex Mono', monospace" font-size="13">&#8212;</text>
      <text x="45" y="44" text-anchor="middle" fill="#64748B" font-size="7">Reserved</text>
    </g>

    <g transform="translate(216, 34)">
      <rect width="90" height="50" rx="4" fill="#1E293B" stroke="#475569" stroke-dasharray="2,2" />
      <text x="45" y="15" text-anchor="middle" fill="#64748B" font-size="8">Bit 5</text>
      <text x="45" y="32" text-anchor="middle" fill="#475569" font-family="'IBM Plex Mono', monospace" font-size="13">&#8212;</text>
      <text x="45" y="44" text-anchor="middle" fill="#64748B" font-size="7">Reserved</text>
    </g>

    <g transform="translate(314, 34)">
      <rect width="90" height="50" rx="4" fill="#581C87" stroke="#A855F7" stroke-width="1.5" />
      <text x="45" y="15" text-anchor="middle" fill="#D8B4FE" font-size="8" font-weight="600">Bit 4 (BCH)</text>
      <text x="45" y="32" text-anchor="middle" fill="#FFFFFF" font-family="'IBM Plex Mono', monospace" font-size="13" font-weight="700">PS</text>
      <text x="45" y="44" text-anchor="middle" fill="#E9D5FF" font-size="7">Serial Priority</text>
    </g>

    <g transform="translate(412, 34)">
      <rect width="90" height="50" rx="4" fill="#581C87" stroke="#A855F7" stroke-width="1.5" />
      <text x="45" y="15" text-anchor="middle" fill="#D8B4FE" font-size="8" font-weight="600">Bit 3 (BBH)</text>
      <text x="45" y="32" text-anchor="middle" fill="#FFFFFF" font-family="'IBM Plex Mono', monospace" font-size="13" font-weight="700">PT1</text>
      <text x="45" y="44" text-anchor="middle" fill="#E9D5FF" font-size="7">Timer 1 Priority</text>
    </g>

    <g transform="translate(510, 34)">
      <rect width="90" height="50" rx="4" fill="#581C87" stroke="#A855F7" stroke-width="1.5" />
      <text x="45" y="15" text-anchor="middle" fill="#D8B4FE" font-size="8" font-weight="600">Bit 2 (BAH)</text>
      <text x="45" y="32" text-anchor="middle" fill="#FFFFFF" font-family="'IBM Plex Mono', monospace" font-size="13" font-weight="700">PX1</text>
      <text x="45" y="44" text-anchor="middle" fill="#E9D5FF" font-size="7">Ext Int 1 Priority</text>
    </g>

    <g transform="translate(608, 34)">
      <rect width="90" height="50" rx="4" fill="#581C87" stroke="#A855F7" stroke-width="1.5" />
      <text x="45" y="15" text-anchor="middle" fill="#D8B4FE" font-size="8" font-weight="600">Bit 1 (B9H)</text>
      <text x="45" y="32" text-anchor="middle" fill="#FFFFFF" font-family="'IBM Plex Mono', monospace" font-size="13" font-weight="700">PT0</text>
      <text x="45" y="44" text-anchor="middle" fill="#E9D5FF" font-size="7">Timer 0 Priority</text>
    </g>

    <g transform="translate(706, 34)">
      <rect width="90" height="50" rx="4" fill="#581C87" stroke="#A855F7" stroke-width="1.5" />
      <text x="45" y="15" text-anchor="middle" fill="#D8B4FE" font-size="8" font-weight="600">Bit 0 (B8H)</text>
      <text x="45" y="32" text-anchor="middle" fill="#FFFFFF" font-family="'IBM Plex Mono', monospace" font-size="13" font-weight="700">PX0</text>
      <text x="45" y="44" text-anchor="middle" fill="#E9D5FF" font-size="7">Ext Int 0 Priority</text>
    </g>
  </g>

  <!-- PRIORITY MATRIX PANEL -->
  <g transform="translate(60, 200)">
    <rect width="820" height="140" rx="8" fill="#1E293B" stroke="#334155" />

    <g transform="translate(25, 20)">
      <rect width="240" height="100" rx="6" fill="#0F172A" stroke="#10B981" stroke-width="1.5" />
      <text x="120" y="24" text-anchor="middle" fill="#34D399" font-size="11" font-weight="700">HIGH PREEMPTS LOW</text>
      <text x="120" y="48" text-anchor="middle" fill="#CBD5E1" font-size="10">High priority (1) interrupt</text>
      <text x="120" y="64" text-anchor="middle" fill="#CBD5E1" font-size="10"><tspan fill="#34D399" font-weight="600">CAN preempt</tspan> an active</text>
      <text x="120" y="80" text-anchor="middle" fill="#CBD5E1" font-size="10">low priority (0) ISR.</text>
    </g>

    <g transform="translate(290, 20)">
      <rect width="240" height="100" rx="6" fill="#0F172A" stroke="#EF4444" stroke-width="1.5" />
      <text x="120" y="24" text-anchor="middle" fill="#F87171" font-size="11" font-weight="700">LOW CANNOT PREEMPT</text>
      <text x="120" y="48" text-anchor="middle" fill="#CBD5E1" font-size="10">Low priority (0) interrupt</text>
      <text x="120" y="64" text-anchor="middle" fill="#CBD5E1" font-size="10"><tspan fill="#EF4444" font-weight="600">CANNOT preempt</tspan> an</text>
      <text x="120" y="80" text-anchor="middle" fill="#CBD5E1" font-size="10">active high priority ISR.</text>
    </g>

    <g transform="translate(555, 20)">
      <rect width="240" height="100" rx="6" fill="#0F172A" stroke="#F59E0B" stroke-width="1.5" />
      <text x="120" y="24" text-anchor="middle" fill="#FBBF24" font-size="11" font-weight="700">EQUAL CANNOT PREEMPT</text>
      <text x="120" y="48" text-anchor="middle" fill="#CBD5E1" font-size="10">Interrupt at same level</text>
      <text x="120" y="64" text-anchor="middle" fill="#CBD5E1" font-size="10"><tspan fill="#FBBF24" font-weight="600">CANNOT preempt</tspan> another</text>
      <text x="120" y="80" text-anchor="middle" fill="#CBD5E1" font-size="10">ISR of the same level.</text>
    </g>
  </g>
</svg>'''

with open("Images/intel_8051_ip_register_priority_levels.svg", "w", encoding="utf-8") as f:
    f.write(svg4)
validate_svg("Images/intel_8051_ip_register_priority_levels.svg")

# 5. intel_8051_priority_nesting_timeline.svg
svg5 = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 940 370" width="100%" height="100%" style="background:#0B1120; font-family:'DM Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
  <defs>
    <marker id="t-arr" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#38BDF8" />
    </marker>
    <marker id="t-amber" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#F59E0B" />
    </marker>
  </defs>

  <!-- Title -->
  <text x="470" y="36" text-anchor="middle" fill="#F8FAFC" font-size="20" font-weight="700" letter-spacing="0.05em">INTERRUPT PREEMPTION &amp; NESTING TIMELINE</text>
  <text x="470" y="60" text-anchor="middle" fill="#94A3B8" font-size="13">High-priority INT1 interrupts Low-priority Timer 0 ISR, preserving stack context</text>

  <!-- TIMELINE DIAGRAM -->
  <g transform="translate(60, 85)">
    <!-- Time Arrow -->
    <line x1="20" y1="200" x2="800" y2="200" stroke="#475569" stroke-width="2" marker-end="url(#t-arr)" />
    <text x="815" y="204" fill="#94A3B8" font-size="11" font-family="'IBM Plex Mono', monospace">Time &#8594;</text>

    <!-- Execution Blocks -->
    <!-- 1. MAIN PROGRAM (0 to 140) -->
    <rect x="20" y="140" width="120" height="40" rx="4" fill="#1E293B" stroke="#64748B" stroke-width="1.5" />
    <text x="80" y="165" text-anchor="middle" fill="#F8FAFC" font-size="11" font-weight="700">MAIN PROGRAM</text>

    <!-- Event 1: Timer 0 Overflow -->
    <line x1="140" y1="180" x2="140" y2="90" stroke="#38BDF8" stroke-width="1.5" stroke-dasharray="3,3" />
    <circle cx="140" cy="180" r="4" fill="#38BDF8" />
    <rect x="90" y="55" width="100" height="28" rx="3" fill="#0C4A6E" />
    <text x="140" y="72" text-anchor="middle" fill="#7DD3FC" font-size="9" font-weight="600">TF0 Overflow</text>

    <!-- 2. TIMER 0 ISR (Low Priority: 140 to 280) -->
    <rect x="140" y="90" width="140" height="40" rx="4" fill="#0C4A6E" stroke="#38BDF8" stroke-width="1.8" />
    <text x="210" y="110" text-anchor="middle" fill="#FFFFFF" font-size="10" font-weight="700">Timer 0 ISR</text>
    <text x="210" y="122" text-anchor="middle" fill="#7DD3FC" font-size="8">(Low Priority: PT0=0)</text>

    <!-- Event 2: High Priority INT1 Arrives -->
    <line x1="280" y1="90" x2="280" y2="15" stroke="#F59E0B" stroke-width="1.5" stroke-dasharray="3,3" />
    <circle cx="280" cy="90" r="4" fill="#F59E0B" />
    <rect x="220" y="-15" width="120" height="28" rx="3" fill="#78350F" />
    <text x="280" y="2" text-anchor="middle" fill="#FDE68A" font-size="9" font-weight="700">INT1 Pulse (PX1=1)</text>

    <!-- 3. INT1 ISR (High Priority: 280 to 450) -->
    <rect x="280" y="15" width="170" height="40" rx="4" fill="#78350F" stroke="#F59E0B" stroke-width="2" />
    <text x="365" y="35" text-anchor="middle" fill="#FFFFFF" font-size="10" font-weight="700">INT1 ISR (PREEMPTION)</text>
    <text x="365" y="47" text-anchor="middle" fill="#FDE68A" font-size="8">High Priority Preempts Timer 0</text>

    <!-- Event 3: RETI from INT1 -->
    <line x1="450" y1="55" x2="450" y2="90" stroke="#10B981" stroke-width="1.5" stroke-dasharray="3,3" />
    <rect x="420" y="65" width="60" height="18" rx="2" fill="#064E3B" />
    <text x="450" y="77" text-anchor="middle" fill="#A7F3D0" font-family="'IBM Plex Mono', monospace" font-size="8">RETI</text>

    <!-- 4. TIMER 0 ISR RESUMES (450 to 570) -->
    <rect x="450" y="90" width="120" height="40" rx="4" fill="#0C4A6E" stroke="#38BDF8" stroke-width="1.8" />
    <text x="510" y="110" text-anchor="middle" fill="#FFFFFF" font-size="10" font-weight="700">Timer 0 Resumes</text>
    <text x="510" y="122" text-anchor="middle" fill="#7DD3FC" font-size="8">Completes Remaining Code</text>

    <!-- Event 4: RETI from Timer 0 -->
    <line x1="570" y1="130" x2="570" y2="140" stroke="#10B981" stroke-width="1.5" stroke-dasharray="3,3" />
    <rect x="540" y="132" width="60" height="18" rx="2" fill="#064E3B" />
    <text x="570" y="144" text-anchor="middle" fill="#A7F3D0" font-family="'IBM Plex Mono', monospace" font-size="8">RETI</text>

    <!-- 5. MAIN PROGRAM RESUMES (570 to 760) -->
    <rect x="570" y="140" width="190" height="40" rx="4" fill="#1E293B" stroke="#64748B" stroke-width="1.5" />
    <text x="665" y="165" text-anchor="middle" fill="#F8FAFC" font-size="11" font-weight="700">MAIN RESUMES</text>

    <!-- Stack Depth Note Below Timeline -->
    <g transform="translate(20, 220)">
      <rect width="740" height="34" rx="4" fill="#0F172A" stroke="#334155" />
      <text x="370" y="16" text-anchor="middle" fill="#CBD5E1" font-size="10">
        <tspan fill="#38BDF8" font-weight="700">Stack Footprint:</tspan> Main PC on Stack (2 bytes) &#8594; Nested INT1 pushes Timer 0 PC (4 bytes total) &#8594; Unwinds cleanly with RETI.
      </text>
      <text x="370" y="28" text-anchor="middle" fill="#64748B" font-size="9">Every nested interrupt level consumes stack space in Internal RAM.</text>
    </g>
  </g>
</svg>'''

with open("Images/intel_8051_priority_nesting_timeline.svg", "w", encoding="utf-8") as f:
    f.write(svg5)
validate_svg("Images/intel_8051_priority_nesting_timeline.svg")

# 6. intel_8051_fixed_polling_sequence.svg
svg6 = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 940 370" width="100%" height="100%" style="background:#0B1120; font-family:'DM Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
  <defs>
    <linearGradient id="cardGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1E293B"/>
      <stop offset="100%" stop-color="#0F172A"/>
    </linearGradient>
    <marker id="poll-arr" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#38BDF8" />
    </marker>
  </defs>

  <!-- Title -->
  <text x="470" y="36" text-anchor="middle" fill="#F8FAFC" font-size="20" font-weight="700" letter-spacing="0.05em">FIXED POLLING SEQUENCE (SAME-PRIORITY TIE-BREAKER)</text>
  <text x="470" y="60" text-anchor="middle" fill="#94A3B8" font-size="13">When multiple pending interrupts have identical IP priority, silicon polls in hardwired order</text>

  <!-- 5 ORDER CARDS IN HORIZONTAL CHAIN -->
  <g transform="translate(30, 95)">
    <!-- 1. INT0 -->
    <g transform="translate(0, 0)">
      <rect width="150" height="95" rx="6" fill="url(#cardGrad)" stroke="#10B981" stroke-width="1.8" />
      <rect width="150" height="24" rx="6" fill="#064E3B" />
      <text x="75" y="17" text-anchor="middle" fill="#6EE7B7" font-size="10" font-weight="700">1. HIGHEST TIE</text>
      <text x="75" y="48" text-anchor="middle" fill="#FFFFFF" font-family="'IBM Plex Mono', monospace" font-size="13" font-weight="700">INT0</text>
      <text x="75" y="64" text-anchor="middle" fill="#34D399" font-size="9">Ext Interrupt 0</text>
      <text x="75" y="80" text-anchor="middle" fill="#64748B" font-family="'IBM Plex Mono', monospace" font-size="9">Vector: 0003H</text>
    </g>

    <!-- Arrow 1 -->
    <line x1="155" y1="48" x2="175" y2="48" stroke="#38BDF8" stroke-width="2" marker-end="url(#poll-arr)" />

    <!-- 2. Timer 0 -->
    <g transform="translate(180, 0)">
      <rect width="150" height="95" rx="6" fill="url(#cardGrad)" stroke="#38BDF8" stroke-width="1.5" />
      <rect width="150" height="24" rx="6" fill="#0C4A6E" />
      <text x="75" y="17" text-anchor="middle" fill="#7DD3FC" font-size="10" font-weight="700">2. SECOND</text>
      <text x="75" y="48" text-anchor="middle" fill="#FFFFFF" font-family="'IBM Plex Mono', monospace" font-size="13" font-weight="700">TIMER 0</text>
      <text x="75" y="64" text-anchor="middle" fill="#38BDF8" font-size="9">Overflow Flag TF0</text>
      <text x="75" y="80" text-anchor="middle" fill="#64748B" font-family="'IBM Plex Mono', monospace" font-size="9">Vector: 000BH</text>
    </g>

    <!-- Arrow 2 -->
    <line x1="335" y1="48" x2="355" y2="48" stroke="#38BDF8" stroke-width="2" marker-end="url(#poll-arr)" />

    <!-- 3. INT1 -->
    <g transform="translate(360, 0)">
      <rect width="150" height="95" rx="6" fill="url(#cardGrad)" stroke="#10B981" stroke-width="1.5" />
      <rect width="150" height="24" rx="6" fill="#064E3B" />
      <text x="75" y="17" text-anchor="middle" fill="#6EE7B7" font-size="10" font-weight="700">3. THIRD</text>
      <text x="75" y="48" text-anchor="middle" fill="#FFFFFF" font-family="'IBM Plex Mono', monospace" font-size="13" font-weight="700">INT1</text>
      <text x="75" y="64" text-anchor="middle" fill="#34D399" font-size="9">Ext Interrupt 1</text>
      <text x="75" y="80" text-anchor="middle" fill="#64748B" font-family="'IBM Plex Mono', monospace" font-size="9">Vector: 0013H</text>
    </g>

    <!-- Arrow 3 -->
    <line x1="515" y1="48" x2="535" y2="48" stroke="#38BDF8" stroke-width="2" marker-end="url(#poll-arr)" />

    <!-- 4. Timer 1 -->
    <g transform="translate(540, 0)">
      <rect width="150" height="95" rx="6" fill="url(#cardGrad)" stroke="#38BDF8" stroke-width="1.5" />
      <rect width="150" height="24" rx="6" fill="#0C4A6E" />
      <text x="75" y="17" text-anchor="middle" fill="#7DD3FC" font-size="10" font-weight="700">4. FOURTH</text>
      <text x="75" y="48" text-anchor="middle" fill="#FFFFFF" font-family="'IBM Plex Mono', monospace" font-size="13" font-weight="700">TIMER 1</text>
      <text x="75" y="64" text-anchor="middle" fill="#38BDF8" font-size="9">Overflow Flag TF1</text>
      <text x="75" y="80" text-anchor="middle" fill="#64748B" font-family="'IBM Plex Mono', monospace" font-size="9">Vector: 001BH</text>
    </g>

    <!-- Arrow 4 -->
    <line x1="695" y1="48" x2="715" y2="48" stroke="#38BDF8" stroke-width="2" marker-end="url(#poll-arr)" />

    <!-- 5. Serial -->
    <g transform="translate(720, 0)">
      <rect width="150" height="95" rx="6" fill="url(#cardGrad)" stroke="#A855F7" stroke-width="1.5" />
      <rect width="150" height="24" rx="6" fill="#581C87" />
      <text x="75" y="17" text-anchor="middle" fill="#E9D5FF" font-size="10" font-weight="700">5. LOWEST TIE</text>
      <text x="75" y="48" text-anchor="middle" fill="#FFFFFF" font-family="'IBM Plex Mono', monospace" font-size="13" font-weight="700">SERIAL</text>
      <text x="75" y="64" text-anchor="middle" fill="#C084FC" font-size="9">UART RI / TI</text>
      <text x="75" y="80" text-anchor="middle" fill="#64748B" font-family="'IBM Plex Mono', monospace" font-size="9">Vector: 0023H</text>
    </g>
  </g>

  <!-- CRITICAL ARCHITECTURAL DISTINCTION BOX -->
  <g transform="translate(50, 220)">
    <rect width="840" height="115" rx="8" fill="#1E293B" stroke="#F59E0B" stroke-width="1.5" />
    <rect width="840" height="26" rx="8" fill="#78350F" />
    <text x="420" y="18" text-anchor="middle" fill="#FDE68A" font-size="11" font-weight="700">CRITICAL DISTINCTION: PROGRAMMABLE IP vs FIXED POLLING SEQUENCE</text>

    <g transform="translate(25, 40)">
      <text x="0" y="16" fill="#FBBF24" font-size="11" font-weight="700">&#8226; IP Register = PREEMPTION AUTHORITY.</text>
      <text x="215" y="16" fill="#CBD5E1" font-size="11">A bit in IP grants an interrupt the power to suspend an active low-priority ISR.</text>

      <text x="0" y="38" fill="#38BDF8" font-size="11" font-weight="700">&#8226; Fixed Polling = SIMULTANEOUS TIE-BREAKER.</text>
      <text x="260" y="38" fill="#CBD5E1" font-size="11">If two pending interrupts have the <tspan fill="#F8FAFC" font-weight="700">SAME</tspan> priority, hardware polls left-to-right.</text>

      <text x="0" y="60" fill="#94A3B8" font-size="10">&#8226; Example: If Serial has IP=1 (High) and INT0 has IP=0 (Low), Serial wins immediately. Polling order only matters when IP bits are identical!</text>
    </g>
  </g>
</svg>'''

with open("Images/intel_8051_fixed_polling_sequence.svg", "w", encoding="utf-8") as f:
    f.write(svg6)
validate_svg("Images/intel_8051_fixed_polling_sequence.svg")

# 7. intel_8051_interrupt_vector_table.svg
svg7 = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 940 390" width="100%" height="100%" style="background:#0B1120; font-family:'DM Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
  <defs>
    <linearGradient id="cardGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1E293B"/>
      <stop offset="100%" stop-color="#0F172A"/>
    </linearGradient>
  </defs>

  <!-- Title -->
  <text x="470" y="36" text-anchor="middle" fill="#F8FAFC" font-size="20" font-weight="700" letter-spacing="0.05em">THE 8051 FIXED VECTOR TABLE</text>
  <text x="470" y="60" text-anchor="middle" fill="#94A3B8" font-size="13">Hardware branches directly to fixed program addresses in low ROM space</text>

  <!-- ROM MEMORY BLOCK -->
  <g transform="translate(60, 85)">
    <rect width="820" height="205" rx="8" fill="url(#cardGrad)" stroke="#38BDF8" stroke-width="1.5" />
    <rect width="820" height="26" rx="8" fill="#0C4A6E" />
    <text x="410" y="18" text-anchor="middle" fill="#7DD3FC" font-size="11" font-weight="700">LOWER PROGRAM ROM ADDRESS SPACE (0000H &#8212; 002FH)</text>

    <!-- 6 Vector Slots -->
    <!-- Slot 0: Reset -->
    <g transform="translate(20, 36)">
      <rect width="120" height="75" rx="4" fill="#0F172A" stroke="#64748B" />
      <text x="60" y="16" text-anchor="middle" fill="#94A3B8" font-size="9" font-weight="600">RESET VECTOR</text>
      <text x="60" y="36" text-anchor="middle" fill="#FFFFFF" font-family="'IBM Plex Mono', monospace" font-size="12" font-weight="700">0000H</text>
      <rect x="10" y="46" width="100" height="20" rx="3" fill="#1E293B" />
      <text x="60" y="60" text-anchor="middle" fill="#38BDF8" font-family="'IBM Plex Mono', monospace" font-size="9">LJMP MAIN</text>
    </g>

    <!-- Slot 1: INT0 -->
    <g transform="translate(150, 36)">
      <rect width="120" height="75" rx="4" fill="#064E3B" stroke="#10B981" stroke-width="1.5" />
      <text x="60" y="16" text-anchor="middle" fill="#6EE7B7" font-size="9" font-weight="700">EXT INT 0 (INT0)</text>
      <text x="60" y="36" text-anchor="middle" fill="#FFFFFF" font-family="'IBM Plex Mono', monospace" font-size="12" font-weight="700">0003H</text>
      <rect x="10" y="46" width="100" height="20" rx="3" fill="#0F172A" />
      <text x="60" y="60" text-anchor="middle" fill="#34D399" font-family="'IBM Plex Mono', monospace" font-size="9">LJMP EX0_ISR</text>
    </g>

    <!-- Slot 2: Timer 0 -->
    <g transform="translate(280, 36)">
      <rect width="120" height="75" rx="4" fill="#0C4A6E" stroke="#38BDF8" stroke-width="1.5" />
      <text x="60" y="16" text-anchor="middle" fill="#7DD3FC" font-size="9" font-weight="700">TIMER 0 (TF0)</text>
      <text x="60" y="36" text-anchor="middle" fill="#FFFFFF" font-family="'IBM Plex Mono', monospace" font-size="12" font-weight="700">000BH</text>
      <rect x="10" y="46" width="100" height="20" rx="3" fill="#0F172A" />
      <text x="60" y="60" text-anchor="middle" fill="#7DD3FC" font-family="'IBM Plex Mono', monospace" font-size="9">LJMP T0_ISR</text>
    </g>

    <!-- Slot 3: INT1 -->
    <g transform="translate(410, 36)">
      <rect width="120" height="75" rx="4" fill="#064E3B" stroke="#10B981" stroke-width="1.5" />
      <text x="60" y="16" text-anchor="middle" fill="#6EE7B7" font-size="9" font-weight="700">EXT INT 1 (INT1)</text>
      <text x="60" y="36" text-anchor="middle" fill="#FFFFFF" font-family="'IBM Plex Mono', monospace" font-size="12" font-weight="700">0013H</text>
      <rect x="10" y="46" width="100" height="20" rx="3" fill="#0F172A" />
      <text x="60" y="60" text-anchor="middle" fill="#34D399" font-family="'IBM Plex Mono', monospace" font-size="9">LJMP EX1_ISR</text>
    </g>

    <!-- Slot 4: Timer 1 -->
    <g transform="translate(540, 36)">
      <rect width="120" height="75" rx="4" fill="#0C4A6E" stroke="#38BDF8" stroke-width="1.5" />
      <text x="60" y="16" text-anchor="middle" fill="#7DD3FC" font-size="9" font-weight="700">TIMER 1 (TF1)</text>
      <text x="60" y="36" text-anchor="middle" fill="#FFFFFF" font-family="'IBM Plex Mono', monospace" font-size="12" font-weight="700">001BH</text>
      <rect x="10" y="46" width="100" height="20" rx="3" fill="#0F172A" />
      <text x="60" y="60" text-anchor="middle" fill="#7DD3FC" font-family="'IBM Plex Mono', monospace" font-size="9">LJMP T1_ISR</text>
    </g>

    <!-- Slot 5: Serial -->
    <g transform="translate(670, 36)">
      <rect width="120" height="75" rx="4" fill="#581C87" stroke="#A855F7" stroke-width="1.5" />
      <text x="60" y="16" text-anchor="middle" fill="#E9D5FF" font-size="9" font-weight="700">SERIAL (RI/TI)</text>
      <text x="60" y="36" text-anchor="middle" fill="#FFFFFF" font-family="'IBM Plex Mono', monospace" font-size="12" font-weight="700">0023H</text>
      <rect x="10" y="46" width="100" height="20" rx="3" fill="#0F172A" />
      <text x="60" y="60" text-anchor="middle" fill="#C084FC" font-family="'IBM Plex Mono', monospace" font-size="9">LJMP UART_ISR</text>
    </g>

    <!-- Spacing Callout -->
    <g transform="translate(20, 125)">
      <rect width="770" height="65" rx="4" fill="#0F172A" stroke="#334155" />
      <text x="385" y="24" text-anchor="middle" fill="#FBBF24" font-size="11" font-weight="700">THE 8-BYTE SPACING WINDOW &#8212; WHY EVERY VECTOR HAS AN LJMP</text>
      <text x="385" y="44" text-anchor="middle" fill="#CBD5E1" font-size="10">Notice: 0003H &#8594; 000BH is exactly 8 bytes. 000BH &#8594; 0013H is exactly 8 bytes. 8 bytes is far too small for a complete handler.</text>
      <text x="385" y="58" text-anchor="middle" fill="#94A3B8" font-size="9">Engineers place a 3-byte jump instruction (LJMP target, opcode 02H) at the vector to branch to the actual ISR body located safely in high memory.</text>
    </g>
  </g>

  <!-- Explanatory note below -->
  <text x="470" y="325" text-anchor="middle" fill="#64748B" font-size="11">Direct hardware PC forcing: the 8051 pushes PC to stack, then sets the Program Counter to the fixed vector address.</text>
</svg>'''

with open("Images/intel_8051_interrupt_vector_table.svg", "w", encoding="utf-8") as f:
    f.write(svg7)
validate_svg("Images/intel_8051_interrupt_vector_table.svg")

# 8. intel_8051_interrupt_lifecycle_flow.svg
svg8 = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 940 370" width="100%" height="100%" style="background:#0B1120; font-family:'DM Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
  <defs>
    <marker id="fl-arr" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#38BDF8" />
    </marker>
    <marker id="fl-green" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#10B981" />
    </marker>
  </defs>

  <!-- Title -->
  <text x="470" y="36" text-anchor="middle" fill="#F8FAFC" font-size="20" font-weight="700" letter-spacing="0.05em">THE 8051 INTERRUPT LIFECYCLE</text>
  <text x="470" y="60" text-anchor="middle" fill="#94A3B8" font-size="13">From physical silicon event to software service routine and RETI unstacking</text>

  <!-- 6 STAGES PIPELINE -->
  <g transform="translate(30, 95)">
    <!-- 1. EVENT -->
    <g transform="translate(0, 0)">
      <rect width="130" height="120" rx="6" fill="#1E293B" stroke="#475569" stroke-width="1.5" />
      <rect width="130" height="24" rx="6" fill="#334155" />
      <text x="65" y="17" text-anchor="middle" fill="#F8FAFC" font-size="10" font-weight="700">1. EVENT</text>
      <text x="65" y="52" text-anchor="middle" fill="#38BDF8" font-size="11" font-weight="600">Hardware Trigger</text>
      <text x="65" y="72" text-anchor="middle" fill="#94A3B8" font-size="9">Pin falling edge</text>
      <text x="65" y="86" text-anchor="middle" fill="#94A3B8" font-size="9">or Timer overflow</text>
      <text x="65" y="105" text-anchor="middle" fill="#64748B" font-size="8">Physical occurrence</text>
    </g>

    <line x1="135" y1="60" x2="150" y2="60" stroke="#38BDF8" stroke-width="2" marker-end="url(#fl-arr)" />

    <!-- 2. FLAG LATCH -->
    <g transform="translate(155, 0)">
      <rect width="130" height="120" rx="6" fill="#1E293B" stroke="#F59E0B" stroke-width="1.5" />
      <rect width="130" height="24" rx="6" fill="#78350F" />
      <text x="65" y="17" text-anchor="middle" fill="#FDE68A" font-size="10" font-weight="700">2. FLAG LATCH</text>
      <text x="65" y="52" text-anchor="middle" fill="#F59E0B" font-size="11" font-weight="600">SFR Bit Raised</text>
      <text x="65" y="72" text-anchor="middle" fill="#CBD5E1" font-family="'IBM Plex Mono', monospace" font-size="10">TFx=1 or IEx=1</text>
      <text x="65" y="90" text-anchor="middle" fill="#94A3B8" font-size="9">in TCON / SCON</text>
      <text x="65" y="105" text-anchor="middle" fill="#64748B" font-size="8">Latched in silicon</text>
    </g>

    <line x1="290" y1="60" x2="305" y2="60" stroke="#38BDF8" stroke-width="2" marker-end="url(#fl-arr)" />

    <!-- 3. AUTHORIZATION -->
    <g transform="translate(310, 0)">
      <rect width="130" height="120" rx="6" fill="#1E293B" stroke="#10B981" stroke-width="1.5" />
      <rect width="130" height="24" rx="6" fill="#064E3B" />
      <text x="65" y="17" text-anchor="middle" fill="#6EE7B7" font-size="10" font-weight="700">3. PERMISSION</text>
      <text x="65" y="52" text-anchor="middle" fill="#34D399" font-size="11" font-weight="600">IE Gate Check</text>
      <text x="65" y="72" text-anchor="middle" fill="#CBD5E1" font-family="'IBM Plex Mono', monospace" font-size="10">EA = 1</text>
      <text x="65" y="90" text-anchor="middle" fill="#CBD5E1" font-family="'IBM Plex Mono', monospace" font-size="10">&amp; Source Bit = 1</text>
      <text x="65" y="105" text-anchor="middle" fill="#64748B" font-size="8">Both gates open</text>
    </g>

    <line x1="445" y1="60" x2="460" y2="60" stroke="#38BDF8" stroke-width="2" marker-end="url(#fl-arr)" />

    <!-- 4. RESOLUTION -->
    <g transform="translate(465, 0)">
      <rect width="130" height="120" rx="6" fill="#1E293B" stroke="#A855F7" stroke-width="1.5" />
      <rect width="130" height="24" rx="6" fill="#581C87" />
      <text x="65" y="17" text-anchor="middle" fill="#E9D5FF" font-size="10" font-weight="700">4. PRIORITY</text>
      <text x="65" y="52" text-anchor="middle" fill="#C084FC" font-size="11" font-weight="600">IP Evaluation</text>
      <text x="65" y="72" text-anchor="middle" fill="#CBD5E1" font-size="9">High vs Low</text>
      <text x="65" y="88" text-anchor="middle" fill="#CBD5E1" font-size="9">Preempt if higher</text>
      <text x="65" y="105" text-anchor="middle" fill="#64748B" font-size="8">Polling tie-breaker</text>
    </g>

    <line x1="600" y1="60" x2="615" y2="60" stroke="#38BDF8" stroke-width="2" marker-end="url(#fl-arr)" />

    <!-- 5. HARDWARE DISPATCH -->
    <g transform="translate(620, 0)">
      <rect width="130" height="120" rx="6" fill="#1E293B" stroke="#38BDF8" stroke-width="1.5" />
      <rect width="130" height="24" rx="6" fill="#0C4A6E" />
      <text x="65" y="17" text-anchor="middle" fill="#7DD3FC" font-size="10" font-weight="700">5. VECTORING</text>
      <text x="65" y="52" text-anchor="middle" fill="#38BDF8" font-size="11" font-weight="600">Stack &amp; Branch</text>
      <text x="65" y="72" text-anchor="middle" fill="#CBD5E1" font-size="9">Push PC to stack</text>
      <text x="65" y="88" text-anchor="middle" fill="#38BDF8" font-family="'IBM Plex Mono', monospace" font-size="10">PC &#8592; Vector</text>
      <text x="65" y="105" text-anchor="middle" fill="#64748B" font-size="8">Auto-clear flag</text>
    </g>

    <line x1="755" y1="60" x2="770" y2="60" stroke="#10B981" stroke-width="2" marker-end="url(#fl-green)" />

    <!-- 6. ISR & RETI -->
    <g transform="translate(775, 0)">
      <rect width="130" height="120" rx="6" fill="#1E293B" stroke="#10B981" stroke-width="1.8" />
      <rect width="130" height="24" rx="6" fill="#064E3B" />
      <text x="65" y="17" text-anchor="middle" fill="#6EE7B7" font-size="10" font-weight="700">6. RETI RETURN</text>
      <text x="65" y="52" text-anchor="middle" fill="#34D399" font-size="11" font-weight="600">Handler &amp; Exit</text>
      <text x="65" y="72" text-anchor="middle" fill="#CBD5E1" font-size="9">Execute ISR body</text>
      <text x="65" y="90" text-anchor="middle" fill="#34D399" font-family="'IBM Plex Mono', monospace" font-size="11" font-weight="700">RETI</text>
      <text x="65" y="105" text-anchor="middle" fill="#64748B" font-size="8">Clear priority latch</text>
    </g>
  </g>

  <!-- Bottom Synthesis Banner -->
  <g transform="translate(30, 245)">
    <rect width="875" height="95" rx="6" fill="#1E293B" stroke="#334155" />
    <text x="25" y="24" fill="#38BDF8" font-size="11" font-weight="700">THE CONVERSATION BETWEEN SILICON COMPONENTS</text>
    <text x="25" y="46" fill="#CBD5E1" font-size="11">The timer didn't know how to interrupt the CPU &#8212; it only knew how to count. When its count overflowed, a bit in TCON changed. The interrupt unit recognized that event, checked IE permissions, resolved IP priorities, pushed the Program Counter, redirected execution to low ROM space, and allowed software to respond.</text>
    <text x="25" y="74" fill="#94A3B8" font-size="10">What looked like a single hardware event was actually an orchestrated conversation across five different Special Function Registers.</text>
  </g>
</svg>'''

with open("Images/intel_8051_interrupt_lifecycle_flow.svg", "w", encoding="utf-8") as f:
    f.write(svg8)
validate_svg("Images/intel_8051_interrupt_lifecycle_flow.svg")

print("All 8 Interrupt SVGs generated and validated successfully!")
