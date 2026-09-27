import os

def create_software_delay_vs_hardware_timer():
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 420" width="100%" height="100%" style="background:#0B1120; font-family:'DM Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1E293B"/>
      <stop offset="100%" stop-color="#0F172A"/>
    </linearGradient>
    <marker id="arrow-red" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#EF4444" />
    </marker>
    <marker id="arrow-green" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#10B981" />
    </marker>
  </defs>

  <!-- Title -->
  <text x="450" y="38" text-anchor="middle" fill="#F8FAFC" font-size="20" font-weight="700" letter-spacing="0.05em">THE PROBLEM WITH WAITING</text>
  <text x="450" y="62" text-anchor="middle" fill="#94A3B8" font-size="13">Software Delay Loops vs Autonomous Silicon Hardware Timers</text>

  <!-- LEFT: SOFTWARE DELAY (CPU TRAPPED) -->
  <g transform="translate(45, 90)">
    <rect width="380" height="295" rx="10" fill="url(#bgGrad)" stroke="#EF4444" stroke-width="1.5" stroke-dasharray="0" />
    <rect width="380" height="36" rx="10" fill="#450A0A" />
    <text x="190" y="23" text-anchor="middle" fill="#FCA5A5" font-size="12" font-weight="700" letter-spacing="0.05em">SOFTWARE DELAY LOOP: CPU BURNING CYCLES</text>

    <!-- Code Block -->
    <rect x="25" y="55" width="330" height="75" rx="6" fill="#0F172A" stroke="#334155" />
    <text x="40" y="78" fill="#F87171" font-family="'IBM Plex Mono', monospace" font-size="12">DELAY: MOV R2, #250</text>
    <text x="40" y="98" fill="#F87171" font-family="'IBM Plex Mono', monospace" font-size="12">LOOP:  DJNZ R2, LOOP</text>
    <text x="40" y="118" fill="#94A3B8" font-family="'IBM Plex Mono', monospace" font-size="11">; CPU trapped in repetitive decrement</text>

    <!-- Spin Flow -->
    <circle cx="190" cy="180" r="32" fill="none" stroke="#EF4444" stroke-width="2" stroke-dasharray="4 4" />
    <text x="190" y="177" text-anchor="middle" fill="#EF4444" font-size="11" font-weight="700">100% CPU</text>
    <text x="190" y="192" text-anchor="middle" fill="#FCA5A5" font-size="10">SPINNING</text>

    <!-- Consequence -->
    <rect x="25" y="232" width="330" height="48" rx="6" fill="#1E293B" />
    <text x="190" y="251" text-anchor="middle" fill="#FCA5A5" font-size="11" font-weight="600">The CPU is completely blind</text>
    <text x="190" y="268" text-anchor="middle" fill="#94A3B8" font-size="10">Cannot calculate, sense, or communicate while waiting</text>
  </g>

  <!-- RIGHT: HARDWARE TIMER (CPU FREED) -->
  <g transform="translate(475, 90)">
    <rect width="380" height="295" rx="10" fill="url(#bgGrad)" stroke="#10B981" stroke-width="1.5" />
    <rect width="380" height="36" rx="10" fill="#064E3B" />
    <text x="190" y="23" text-anchor="middle" fill="#6EE7B7" font-size="12" font-weight="700" letter-spacing="0.05em">HARDWARE TIMER: AUTONOMOUS COUNTING</text>

    <!-- Parallel Streams -->
    <g transform="translate(25, 55)">
      <!-- CPU Box -->
      <rect width="330" height="42" rx="6" fill="#0F172A" stroke="#38BDF8" stroke-width="1" />
      <text x="15" y="26" fill="#38BDF8" font-size="12" font-weight="600">CPU Core:</text>
      <text x="90" y="26" fill="#E2E8F0" font-size="11">Executes real application tasks freely</text>
    </g>

    <!-- Silicon Counter Box -->
    <g transform="translate(25, 115)">
      <rect width="330" height="75" rx="6" fill="#0F172A" stroke="#10B981" stroke-width="1.5" />
      <text x="15" y="24" fill="#34D399" font-size="12" font-weight="600">Hardware Timer (TL0 / TH0):</text>
      <text x="15" y="44" fill="#94A3B8" font-size="11">Counts machine cycles silently in silicon circuitry</text>
      <text x="15" y="62" fill="#6EE7B7" font-family="'IBM Plex Mono', monospace" font-size="11">0000H → ... → FFFFH → OVERFLOW EVENT</text>
    </g>

    <!-- Consequence -->
    <rect x="25" y="232" width="330" height="48" rx="6" fill="#064E3B" fill-opacity="0.4" stroke="#10B981" stroke-width="1" />
    <text x="190" y="251" text-anchor="middle" fill="#34D399" font-size="11" font-weight="700">Zero CPU overhead during counting</text>
    <text x="190" y="268" text-anchor="middle" fill="#A7F3D0" font-size="10">Hardware alerts the CPU only when the time period expires</text>
  </g>
