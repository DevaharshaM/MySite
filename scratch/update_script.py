# Script to update script.js with complete 4-mode 8051 EdgeCase workbench and register the exploration

with open("script.js", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update Controller explorations list in script.js (around line 190)
target_controller = '{ id: "the-8051-when-time-becomes-a-signal", title: "The 8051 \u2014 When Time Becomes a Signal" }'
new_controller = '{ id: "the-8051-when-time-becomes-a-signal", title: "The 8051 \u2014 When Time Becomes a Signal" },\n      { id: "the-8051-four-shapes-of-time", title: "The 8051 \u2014 Four Shapes of Time" }'

if target_controller in content and 'the-8051-four-shapes-of-time' not in content[:50000]:
    content = content.replace(target_controller, new_controller, 1)
    print("Updated Controller node explorations in script.js")
else:
    print("Controller node in script.js already has the-8051-four-shapes-of-time or pattern not found")

# 2. Replace the 8051 timer workbench code at the end of script.js
marker = '// 8051 Timer/Counter Interactive Workbench'
idx = content.find(marker)
if idx != -1:
    before = content[:idx]
    
    new_workbench_js = '''// 8051 Timer/Counter Interactive Workbench — Four Shapes of Time
// ----------------------------------------------------------------------------
(function() {
  // Configuration State
  let cfgTimer = 0;           // 0 (Timer 0) or 1 (Timer 1)
  let cfgSource = 'timer';    // 'timer' (Osc / 12) or 'counter' (Pin T0/T1)
  let cfgMode = 1;            // 0 (13-bit), 1 (16-bit), 2 (8-bit auto-reload), 3 (split)

  // Runtime Registers
  let thVal = 0;              // High byte (or reload latch in Mode 2)
  let tlVal = 0;              // Low byte
  let tfVal = 0;              // Overflow flag (TF0 or TF1)
  let trVal = 0;              // Run bit (TR0 or TR1)
  let th0_mode3_run = 0;      // TR1 used to run TH0 in Mode 3
  let th0_mode3_tf = 0;       // TF1 set when TH0 overflows in Mode 3

  let isRunning = false;
  let runInterval = null;

  function toHex(n, len) {
    return n.toString(16).toUpperCase().padStart(len, '0');
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

  function renderTopologyView() {
    const el = document.getElementById('tsim-topology-view');
    if (!el) return;

    const t = cfgTimer;
    const pinName = t === 0 ? 'P3.4 (T0)' : 'P3.5 (T1)';
    const srcText = cfgSource === 'timer' ? 'Osc &divide; 12 (1 &mu;s)' : 'Pin ' + pinName;
    const srcColor = cfgSource === 'timer' ? '#38BDF8' : '#F59E0B';

    let html = '';

    if (cfgMode === 0) {
      // Mode 0: 13-Bit Counter (8b THx + 5b TLx)
      html = `
        <div style="display:flex; align-items:center; justify-content:center; flex-wrap:wrap; gap:8px; width:100%;">
          <div style="background:#1E293B; border:1px solid ${srcColor}; padding:6px 10px; border-radius:6px; font-size:0.75rem; color:${srcColor}; font-weight:600;">
            ${srcText}
          </div>
          <span style="color:#64748B;">&rarr;</span>
          <div style="background:#0F172A; border:1px solid #10B981; padding:4px 8px; border-radius:4px; font-size:0.7rem; color:#10B981; font-family:'IBM Plex Mono', monospace;">
            TR${t}=${trVal}
          </div>
          <span style="color:#64748B;">&rarr;</span>
          <div style="background:#0C4A6E; border:1.5px solid #38BDF8; padding:8px 12px; border-radius:6px; text-align:center;">
            <div style="font-size:0.7rem; font-weight:700; color:#7DD3FC;">TL${t} [Bits 4..0]</div>
            <div style="font-size:0.65rem; color:#94A3B8;">5-Bit Prescaler (0..31)</div>
            <div style="font-family:'IBM Plex Mono', monospace; font-size:0.8rem; font-weight:700; color:#38BDF8; margin-top:2px;">
              Val: ${tlVal & 0x1F} / 31
            </div>
            <div style="font-size:0.6rem; color:#64748B; margin-top:2px;">Bits 7..5 Disconnected</div>
          </div>
          <span style="color:#10B981; font-weight:bold; font-size:0.75rem;">&divide;32 &rarr;</span>
          <div style="background:#064E3B; border:1.5px solid #10B981; padding:8px 12px; border-radius:6px; text-align:center;">
            <div style="font-size:0.7rem; font-weight:700; color:#6EE7B7;">TH${t} [Bits 7..0]</div>
            <div style="font-size:0.65rem; color:#A7F3D0;">8-Bit Counter (0..255)</div>
            <div style="font-family:'IBM Plex Mono', monospace; font-size:0.8rem; font-weight:700; color:#34D399; margin-top:2px;">
              Val: ${thVal} / 255
            </div>
          </div>
          <span style="color:#F59E0B; font-weight:bold; font-size:0.75rem;">&rarr;</span>
          <div style="background:#78350F; border:1.5px solid #F59E0B; padding:8px 12px; border-radius:6px; text-align:center;">
            <div style="font-size:0.7rem; font-weight:700; color:#FDE68A;">TF${t} Flag</div>
            <div style="font-family:'IBM Plex Mono', monospace; font-size:0.8rem; font-weight:700; color:#F59E0B;">
              ${tfVal === 1 ? 'TF' + t + '=1 (OVERFLOW)' : 'TF' + t + '=0'}
            </div>
          </div>
        </div>
      `;
    } else if (cfgMode === 1) {
      // Mode 1: 16-Bit Cascaded Counter
      html = `
        <div style="display:flex; align-items:center; justify-content:center; flex-wrap:wrap; gap:8px; width:100%;">
          <div style="background:#1E293B; border:1px solid ${srcColor}; padding:6px 10px; border-radius:6px; font-size:0.75rem; color:${srcColor}; font-weight:600;">
            ${srcText}
          </div>
          <span style="color:#64748B;">&rarr;</span>
          <div style="background:#0F172A; border:1px solid #10B981; padding:4px 8px; border-radius:4px; font-size:0.7rem; color:#10B981; font-family:'IBM Plex Mono', monospace;">
            TR${t}=${trVal}
          </div>
          <span style="color:#64748B;">&rarr;</span>
          <div style="background:#0369A1; border:1.5px solid #38BDF8; padding:8px 12px; border-radius:6px; text-align:center;">
            <div style="font-size:0.7rem; font-weight:700; color:#FFFFFF;">TL${t} (Low Byte)</div>
            <div style="font-size:0.65rem; color:#BAE6FD;">Counts 00H &rarr; FFH</div>
            <div style="font-family:'IBM Plex Mono', monospace; font-size:0.85rem; font-weight:700; color:#E0F2FE; margin-top:2px;">
              ${toHex(tlVal, 2)}H (${tlVal})
            </div>
          </div>
          <span style="color:#38BDF8; font-weight:bold; font-size:0.75rem;">&divide;256 &rarr;</span>
          <div style="background:#064E3B; border:1.5px solid #10B981; padding:8px 12px; border-radius:6px; text-align:center;">
            <div style="font-size:0.7rem; font-weight:700; color:#FFFFFF;">TH${t} (High Byte)</div>
            <div style="font-size:0.65rem; color:#A7F3D0;">Counts 00H &rarr; FFH</div>
            <div style="font-family:'IBM Plex Mono', monospace; font-size:0.85rem; font-weight:700; color:#6EE7B7; margin-top:2px;">
              ${toHex(thVal, 2)}H (${thVal})
            </div>
          </div>
          <span style="color:#F59E0B; font-weight:bold; font-size:0.75rem;">&rarr;</span>
          <div style="background:#78350F; border:1.5px solid #F59E0B; padding:8px 12px; border-radius:6px; text-align:center;">
            <div style="font-size:0.7rem; font-weight:700; color:#FDE68A;">TF${t} Flag</div>
            <div style="font-family:'IBM Plex Mono', monospace; font-size:0.8rem; font-weight:700; color:#F59E0B;">
              ${tfVal === 1 ? 'TF' + t + '=1 (OVERFLOW)' : 'TF' + t + '=0'}
            </div>
          </div>
        </div>
      `;
    } else if (cfgMode === 2) {
      // Mode 2: 8-Bit Auto-Reload
      html = `
        <div style="display:flex; flex-direction:column; align-items:center; gap:8px; width:100%;">
          <!-- THx Reload Latch Row -->
          <div style="display:flex; align-items:center; gap:8px;">
            <div style="background:#064E3B; border:1.5px solid #10B981; padding:6px 14px; border-radius:6px; text-align:center;">
              <span style="font-size:0.7rem; font-weight:700; color:#6EE7B7;">TH${t} RELOAD LATCH:</span>
              <span style="font-family:'IBM Plex Mono', monospace; font-size:0.85rem; font-weight:700; color:#FFFFFF; margin-left:6px;">${toHex(thVal, 2)}H (${thVal})</span>
              <span style="font-size:0.65rem; color:#A7F3D0; margin-left:6px;">[Protected Baseline]</span>
            </div>
          </div>
          <div style="color:#10B981; font-size:0.75rem; font-weight:700; display:flex; align-items:center; gap:4px;">
            &darr; Silicon Auto-Reload Path (Instant Copy TL${t} &larr; TH${t} on Overflow)
          </div>
          <!-- Live TLx Counter Row -->
          <div style="display:flex; align-items:center; justify-content:center; flex-wrap:wrap; gap:8px;">
            <div style="background:#1E293B; border:1px solid ${srcColor}; padding:6px 10px; border-radius:6px; font-size:0.75rem; color:${srcColor}; font-weight:600;">
              ${srcText}
            </div>
            <span style="color:#64748B;">&rarr;</span>
            <div style="background:#0F172A; border:1px solid #10B981; padding:4px 8px; border-radius:4px; font-size:0.7rem; color:#10B981; font-family:'IBM Plex Mono', monospace;">
              TR${t}=${trVal}
            </div>
            <span style="color:#64748B;">&rarr;</span>
            <div style="background:#0369A1; border:1.5px solid #38BDF8; padding:8px 14px; border-radius:6px; text-align:center;">
              <div style="font-size:0.7rem; font-weight:700; color:#FFFFFF;">TL${t} LIVE COUNTER</div>
              <div style="font-family:'IBM Plex Mono', monospace; font-size:0.95rem; font-weight:700; color:#E0F2FE;">
                ${toHex(tlVal, 2)}H (${tlVal} / 255)
              </div>
            </div>
            <span style="color:#F59E0B; font-weight:bold; font-size:0.75rem;">&rarr; Rollover &rarr;</span>
            <div style="background:#78350F; border:1.5px solid #F59E0B; padding:8px 12px; border-radius:6px; text-align:center;">
              <div style="font-size:0.7rem; font-weight:700; color:#FDE68A;">TF${t} Flag</div>
              <div style="font-family:'IBM Plex Mono', monospace; font-size:0.8rem; font-weight:700; color:#F59E0B;">
                ${tfVal === 1 ? 'TF' + t + '=1 (ASSERTED)' : 'TF' + t + '=0'}
              </div>
            </div>
          </div>
        </div>
      `;
    } else if (cfgMode === 3) {
      // Mode 3: Split Timer
      if (t === 1) {
        html = `
          <div style="text-align:center; padding:12px; background:#1E293B; border:1.5px dashed #EF4444; border-radius:6px; color:#FCA5A5;">
            <div style="font-size:0.85rem; font-weight:700; color:#EF4444;">TIMER 1 HALTED (MODE 3)</div>
            <div style="font-size:0.75rem; color:#CBD5E1; margin-top:4px;">
              In classic 8051 silicon, placing Timer 1 in Mode 3 halts its clock input. Timer 1 simply stops counting. Mode 3 is designed specifically for Timer 0.
            </div>
          </div>
        `;
      } else {
        html = `
          <div style="display:flex; flex-direction:column; gap:10px; width:100%;">
            <!-- Split Path A: TL0 -->
            <div style="display:flex; align-items:center; justify-content:center; flex-wrap:wrap; gap:8px; background:#0F172A; padding:6px; border-radius:6px; border:1px solid #0369A1;">
              <span style="font-size:0.7rem; font-weight:700; color:#38BDF8;">PATH A (TL0):</span>
              <div style="background:#1E293B; border:1px solid ${srcColor}; padding:4px 8px; border-radius:4px; font-size:0.7rem; color:${srcColor};">
                ${srcText}
              </div>
              <span style="color:#64748B;">&rarr;</span>
              <div style="background:#0F172A; border:1px solid #10B981; padding:2px 6px; border-radius:4px; font-size:0.65rem; color:#10B981; font-family:'IBM Plex Mono', monospace;">
                TR0=${trVal}
              </div>
              <span style="color:#64748B;">&rarr;</span>
              <div style="background:#0369A1; padding:4px 10px; border-radius:4px; font-family:'IBM Plex Mono', monospace; font-size:0.8rem; font-weight:700; color:#FFFFFF;">
                TL0: ${toHex(tlVal, 2)}H (${tlVal})
              </div>
              <span style="color:#64748B;">&rarr;</span>
              <div style="background:#78350F; padding:4px 8px; border-radius:4px; font-family:'IBM Plex Mono', monospace; font-size:0.75rem; color:#FDE68A;">
                TF0=${tfVal}
              </div>
            </div>
            <!-- Split Path B: TH0 (Borrowed TR1 / TF1) -->
            <div style="display:flex; align-items:center; justify-content:center; flex-wrap:wrap; gap:8px; background:#0F172A; padding:6px; border-radius:6px; border:1px solid #581C87;">
              <span style="font-size:0.7rem; font-weight:700; color:#C084FC;">PATH B (TH0):</span>
              <div style="background:#1E293B; border:1px solid #A855F7; padding:4px 8px; border-radius:4px; font-size:0.7rem; color:#A855F7;">
                Osc &divide; 12 (Timer Only)
              </div>
              <span style="color:#64748B;">&rarr;</span>
              <div style="background:#0F172A; border:1px solid #A855F7; padding:2px 6px; border-radius:4px; font-size:0.65rem; color:#C084FC; font-family:'IBM Plex Mono', monospace;">
                TR1=${th0_mode3_run} (BORROWED)
              </div>
              <span style="color:#64748B;">&rarr;</span>
              <div style="background:#6B21A8; padding:4px 10px; border-radius:4px; font-family:'IBM Plex Mono', monospace; font-size:0.8rem; font-weight:700; color:#FFFFFF;">
                TH0: ${toHex(thVal, 2)}H (${thVal})
              </div>
              <span style="color:#64748B;">&rarr;</span>
              <div style="background:#78350F; padding:4px 8px; border-radius:4px; font-family:'IBM Plex Mono', monospace; font-size:0.75rem; color:#FDE68A;">
                TF1=${th0_mode3_tf} (BORROWED)
              </div>
            </div>
            <div style="font-size:0.7rem; color:#94A3B8; text-align:center;">
              &#10003; Timer 1 runs free in background without interrupt flags (Ideal for UART Baud Generation)
            </div>
          </div>
        `;
      }
    }

    el.innerHTML = html;
  }

  function updateUI(narrativeOverride) {
    const t = cfgTimer;
    const tStr = t === 0 ? '0' : '1';
    const pinName = t === 0 ? 'P3.4 (T0)' : 'P3.5 (T1)';
    const thAddr = t === 0 ? '8CH' : '8DH';
    const tlAddr = t === 0 ? '8AH' : '8BH';

    // 1. Update Timer Buttons
    const btnT0 = document.getElementById('tsim-btn-timer-0');
    const btnT1 = document.getElementById('tsim-btn-timer-1');
    if (btnT0 && btnT1) {
      if (t === 0) {
        btnT0.style.background = '#064E3B'; btnT0.style.borderColor = '#10B981'; btnT0.style.color = '#FFFFFF';
        btnT1.style.background = '#1E293B'; btnT1.style.borderColor = '#475569'; btnT1.style.color = '#94A3B8';
      } else {
        btnT1.style.background = '#312E81'; btnT1.style.borderColor = '#818CF8'; btnT1.style.color = '#FFFFFF';
        btnT0.style.background = '#1E293B'; btnT0.style.borderColor = '#475569'; btnT0.style.color = '#94A3B8';
      }
    }

    // 2. Update Source Buttons
    const btnSrcT = document.getElementById('tsim-btn-src-timer');
    const btnSrcC = document.getElementById('tsim-btn-src-counter');
    if (btnSrcT && btnSrcC) {
      if (cfgSource === 'timer') {
        btnSrcT.style.background = '#0C4A6E'; btnSrcT.style.borderColor = '#38BDF8'; btnSrcT.style.color = '#FFFFFF';
        btnSrcC.style.background = '#1E293B'; btnSrcC.style.borderColor = '#475569'; btnSrcC.style.color = '#94A3B8';
      } else {
        btnSrcC.style.background = '#78350F'; btnSrcC.style.borderColor = '#F59E0B'; btnSrcC.style.color = '#FFFFFF';
        btnSrcT.style.background = '#1E293B'; btnSrcT.style.borderColor = '#475569'; btnSrcT.style.color = '#94A3B8';
      }
    }

    // 3. Update Mode Buttons
    for (let m = 0; m <= 3; m++) {
      const btnM = document.getElementById('tsim-btn-mode-' + m);
      if (btnM) {
        if (cfgMode === m) {
          btnM.style.background = '#1E3A8A'; btnM.style.borderColor = '#60A5FA'; btnM.style.color = '#FFFFFF';
        } else {
          btnM.style.background = '#1E293B'; btnM.style.borderColor = '#475569'; btnM.style.color = '#94A3B8';
        }
      }
    }

    // 4. Update External Pulse Button Visibility
    const btnPulse = document.getElementById('tsim-btn-ext-pulse');
    if (btnPulse) {
      if (cfgSource === 'counter' && !(cfgMode === 3 && t === 1)) {
        btnPulse.style.display = 'inline-flex';
        btnPulse.innerHTML = '&#9889; TICK EXTERNAL PIN (' + (t === 0 ? 'T0' : 'T1') + ')';
      } else {
        btnPulse.style.display = 'none';
      }
    }

    // 5. Calculate and Update TMOD Hex & Bitfield
    const ctBit = cfgSource === 'counter' ? 1 : 0;
    const m1Bit = (cfgMode >> 1) & 1;
    const m0Bit = cfgMode & 1;
    let tmodByte = 0;
    if (t === 0) {
      tmodByte = (ctBit << 2) | (m1Bit << 1) | m0Bit;
    } else {
      tmodByte = ((ctBit << 2) | (m1Bit << 1) | m0Bit) << 4;
    }

    const elTmodHex = document.getElementById('tsim-tmod-hex');
    if (elTmodHex) elTmodHex.innerText = toHex(tmodByte, 2) + 'H';

    const elTmodSum = document.getElementById('tsim-tmod-summary');
    if (elTmodSum) {
      const mNames = ['Mode 0 (13-Bit)', 'Mode 1 (16-Bit)', 'Mode 2 (8-Bit Auto-Reload)', 'Mode 3 (Split Timer)'];
      elTmodSum.innerText = 'Timer ' + t + ': ' + mNames[cfgMode] + ' \u2022 C/T=' + ctBit;
    }

    // Update bit cells
    const ctEl = document.getElementById('val-tmod-ct0');
    if (ctEl) ctEl.innerText = t === 0 ? ctBit : 0;
    const m1El = document.getElementById('val-tmod-m1');
    if (m1El) m1El.innerText = t === 0 ? m1Bit : 0;
    const m0El = document.getElementById('val-tmod-m0');
    if (m0El) m0El.innerText = t === 0 ? m0Bit : 0;

    // 6. Update Register Readouts
    const elThLabel = document.getElementById('tsim-th-label');
    const elThRole = document.getElementById('tsim-th-role');
    const elThHex = document.getElementById('tsim-th-hex');
    const elThDec = document.getElementById('tsim-th-dec');

    const elTlLabel = document.getElementById('tsim-tl-label');
    const elTlRole = document.getElementById('tsim-tl-role');
    const elTlHex = document.getElementById('tsim-tl-hex');
    const elTlDec = document.getElementById('tsim-tl-dec');

    if (elThLabel) elThLabel.innerText = 'TH' + tStr + ' REGISTER (' + thAddr + ')';
    if (elTlLabel) elTlLabel.innerText = 'TL' + tStr + ' REGISTER (' + tlAddr + ')';

    if (cfgMode === 0) {
      if (elThRole) elThRole.innerText = '8-Bit High Counter (Bits 12..5)';
      if (elTlRole) elTlRole.innerText = '5-Bit Low Prescaler (Bits 4..0)';
      if (elThHex) elThHex.innerText = toHex(thVal, 2) + 'H';
      if (elThDec) elThDec.innerText = 'Dec: ' + thVal;
      if (elTlHex) elTlHex.innerText = toHex(tlVal & 0x1F, 2) + 'H';
      if (elTlDec) elTlDec.innerText = 'Active: ' + (tlVal & 0x1F) + ' / 31';
    } else if (cfgMode === 1) {
      if (elThRole) elThRole.innerText = 'Cascaded High Byte (Bits 15..8)';
      if (elTlRole) elTlRole.innerText = 'Cascaded Low Byte (Bits 7..0)';
      if (elThHex) elThHex.innerText = toHex(thVal, 2) + 'H';
      if (elThDec) elThDec.innerText = 'Dec: ' + thVal;
      if (elTlHex) elTlHex.innerText = toHex(tlVal, 2) + 'H';
      if (elTlDec) elTlDec.innerText = 'Dec: ' + tlVal;
    } else if (cfgMode === 2) {
      if (elThRole) elThRole.innerText = 'Protected Auto-Reload Latch';
      if (elTlRole) elTlRole.innerText = 'Live 8-Bit Counter (Reloads from TH' + tStr + ')';
      if (elThHex) elThHex.innerText = toHex(thVal, 2) + 'H';
      if (elThDec) elThDec.innerText = 'Reload: ' + thVal;
      if (elTlHex) elTlHex.innerText = toHex(tlVal, 2) + 'H';
      if (elTlDec) elTlDec.innerText = 'Live: ' + tlVal + ' / 255';
    } else if (cfgMode === 3) {
      if (t === 0) {
        if (elThRole) elThRole.innerText = 'Independent 8-Bit Timer (Borrows TR1/TF1)';
        if (elTlRole) elTlRole.innerText = 'Independent 8-Bit Timer/Counter (Uses TR0/TF0)';
        if (elThHex) elThHex.innerText = toHex(thVal, 2) + 'H';
        if (elThDec) elThDec.innerText = 'TH0: ' + thVal;
        if (elTlHex) elTlHex.innerText = toHex(tlVal, 2) + 'H';
        if (elTlDec) elTlDec.innerText = 'TL0: ' + tlVal;
      } else {
        if (elThRole) elThRole.innerText = 'Halted';
        if (elTlRole) elTlRole.innerText = 'Halted';
        if (elThHex) elThHex.innerText = toHex(thVal, 2) + 'H';
        if (elTlHex) elTlHex.innerText = toHex(tlVal, 2) + 'H';
      }
    }

    // 7. Update Progress Bar & Total State Count
    const elCountState = document.getElementById('tsim-count-state');
    const elProg = document.getElementById('tsim-progress-bar');
    if (elCountState && elProg) {
      if (cfgMode === 0) {
        const full13 = ((thVal & 0xFF) << 5) | (tlVal & 0x1F);
        const pct = ((full13 / 8191) * 100).toFixed(1);
        elCountState.innerText = full13 + ' / 8191 (1FFFH)';
        elProg.style.width = Math.min(100, pct) + '%';
      } else if (cfgMode === 1) {
        const full16 = (thVal << 8) | tlVal;
        const pct = ((full16 / 65535) * 100).toFixed(1);
        elCountState.innerText = full16 + ' / 65535 (FFFFH)';
        elProg.style.width = Math.min(100, pct) + '%';
      } else if (cfgMode === 2) {
        const pct = ((tlVal / 255) * 100).toFixed(1);
        elCountState.innerText = tlVal + ' / 255 (FFH)';
        elProg.style.width = Math.min(100, pct) + '%';
      } else if (cfgMode === 3) {
        if (t === 0) {
          elCountState.innerText = 'TL0: ' + tlVal + '/255 | TH0: ' + thVal + '/255';
          elProg.style.width = (((tlVal + thVal) / 510) * 100).toFixed(1) + '%';
        } else {
          elCountState.innerText = 'Timer 1 Halted';
          elProg.style.width = '0%';
        }
      }
    }

    // 8. Update Flags
    const elTr = document.getElementById('tsim-tr-flag');
    if (elTr) {
      if (cfgMode === 3 && t === 0) {
        elTr.innerText = 'TR0=' + trVal + ' | TR1=' + th0_mode3_run;
        elTr.style.color = (trVal || th0_mode3_run) ? '#10B981' : '#64748B';
      } else {
        elTr.innerText = 'TR' + tStr + ' = ' + trVal + (trVal === 1 ? ' (RUNNING)' : ' (HALTED)');
        elTr.style.color = trVal === 1 ? '#10B981' : '#64748B';
      }
    }

    const elTf = document.getElementById('tsim-tf-flag');
    if (elTf) {
      if (tfVal === 1) {
        elTf.innerText = 'TF' + tStr + ' = 1 (OVERFLOW ASSERTED!)';
        elTf.style.color = '#EF4444';
        elTf.style.background = 'rgba(239, 68, 68, 0.2)';
      } else {
        elTf.innerText = 'TF' + tStr + ' = 0 (NO OVERFLOW)';
        elTf.style.color = '#64748B';
        elTf.style.background = '#0F172A';
      }
    }

    // 9. Update Run Button
    const btnRun = document.getElementById('tsim-btn-run');
    if (btnRun) {
      if (isRunning) {
        btnRun.innerHTML = '&#9208; PAUSE';
        btnRun.style.background = '#EF4444';
        btnRun.style.color = '#FFFFFF';
      } else {
        btnRun.innerHTML = '&#9654; RUN CLOCK';
        btnRun.style.background = '#10B981';
        btnRun.style.color = '#0F172A';
      }
    }

    // 10. Update Topology View
    renderTopologyView();

    // 11. Update Path Description
    const elPathDesc = document.getElementById('tsim-path-description');
    if (elPathDesc) {
      const srcLabel = cfgSource === 'timer' ? 'Internal Machine Cycles (Osc / 12)' : 'External Pin ' + pinName;
      if (cfgMode === 0) {
        elPathDesc.innerHTML = `<span style="color:#38BDF8; font-weight:600;">MODE 0 PATH:</span> ${srcLabel} &rarr; TR${tStr} Gate &rarr; TL${tStr} (5 bits, 0..31) &rarr; TH${tStr} (8 bits) &rarr; TF${tStr} at 1FFFH (8,192 states).`;
      } else if (cfgMode === 1) {
        elPathDesc.innerHTML = `<span style="color:#60A5FA; font-weight:600;">MODE 1 PATH:</span> ${srcLabel} &rarr; TR${tStr} Gate &rarr; TL${tStr} (8 bits) &rarr; TH${tStr} (8 bits) &rarr; TF${tStr} at FFFFH (65,536 states).`;
      } else if (cfgMode === 2) {
        elPathDesc.innerHTML = `<span style="color:#10B981; font-weight:600;">MODE 2 PATH:</span> ${srcLabel} &rarr; TR${tStr} Gate &rarr; TL${tStr} increments &rarr; on FFH overflow: hardware sets TF${tStr}=1 and copies TH${tStr} (${toHex(thVal, 2)}H) directly into TL${tStr}!`;
      } else if (cfgMode === 3) {
        if (t === 0) {
          elPathDesc.innerHTML = `<span style="color:#C084FC; font-weight:600;">MODE 3 SPLIT:</span> TL0 operated by TR0/TF0 (${srcLabel}). TH0 strictly internal timer operated by borrowed TR1/TF1. Timer 1 runs free.`;
        } else {
          elPathDesc.innerHTML = `<span style="color:#EF4444; font-weight:600;">MODE 3 (TIMER 1):</span> Timer 1 is halted in Mode 3 by classic 8051 silicon specification.`;
        }
      }
    }

    // 12. Update Narrative Log
    const elLog = document.getElementById('tsim-trace-log');
    if (elLog && narrativeOverride) {
      elLog.innerHTML = narrativeOverride;
    }
  }

  function stopRunning() {
    if (isRunning) {
      isRunning = false;
      if (runInterval) clearInterval(runInterval);
      runInterval = null;
    }
  }

  function tick(isExternal) {
    flashLed(isExternal ? '#F59E0B' : '#38BDF8');
    const t = cfgTimer;
    const tStr = t === 0 ? '0' : '1';
    let narrative = '';

    if (cfgMode === 0) {
      // 13-Bit Mode
      let low5 = tlVal & 0x1F;
      low5++;
      if (low5 > 0x1F) {
        low5 = 0;
        thVal = (thVal + 1) & 0xFF;
        if (thVal === 0) {
          // Overflow at 1FFFH
          tfVal = 1;
          narrative = `<strong style="color:#EF4444;">[13-BIT OVERFLOW]</strong> Counter rolled from <code>1FFFH</code> &rarr; <code>0000H</code>! Hardware asserted <strong>TF${tStr} = 1</strong>.`;
          setTimeout(() => { tfVal = 0; updateUI(); }, 400);
        } else {
          narrative = `<strong style="color:#10B981;">[PRESCALER ROLLOVER]</strong> TL${tStr} (bits 4..0) completed 32 pulses &rarr; Cascaded 1 carry into TH${tStr} (now ${toHex(thVal, 2)}H).`;
        }
      } else {
        if (isExternal) {
          narrative = `<strong style="color:#F59E0B;">[EXTERNAL PULSE]</strong> Pin ${t === 0 ? 'T0' : 'T1'} triggered. 5-bit prescaler incremented to <code>${low5}</code> / 31.`;
        } else {
          narrative = `<strong style="color:#38BDF8;">[TICK]</strong> Clock cycle advanced prescaler in TL${tStr} to <code>${low5}</code> / 31. Total count: ${((thVal << 5) | low5)}.`;
        }
      }
      tlVal = (tlVal & 0xE0) | low5; // preserve upper 3 bits untouched

    } else if (cfgMode === 1) {
      // 16-Bit Mode
      let full16 = (thVal << 8) | tlVal;
      full16++;
      if (full16 > 0xFFFF) {
        full16 = 0;
        thVal = 0;
        tlVal = 0;
        tfVal = 1;
        narrative = `<strong style="color:#EF4444;">[16-BIT OVERFLOW ROLLOVER]</strong> TH${tStr}:TL${tStr} rolled over <code>FFFFH</code> &rarr; <code>0000H</code>! Hardware asserted <strong>TF${tStr} = 1</strong>.`;
        setTimeout(() => { tfVal = 0; updateUI(); }, 400);
      } else {
        thVal = (full16 >> 8) & 0xFF;
        tlVal = full16 & 0xFF;
        if (isExternal) {
          narrative = `<strong style="color:#F59E0B;">[EXTERNAL PULSE]</strong> Pin ${t === 0 ? 'T0' : 'T1'} transitioned. Counter advanced to <code>${toHex(full16, 4)}H</code> (${full16}).`;
        } else if (full16 >= 0xFFFA) {
          narrative = `<strong style="color:#F59E0B;">[NEAR ROLLOVER]</strong> Counter at <code>${toHex(full16, 4)}H</code>. Exactly ${65536 - full16} cycle(s) until 16-bit overflow!`;
        } else if (!isRunning || full16 % 15 === 0) {
          narrative = `<strong style="color:#38BDF8;">[16-BIT COUNTING]</strong> Machine cycle clock incrementing TH${tStr}:TL${tStr} in silicon (${toHex(full16, 4)}H).`;
        }
      }

    } else if (cfgMode === 2) {
      // 8-Bit Auto-Reload Mode
      tlVal++;
      if (tlVal > 0xFF) {
        tfVal = 1;
        tlVal = thVal; // Instant hardware copy!
        narrative = `<strong style="color:#E879F9;">[8-BIT AUTO-RELOAD]</strong> TL${tStr} reached <code>FFH</code> &rarr; Hardware asserted <strong>TF${tStr} = 1</strong> and <em>instantly copied</em> <code>TH${tStr} (${toHex(thVal, 2)}H)</code> back into <code>TL${tStr}</code> with zero software latency!`;
        setTimeout(() => { tfVal = 0; updateUI(); }, 400);
      } else {
        if (isExternal) {
          narrative = `<strong style="color:#F59E0B;">[EXTERNAL PULSE]</strong> TL${tStr} incremented to <code>${toHex(tlVal, 2)}H</code> (${tlVal}). TH${tStr} holds baseline reload (${toHex(thVal, 2)}H).`;
        } else if (tlVal >= 0xFA) {
          narrative = `<strong style="color:#F59E0B;">[NEAR RELOAD]</strong> TL${tStr} at <code>${toHex(tlVal, 2)}H</code>. Only ${256 - tlVal} pulse(s) until overflow and hardware reload!`;
        } else if (!isRunning || tlVal % 10 === 0) {
          narrative = `<strong style="color:#10B981;">[AUTO-RELOAD ACTIVE]</strong> TL${tStr} counting toward FFH. TH${tStr} latch preserves ${toHex(thVal, 2)}H.`;
        }
      }

    } else if (cfgMode === 3) {
      // Mode 3: Split Timer
      if (t === 1) {
        narrative = `<span style="color:#EF4444;">Timer 1 is halted in Mode 3. No pulses counted.</span>`;
      } else {
        // TL0 increments
        tlVal = (tlVal + 1) & 0xFF;
        if (tlVal === 0) {
          tfVal = 1;
          setTimeout(() => { tfVal = 0; updateUI(); }, 400);
        }
        // TH0 also increments (internal timer only)
        if (!isExternal) {
          thVal = (thVal + 1) & 0xFF;
          if (thVal === 0) {
            th0_mode3_tf = 1;
            setTimeout(() => { th0_mode3_tf = 0; updateUI(); }, 400);
          }
        }
        narrative = `<strong style="color:#C084FC;">[SPLIT DUAL COUNT]</strong> TL0=${toHex(tlVal, 2)}H (runs via TR0) \u2022 TH0=${toHex(thVal, 2)}H (runs via borrowed TR1).`;
      }
    }

    updateUI(narrative);
  }

  window.edgeCaseAction = function(action, param) {
    if (action === 'set_timer') {
      stopRunning();
      cfgTimer = param; // 0 or 1
      trVal = 0;
      tfVal = 0;
      if (cfgMode === 2) {
        thVal = 0xD0; tlVal = 0xD0;
      } else {
        thVal = 0; tlVal = 0;
      }
      updateUI(`<strong style="color:#10B981;">[TIMER ${cfgTimer} SELECTED]</strong> Switched to Timer ${cfgTimer}. Active registers: TH${cfgTimer}, TL${cfgTimer}, TR${cfgTimer}, and TF${cfgTimer}.`);
    } else if (action === 'set_source') {
      stopRunning();
      cfgSource = param; // 'timer' or 'counter'
      trVal = 0;
      updateUI(cfgSource === 'timer'
        ? `<strong style="color:#38BDF8;">[SOURCE: TIMER]</strong> C/T = 0 in TMOD. Counter clocked by internal machine cycles (Osc &divide; 12 = 1 &mu;s).`
        : `<strong style="color:#F59E0B;">[SOURCE: COUNTER]</strong> C/T = 1 in TMOD. Hardware waits for falling edges on external Pin ${cfgTimer === 0 ? 'P3.4 (T0)' : 'P3.5 (T1)'}. Use the Pulse button!`);
    } else if (action === 'set_mode') {
      stopRunning();
      cfgMode = param; // 0, 1, 2, 3
      trVal = 0;
      tfVal = 0;
      th0_mode3_run = 0;
      th0_mode3_tf = 0;
      if (cfgMode === 0) {
        thVal = 0; tlVal = 0;
        updateUI(`<strong style="color:#38BDF8;">[MODE 0: 13-BIT COUNTER]</strong> TH${cfgTimer} (8b) + TL${cfgTimer} (5b prescaler). Capacity: 8,192 counts (0000H &rarr; 1FFFH).`);
      } else if (cfgMode === 1) {
        thVal = 0; tlVal = 0;
        updateUI(`<strong style="color:#60A5FA;">[MODE 1: 16-BIT COUNTER]</strong> TH${cfgTimer}:TL${cfgTimer} cascaded. Full capacity: 65,536 counts (0000H &rarr; FFFFH).`);
      } else if (cfgMode === 2) {
        thVal = 0xD0; // Default reload value (208)
        tlVal = 0xD0;
        updateUI(`<strong style="color:#E879F9;">[MODE 2: 8-BIT AUTO-RELOAD]</strong> TL${cfgTimer} counts live (${toHex(tlVal, 2)}H &rarr; FFH). TH${cfgTimer} holds protected reload value (${toHex(thVal, 2)}H).`);
      } else if (cfgMode === 3) {
        if (cfgTimer === 0) {
          thVal = 0; tlVal = 0;
          th0_mode3_run = 1;
          updateUI(`<strong style="color:#C084FC;">[MODE 3: SPLIT TIMER 0]</strong> Timer 0 split into two independent 8-bit counters: TL0 (TR0/TF0) and TH0 (borrowed TR1/TF1).`);
        } else {
          updateUI(`<strong style="color:#EF4444;">[MODE 3: TIMER 1]</strong> Classic 8051 silicon specification: placing Timer 1 in Mode 3 halts Timer 1.`);
        }
      }
    } else if (action === 'toggle_run') {
      if (isRunning) {
        stopRunning();
        trVal = 0;
        th0_mode3_run = 0;
        updateUI(`<strong style="color:#CBD5E1;">[HALTED]</strong> TR${cfgTimer} cleared to 0. Hardware clock gate closed.`);
      } else {
        if (cfgMode === 3 && cfgTimer === 1) {
          updateUI(`<strong style="color:#EF4444;">[CANNOT RUN]</strong> Timer 1 is halted in Mode 3.`);
          return;
        }
        if (cfgSource === 'counter') {
          updateUI(`<strong style="color:#F59E0B;">[COUNTER MODE READY]</strong> TR${cfgTimer}=1. Awaiting external pin transitions. Click <strong>TICK EXTERNAL PIN</strong> to feed pulses!`);
          trVal = 1;
          updateUI();
          return;
        }
        isRunning = true;
        trVal = 1;
        if (cfgMode === 3 && cfgTimer === 0) th0_mode3_run = 1;
        runInterval = setInterval(() => {
          tick(false);
        }, 90);
        updateUI(`<strong style="color:#10B981;">[RUNNING]</strong> TR${cfgTimer}=1. Internal machine cycle pulses streaming into counter.`);
      }
    } else if (action === 'step') {
      stopRunning();
      trVal = 1;
      tick(cfgSource === 'counter');
    } else if (action === 'pulse_pin') {
      trVal = 1;
      tick(true);
    } else if (action === 'pulse_burst') {
      for (let i = 0; i < 10; i++) {
        tick(cfgSource === 'counter');
      }
    } else if (action === 'preset_overflow') {
      stopRunning();
      if (cfgMode === 0) {
        thVal = 0xFF; tlVal = 0x1C; // 4 ticks away from 1FFFH
        updateUI(`<strong style="color:#F59E0B;">[PRESET NEAR OVERFLOW]</strong> Loaded 13-bit counter to 1FFCH. Exactly 4 pulses until rollover and TF${cfgTimer} assertion!`);
      } else if (cfgMode === 1) {
        thVal = 0xFF; tlVal = 0xFC; // 4 ticks away from FFFFH
        updateUI(`<strong style="color:#F59E0B;">[PRESET NEAR OVERFLOW]</strong> Loaded 16-bit counter to FFFCH. Exactly 4 pulses until rollover and TF${cfgTimer} assertion!`);
      } else if (cfgMode === 2) {
        thVal = 0xD0; tlVal = 0xFD; // 3 ticks away from FFH
        updateUI(`<strong style="color:#E879F9;">[PRESET NEAR AUTO-RELOAD]</strong> TL${cfgTimer} = FDH with TH${cfgTimer} Reload = D0H. Exactly 3 pulses until rollover and auto-reload!`);
      } else if (cfgMode === 3) {
        tlVal = 0xFD; thVal = 0xFE;
        updateUI(`<strong style="color:#C084FC;">[PRESET NEAR OVERFLOW]</strong> Preloaded TL0=FDH and TH0=FEH near 8-bit limits.`);
      }
    } else if (action === 'reset') {
      stopRunning();
      trVal = 0;
      tfVal = 0;
      th0_mode3_run = 0;
      th0_mode3_tf = 0;
      if (cfgMode === 2) {
        thVal = 0xD0; tlVal = 0xD0;
      } else {
        thVal = 0; tlVal = 0;
      }
      updateUI(`<strong style="color:#38BDF8;">[RESET]</strong> Registers and flags restored to default state.`);
    }
  };

  // Immediate initial paint
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => updateUI());
  } else {
    setTimeout(updateUI, 50);
  }
})();
'''
    content = before + new_workbench_js
    print("Replaced workbench logic at the end of script.js successfully")
else:
    print("Marker not found in script.js!")

with open("script.js", "w", encoding="utf-8") as f:
    f.write(content)

print(f"Updated script.js successfully! Total lines: {len(content.splitlines())}")
