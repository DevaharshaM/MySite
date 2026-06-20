import streamlit as st
import time

# Set page config
st.set_page_config(
    page_title="PrajnaEdge - SPI: The Shared Rhythm",
    page_icon="⚡",
    layout="wide"
)

# Custom Styling aligned with the PrajnaEdge minimal dark-mode theme
st.markdown("""
<style>
    body, [data-testid="stAppViewContainer"] {
        background-color: #0F172A !important;
        color: #E2E8F0 !important;
    }
    .panel-box {
        background-color: #1E293B;
        border: 1px solid rgba(148, 163, 184, 0.12);
        border-radius: 8px;
        padding: 1.25rem;
        margin-bottom: 1.25rem;
        transition: all 0.3s ease;
    }
    .panel-title {
        font-family: 'Syne', sans-serif;
        font-weight: 700;
        font-size: 0.9rem;
        color: #FFFFFF;
        text-transform: uppercase;
        margin-bottom: 0.75rem;
        display: flex;
        align-items: center;
        gap: 0.4rem;
        letter-spacing: 0.05em;
    }
    .panel-title::before {
        content: "⚡";
        color: #3B82F6;
    }
    .pipeline-step {
        font-family: monospace;
        font-size: 0.75rem;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        margin-bottom: 0.35rem;
        font-weight: bold;
    }
    .agreement-item {
        font-family: monospace;
        font-size: 0.85rem;
        padding: 0.25rem 0.5rem;
        margin-bottom: 0.4rem;
        border-radius: 4px;
    }
    .agreement-ok {
        background: rgba(16, 185, 129, 0.08);
        color: #10B981;
        border: 1px solid rgba(16, 185, 129, 0.15);
    }
    .agreement-fail {
        background: rgba(239, 68, 68, 0.08);
        color: #EF6868;
        border: 1px solid rgba(239, 68, 68, 0.15);
    }
    .register-container {
        display: flex;
        gap: 0.25rem;
        margin-top: 0.5rem;
        background: #0F172A;
        padding: 0.4rem;
        border-radius: 6px;
        border: 1px solid rgba(148, 163, 184, 0.08);
        width: max-content;
    }
    .register-cell {
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 32px;
        border: 1px solid rgba(148, 163, 184, 0.1);
        background: #1E293B;
        border-radius: 3px;
        font-family: monospace;
    }
    .register-label {
        font-size: 0.55rem;
        color: #64748B;
        border-bottom: 1px solid rgba(148, 163, 184, 0.1);
        width: 100%;
        text-align: center;
        padding: 0.1rem 0;
    }
    .register-val {
        font-size: 0.8rem;
        font-weight: bold;
        color: #FFF;
        padding: 0.2rem 0;
    }
    .terminal-box {
        background: #0F172A;
        border: 1px solid rgba(148, 163, 184, 0.12);
        border-radius: 8px;
        padding: 0.8rem;
        font-family: monospace;
        font-size: 0.75rem;
        height: 180px;
        overflow-y: auto;
        line-height: 1.5;
        color: #A5F3FC;
    }
</style>
""", unsafe_allow_html=True)

st.title("EdgeCase: The Shared Rhythm")
st.subheader("Why SPI devices must agree on timing.")
st.caption("Configure Clock Polarity (CPOL) and Clock Phase (CPHA) registers to watch how timing sync works or breaks.")

# Initialize Session State
if "spi_msg" not in st.session_state:
    st.session_state.spi_msg = "Hello"
if "spi_temp_msg" not in st.session_state:
    st.session_state.spi_temp_msg = "Hello"
if "spi_animating" not in st.session_state:
    st.session_state.spi_animating = False
if "spi_anim_step" not in st.session_state:
    st.session_state.spi_anim_step = 20  # 20 = static finished state
if "spi_logs" not in st.session_state:
    st.session_state.spi_logs = []