</svg>'''
    with open('Images/intel_8051_software_delay_vs_hardware_timer.svg', 'w', encoding='utf-8') as f:
        f.write(svg)
    print('Created Images/intel_8051_software_delay_vs_hardware_timer.svg')

def create_timer_clock_to_overflow():
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 380" width="100%" height="100%" style="background:#0B1120; font-family:'DM Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
  <defs>
    <marker id="t-arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#38BDF8" />
    </marker>
    <marker id="t-overflow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#F59E0B" />
    </marker>
  </defs>

  <!-- Title -->
  <text x="450" y="38" text-anchor="middle" fill="#F8FAFC" font-size="20" font-weight="700" letter-spacing="0.05em">THE CLOCK TO OVERFLOW PIPELINE</text>
  <text x="450" y="62" text-anchor="middle" fill="#94A3B8" font-size="13">How periodic clock events translate into hardware alerts in silicon</text>

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
      <text x="65" y="98" text-anchor="middle" fill="#E2E8F0" font-family="'IBM Plex Mono', monospace" font-size="11" font-weight="600">= 1 µs tick</text>
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
      <text x="60" y="78" text-anchor="middle" fill="#93C5FD" font-family="'IBM Plex Mono', monospace" font-size="11">TCON.4</text>
      <circle cx="60" cy="102" r="12" fill="#0F172A" stroke="#38BDF8" stroke-width="1.5" />
      <line x1="52" y1="108" x2="68" y2="96" stroke="#10B981" stroke-width="2" />
      <text x="60" y="125" text-anchor="middle" fill="#94A3B8" font-size="9">Software Switch</text>
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
      <text x="47" y="58" text-anchor="middle" fill="#94A3B8" font-size="10">TH0</text>
      <text x="47" y="76" text-anchor="middle" fill="#34D399" font-family="'IBM Plex Mono', monospace" font-size="11" font-weight="600">8AH</text>

      <rect x="90" y="42" width="65" height="42" rx="4" fill="#0F172A" stroke="#334155" />
      <text x="122" y="58" text-anchor="middle" fill="#94A3B8" font-size="10">TL0</text>
      <text x="122" y="76" text-anchor="middle" fill="#34D399" font-family="'IBM Plex Mono', monospace" font-size="11" font-weight="600">8BH</text>

      <text x="85" y="108" text-anchor="middle" fill="#CBD5E1" font-size="11">Increments every tick</text>
      <text x="85" y="128" text-anchor="middle" fill="#6EE7B7" font-family="'IBM Plex Mono', monospace" font-size="10">0000H → FFFFH</text>
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
      <text x="70" y="78" text-anchor="middle" fill="#FDE68A" font-family="'IBM Plex Mono', monospace" font-size="11">TCON.5 = 1</text>
      <rect x="20" y="94" width="100" height="26" rx="4" fill="#451A03" stroke="#F59E0B" />
      <text x="70" y="111" text-anchor="middle" fill="#FDE68A" font-size="10" font-weight="600">CPU Responds</text>
    </g>
  </g>

  <!-- BOTTOM REFLECTION -->
  <text x="450" y="320" text-anchor="middle" fill="#94A3B8" font-size="12">A timer does not generate time out of nothing. It counts the continuous rhythm of the machine.</text>
  <text x="450" y="340" text-anchor="middle" fill="#38BDF8" font-size="12" font-weight="600">When the counter overflows, time has become a hardware event.</text>
</svg>'''
    with open('Images/intel_8051_timer_clock_to_overflow.svg', 'w', encoding='utf-8') as f:
        f.write(svg)
    print('Created Images/intel_8051_timer_clock_to_overflow.svg')

