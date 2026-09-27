import xml.etree.ElementTree as ET

# 1. intel_8051_timer_vs_counter_sources.svg
svg1 = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 380" width="100%" height="100%" style="background:#0B1120; font-family:'DM Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
  <defs>
    <linearGradient id="boxGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1E293B"/>
      <stop offset="100%" stop-color="#0F172A"/>
    </linearGradient>
    <marker id="m-arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#38BDF8" />
    </marker>
    <marker id="m-amber" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#F59E0B" />
    </marker>
    <marker id="m-green" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#10B981" />
    </marker>
  </defs>

  <!-- Title -->
  <text x="450" y="38" text-anchor="middle" fill="#F8FAFC" font-size="20" font-weight="700" letter-spacing="0.05em">TIMER OR COUNTER? THE PULSE SOURCE</text>
  <text x="450" y="62" text-anchor="middle" fill="#94A3B8" font-size="13">The counting register is identical. What changes is what triggers the count.</text>

  <!-- UPPER PATH: TIMER MODE (C/T = 0) -->
  <g transform="translate(50, 90)">
    <rect width="250" height="90" rx="8" fill="url(#boxGrad)" stroke="#38BDF8" stroke-width="1.5" />
    <rect width="250" height="26" rx="8" fill="#0C4A6E" />
    <text x="125" y="18" text-anchor="middle" fill="#7DD3FC" font-size="11" font-weight="700">TIMER MODE (C/T = 0)</text>
    <text x="125" y="52" text-anchor="middle" fill="#F8FAFC" font-size="12" font-weight="600">Internal Machine Cycles</text>
    <text x="125" y="72" text-anchor="middle" fill="#94A3B8" font-size="11">Oscillator / 12 (Predictable Time)</text>

    <!-- Output wire -->
    <path d="M 255 45 L 360 45" fill="none" stroke="#38BDF8" stroke-width="2" marker-end="url(#m-arrow)" />
  </g>

  <!-- LOWER PATH: COUNTER MODE (C/T = 1) -->
  <g transform="translate(50, 220)">
    <rect width="250" height="90" rx="8" fill="url(#boxGrad)" stroke="#F59E0B" stroke-width="1.5" />
    <rect width="250" height="26" rx="8" fill="#78350F" />
    <text x="125" y="18" text-anchor="middle" fill="#FCD34D" font-size="11" font-weight="700">COUNTER MODE (C/T = 1)</text>
    <text x="125" y="52" text-anchor="middle" fill="#F8FAFC" font-size="12" font-weight="600">External Input Pin</text>
    <text x="125" y="72" text-anchor="middle" fill="#FDE68A" font-family="'IBM Plex Mono', monospace" font-size="11">Pin P3.4 (T0) / P3.5 (T1)</text>

    <!-- Output wire -->
    <path d="M 255 45 L 360 45" fill="none" stroke="#F59E0B" stroke-width="2" marker-end="url(#m-amber)" />
  </g>

  <!-- MULTIPLEXER SWITCH (C/T BIT IN TMOD) -->
  <g transform="translate(420, 140)">
    <rect width="140" height="120" rx="8" fill="#1E293B" stroke="#475569" stroke-width="1.5" />
    <text x="70" y="24" text-anchor="middle" fill="#E2E8F0" font-size="11" font-weight="700">C/T SWITCH</text>
    <text x="70" y="42" text-anchor="middle" fill="#94A3B8" font-family="'IBM Plex Mono', monospace" font-size="10">(in TMOD: 89H)</text>
    
    <!-- Switch graphic -->
    <circle cx="35" cy="65" r="4" fill="#38BDF8" />
    <text x="20" y="68" fill="#38BDF8" font-size="10">0</text>
    <circle cx="35" cy="95" r="4" fill="#F59E0B" />
    <text x="20" y="98" fill="#F59E0B" font-size="10">1</text>
    <circle cx="105" cy="80" r="4" fill="#10B981" />

    <line x1="105" y1="80" x2="38" y2="67" stroke="#10B981" stroke-width="2.5" />
  </g>

  <!-- WIRE TO COUNTER -->
  <line x1="565" y1="200" x2="620" y2="200" stroke="#10B981" stroke-width="2.5" marker-end="url(#m-green)" />

  <!-- COUNTER REGISTER -->
  <g transform="translate(625, 125)">
    <rect width="225" height="150" rx="8" fill="#064E3B" fill-opacity="0.4" stroke="#10B981" stroke-width="1.5" />
    <rect width="225" height="28" rx="8" fill="#064E3B" />
    <text x="112" y="19" text-anchor="middle" fill="#34D399" font-size="11" font-weight="700">HARDWARE COUNTER</text>

    <text x="112" y="60" text-anchor="middle" fill="#E2E8F0" font-size="12" font-weight="600">THx : TLx (16 Bits)</text>
    <text x="112" y="85" text-anchor="middle" fill="#94A3B8" font-size="11">Increments by 1 on each pulse</text>
    <text x="112" y="110" text-anchor="middle" fill="#6EE7B7" font-size="11">Does not care where pulse came from</text>
    <text x="112" y="132" text-anchor="middle" fill="#A7F3D0" font-size="10">Only counts.</text>
  </g>