# ====================================================
# CONFIGURATION PANEL (MASTER vs SLAVE SETTINGS)
# ====================================================
st.markdown('<div class="pipeline-step">Timing Configuration</div>', unsafe_allow_html=True)
with st.container():
    st.markdown('<div class="panel-box">', unsafe_allow_html=True)
    m_col, s_col, status_col = st.columns([1, 1, 1])
    
    with m_col:
        st.markdown('<div class="panel-title" style="color:#3B82F6;">Master Timing Registers</div>', unsafe_allow_html=True)
        m_cpol = st.selectbox("Master CPOL", [0, 1], format_func=lambda x: f"CPOL = {x} (Idle {'Low' if x==0 else 'High'})", key="m_cpol")
        m_cpha = st.selectbox("Master CPHA", [0, 1], format_func=lambda x: f"CPHA = {x} (Sample on {'Leading' if x==0 else 'Trailing'} Edge)", key="m_cpha")

    with s_col:
        st.markdown('<div class="panel-title" style="color:#FFF;">Slave Timing Registers</div>', unsafe_allow_html=True)
        s_cpol = st.selectbox("Slave CPOL", [0, 1], format_func=lambda x: f"CPOL = {x} (Idle {'Low' if x==0 else 'High'})", key="s_cpol")
        s_cpha = st.selectbox("Slave CPHA", [0, 1], format_func=lambda x: f"CPHA = {x} (Sample on {'Leading' if x==0 else 'Trailing'} Edge)", key="s_cpha")

    with status_col:
        st.markdown('<div class="panel-title" style="color:#10B981;">Mode Agreement</div>', unsafe_allow_html=True)
        cpol_ok = (m_cpol == s_cpol)
        cpha_ok = (m_cpha == s_cpha)
        agreement_ok = cpol_ok and cpha_ok
        
        cpol_icon = "✓" if cpol_ok else "✗"
        cpol_class = "agreement-ok" if cpol_ok else "agreement-fail"
        st.markdown(f'<div class="agreement-item {cpol_class}">{cpol_icon} Clock Polarity: Master={m_cpol} vs Slave={s_cpol}</div>', unsafe_allow_html=True)
        
        cpha_icon = "✓" if cpha_ok else "✗"
        cpha_class = "agreement-ok" if cpha_ok else "agreement-fail"
        st.markdown(f'<div class="agreement-item {cpha_class}">{cpha_icon} Clock Phase: Master={m_cpha} vs Slave={s_cpha}</div>', unsafe_allow_html=True)
        
        if agreement_ok:
            st.markdown('<div class="agreement-item agreement-ok" style="font-weight:bold;text-align:center;">✓ Bus Synchronized (Mode {})</div>'.format((m_cpol << 1) | m_cpha), unsafe_allow_html=True)
        else:
            st.markdown('<div class="agreement-item agreement-fail" style="font-weight:bold;text-align:center;">✗ Phase Mismatch Detected!</div>', unsafe_allow_html=True)
            
    st.markdown('</div>', unsafe_allow_html=True)

# ====================================================
# CONTROLS
# ====================================================
st.markdown('<div class="pipeline-step">System Controls</div>', unsafe_allow_html=True)
with st.container():
    st.markdown('<div class="panel-box">', unsafe_allow_html=True)
    msg_col, btn_col = st.columns([3, 1])
    with msg_col:
        msg_input = st.text_input("Enter Message (Press Enter/TRANSMIT to send)", value=st.session_state.spi_temp_msg, max_chars=12)
        st.session_state.spi_temp_msg = msg_input
    with btn_col:
        st.markdown('<div style="height:28px;"></div>', unsafe_allow_html=True)
        transmit_clicked = st.button("TRANSMIT", use_container_width=True)
        
    if transmit_clicked:
        st.session_state.spi_msg = st.session_state.spi_temp_msg if st.session_state.spi_temp_msg else " "
        st.session_state.spi_animating = True
        st.session_state.spi_anim_step = 0
        st.session_state.spi_logs = ["[0.0ms] Master asserts CS low... Starting SPI transaction."]
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# Parse active character
active_char = st.session_state.spi_msg[0] if len(st.session_state.spi_msg) > 0 else ' '
char_code = ord(active_char)
tx_bits = [(char_code >> (7 - b)) & 1 for b in range(8)]

# Determine simulation parameters
# SPI SCLK phase coordinates:
# Edges: 135, 170, 205, 240, 275, 310, 345, 380, 415, 450, 485, 520, 555, 590, 625, 660
x_edges = [135 + i * 35 for i in range(16)]