def create_timer_vs_counter_sources():
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 380" width="100%" height="100%" style="background:#0B1120; font-family:'DM Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
  <defs>
    <linearGradient id="boxGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1E293B"/>
      <stop offset="100%" stop-color="#0F172A"/>
    </linearGradient>
    <marker id="m-arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#38BDF8" />
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
    <text x="125" y="72" text-anchor="middle" fill="#94A3B8" font-size="11">Oscillator &divide; 12 (Predictable Time)</text>

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
    <path d="M 255 45 L 360 45" fill="none" stroke="#F59E0B" stroke-width="2" marker-end="url(#m-arrow)" />
  </g>

  <!-- MULTIPLEXER SWITCH (C/T BIT IN TMOD) -->
  <g transform="translate(420, 140)">
    <rect width="140" height="120" rx="8" fill="#1E293B" stroke="#475569" stroke-width="1.5" />
    <text x="70" y="24" text-anchor="middle" fill="#E2E8F0" font-size="11" font-weight="700">C/T SWITCH</text>
    <text x="70" y="42" text-anchor="middle" fill="#94A3B8" font-family="'IBM Plex Mono', monospace" font-size="10">(in TMOD)</text>
    
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
    with open('Images/intel_8051_timer_vs_counter_sources.svg', 'w', encoding='utf-8') as f:
        f.write(svg)
    print('Created Images/intel_8051_timer_vs_counter_sources.svg')