</svg>'''

# 2. intel_8051_two_timers_architecture.svg
svg2 = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 380" width="100%" height="100%" style="background:#0B1120; font-family:'DM Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
  <defs>
    <linearGradient id="cardGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1E293B"/>
      <stop offset="100%" stop-color="#0F172A"/>
    </linearGradient>
  </defs>

  <!-- Title -->
  <text x="450" y="38" text-anchor="middle" fill="#F8FAFC" font-size="20" font-weight="700" letter-spacing="0.05em">TWO TIMERS, ONE ARCHITECTURAL PATTERN</text>
  <text x="450" y="62" text-anchor="middle" fill="#94A3B8" font-size="13">Independent 16-bit hardware counters orchestrated through shared control SFRs</text>

  <!-- SHARED CONTROL PANEL ROW -->
  <g transform="translate(60, 85)">
    <!-- TMOD (89H) -->
    <g transform="translate(0, 0)">
      <rect width="365" height="85" rx="8" fill="url(#cardGrad)" stroke="#38BDF8" stroke-width="1.5" />
      <rect width="365" height="26" rx="8" fill="#0C4A6E" />
      <text x="182" y="18" text-anchor="middle" fill="#7DD3FC" font-size="11" font-weight="700">TMOD (89H) &#8212; MODE CONFIGURATION (BYTE-ONLY)</text>
      
      <!-- Bit Split -->
      <g transform="translate(15, 36)">
        <rect width="160" height="36" rx="4" fill="#0F172A" stroke="#334155" />
        <text x="80" y="16" text-anchor="middle" fill="#818CF8" font-size="10" font-weight="600">Timer 1 Config (Bits 7..4)</text>
        <text x="80" y="30" text-anchor="middle" fill="#94A3B8" font-family="'IBM Plex Mono', monospace" font-size="9">GATE | C/T | M1 | M0</text>

        <rect x="175" y="0" width="160" height="36" rx="4" fill="#0F172A" stroke="#334155" />
        <text x="255" y="16" text-anchor="middle" fill="#34D399" font-size="10" font-weight="600">Timer 0 Config (Bits 3..0)</text>
        <text x="255" y="30" text-anchor="middle" fill="#94A3B8" font-family="'IBM Plex Mono', monospace" font-size="9">GATE | C/T | M1 | M0</text>
      </g>
    </g>

    <!-- TCON (88H) -->
    <g transform="translate(415, 0)">
      <rect width="365" height="85" rx="8" fill="url(#cardGrad)" stroke="#10B981" stroke-width="1.5" />
      <rect width="365" height="26" rx="8" fill="#064E3B" />
      <text x="182" y="18" text-anchor="middle" fill="#6EE7B7" font-size="11" font-weight="700">TCON (88H) &#8212; RUN / STATUS LEVERS (BIT-ADDRESSABLE)</text>
      
      <!-- Bit Split -->
      <g transform="translate(15, 36)">
        <rect width="160" height="36" rx="4" fill="#0F172A" stroke="#334155" />
        <text x="80" y="16" text-anchor="middle" fill="#818CF8" font-size="10" font-weight="600">Timer 1 (Bits 7..6)</text>
        <text x="80" y="30" text-anchor="middle" fill="#CBD5E1" font-family="'IBM Plex Mono', monospace" font-size="9">TF1 (8FH) | TR1 (8EH)</text>

        <rect x="175" y="0" width="160" height="36" rx="4" fill="#0F172A" stroke="#334155" />
        <text x="255" y="16" text-anchor="middle" fill="#34D399" font-size="10" font-weight="600">Timer 0 (Bits 5..4)</text>
        <text x="255" y="30" text-anchor="middle" fill="#CBD5E1" font-family="'IBM Plex Mono', monospace" font-size="9">TF0 (8DH) | TR0 (8CH)</text>
      </g>
    </g>
  </g>

  <!-- TIMER 0 CARD -->
  <g transform="translate(60, 195)">
    <rect width="375" height="175" rx="8" fill="url(#cardGrad)" stroke="#10B981" stroke-width="1.5" />
    <rect width="375" height="32" rx="8" fill="#064E3B" />
    <text x="20" y="21" fill="#6EE7B7" font-size="12" font-weight="700">TIMER 0 (16-BIT COUNTER)</text>

    <text x="25" y="60" fill="#94A3B8" font-size="11">Physical Counting Registers:</text>

    <!-- TL0 (8AH) / TH0 (8CH) -->
    <g transform="translate(25, 75)">
      <rect x="0" y="0" width="155" height="46" rx="4" fill="#0F172A" stroke="#334155" />
      <text x="15" y="20" fill="#94A3B8" font-size="10">Low Byte (8AH)</text>
      <text x="15" y="36" fill="#34D399" font-family="'IBM Plex Mono', monospace" font-size="13" font-weight="600">TL0 = 8AH</text>

      <rect x="170" y="0" width="155" height="46" rx="4" fill="#0F172A" stroke="#334155" />
      <text x="185" y="20" fill="#94A3B8" font-size="10">High Byte (8CH)</text>
      <text x="185" y="36" fill="#34D399" font-family="'IBM Plex Mono', monospace" font-size="13" font-weight="600">TH0 = 8CH</text>
    </g>

    <text x="25" y="145" fill="#CBD5E1" font-size="11">Run bit: <tspan fill="#38BDF8" font-family="'IBM Plex Mono', monospace">TR0 (8CH)</tspan>  |  Overflow flag: <tspan fill="#F59E0B" font-family="'IBM Plex Mono', monospace">TF0 (8DH)</tspan></text>
    <text x="25" y="162" fill="#94A3B8" font-size="10">External input pin: P3.4 (T0)</text>
  </g>

  <!-- TIMER 1 CARD -->
  <g transform="translate(465, 195)">
    <rect width="375" height="175" rx="8" fill="url(#cardGrad)" stroke="#6366F1" stroke-width="1.5" />
    <rect width="375" height="32" rx="8" fill="#312E81" />
    <text x="20" y="21" fill="#A5B4FC" font-size="12" font-weight="700">TIMER 1 (16-BIT COUNTER)</text>

    <text x="25" y="60" fill="#94A3B8" font-size="11">Physical Counting Registers:</text>

    <!-- TL1 (8BH) / TH1 (8DH) -->
    <g transform="translate(25, 75)">
      <rect x="0" y="0" width="155" height="46" rx="4" fill="#0F172A" stroke="#334155" />
      <text x="15" y="20" fill="#94A3B8" font-size="10">Low Byte (8BH)</text>
      <text x="15" y="36" fill="#818CF8" font-family="'IBM Plex Mono', monospace" font-size="13" font-weight="600">TL1 = 8BH</text>

      <rect x="170" y="0" width="155" height="46" rx="4" fill="#0F172A" stroke="#334155" />
      <text x="185" y="20" fill="#94A3B8" font-size="10">High Byte (8DH)</text>
      <text x="185" y="36" fill="#818CF8" font-family="'IBM Plex Mono', monospace" font-size="13" font-weight="600">TH1 = 8DH</text>
    </g>

    <text x="25" y="145" fill="#CBD5E1" font-size="11">Run bit: <tspan fill="#38BDF8" font-family="'IBM Plex Mono', monospace">TR1 (8EH)</tspan>  |  Overflow flag: <tspan fill="#F59E0B" font-family="'IBM Plex Mono', monospace">TF1 (8FH)</tspan></text>
    <text x="25" y="162" fill="#94A3B8" font-size="10">External input pin: P3.5 (T1) | Often generates UART baud rate</text>
  </g>
</svg>'''