# Master shift and sample edges
# For Master:
# if CPHA = 0: data changed at trailing edges (odd indexes: 170, 240, ...), sampled at leading edges (even indexes: 135, 205, ...)
# if CPHA = 1: data changed at leading edges (even indexes: 135, 205, ...), sampled at trailing edges (odd indexes: 170, 240, ...)
# Slave samples based on Slave CPOL and CPHA.
# If Slave Mode == Master Mode, the slave samples align perfectly with Master Tx windows.
# Otherwise they are misaligned (sampling right on transition or wrong phases).

# Slave sampling ticks coordinates:
if s_cpha == 0:
    slave_sample_xs = [x_edges[i] for i in range(0, 16, 2)]
else:
    slave_sample_xs = [x_edges[i] for i in range(1, 16, 2)]

# Draw Waveforms SVG
svg_w = 900
svg_h = 230
pad_left = 80
pad_right = 30
disp_w = svg_w - pad_left - pad_right

svg_blocks = []

# 1. CS Line waveform (asserted low at x=100, high at x=695)
cs_y_high = 30
cs_y_low = 45
cs_path = f"M 0,{cs_y_high} L 100,{cs_y_high} L 100,{cs_y_low} L 695,{cs_y_low} L 695,{cs_y_high} L {svg_w},{cs_y_high}"
svg_blocks.append(f'<path d="{cs_path}" fill="none" stroke="#F59E0B" stroke-width="2" />')
svg_blocks.append(f'<text x="{pad_left - 15}" y="{cs_y_low - 2}" fill="#F59E0B" font-family="monospace" font-size="8" text-anchor="end">CS</text>')

# 2. SCLK Line waveform
sclk_y_high = 70
sclk_y_low = 90
sclk_idle = sclk_y_high if m_cpol == 1 else sclk_y_low
sclk_active = sclk_y_low if m_cpol == 1 else sclk_y_high

sclk_path = f"M 0,{sclk_idle} L 135,{sclk_idle}"
curr_y = sclk_idle
for x in x_edges:
    next_y = sclk_active if curr_y == sclk_idle else sclk_idle
    sclk_path += f" L {x},{curr_y} L {x},{next_y}"
    curr_y = next_y
sclk_path += f" L {svg_w},{sclk_idle}"

svg_blocks.append(f'<path d="{sclk_path}" fill="none" stroke="#3B82F6" stroke-width="2" />')
svg_blocks.append(f'<text x="{pad_left - 15}" y="{sclk_y_low - 2}" fill="#3B82F6" font-family="monospace" font-size="8" text-anchor="end">SCLK</text>')

# 3. MOSI Waveform
# Data windows depend on CPHA
mosi_y_high = 115
mosi_y_low = 135

mosi_path = f"M 0,{mosi_y_high} L 100,{mosi_y_high}"
# Let's map MOSI segments
mosi_segments = []
if m_cpha == 0:
    # Bit 7 is driven immediately on CS falling edge (x=100)
    mosi_segments.append((100, 170, tx_bits[0]))
    for b in range(1, 8):
        mosi_segments.append((170 + (b - 1) * 70, 170 + b * 70, tx_bits[b]))
    mosi_segments.append((660, svg_w, 1))
else:
    # Bit 7 driven on first SCLK edge (x=135)
    mosi_segments.append((100, 135, 1))
    for b in range(8):
        mosi_segments.append((135 + b * 70, 135 + (b + 1) * 70, tx_bits[b]))
    mosi_segments.append((695, svg_w, 1))

# Draw MOSI path from segments
for start_x, end_x, val in mosi_segments:
    y_val = mosi_y_high if val == 1 else mosi_y_low
    mosi_path += f" L {start_x},{y_val} L {end_x},{y_val}"
svg_blocks.append(f'<path d="{mosi_path}" fill="none" stroke="#FFFFFF" stroke-width="2" />')
svg_blocks.append(f'<text x="{pad_left - 15}" y="{mosi_y_low - 2}" fill="#FFFFFF" font-family="monospace" font-size="8" text-anchor="end">MOSI</text>')

# 4. MISO Waveform (returns 0x5A = 01011010)
miso_bits = [0, 1, 0, 1, 1, 0, 1, 0]
miso_y_high = 160
miso_y_low = 180