def create_two_timers_architecture():
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 400" width="100%" height="100%" style="background:#0B1120; font-family:'DM Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
  <defs>
    <linearGradient id="cardGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1E293B"/>
      <stop offset="100%" stop-color="#0F172A"/>
    </linearGradient>
  </defs>

  <!-- Title -->
  <text x="450" y="38" text-anchor="middle" fill="#F8FAFC" font-size="20" font-weight="700" letter-spacing="0.05em">TWO TIMERS, ONE ARCHITECTURAL PATTERN</text>
  <text x="450" y="62" text-anchor="middle" fill="#94A3B8" font-size="13">The classic 8051 pairs two independent 16-bit counters under shared control SFRs</text>

  <!-- SHARED SUPERVISION BOX -->
  <g transform="translate(60, 90)">
    <rect width="780" height="75" rx="8" fill="#1E293B" stroke="#334155" stroke-width="1.5" />
    <text x="25" y="28" fill="#94A3B8" font-size="11" font-weight="700" letter-spacing="0.05em">SHARED SUPERVISORY SFRS</text>

    <!-- TMOD -->
    <rect x="25" y="38" width="345" height="26" rx="4" fill="#0F172A" stroke="#38BDF8" />
    <text x="35" y="55" fill="#38BDF8" font-family="'IBM Plex Mono', monospace" font-size="11" font-weight="600">TMOD (89H):</text>
    <text x="125" y="55" fill="#CBD5E1" font-size="11">Shared mode configuration (Timer 1 upper / Timer 0 lower)</text>

    <!-- TCON -->
    <rect x="410" y="38" width="345" height="26" rx="4" fill="#0F172A" stroke="#38BDF8" />
    <text x="420" y="55" fill="#38BDF8" font-family="'IBM Plex Mono', monospace" font-size="11" font-weight="600">TCON (88H):</text>
    <text x="510" y="55" fill="#CBD5E1" font-size="11">Shared run control (TR1, TR0) and overflow flags (TF1, TF0)</text>
  </g>

  <!-- TIMER 0 CARD -->
  <g transform="translate(60, 195)">
    <rect width="375" height="175" rx="8" fill="url(#cardGrad)" stroke="#10B981" stroke-width="1.5" />
    <rect width="375" height="32" rx="8" fill="#064E3B" />
    <text x="20" y="21" fill="#34D399" font-size="12" font-weight="700">TIMER 0 (16-BIT COUNTER)</text>

    <text x="25" y="60" fill="#94A3B8" font-size="11">Physical Counting Registers:</text>

    <!-- TH0 / TL0 -->
    <g transform="translate(25, 75)">
      <rect width="155" height="46" rx="4" fill="#0F172A" stroke="#334155" />
      <text x="15" y="20" fill="#94A3B8" font-size="10">High Byte</text>
      <text x="15" y="36" fill="#34D399" font-family="'IBM Plex Mono', monospace" font-size="13" font-weight="600">TH0 (8AH)</text>

      <rect x="170" y="0" width="155" height="46" rx="4" fill="#0F172A" stroke="#334155" />
      <text x="185" y="20" fill="#94A3B8" font-size="10">Low Byte</text>
      <text x="185" y="36" fill="#34D399" font-family="'IBM Plex Mono', monospace" font-size="13" font-weight="600">TL0 (8BH)</text>
    </g>

    <text x="25" y="145" fill="#CBD5E1" font-size="11">Run bit: <tspan fill="#38BDF8" font-family="'IBM Plex Mono', monospace">TR0</tspan> &nbsp;|&nbsp; Overflow flag: <tspan fill="#F59E0B" font-family="'IBM Plex Mono', monospace">TF0</tspan></text>
    <text x="25" y="162" fill="#94A3B8" font-size="10">External input pin: P3.4 (T0)</text>
  </g>

  <!-- TIMER 1 CARD -->
  <g transform="translate(465, 195)">
    <rect width="375" height="175" rx="8" fill="url(#cardGrad)" stroke="#6366F1" stroke-width="1.5" />
    <rect width="375" height="32" rx="8" fill="#312E81" />
    <text x="20" y="21" fill="#A5B4FC" font-size="12" font-weight="700">TIMER 1 (16-BIT COUNTER)</text>

    <text x="25" y="60" fill="#94A3B8" font-size="11">Physical Counting Registers:</text>

    <!-- TH1 / TL1 -->
    <g transform="translate(25, 75)">
      <rect width="155" height="46" rx="4" fill="#0F172A" stroke="#334155" />
      <text x="15" y="20" fill="#94A3B8" font-size="10">High Byte</text>
      <text x="15" y="36" fill="#818CF8" font-family="'IBM Plex Mono', monospace" font-size="13" font-weight="600">TH1 (8CH)</text>

      <rect x="170" y="0" width="155" height="46" rx="4" fill="#0F172A" stroke="#334155" />
      <text x="185" y="20" fill="#94A3B8" font-size="10">Low Byte</text>
      <text x="185" y="36" fill="#818CF8" font-family="'IBM Plex Mono', monospace" font-size="13" font-weight="600">TL1 (8DH)</text>
    </g>

    <text x="25" y="145" fill="#CBD5E1" font-size="11">Run bit: <tspan fill="#38BDF8" font-family="'IBM Plex Mono', monospace">TR1</tspan> &nbsp;|&nbsp; Overflow flag: <tspan fill="#F59E0B" font-family="'IBM Plex Mono', monospace">TF1</tspan></text>
    <text x="25" y="162" fill="#94A3B8" font-size="10">External input pin: P3.5 (T1) | Often generates UART baud rate</text>
  </g>
