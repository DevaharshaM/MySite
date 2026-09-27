upgraded_sim_code = '''// -------------------------------------------------------------
// 8051 Timer 0 Interactive Workbench (Section 8 EdgeCase)
// -------------------------------------------------------------
(function() {
  let timerSimRunning = false;
  let timerSimInterval = null;
  let timerSimCount = 0;
  let timerSimMode = 'timer'; // 'timer' or 'counter'
  let timerSimTF0 = 0;
  let timerSimPin = 0;
  let timerSimCpuAction = 'Waiting for TF0 flag...';
  let timerSimWaveHistory = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];

  function toHex(n, len) {
    return n.toString(16).toUpperCase().padStart(len, '0');
  }

  function updateWaveform() {
    const waveLine = document.getElementById('tsim-wave-line');
    if (!waveLine) return;
    const pts = [];
    const step_x = 200.0 / (timerSimWaveHistory.length - 1);
    for (let i = 0; i < timerSimWaveHistory.length; i++) {
      const x = i * step_x;
      const y = timerSimWaveHistory[i] === 1 ? 6 : 24;
      if (i > 0) {
        const prev_y = timerSimWaveHistory[i - 1] === 1 ? 6 : 24;
        if (prev_y !== y) {
          pts.push(x.toFixed(1) + ',' + prev_y);
        }
      }
      pts.push(x.toFixed(1) + ',' + y);
    }
    waveLine.setAttribute('points', pts.join(' '));
  }

  function updateTimerUI(narrativeOverride) {
    const elCountHex = document.getElementById('tsim-count-hex');
    if (!elCountHex) return; // Not on page

    const th0 = Math.floor(timerSimCount / 256);
    const tl0 = timerSimCount % 256;

    elCountHex.innerText = toHex(timerSimCount, 4) + 'H';
    const elTh0 = document.getElementById('tsim-th0-val');
    if (elTh0) elTh0.innerText = toHex(th0, 2) + 'H';
    const elTl0 = document.getElementById('tsim-tl0-val');
    if (elTl0) elTl0.innerText = toHex(tl0, 2) + 'H';

    const progBar = document.getElementById('tsim-prog-bar');
    if (progBar) {
      const pct = ((timerSimCount / 65535) * 100).toFixed(1);
      progBar.style.width = pct + '%';
    }
    const countDec = document.getElementById('tsim-count-dec');
    if (countDec) countDec.innerText = timerSimCount + ' / 65535 counts';

    // TF0 Badge (TCON.5)
    const tf0Badge = document.getElementById('tsim-tf0-badge');
    if (tf0Badge) {
      if (timerSimTF0 === 1) {
        tf0Badge.innerText = 'TF0 = 1 (OVERFLOW ASSERTED)';
        tf0Badge.style.color = '#EF4444';
        tf0Badge.style.background = 'rgba(239, 68, 68, 0.15)';
      } else {
        tf0Badge.innerText = 'TF0 = 0 (IDLE)';
        tf0Badge.style.color = '#64748B';
        tf0Badge.style.background = '#0F172A';
      }
    }

    // CPU Software Response Display
    const elCpuAction = document.getElementById('tsim-cpu-action');
    if (elCpuAction) {
      elCpuAction.innerHTML = timerSimCpuAction;
    }

    // Pin Badge (Physical Output)
    const pinBadge = document.getElementById('tsim-pin-badge');
    if (pinBadge) {
      if (timerSimPin === 1) {
        pinBadge.innerText = 'HIGH (+5V)';
        pinBadge.style.color = '#10B981';
      } else {
        pinBadge.innerText = 'LOW (0V)';
        pinBadge.style.color = '#38BDF8';
      }
    }

    // Run Button
    const btnRun = document.getElementById('tsim-btn-run');
    if (btnRun) {
      if (timerSimRunning) {
        btnRun.innerText = '⏸ PAUSE';
        btnRun.style.background = '#EF4444';
        btnRun.style.color = '#FFFFFF';
      } else {
        btnRun.innerText = '▶ RUN';
        btnRun.style.background = '#10B981';
        btnRun.style.color = '#0F172A';
      }
    }

    // Source Mode Buttons
    const btnModeT = document.getElementById('tsim-btn-mode-t');
    const btnModeC = document.getElementById('tsim-btn-mode-c');
    const btnExtPulse = document.getElementById('tsim-btn-ext-pulse');
    const lblPulse = document.getElementById('tsim-pulse-label');

    if (btnModeT && btnModeC) {
      if (timerSimMode === 'timer') {
        btnModeT.style.background = '#0C4A6E';
        btnModeT.style.borderColor = '#38BDF8';
        btnModeT.style.color = '#FFFFFF';
        btnModeC.style.background = '#1E293B';
        btnModeC.style.borderColor = '#475569';
        btnModeC.style.color = '#94A3B8';
        if (btnExtPulse) btnExtPulse.style.display = 'none';
        if (lblPulse) lblPulse.innerText = 'Internal Machine Cycle Clock (Oscillator / 12)';
      } else {
        btnModeC.style.background = '#78350F';
        btnModeC.style.borderColor = '#F59E0B';
        btnModeC.style.color = '#FFFFFF';
        btnModeT.style.background = '#1E293B';
        btnModeT.style.borderColor = '#475569';
        btnModeT.style.color = '#94A3B8';
        if (btnExtPulse) btnExtPulse.style.display = 'inline-block';
        if (lblPulse) lblPulse.innerText = 'External Input Pin P3.4 (T0)';
      }
    }

    // Live Waveform update
    updateWaveform();

    // Narrative Trace update
    const nar = document.getElementById('tsim-narrative');
    if (nar && narrativeOverride) {
      nar.innerHTML = narrativeOverride;
    }
  }

  function flashLed(color) {
    const led = document.getElementById('tsim-pulse-led');
    if (!led) return;
    led.style.background = color || '#38BDF8';
    led.style.boxShadow = '0 0 8px ' + (color || '#38BDF8');
    setTimeout(() => {
      led.style.background = '#334155';
      led.style.boxShadow = 'none';
    }, 70);
  }

  function timerTick(isExternal) {
    flashLed(isExternal ? '#F59E0B' : '#38BDF8');
    timerSimCount++;
    let narrative = '';

    if (timerSimCount > 65535) {
      timerSimCount = 0;
      timerSimTF0 = 1;
      
      // Separate hardware overflow from software response:
      // In the 8051, TF0=1 alerts the CPU. Software (ISR or polling loop) executes CPL P1.0 and clears TF0.
      timerSimPin = timerSimPin === 0 ? 1 : 0;
      timerSimCpuAction = '<span style="color:#F59E0B; font-weight:700;">TF0 DETECTED &rarr;</span> Executed: <code style="color:#38BDF8;">CPL P1.0</code> &amp; <code style="color:#34D399;">CLR TF0</code>';
      
      narrative = '<strong style="color:#EF4444;">[HARDWARE ROLLOVER]</strong> TH0:TL0 rolled from <code>FFFFH</code> &rarr; <code>0000H</code> and asserted <strong>TF0 = 1</strong>.<br>' +
                  '<strong style="color:#F59E0B;">[CPU RESPONSE]</strong> CPU detected TF0, executed <code>CPL P1.0</code> to invert the pin latch to <strong>' + (timerSimPin === 1 ? 'HIGH (+5V)' : 'LOW (0V)') + '</strong>, and executed <code>CLR TF0</code>.';
      
      // Auto-clear TF0 after simulated CPU intervention for visual clarity
      setTimeout(() => {
        timerSimTF0 = 0;
        updateTimerUI();
      }, 350);

    } else {
      timerSimCpuAction = 'Waiting for TF0 flag (CPU free for other tasks)...';
      if (isExternal) {
        narrative = '<strong style="color:#F59E0B;">[EXTERNAL PULSE]</strong> Pin P3.4 (T0) pulse arrived. Hardware incremented counter to <code>' + toHex(timerSimCount, 4) + 'H</code> (' + timerSimCount + ').';
      } else if (timerSimCount >= 65520) {
        narrative = '<strong style="color:#F59E0B;">[NEAR ROLLOVER]</strong> Counter at <code>' + toHex(timerSimCount, 4) + 'H</code> (' + timerSimCount + '). Only ' + (65536 - timerSimCount) + ' cycle(s) until rollover!';
      } else if (!timerSimRunning || timerSimCount % 15 === 0) {
        narrative = '<strong style="color:#10B981;">[AUTONOMOUS HARDWARE]</strong> Machine cycle clock pulses quietly increment TH0:TL0 in silicon. CPU is 100% free.';
      }
    }

    timerSimWaveHistory.push(timerSimPin);
    if (timerSimWaveHistory.length > 20) {
      timerSimWaveHistory.shift();
    }

    updateTimerUI(narrative);
  }

  window.timerSimAction = function(action) {
    if (action === 'toggle') {
      if (timerSimRunning) {
        timerSimRunning = false;
        if (timerSimInterval) clearInterval(timerSimInterval);
        timerSimInterval = null;
        updateTimerUI('<strong style="color:#CBD5E1;">[GATE CLEARED]</strong> CPU executed <code>CLR TR0</code>. Hardware counter halted at <code>' + toHex(timerSimCount, 4) + 'H</code>.');
      } else {
        if (timerSimMode === 'counter') {
          updateTimerUI('<strong style="color:#F59E0B;">[COUNTER MODE ACTIVE]</strong> Pulses arrive from external transitions on Pin P3.4 (T0). Click <strong>⚡ PULSE PIN T0</strong> or switch to Timer Mode.');
          return;
        }
        timerSimRunning = true;
        timerSimInterval = setInterval(() => {
          timerTick(false);
        }, 80);
        updateTimerUI('<strong style="color:#10B981;">[RUN GATE OPEN]</strong> CPU executed <code>SETB TR0</code>. Machine cycles quietly incrementing TH0:TL0 in silicon.');
      }
    } else if (action === 'step') {
      if (timerSimRunning) {
        timerSimRunning = false;
        if (timerSimInterval) clearInterval(timerSimInterval);
        timerSimInterval = null;
      }
      timerTick(timerSimMode === 'counter');
    } else if (action === 'reset') {
      if (timerSimRunning) {
        timerSimRunning = false;
        if (timerSimInterval) clearInterval(timerSimInterval);
        timerSimInterval = null;
      }
      timerSimCount = 0;
      timerSimTF0 = 0;
      timerSimPin = 0;
      timerSimCpuAction = 'Waiting for TF0 flag (CPU free for other tasks)...';
      timerSimWaveHistory.fill(0);
      updateTimerUI('<strong style="color:#38BDF8;">[RESET]</strong> TH0:TL0 cleared to <code>0000H</code>. TF0 cleared. Pin P1.0 reset to LOW (0V).');
    } else if (action === 'preset_fff8') {
      timerSimCount = 0xFFF8;
      timerSimTF0 = 0;
      updateTimerUI('<strong style="color:#F59E0B;">[PRESET LOADED: FFF8H]</strong> Counter loaded with 65,528. Exactly 8 machine cycles until rollover!');
    } else if (action === 'preset_8000') {
      timerSimCount = 0x8000;
      timerSimTF0 = 0;
      updateTimerUI('<strong style="color:#38BDF8;">[PRESET LOADED: 8000H]</strong> Counter loaded with 32,768 (mid-scale).');
    } else if (action === 'mode_timer') {
      timerSimMode = 'timer';
      updateTimerUI('<strong style="color:#38BDF8;">[MODE SWITCH: C/T = 0]</strong> Switched to Timer Mode in TMOD (89H). Pulse source: internal machine cycle clock.');
    } else if (action === 'mode_counter') {
      if (timerSimRunning) {
        timerSimRunning = false;
        if (timerSimInterval) clearInterval(timerSimInterval);
        timerSimInterval = null;
      }
      timerSimMode = 'counter';
      updateTimerUI('<strong style="color:#F59E0B;">[MODE SWITCH: C/T = 1]</strong> Switched to Counter Mode in TMOD (89H). Pulse source: external Pin P3.4 (T0). Click <strong>⚡ PULSE PIN T0</strong> to feed pulses.');
    } else if (action === 'pulse_ext') {
      timerTick(true);
    } else if (action === 'clear_tf0') {
      timerSimTF0 = 0;
      timerSimCpuAction = 'Software executed <code style="color:#34D399;">CLR TF0</code>.';
      updateTimerUI('<strong style="color:#34D399;">[SOFTWARE ACTION]</strong> CPU executed <code>CLR TF0</code>. Flag reset to 0.');
    }
  };
})();
'''

with open('script.js', 'r', encoding='utf-8') as f:
    js_content = f.read()

marker = '// 8051 Timer 0 Interactive Workbench (Section 8 EdgeCase)'
idx = js_content.find(marker)
if idx != -1:
    base_js = js_content[:idx]
    with open('script.js', 'w', encoding='utf-8') as f:
        f.write(base_js + upgraded_sim_code)
    print("Replaced timer simulator in script.js with upgraded 3-stage logic")
else:
    print("Marker not found, appending...")
    with open('script.js', 'a', encoding='utf-8') as f:
        f.write('\n\n' + upgraded_sim_code)