miso_path = f"M 0,{miso_y_high} L 100,{miso_y_high}"
miso_segments = []
if m_cpha == 0:
    miso_segments.append((100, 170, miso_bits[0]))
    for b in range(1, 8):
        miso_segments.append((170 + (b - 1) * 70, 170 + b * 70, miso_bits[b]))
    miso_segments.append((660, svg_w, 1))
else:
    miso_segments.append((100, 135, 1))
    for b in range(8):
        miso_segments.append((135 + b * 70, 135 + (b + 1) * 70, miso_bits[b]))
    miso_segments.append((695, svg_w, 1))

for start_x, end_x, val in miso_segments:
    y_val = miso_y_high if val == 1 else miso_y_low
    miso_path += f" L {start_x},{y_val} L {end_x},{y_val}"
svg_blocks.append(f'<path d="{miso_path}" fill="none" stroke="#10B981" stroke-width="2" />')
svg_blocks.append(f'<text x="{pad_left - 15}" y="{miso_y_low - 2}" fill="#10B981" font-family="monospace" font-size="8" text-anchor="end">MISO</text>')

# 5. Draw Slave Sampling Ticks (only if step >= index)
step = st.session_state.spi_anim_step
for idx, xs in enumerate(slave_sample_xs):
    if step >= idx * 2 + 1:
        color = "#10B981" if agreement_ok else "#EF6868"
        dash = "1,2" if not agreement_ok else "2,2"
        # Find sampled MOSI value
        sampled_val = 1
        for start_x, end_x, val in mosi_segments:
            if start_x <= xs <= end_x:
                sampled_val = val
                break
        
        svg_blocks.append(f'<line x1="{xs}" y1="50" x2="{xs}" y2="200" stroke="{color}" stroke-dasharray="{dash}" stroke-width="1" />')
        svg_blocks.append(f'<circle cx="{xs}" cy="{sclk_idle if (xs in slave_sample_xs and not cpha_ok) else sclk_active}" r="3" fill="{color}" />')
        svg_blocks.append(f'<circle cx="{xs}" cy="{mosi_y_high if sampled_val==1 else mosi_y_low}" r="3.5" fill="{color}" stroke="#0F172A" />')
        svg_blocks.append(f'<text x="{xs}" y="215" fill="{color}" font-family="monospace" font-size="8" text-anchor="middle" font-weight="bold">S{idx}({sampled_val})</text>')

# 6. Glowing Time Sweep Cursor
if st.session_state.spi_animating and step < 18:
    cursor_x = 100 + step * 35
    svg_blocks.append(f'<line x1="{cursor_x}" y1="15" x2="{cursor_x}" y2="200" stroke="#3B82F6" stroke-width="1.5" />')

# Compile SVG
svg_content = f'<svg viewBox="0 0 {svg_w} {svg_h}" width="100%">{"".join(svg_blocks)}</svg>'