</svg>'''
    with open('Images/intel_8051_two_timers_architecture.svg', 'w', encoding='utf-8') as f:
        f.write(svg)
    print('Created Images/intel_8051_two_timers_architecture.svg')

def create_timer_to_waveform():
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 380" width="100%" height="100%" style="background:#0B1120; font-family:'DM Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
  <defs>
    <marker id="w-arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#38BDF8" />
    </marker>
  </defs>

  <!-- Title -->
  <text x="450" y="38" text-anchor="middle" fill="#F8FAFC" font-size="20" font-weight="700" letter-spacing="0.05em">WHEN COUNTING BECOMES A WAVEFORM</text>
  <text x="450" y="62" text-anchor="middle" fill="#94A3B8" font-size="13">Periodic overflow events toggle an output pin to generate a physical electrical signal</text>

  <!-- 1. TIMER COUNT (SAWTOOTH) -->
  <g transform="translate(60, 95)">
    <text x="0" y="18" fill="#38BDF8" font-size="12" font-weight="700">1. SILICON COUNTER VALUE (TH0:TL0)</text>
    <text x="780" y="18" text-anchor="end" fill="#94A3B8" font-family="'IBM Plex Mono', monospace" font-size="11">FFFFH (Overflow)</text>

    <!-- Sawtooth Wave -->
    <path d="M 0 120 L 150 40 L 150 120 L 300 40 L 300 120 L 450 40 L 450 120 L 600 40 L 600 120 L 750 40 L 750 120" fill="none" stroke="#38BDF8" stroke-width="2" />
    
    <!-- Dashed Overflow Threshold -->
    <line x1="0" y1="40" x2="780" y2="40" stroke="#F59E0B" stroke-width="1" stroke-dasharray="4 4" />
    <text x="15" y="35" fill="#F59E0B" font-size="10">Overflow limit</text>

    <!-- Overflow pulses -->
    <circle cx="150" cy="40" r="4" fill="#F59E0B" />
    <circle cx="300" cy="40" r="4" fill="#F59E0B" />
    <circle cx="450" cy="40" r="4" fill="#F59E0B" />
    <circle cx="600" cy="40" r="4" fill="#F59E0B" />
    <circle cx="750" cy="40" r="4" fill="#F59E0B" />

    <!-- Pulse arrows down -->
    <line x1="150" y1="45" x2="150" y2="135" stroke="#F59E0B" stroke-width="1.5" stroke-dasharray="2 2" />
    <line x1="300" y1="45" x2="300" y2="135" stroke="#F59E0B" stroke-width="1.5" stroke-dasharray="2 2" />
    <line x1="450" y1="45" x2="450" y2="135" stroke="#F59E0B" stroke-width="1.5" stroke-dasharray="2 2" />
    <line x1="600" y1="45" x2="600" y2="135" stroke="#F59E0B" stroke-width="1.5" stroke-dasharray="2 2" />
    <line x1="750" y1="45" x2="750" y2="135" stroke="#F59E0B" stroke-width="1.5" stroke-dasharray="2 2" />
  </g>

  <!-- 2. PHYSICAL PIN OUTPUT (SQUARE WAVEFORM) -->
  <g transform="translate(60, 245)">
    <text x="0" y="18" fill="#10B981" font-size="12" font-weight="700">2. PHYSICAL PIN OUTPUT (e.g. Pin P1.0 toggled on each overflow)</text>
    <text x="780" y="18" text-anchor="end" fill="#94A3B8" font-size="11">Square Wave Signal</text>

    <!-- Square Wave -->
    <path d="M 0 80 L 150 80 L 150 30 L 300 30 L 300 80 L 450 80 L 450 30 L 600 30 L 600 80 L 750 80 L 750 30 L 780 30" fill="none" stroke="#10B981" stroke-width="2.5" />

    <text x="75" y="98" text-anchor="middle" fill="#94A3B8" font-size="10">LOW</text>
    <text x="225" y="24" text-anchor="middle" fill="#34D399" font-size="10" font-weight="600">HIGH</text>
    <text x="375" y="98" text-anchor="middle" fill="#94A3B8" font-size="10">LOW</text>
    <text x="525" y="24" text-anchor="middle" fill="#34D399" font-size="10" font-weight="600">HIGH</text>
    <text x="675" y="98" text-anchor="middle" fill="#94A3B8" font-size="10">LOW</text>
  </g>
</svg>'''
    with open('Images/intel_8051_timer_to_waveform.svg', 'w', encoding='utf-8') as f:
        f.write(svg)
    print('Created Images/intel_8051_timer_to_waveform.svg')

if __name__ == '__main__':
    create_software_delay_vs_hardware_timer()
    create_timer_clock_to_overflow()
    create_timer_vs_counter_sources()
    create_two_timers_architecture()
    create_timer_to_waveform()