# 3. intel_8051_timer_clock_to_overflow.svg
svg3 = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 380" width="100%" height="100%" style="background:#0B1120; font-family:'DM Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
  <defs>
    <marker id="t-arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#38BDF8" />
    </marker>
    <marker id="t-overflow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#F59E0B" />
    </marker>
  </defs>

  <!-- Title -->
  <text x="450" y="38" text-anchor="middle" fill="#F8FAFC" font-size="20" font-weight="700" letter-spacing="0.05em">THE 8051 CLOCK-TO-OVERFLOW PIPELINE</text>
  <text x="450" y="62" text-anchor="middle" fill="#94A3B8" font-size="13">From oscillator rhythm to hardware flag in the 8051 architecture</text>

  <!-- STAGES -->
  <g transform="translate(40, 95)">
    <!-- 1. CRYSTAL OSCILLATOR -->
    <g transform="translate(0, 30)">
      <rect width="140" height="130" rx="8" fill="#1E293B" stroke="#475569" stroke-width="1.5" />
      <rect width="140" height="28" rx="8" fill="#334155" />
      <text x="70" y="19" text-anchor="middle" fill="#F8FAFC" font-size="11" font-weight="700">1. OSCILLATOR</text>
      <text x="70" y="58" text-anchor="middle" fill="#38BDF8" font-size="12" font-weight="600">Crystal Clock</text>
      <text x="70" y="78" text-anchor="middle" fill="#94A3B8" font-family="'IBM Plex Mono', monospace" font-size="11">12 MHz</text>
      <path d="M 25 108 Q 40 92 55 108 T 85 108 T 115 108" fill="none" stroke="#38BDF8" stroke-width="1.5" />
      <text x="70" y="125" text-anchor="middle" fill="#64748B" font-size="9">Continuous rhythm</text>
    </g>

    <!-- ARROW 1 -->
    <line x1="145" y1="95" x2="175" y2="95" stroke="#38BDF8" stroke-width="2" marker-end="url(#t-arrow)" />

    <!-- 2. PRESCALER (DIVIDE BY 12) -->
    <g transform="translate(180, 30)">
      <rect width="130" height="130" rx="8" fill="#1E293B" stroke="#475569" stroke-width="1.5" />
      <rect width="130" height="28" rx="8" fill="#334155" />
      <text x="65" y="19" text-anchor="middle" fill="#F8FAFC" font-size="11" font-weight="700">2. PRESCALER</text>
      <text x="65" y="58" text-anchor="middle" fill="#38BDF8" font-size="12" font-weight="600">Divide by 12</text>
      <text x="65" y="78" text-anchor="middle" fill="#94A3B8" font-size="10">1 Machine Cycle</text>
      <text x="65" y="98" text-anchor="middle" fill="#E2E8F0" font-family="'IBM Plex Mono', monospace" font-size="11" font-weight="600">= 1 &#181;s tick</text>
      <text x="65" y="122" text-anchor="middle" fill="#64748B" font-size="9">(at 12 MHz xtal)</text>
    </g>

    <!-- ARROW 2 -->
    <line x1="315" y1="95" x2="345" y2="95" stroke="#38BDF8" stroke-width="2" marker-end="url(#t-arrow)" />

    <!-- 3. RUN GATE (TR0) -->
    <g transform="translate(350, 30)">
      <rect width="120" height="130" rx="8" fill="#1E293B" stroke="#2563EB" stroke-width="1.5" />
      <rect width="120" height="28" rx="8" fill="#1D4ED8" />
      <text x="60" y="19" text-anchor="middle" fill="#F8FAFC" font-size="11" font-weight="700">3. RUN GATE</text>
      <text x="60" y="58" text-anchor="middle" fill="#60A5FA" font-size="12" font-weight="600">TR0 Bit</text>
      <text x="60" y="78" text-anchor="middle" fill="#93C5FD" font-family="'IBM Plex Mono', monospace" font-size="11">TCON.4 (8CH)</text>
      <circle cx="60" cy="102" r="12" fill="#0F172A" stroke="#38BDF8" stroke-width="1.5" />
      <line x1="52" y1="108" x2="68" y2="96" stroke="#10B981" stroke-width="2" />
      <text x="60" y="125" text-anchor="middle" fill="#94A3B8" font-size="9">SETB TR0</text>
    </g>

    <!-- ARROW 3 -->
    <line x1="475" y1="95" x2="505" y2="95" stroke="#38BDF8" stroke-width="2" marker-end="url(#t-arrow)" />

    <!-- 4. 16-BIT COUNTER (TH0:TL0) -->
    <g transform="translate(510, 20)">
      <rect width="170" height="150" rx="8" fill="#1E293B" stroke="#10B981" stroke-width="1.5" />
      <rect width="170" height="28" rx="8" fill="#064E3B" />
      <text x="85" y="19" text-anchor="middle" fill="#34D399" font-size="11" font-weight="700">4. 16-BIT COUNTER</text>
      
      <!-- Registers -->
      <rect x="15" y="42" width="65" height="42" rx="4" fill="#0F172A" stroke="#334155" />
      <text x="47" y="58" text-anchor="middle" fill="#94A3B8" font-size="10">TL0</text>
      <text x="47" y="76" text-anchor="middle" fill="#34D399" font-family="'IBM Plex Mono', monospace" font-size="11" font-weight="600">8AH</text>

      <rect x="90" y="42" width="65" height="42" rx="4" fill="#0F172A" stroke="#334155" />
      <text x="122" y="58" text-anchor="middle" fill="#94A3B8" font-size="10">TH0</text>
      <text x="122" y="76" text-anchor="middle" fill="#34D399" font-family="'IBM Plex Mono', monospace" font-size="11" font-weight="600">8CH</text>

      <text x="85" y="108" text-anchor="middle" fill="#CBD5E1" font-size="11">Increments every tick</text>
      <text x="85" y="128" text-anchor="middle" fill="#6EE7B7" font-family="'IBM Plex Mono', monospace" font-size="10">0000H &#8594; FFFFH</text>
      <text x="85" y="145" text-anchor="middle" fill="#94A3B8" font-size="9">Up to 65,536 counts</text>
    </g>

    <!-- ARROW 4 (OVERFLOW) -->
    <line x1="685" y1="95" x2="715" y2="95" stroke="#F59E0B" stroke-width="2.5" marker-end="url(#t-overflow)" />

    <!-- 5. OVERFLOW FLAG (TF0) -->
    <g transform="translate(720, 30)">
      <rect width="140" height="130" rx="8" fill="#1E293B" stroke="#F59E0B" stroke-width="1.5" />
      <rect width="140" height="28" rx="8" fill="#78350F" />
      <text x="70" y="19" text-anchor="middle" fill="#FCD34D" font-size="11" font-weight="700">5. OVERFLOW EVENT</text>
      <text x="70" y="58" text-anchor="middle" fill="#F59E0B" font-size="12" font-weight="700">TF0 Flag</text>
      <text x="70" y="78" text-anchor="middle" fill="#FDE68A" font-family="'IBM Plex Mono', monospace" font-size="11">TCON.5 (8DH) = 1</text>
      <rect x="15" y="94" width="110" height="26" rx="4" fill="#451A03" stroke="#F59E0B" />
      <text x="70" y="111" text-anchor="middle" fill="#FDE68A" font-size="10" font-weight="600">CPU Responds (ISR)</text>
    </g>
  </g>

  <!-- BOTTOM REFLECTION -->
  <text x="450" y="320" text-anchor="middle" fill="#94A3B8" font-size="12">A timer does not generate time out of nothing. It counts the continuous machine cycles of the 8051.</text>
  <text x="450" y="340" text-anchor="middle" fill="#38BDF8" font-size="12" font-weight="600">When the counter overflows, time has become a hardware event.</text>