# Render Waveform
st.markdown('<div class="pipeline-step">Physical Waveform Timing Trace (Inspecting First Character)</div>', unsafe_allow_html=True)
with st.container():
    st.markdown('<div class="panel-box" style="margin-bottom: 0.5rem;">', unsafe_allow_html=True)
    st.markdown(f'<div style="background:#0F172A; padding:0; overflow-x:auto;">{svg_content}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.caption("Waveform traces: CS line (active low), SCLK pulse train, MOSI/MISO data windows, and slave sampling marks (green = matching, red = mismatched/corrupted).")

# ====================================================
# SLAVE RECONSTRUCTED REGISTER SHIFT PREVIEW
# ====================================================
# Compute Slave RX bits up to current step
rx_register_bits = ["_"] * 8
for idx in range(8):
    if step >= idx * 2 + 1:
        xs = slave_sample_xs[idx]
        sampled_val = 0
        for start_x, end_x, val in mosi_segments:
            if start_x <= xs <= end_x:
                sampled_val = val
                break
        rx_register_bits[idx] = str(sampled_val)

cells_html = []
for idx in range(8):
    cls = "register-cell"
    if rx_register_bits[idx] != "_":
        cls += " fifo-active-rx" if agreement_ok else " fifo-active"
    cells_html.append(f"""
    <div class="{cls}" style="display:inline-block; margin-right:0.25rem;">
        <div class="register-label">D{7-idx}</div>
        <div class="register-val">{rx_register_bits[idx]}</div>
    </div>
    """)

# ====================================================
# TRANSACTION LOG & DATA RECOVERY OUTCOME
# ====================================================
log_col, out_col = st.columns(2)

with log_col:
    st.markdown('<div class="pipeline-step">Protocol Transaction Log</div>', unsafe_allow_html=True)
    
    # Generate live logging list based on step
    logs = ["[0.0ms] Master asserts CS low... Starting SPI transaction."]
    if step >= 1:
        logs.append(f"[0.2ms] SCLK active. Polarity Idle={'High' if m_cpol==1 else 'Low'}. Phase CPHA={m_cpha}.")
    for idx in range(8):
        if step >= idx * 2 + 1:
            xs = slave_sample_xs[idx]
            # MOSI
            val = 0
            for start_x, end_x, v in mosi_segments:
                if start_x <= xs <= end_x:
                    val = v
                    break
            edge_type = "leading" if ((idx % 2 == 0) if s_cpha==0 else (idx % 2 != 0)) else "trailing"
            edge_direction = "rising" if ((m_cpol == 0) if edge_type=="leading" else (m_cpol == 1)) else "falling"
            
            logs.append(f"[Bit {7-idx}] Slave samples MOSI on {edge_direction} edge -> Read {val}.")
            if not agreement_ok:
                logs.append(f"[WARNING] Timing mismatch! Slave sampled on unstable boundary.")
    if step >= 16:
        logs.append("[2.8ms] SCLK clock train finishes.")
        logs.append("[3.0ms] Master deasserts CS High... Transaction closed.")
        if agreement_ok:
            logs.append("[SUCCESS] Bus alignment clean. Data verified.")
        else:
            logs.append("[FAIL] Phase mismatch. Slave sampled transitions. Bits corrupted.")
            
    st.markdown(f'<div class="terminal-box">{"<br>".join(logs)}</div>', unsafe_allow_html=True)

with out_col:
    st.markdown('<div class="pipeline-step">Data Recovery Outcome</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="panel-box" style="height: 180px; margin:0; display:flex; flex-direction:column; justify-content:center; gap:0.5rem;">', unsafe_allow_html=True)
        
        # Display registers
        st.markdown('<div style="font-family:monospace; font-size:0.75rem; color:#64748B; text-transform:uppercase;">Slave Shift Register (Input Buffer):</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="register-container" style="margin:0;">{"".join(cells_html)}</div>', unsafe_allow_html=True)
        
        # Decode outcome
        # If agreement ok: message recovered. If mismatch, corrupted.
        recovered_str = ""
        if step >= 16:
            if agreement_ok:
                recovered_str = st.session_state.spi_msg
            else:
                # Simulat logic corruption
                for char in st.session_state.spi_msg:
                    val = ord(char)
                    # Shift left or garble
                    if m_cpha != s_cpha and m_cpol == s_cpol:
                        # phase mismatch: shift bits left by 1
                        rec_val = (val << 1) & 0xFF
                    elif m_cpol != s_cpol and m_cpha == s_cpha:
                        # polarity mismatch: shift right
                        rec_val = (val >> 1) & 0xFF
                    else:
                        # both mismatch: invert
                        rec_val = (~val) & 0xFF
                    recovered_str += chr(rec_val) if 32 <= rec_val <= 126 else "?"
        else:
            recovered_str = "..."
            
        st.markdown(f"""
        <div style="display:grid; grid-template-columns: 1fr 1fr; gap:0.5rem; font-family:monospace; margin-top:0.4rem;">
            <div>
                <span style="color:#64748B; font-size:0.65rem; display:block;">TX DATA</span>
                <span style="font-weight:bold; font-size:1.1rem; color:#FFF;">{st.session_state.spi_msg}</span>
            </div>
            <div>
                <span style="color:#64748B; font-size:0.65rem; display:block;">RX RECOVERED</span>
                <span style="font-weight:bold; font-size:1.1rem; color:{'#10B981' if agreement_ok else '#EF6868'};">{recovered_str}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

# ====================================================
# ANIMATION LOOP DRIVER
# ====================================================
if st.session_state.spi_animating:
    if st.session_state.spi_anim_step < 17:
        time.sleep(0.15)
        st.session_state.spi_anim_step += 1
        st.rerun()
    else:
        st.session_state.spi_animating = False
        st.rerun()
