sim_code = '''
// -------------------------------------------------------------
// 8051 Timer 0 Interactive Workbench (Section 8 EdgeCase)
// -------------------------------------------------------------
(function() {
  let timerSimRunning = false;
  let timerSimInterval = null;
  let timerSimCount = 0;
  let timerSimMode = 'timer'; // 'timer' or 'counter'
  let timerSimTF0 = 0;
  let timerSimPin = 0;
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

    // TF0 Badge
    const tf0Badge = document.getElementById('tsim-tf0-badge');
    if (tf0Badge) {
      if (timerSimTF0 === 1) {
        tf0Badge.innerText = 'TF0 = 1 (OVERFLOW!)';
        tf0Badge.style.color = '#EF4444';
      } else {
        tf0Badge.innerText = 'TF0 = 0 (IDLE)';
        tf0Badge.style.color = '#64748B';
      }
    }

    // Pin Badge
    const pinBadge = document.getElementById('tsim-pin-badge');
    if (pinBadge) {
      if (timerSimPin === 1) {
        pinBadge.innerText = 'HIGH (5V)';
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
        if (lblPulse) lblPulse.innerText = 'Machine Cycle Clock';
      } else {
        btnModeC.style.background = '#78350F';
        btnModeC.style.borderColor = '#F59E0B';
        btnModeC.style.color = '#FFFFFF';
        btnModeT.style.background = '#1E293B';
        btnModeT.style.borderColor = '#475569';
        btnModeT.style.color = '#94A3B8';
        if (btnExtPulse) btnExtPulse.style.display = 'inline-block';
        if (lblPulse) lblPulse.innerText = 'External Pin P3.4 (T0)';
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
      timerSimPin = timerSimPin === 0 ? 1 : 0;
      narrative = '<strong style="color:#EF4444;">OVERFLOW ROLLOVER:</strong> Counter rolled over from <code>FFFFH</code> to <code>0000H</code>! Hardware set <strong>TF0 = 1</strong> and toggled Pin P1.0 to <strong>' + (timerSimPin === 1 ? 'HIGH (5V)' : 'LOW (0V)') + '</strong>.';
    } else {
      if (isExternal) {
        narrative = '<strong style="color:#F59E0B;">PIN PULSE REGISTERED:</strong> External pulse detected on P3.4 (T0). Hardware incremented count to <code>' + toHex(timerSimCount, 4) + 'H</code> (' + timerSimCount + ').';
      } else if (timerSimCount >= 65520) {
        narrative = '<strong style="color:#F59E0B;">APPROACHING LIMIT:</strong> Count is <code>' + toHex(timerSimCount, 4) + 'H</code> (' + timerSimCount + '). Exactly ' + (65536 - timerSimCount) + ' cycle(s) until 16-bit rollover!';
      } else if (!timerSimRunning || timerSimCount % 15 === 0) {
        narrative = '<strong style="color:#10B981;">AUTONOMOUS COUNTING:</strong> Clock pulses increment TH0:TL0 directly in hardware. The CPU does not spend cycles counting.';
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
        updateTimerUI('<strong style="color:#CBD5E1;">PAUSED:</strong> Timer 0 run gate cleared (TR0 = 0). Hardware counter halted at <code>' + toHex(timerSimCount, 4) + 'H</code>.');
      } else {
        if (timerSimMode === 'counter') {
          updateTimerUI('<strong style="color:#F59E0B;">COUNTER MODE ACTIVE:</strong> In counter mode, pulses arrive from external events on Pin T0 (P3.4). Click <strong>⚡ PULSE PIN T0</strong> or switch to Timer Mode.');
          return;
        }
        timerSimRunning = true;
        timerSimInterval = setInterval(() => {
          timerTick(false);
        }, 70);
        updateTimerUI('<strong style="color:#10B981;">RUNNING:</strong> Timer 0 run gate set (TR0 = 1). Pulses incrementing TH0:TL0 in hardware.');
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
      timerSimWaveHistory.fill(0);
      updateTimerUI('<strong style="color:#38BDF8;">RESET:</strong> TH0:TL0 cleared to <code>0000H</code>. TF0 cleared. Pin P1.0 set to LOW.');
    } else if (action === 'preset_fff8') {
      timerSimCount = 0xFFF8;
      timerSimTF0 = 0;
      updateTimerUI('<strong style="color:#F59E0B;">PRESET LOADED (FFF8H):</strong> TH0:TL0 set to 65,528. Exactly 8 machine cycles until rollover!');
    } else if (action === 'preset_8000') {
      timerSimCount = 0x8000;
      timerSimTF0 = 0;
      updateTimerUI('<strong style="color:#38BDF8;">PRESET LOADED (8000H):</strong> TH0:TL0 set to 32,768 (half-scale).');
    } else if (action === 'mode_timer') {
      timerSimMode = 'timer';
      updateTimerUI('<strong style="color:#38BDF8;">MODE SWITCH (C/T = 0):</strong> Switched to Timer Mode. Source is internal machine cycle clock.');
    } else if (action === 'mode_counter') {
      if (timerSimRunning) {
        timerSimRunning = false;
        if (timerSimInterval) clearInterval(timerSimInterval);
        timerSimInterval = null;
      }
      timerSimMode = 'counter';
      updateTimerUI('<strong style="color:#F59E0B;">MODE SWITCH (C/T = 1):</strong> Switched to Counter Mode. Source is external Pin P3.4 (T0). Click <strong>⚡ PULSE PIN T0</strong> to feed pulses.');
    } else if (action === 'pulse_ext') {
      timerTick(true);
    } else if (action === 'clear_tf0') {
      timerSimTF0 = 0;
      updateTimerUI('<strong style="color:#34D399;">SOFTWARE CLEAR:</strong> CPU executed <code>CLR TF0</code>. Overflow flag reset to 0.');
    }
  };
})();
'''

with open('script.js', 'r', encoding='utf-8') as f:
    orig = f.read()

if 'window.timerSimAction' not in orig:
    with open('script.js', 'w', encoding='utf-8') as f:
        f.write(orig + '\n' + sim_code)
    print("Successfully appended timerSimAction to script.js")
else:
    print("timerSimAction already present in script.js")