</svg>'''

# 4. intel_8051_timer_to_waveform.svg
svg4 = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 420" width="100%" height="100%" style="background:#0B1120; font-family:'DM Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
  <defs>
    <marker id="w-arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#38BDF8" />
    </marker>
    <marker id="w-amber" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#F59E0B" />
    </marker>
    <marker id="w-green" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#10B981" />
    </marker>
  </defs>

  <!-- Title -->
  <text x="450" y="35" text-anchor="middle" fill="#F8FAFC" font-size="20" font-weight="700" letter-spacing="0.05em">FROM OVERFLOW EVENT TO PHYSICAL WAVEFORM</text>
  <text x="450" y="58" text-anchor="middle" fill="#94A3B8" font-size="13">The causal chain: Hardware overflow triggers CPU/ISR response to toggle an output pin</text>

  <!-- 1. TIMER COUNT (SAWTOOTH) -->
  <g transform="translate(60, 85)">
    <text x="0" y="16" fill="#38BDF8" font-size="12" font-weight="700">[HARDWARE] 1. SILICON COUNTER (TH0:TL0)</text>
    <text x="780" y="16" text-anchor="end" fill="#94A3B8" font-family="'IBM Plex Mono', monospace" font-size="11">FFFFH (Limit)</text>

    <!-- Sawtooth Wave -->
    <path d="M 0 100 L 150 30 L 150 100 L 300 30 L 300 100 L 450 30 L 450 100 L 600 30 L 600 100 L 750 30 L 750 100" fill="none" stroke="#38BDF8" stroke-width="2" />
    
    <!-- Dashed Overflow Threshold -->
    <line x1="0" y1="30" x2="780" y2="30" stroke="#F59E0B" stroke-width="1" stroke-dasharray="4 4" />
    <text x="15" y="25" fill="#F59E0B" font-size="10">Overflow Rollover (FFFFH &#8594; 0000H)</text>

    <!-- Overflow pulses -->
    <circle cx="150" cy="30" r="4" fill="#F59E0B" />
    <circle cx="300" cy="30" r="4" fill="#F59E0B" />
    <circle cx="450" cy="30" r="4" fill="#F59E0B" />
    <circle cx="600" cy="30" r="4" fill="#F59E0B" />
    <circle cx="750" cy="30" r="4" fill="#F59E0B" />

    <!-- Pulse arrows down -->
    <line x1="150" y1="35" x2="150" y2="115" stroke="#F59E0B" stroke-width="1.5" stroke-dasharray="2 2" marker-end="url(#w-amber)" />
    <line x1="300" y1="35" x2="300" y2="115" stroke="#F59E0B" stroke-width="1.5" stroke-dasharray="2 2" marker-end="url(#w-amber)" />
    <line x1="450" y1="35" x2="450" y2="115" stroke="#F59E0B" stroke-width="1.5" stroke-dasharray="2 2" marker-end="url(#w-amber)" />
    <line x1="600" y1="35" x2="600" y2="115" stroke="#F59E0B" stroke-width="1.5" stroke-dasharray="2 2" marker-end="url(#w-amber)" />
    <line x1="750" y1="35" x2="750" y2="115" stroke="#F59E0B" stroke-width="1.5" stroke-dasharray="2 2" marker-end="url(#w-amber)" />
  </g>

  <!-- 2. INTERMEDIATE SOFTWARE RESPONSE (CAUSAL BRIDGE) -->
  <g transform="translate(60, 215)">
    <rect width="780" height="42" rx="6" fill="#1E293B" stroke="#F59E0B" stroke-width="1" />
    <text x="20" y="26" fill="#FCD34D" font-size="11" font-weight="700">[CPU / SOFTWARE]</text>
    <text x="145" y="26" fill="#E2E8F0" font-size="11">Hardware sets <tspan fill="#F59E0B" font-family="'IBM Plex Mono', monospace" font-weight="700">TF0 = 1</tspan> &#8594; CPU ISR or polling loop executes <tspan fill="#38BDF8" font-family="'IBM Plex Mono', monospace" font-weight="700">CPL P1.0</tspan> &#8594; Pin port latch state inverts</text>
  </g>

  <!-- 3. PHYSICAL PIN OUTPUT (SQUARE WAVEFORM) -->
  <g transform="translate(60, 275)">
    <text x="0" y="16" fill="#10B981" font-size="12" font-weight="700">[PHYSICAL WORLD] 3. PIN P1.0 ELECTRICAL VOLTAGE</text>
    <text x="780" y="16" text-anchor="end" fill="#94A3B8" font-size="11">Square Waveform</text>

    <!-- Square Wave -->
    <path d="M 0 80 L 150 80 L 150 30 L 300 30 L 300 80 L 450 80 L 450 30 L 600 30 L 600 80 L 750 80 L 750 30 L 780 30" fill="none" stroke="#10B981" stroke-width="2.5" />

    <text x="75" y="98" text-anchor="middle" fill="#94A3B8" font-size="10">LOW (0V)</text>
    <text x="225" y="24" text-anchor="middle" fill="#34D399" font-size="10" font-weight="600">HIGH (+5V)</text>
    <text x="375" y="98" text-anchor="middle" fill="#94A3B8" font-size="10">LOW (0V)</text>
    <text x="525" y="24" text-anchor="middle" fill="#34D399" font-size="10" font-weight="600">HIGH (+5V)</text>
    <text x="675" y="98" text-anchor="middle" fill="#94A3B8" font-size="10">LOW (0V)</text>
  </g>

  <!-- FOOTER NOTE -->
  <text x="450" y="395" text-anchor="middle" fill="#64748B" font-size="11">Classic 8051 timers do not directly toggle GPIO pins; hardware asserts TF0, and CPU software inverts the pin.</text>
</svg>'''

files = {
    'Images/intel_8051_timer_vs_counter_sources.svg': svg1,
    'Images/intel_8051_two_timers_architecture.svg': svg2,
    'Images/intel_8051_timer_clock_to_overflow.svg': svg3,
    'Images/intel_8051_timer_to_waveform.svg': svg4
}

for path, content in files.items():
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    # validate XML
    ET.fromstring(content)
    print(f"Validated and saved: {path}")
