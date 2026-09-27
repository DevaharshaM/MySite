sim_code_v2 = '''// -------------------------------------------------------------
// 8051 Timer/Counter Interactive Workbench (Section 8 EdgeCase)
// -------------------------------------------------------------
(function() {
  // Configuration State
  let cfgSource = 'timer';    // 'timer' or 'counter'
  let cfgTimer = 0;           // 0 (Timer 0) or 1 (Timer 1)
  let cfgMode = 1;            // 1 (16-bit) or 2 (8-bit auto-reload)

  // Runtime State
  let isRunning = false;
  let runInterval = null;
  let thVal = 0;              // High byte (or reload value in Mode 2)
  let tlVal = 0;              // Low byte
  let tfVal = 0;              // Overflow flag (TF0 or TF1)
  let trVal = 0;              // Run bit (TR0 or TR1)
  let pinState = 0;           // Pin P1.0 simulated output (0 or 1)
  let cpuActionText = 'Hardware idle. Press RUN or STEP.';
  let waveHistory = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];

  function toHex(n, len) {
    return n.toString(16).toUpperCase().padStart(len, '0');
  }

  function updateWaveform() {
    const waveLine = document.getElementById('tsim-wave-line');
    if (!waveLine) return;
    const pts = [];
    const step_x = 200.0 / (waveHistory.length - 1);
    for (let i = 0; i < waveHistory.length; i++) {
      const x = i * step_x;
      const y = waveHistory[i] === 1 ? 6 : 24;
      if (i > 0) {
        const prev_y = waveHistory[i - 1] === 1 ? 6 : 24;
        if (prev_y !== y) {
          pts.push(x.toFixed(1) + ',' + prev_y);
        }
      }
      pts.push(x.toFixed(1) + ',' + y);
    }
    waveLine.setAttribute('points', pts.join(' '));
  }

  function flashLed(color) {
    const led = document.getElementById('tsim-pulse-led');
    if (!led) return;
    led.style.background = color || '#38BDF8';
    led.style.boxShadow = '0 0 10px ' + (color || '#38BDF8');
    setTimeout(() => {
      led.style.background = '#334155';
      led.style.boxShadow = 'none';
    }, 70);
  }

  function updateUI(narrativeOverride) {
    const elContainer = document.getElementById('edgecase-workbench-root');
    if (!elContainer) return;

    const tStr = cfgTimer === 0 ? '0' : '1';
    const pinName = cfgTimer === 0 ? 'P3.4 (T0)' : 'P3.5 (T1)';
    const thAddr = cfgTimer === 0 ? '8CH' : '8DH';
    const tlAddr = cfgTimer === 0 ? '8AH' : '8BH';
    const trBit = cfgTimer === 0 ? 'TR0 (8CH)' : 'TR1 (8EH)';
    const tfBit = cfgTimer === 0 ? 'TF0 (8DH)' : 'TF1 (8FH)';

    // Update Configuration Tab Buttons
    // 1. Source buttons
    const btnSrcT = document.getElementById('tsim-cfg-src-timer');
    const btnSrcC = document.getElementById('tsim-cfg-src-counter');
    if (btnSrcT && btnSrcC) {
      if (cfgSource === 'timer') {
        btnSrcT.style.background = '#0C4A6E'; btnSrcT.style.borderColor = '#38BDF8'; btnSrcT.style.color = '#FFFFFF';
        btnSrcC.style.background = '#1E293B'; btnSrcC.style.borderColor = '#475569'; btnSrcC.style.color = '#94A3B8';
      } else {
        btnSrcC.style.background = '#78350F'; btnSrcC.style.borderColor = '#F59E0B'; btnSrcC.style.color = '#FFFFFF';
        btnSrcT.style.background = '#1E293B'; btnSrcT.style.borderColor = '#475569'; btnSrcT.style.color = '#94A3B8';
      }
    }

    // 2. Timer Select buttons
    const btnT0 = document.getElementById('tsim-cfg-timer-0');
    const btnT1 = document.getElementById('tsim-cfg-timer-1');
    if (btnT0 && btnT1) {
      if (cfgTimer === 0) {
        btnT0.style.background = '#064E3B'; btnT0.style.borderColor = '#10B981'; btnT0.style.color = '#FFFFFF';
        btnT1.style.background = '#1E293B'; btnT1.style.borderColor = '#475569'; btnT1.style.color = '#94A3B8';
      } else {
        btnT1.style.background = '#312E81'; btnT1.style.borderColor = '#818CF8'; btnT1.style.color = '#FFFFFF';
        btnT0.style.background = '#1E293B'; btnT0.style.borderColor = '#475569'; btnT0.style.color = '#94A3B8';
      }
    }

    // 3. Mode Select buttons
    const btnM1 = document.getElementById('tsim-cfg-mode-1');
    const btnM2 = document.getElementById('tsim-cfg-mode-2');
    if (btnM1 && btnM2) {
      if (cfgMode === 1) {
        btnM1.style.background = '#1E3A8A'; btnM1.style.borderColor = '#60A5FA'; btnM1.style.color = '#FFFFFF';
        btnM2.style.background = '#1E293B'; btnM2.style.borderColor = '#475569'; btnM2.style.color = '#94A3B8';
      } else {
        btnM2.style.background = '#4A044E'; btnM2.style.borderColor = '#E879F9'; btnM2.style.color = '#FFFFFF';
        btnM1.style.background = '#1E293B'; btnM1.style.borderColor = '#475569'; btnM1.style.color = '#94A3B8';
      }
    }

    // External Pulse Button Visibility
    const btnPulse = document.getElementById('tsim-btn-ext-pulse');
    if (btnPulse) {
      if (cfgSource === 'counter') {
        btnPulse.style.display = 'inline-flex';
        btnPulse.innerHTML = '&#9889; PULSE EXTERNAL PIN ' + pinName;
      } else {
        btnPulse.style.display = 'none';
      }
    }

    // Update Active Hardware Path Banner
    const elPath = document.getElementById('tsim-active-path-label');
    if (elPath) {
      if (cfgSource === 'timer') {
        elPath.innerHTML = '<span style="color:#38BDF8;">INTERNAL CLOCK:</span> 12 MHz Crystal / 12 &rarr; TR' + tStr + ' Run Gate &rarr; ' +
          (cfgMode === 1 ? 'TH' + tStr + ':TL' + tStr + ' (16-bit)' : 'TL' + tStr + ' (8-bit with TH' + tStr + ' Auto-Reload)') +
          ' &rarr; TF' + tStr + ' Overflow &rarr; CPU';
      } else {
        elPath.innerHTML = '<span style="color:#F59E0B;">EXTERNAL COUNTER:</span> Negative edge on Pin ' + pinName + ' &rarr; TR' + tStr + ' Gate &rarr; ' +
          (cfgMode === 1 ? 'TH' + tStr + ':TL' + tStr + ' (16-bit)' : 'TL' + tStr + ' (8-bit with TH' + tStr + ' Auto-Reload)') +
          ' &rarr; TF' + tStr + ' Overflow';
      }
    }

    // Update Register Labels and Values
    const lblTh = document.getElementById('tsim-lbl-th');
    const valTh = document.getElementById('tsim-val-th');
    const lblTl = document.getElementById('tsim-lbl-tl');
    const valTl = document.getElementById('tsim-val-tl');
    const elModeTag = document.getElementById('tsim-reg-mode-tag');

    if (lblTh) lblTh.innerText = 'TH' + tStr + ' (' + thAddr + ')' + (cfgMode === 2 ? ' [RELOAD VALUE]' : ' [HIGH BYTE]');
    if (valTh) valTh.innerText = toHex(thVal, 2) + 'H';
    if (lblTl) lblTl.innerText = 'TL' + tStr + ' (' + tlAddr + ')' + (cfgMode === 2 ? ' [LIVE COUNTER]' : ' [LOW BYTE]');
    if (valTl) valTl.innerText = toHex(tlVal, 2) + 'H';
    if (elModeTag) elModeTag.innerText = cfgMode === 1 ? 'Mode 1: 16-Bit Cascading Counter' : 'Mode 2: 8-Bit Auto-Reload (Reload from TH' + tStr + ')';

    // Progress Bar
    const progBar = document.getElementById('tsim-prog-bar');
    const txtCount = document.getElementById('tsim-count-display');
    if (progBar && txtCount) {
      if (cfgMode === 1) {
        const fullCount = (thVal << 8) | tlVal;
        const pct = ((fullCount / 65535) * 100).toFixed(1);
        progBar.style.width = pct + '%';
        txtCount.innerText = toHex(fullCount, 4) + 'H (' + fullCount + ' / 65535)';
      } else {
        const pct = ((tlVal / 255) * 100).toFixed(1);
        progBar.style.width = pct + '%';
        txtCount.innerText = toHex(tlVal, 2) + 'H (' + tlVal + ' / 255) | Reload: ' + toHex(thVal, 2) + 'H';
      }
    }

    // TF Flag Badge
    const elTf = document.getElementById('tsim-tf-badge');
    if (elTf) {
      if (tfVal === 1) {
        elTf.innerText = 'TF' + tStr + ' = 1 (OVERFLOW ASSERTED)';
        elTf.style.color = '#EF4444';
        elTf.style.background = 'rgba(239, 68, 68, 0.2)';
      } else {
        elTf.innerText = 'TF' + tStr + ' = 0 (IDLE)';
        elTf.style.color = '#64748B';
        elTf.style.background = '#0F172A';
      }
    }

    // CPU Software Response Text
    const elCpu = document.getElementById('tsim-cpu-action');
    if (elCpu) elCpu.innerHTML = cpuActionText;

    // Pin Badge
    const elPin = document.getElementById('tsim-pin-badge');
    if (elPin) {
      if (pinState === 1) {
        elPin.innerText = 'HIGH (+5V)';
        elPin.style.color = '#10B981';
      } else {
        elPin.innerText = 'LOW (0V)';
        elPin.style.color = '#38BDF8';
      }
    }

    // Run / Pause Button
    const btnRun = document.getElementById('tsim-btn-run');
    if (btnRun) {
      if (isRunning) {
        btnRun.innerHTML = '&#9208; PAUSE';
        btnRun.style.background = '#EF4444';
        btnRun.style.color = '#FFFFFF';
      } else {
        btnRun.innerHTML = '&#9654; RUN';
        btnRun.style.background = '#10B981';
        btnRun.style.color = '#0F172A';
      }
    }

    // Waveform
    updateWaveform();

    // Narrative Trace
    const elNar = document.getElementById('tsim-narrative');
    if (elNar && narrativeOverride) {
      elNar.innerHTML = narrativeOverride;
    }
  }

  function tick(isExternalPulse) {
    flashLed(isExternalPulse ? '#F59E0B' : '#38BDF8');
    const tStr = cfgTimer === 0 ? '0' : '1';
    let narrative = '';

    if (cfgMode === 1) {
      // 16-Bit Mode
      let full = (thVal << 8) | tlVal;
      full++;
      if (full > 0xFFFF) {
        full = 0;
        thVal = 0;
        tlVal = 0;
        tfVal = 1;
        pinState = pinState === 0 ? 1 : 0;
        cpuActionText = '<span style="color:#F59E0B; font-weight:700;">TF' + tStr + ' DETECTED &rarr;</span> CPU executed: <code style="color:#38BDF8;">CPL P1.0</code> &amp; <code style="color:#34D399;">CLR TF' + tStr + '</code>';
        narrative = '<strong style="color:#EF4444;">[16-BIT OVERFLOW ROLLOVER]</strong> TH' + tStr + ':TL' + tStr + ' rolled over from <code>FFFFH</code> &rarr; <code>0000H</code>! Hardware set <strong>TF' + tStr + ' = 1</strong>.<br>' +
                    '<strong style="color:#F59E0B;">[CPU / ISR ACTION]</strong> CPU detected TF' + tStr + ', executed <code>CPL P1.0</code> (Pin switched to ' + (pinState === 1 ? 'HIGH +5V' : 'LOW 0V') + '), and executed <code>CLR TF' + tStr + '</code>.';
        setTimeout(() => { tfVal = 0; updateUI(); }, 400);
      } else {
        thVal = (full >> 8) & 0xFF;
        tlVal = full & 0xFF;
        cpuActionText = 'Hardware counting. CPU free for other tasks...';
        if (isExternalPulse) {
          narrative = '<strong style="color:#F59E0B;">[EXTERNAL PULSE]</strong> Pin ' + (cfgTimer === 0 ? 'P3.4 (T0)' : 'P3.5 (T1)') + ' transitioned. Hardware counter incremented to <code>' + toHex(full, 4) + 'H</code> (' + full + ').';
        } else if (full >= 0xFFF8) {
          narrative = '<strong style="color:#F59E0B;">[NEAR ROLLOVER]</strong> Counter at <code>' + toHex(full, 4) + 'H</code> (' + full + '). Exactly ' + (65536 - full) + ' cycle(s) until 16-bit rollover!';
        } else if (!isRunning || full % 15 === 0) {
          narrative = '<strong style="color:#10B981;">[TIMER MODE COUNTING]</strong> Machine cycle clock pulses quietly incrementing TH' + tStr + ':TL' + tStr + ' in silicon.';
        }
      }
    } else {
      // Mode 2: 8-Bit Auto-Reload
      tlVal++;
      if (tlVal > 0xFF) {
        tfVal = 1;
        // Hardware auto-reloads TL from TH!
        tlVal = thVal;
        pinState = pinState === 0 ? 1 : 0;
        cpuActionText = '<span style="color:#E879F9; font-weight:700;">AUTO-RELOAD TRIGGERED:</span> TL' + tStr + ' reloaded from TH' + tStr + ' (' + toHex(thVal, 2) + 'H)! <code style="color:#38BDF8;">CPL P1.0</code> executed.';
        narrative = '<strong style="color:#E879F9;">[8-BIT AUTO-RELOAD EVENT]</strong> TL' + tStr + ' rolled over <code>FFH</code> &rarr; <code>00H</code>! Hardware asserted <strong>TF' + tStr + ' = 1</strong> and <em>instantly copied</em> <code>TH' + tStr + ' (' + toHex(thVal, 2) + 'H)</code> into <code>TL' + tStr + '</code> without software overhead!<br>' +
                    '<strong style="color:#F59E0B;">[CPU / ISR ACTION]</strong> CPU inverted Pin P1.0 to ' + (pinState === 1 ? 'HIGH (+5V)' : 'LOW (0V)') + ' and acknowledged TF' + tStr + '.';
        setTimeout(() => { tfVal = 0; updateUI(); }, 400);
      } else {
        cpuActionText = 'TL' + tStr + ' counting (' + toHex(tlVal, 2) + 'H). TH' + tStr + ' holding reload value (' + toHex(thVal, 2) + 'H).';
        if (isExternalPulse) {
          narrative = '<strong style="color:#F59E0B;">[EXTERNAL PULSE]</strong> Pin ' + (cfgTimer === 0 ? 'P3.4' : 'P3.5') + ' pulsed. TL' + tStr + ' incremented to <code>' + toHex(tlVal, 2) + 'H</code> (' + tlVal + ').';
        } else if (tlVal >= 0xFA) {
          narrative = '<strong style="color:#F59E0B;">[NEAR RELOAD]</strong> TL' + tStr + ' at <code>' + toHex(tlVal, 2) + 'H</code>. Only ' + (256 - tlVal) + ' pulse(s) until overflow and auto-reload from TH' + tStr + '!';
        } else if (!isRunning || tlVal % 10 === 0) {
          narrative = '<strong style="color:#38BDF8;">[AUTO-RELOAD MODE]</strong> TL' + tStr + ' counts pulses. TH' + tStr + ' holds the baseline reload value (' + toHex(thVal, 2) + 'H).';
        }
      }
    }

    waveHistory.push(pinState);
    if (waveHistory.length > 20) waveHistory.shift();

    updateUI(narrative);
  }

  function stopRunning() {
    if (isRunning) {
      isRunning = false;
      if (runInterval) clearInterval(runInterval);
      runInterval = null;
    }
  }

  window.edgeCaseAction = function(action, param) {
    if (action === 'set_source') {
      stopRunning();
      cfgSource = param; // 'timer' or 'counter'
      updateUI(cfgSource === 'timer'
        ? '<strong style="color:#38BDF8;">[SOURCE: TIMER MODE]</strong> C/T = 0 in TMOD. Pulses come from the internal machine cycle clock.'
        : '<strong style="color:#F59E0B;">[SOURCE: COUNTER MODE]</strong> C/T = 1 in TMOD. Hardware waits for external pulses on Pin ' + (cfgTimer === 0 ? 'P3.4 (T0)' : 'P3.5 (T1)') + '. Click the Pulse button to feed events!');
    } else if (action === 'set_timer') {
      stopRunning();
      cfgTimer = param; // 0 or 1
      updateUI('<strong style="color:#6EE7B7;">[TIMER SELECT: TIMER ' + cfgTimer + ']</strong> Switched to Timer ' + cfgTimer + '. Using registers TH' + cfgTimer + ', TL' + cfgTimer + ', TR' + cfgTimer + ', and TF' + cfgTimer + '.');
    } else if (action === 'set_mode') {
      stopRunning();
      cfgMode = param; // 1 or 2
      if (cfgMode === 1) {
        thVal = 0; tlVal = 0;
        updateUI('<strong style="color:#60A5FA;">[MODE SELECT: MODE 1 (16-BIT)]</strong> Full 16-bit cascading counter (TH' + cfgTimer + ':TL' + cfgTimer + '). Counts 0000H to FFFFH.');
      } else {
        thVal = 0xD0; // default reload value
        tlVal = 0xD0;
        updateUI('<strong style="color:#E879F9;">[MODE SELECT: MODE 2 (8-BIT AUTO-RELOAD)]</strong> TL' + cfgTimer + ' counts 00H to FFH. TH' + cfgTimer + ' holds reload value (D0H = 208). When TL' + cfgTimer + ' overflows, it instantly reloads from TH' + cfgTimer + '!');
      }
    } else if (action === 'toggle_run') {
      if (isRunning) {
        stopRunning();
        updateUI('<strong style="color:#CBD5E1;">[HALTED]</strong> TR' + cfgTimer + ' cleared to 0. Hardware counter paused.');
      } else {
        if (cfgSource === 'counter') {
          updateUI('<strong style="color:#F59E0B;">[COUNTER MODE]</strong> In Counter mode, the counter advances when external physical events arrive. Click <strong>&#9889; PULSE EXTERNAL PIN</strong> to generate pulses!');
          return;
        }
        isRunning = true;
        runInterval = setInterval(() => {
          tick(false);
        }, 80);
        updateUI('<strong style="color:#10B981;">[RUNNING]</strong> TR' + cfgTimer + ' set to 1. Internal machine cycles streaming into counter.');
      }
    } else if (action === 'step') {
      stopRunning();
      tick(cfgSource === 'counter');
    } else if (action === 'pulse_pin') {
      tick(true);
    } else if (action === 'preset_overflow') {
      stopRunning();
      if (cfgMode === 1) {
        thVal = 0xFF;
        tlVal = 0xF8;
        updateUI('<strong style="color:#F59E0B;">[PRESET: NEAR 16-BIT OVERFLOW]</strong> Loaded FFF8H into TH' + cfgTimer + ':TL' + cfgTimer + '. Exactly 8 pulses remaining before rollover!');
      } else {
        thVal = 0xD0;
        tlVal = 0xFD;
        updateUI('<strong style="color:#E879F9;">[PRESET: NEAR AUTO-RELOAD]</strong> Loaded TL' + cfgTimer + ' = FDH with TH' + cfgTimer + ' Reload = D0H. Exactly 3 pulses remaining before rollover and reload!');
      }
    } else if (action === 'preset_mid') {
      stopRunning();
      if (cfgMode === 1) {
        thVal = 0x80; tlVal = 0x00;
        updateUI('<strong style="color:#38BDF8;">[PRESET: MID-SCALE]</strong> Loaded 8000H (32,768 counts) into 16-bit counter.');
      } else {
        thVal = 0x80; tlVal = 0x80;
        updateUI('<strong style="color:#38BDF8;">[PRESET: MID-SCALE]</strong> Loaded 80H (128 counts) into 8-bit auto-reload counter.');
      }
    } else if (action === 'reset') {
      stopRunning();
      tfVal = 0;
      pinState = 0;
      waveHistory.fill(0);
      if (cfgMode === 1) {
        thVal = 0; tlVal = 0;
      } else {
        thVal = 0xD0; tlVal = 0xD0;
      }
      cpuActionText = 'Hardware reset to initial state.';
      updateUI('<strong style="color:#38BDF8;">[RESET]</strong> Counter reset to initial state. TF' + cfgTimer + ' cleared.');
    }
  };

  // Backwards compatibility alias for any existing onclick hooks
  window.timerSimAction = function(action) {
    if (action === 'toggle') window.edgeCaseAction('toggle_run');
    else if (action === 'step') window.edgeCaseAction('step');
    else if (action === 'reset') window.edgeCaseAction('reset');
    else if (action === 'preset_fff8') window.edgeCaseAction('preset_overflow');
    else if (action === 'preset_8000') window.edgeCaseAction('preset_mid');
    else if (action === 'mode_timer') window.edgeCaseAction('set_source', 'timer');
    else if (action === 'mode_counter') window.edgeCaseAction('set_source', 'counter');
    else if (action === 'pulse_ext') window.edgeCaseAction('pulse_pin');
    else if (action === 'clear_tf0') { tfVal = 0; updateUI('<strong style="color:#34D399;">[CLEAR]</strong> TF flag cleared.'); }
  };
})();
'''

with open('script.js', 'r', encoding='utf-8') as f:
    js = f.read()

marker = '// -------------------------------------------------------------\n// 8051 Timer 0 Interactive Workbench (Section 8 EdgeCase)'
if marker not in js:
    marker = '// 8051 Timer 0 Interactive Workbench (Section 8 EdgeCase)'

idx = js.find(marker)
if idx != -1:
    base_js = js[:idx]
    with open('script.js', 'w', encoding='utf-8') as f:
        f.write(base_js + sim_code_v2)
    print("Replaced with new configuration-driven EdgeCase simulator in script.js")
else:
    with open('script.js', 'a', encoding='utf-8') as f:
        f.write('\n\n' + sim_code_v2)
    print("Appended new EdgeCase simulator to script.js")
