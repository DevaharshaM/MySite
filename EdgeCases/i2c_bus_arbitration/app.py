import streamlit as st
import time

# Set page config
st.set_page_config(
    page_title="PrajnaEdge - I2C: The Polite Argument",
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
    .agreement-warning {
        background: rgba(245, 158, 11, 0.08);
        color: #F59E0B;
        border: 1px solid rgba(245, 158, 11, 0.15);
    }
    .agreement-fail {
        background: rgba(239, 68, 68, 0.08);
        color: #EF6868;
        border: 1px solid rgba(239, 68, 68, 0.15);
    }
    .terminal-box {
        background: #0F172A;
        border: 1px solid rgba(148, 163, 184, 0.12);
        border-radius: 8px;
        padding: 0.8rem;
        font-family: monospace;
        font-size: 0.75rem;
        height: 200px;
        overflow-y: auto;
        line-height: 1.5;
        color: #A5F3FC;
    }
</style>
""", unsafe_allow_html=True)

st.title("EdgeCase: The Polite Argument")
st.subheader("I2C Multi-Master Bus Arbitration Simulator")
st.caption("Configure output bytes for Master A and Master B to watch how they resolve contention gracefully at the physical wire level.")

# Initialize Session State
if "arb_a" not in st.session_state:
    st.session_state.arb_a = "0x5A"
if "arb_b" not in st.session_state:
    st.session_state.arb_b = "0x6C"
if "arb_animating" not in st.session_state:
    st.session_state.arb_animating = False
if "arb_anim_step" not in st.session_state:
    st.session_state.arb_anim_step = 20

# ====================================================
# CONFIGURATION PANEL
# ====================================================
st.markdown('<div class="pipeline-step">Arbitration Setup</div>', unsafe_allow_html=True)
with st.container():
    st.markdown('<div class="panel-box">', unsafe_allow_html=True)
    a_col, b_col, status_col = st.columns([1.5, 1.5, 1])
    
    with a_col:
        st.markdown('<div class="panel-title" style="color:#3B82F6;">Master A Output</div>', unsafe_allow_html=True)
        val_a_str = st.selectbox("Byte to Transmit (A)", ["0x5A", "0x6C", "0x7F"], key="sel_a")
        st.session_state.arb_a = val_a_str
        
    with b_col:
        st.markdown('<div class="panel-title" style="color:#EC4899;">Master B Output</div>', unsafe_allow_html=True)
        val_b_str = st.selectbox("Byte to Transmit (B)", ["0x5A", "0x6C", "0x3C"], key="sel_b")
        st.session_state.arb_b = val_b_str

    val_a = int(st.session_state.arb_a, 16)
    val_b = int(st.session_state.arb_b, 16)

    # Convert to bits
    bits_a = [(val_a >> i) & 1 for i in range(7, -1, -1)]
    bits_b = [(val_b >> i) & 1 for i in range(7, -1, -1)]

    # Calculate arbitration dropouts
    active_a = True
    active_b = True
    lost_step_a = -1
    lost_step_b = -1
    actual_sda_bits = []

    for i in range(8):
        bit_a = bits_a[i] if active_a else 1
        bit_b = bits_b[i] if active_b else 1
        shared_bit = bit_a & bit_b
        actual_sda_bits.append(shared_bit)

        if active_a and bit_a == 1 and shared_bit == 0:
            active_a = false = False
            lost_step_a = i
        if active_b and bit_b == 1 and shared_bit == 0:
            active_b = false = False
            lost_step_b = i

    with status_col:
        st.markdown('<div class="panel-title" style="color:#10B981;">Arbitration Status</div>', unsafe_allow_html=True)
        if lost_step_a == -1 and lost_step_b == -1:
            st.markdown('<div class="agreement-item agreement-ok" style="font-weight:bold;text-align:center;">✓ Bytes Identical.<br>No Collision.</div>', unsafe_allow_html=True)
        elif lost_step_a != -1:
            st.markdown('<div class="agreement-item agreement-warning" style="font-weight:bold;text-align:center;">✓ Master B Victorious.<br>A backed off.</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="agreement-item agreement-warning" style="font-weight:bold;text-align:center;">✓ Master A Victorious.<br>B backed off.</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ====================================================
# SYSTEM CONTROLS
# ====================================================
st.markdown('<div class="pipeline-step">System Controls</div>', unsafe_allow_html=True)
with st.container():
    st.markdown('<div class="panel-box">', unsafe_allow_html=True)
    c_desc, c_btn = st.columns([3, 1])
    with c_desc:
        st.markdown('<div style="font-family:monospace;font-size:0.85rem;color:#FFF;height:38px;display:flex;align-items:center;">Both masters clock in sync. The open-drain wired-AND bus pulls the line low when they conflict.</div>', unsafe_allow_html=True)
    with c_btn:
        arb_transmit_clicked = st.button("START ARBITRATION", use_container_width=True)
        if arb_transmit_clicked:
            st.session_state.arb_animating = True
            st.session_state.arb_anim_step = 0
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

step = st.session_state.arb_anim_step

# ====================================================
# SVG TIMING WAVEFORMS
# ====================================================
svg_w = 950
svg_h = 240
pad_left = 110
y_a_high, y_a_low = 25, 40
y_b_high, y_b_low = 70, 85
y_shared_high, y_shared_low = 115, 130
y_scl_high, y_scl_low = 160, 175

x_edges = [pad_left + 45 + i * 70 for i in range(9)]
svg_blocks = []

# Master A SDA Waveform
path_a = f"M 0,{y_a_high} L {x_edges[0]},{y_a_high}"
act_a = True
for i in range(8):
    startX = x_edges[i]
    endX = x_edges[i+1]
    bit = bits_a[i] if act_a else 1
    yVal = y_a_high if bit == 1 else y_a_low
    path_a += f" L {startX},{yVal} L {endX},{yVal}"
    if act_a and lost_step_a == i: act_a = False
path_a += f" L {svg_w},{y_a_high}"
svg_blocks.append(f'<path d="{path_a}" fill="none" stroke="#3B82F6" stroke-width="1.5" />')
svg_blocks.append(f'<text x="{pad_left - 15}" y="{y_a_low}" fill="#3B82F6" font-family="monospace" font-size="8" text-anchor="end">Master A SDA</text>')

# Master B SDA Waveform
path_b = f"M 0,{y_b_high} L {x_edges[0]},{y_b_high}"
act_b = True
for i in range(8):
    startX = x_edges[i]
    endX = x_edges[i+1]
    bit = bits_b[i] if act_b else 1
    yVal = y_b_high if bit == 1 else y_b_low
    path_b += f" L {startX},{yVal} L {endX},{yVal}"
    if act_b and lost_step_b == i: act_b = False
path_b += f" L {svg_w},{y_b_high}"
svg_blocks.append(f'<path d="{path_b}" fill="none" stroke="#EC4899" stroke-width="1.5" />')
svg_blocks.append(f'<text x="{pad_left - 15}" y="{y_b_low}" fill="#EC4899" font-family="monospace" font-size="8" text-anchor="end">Master B SDA</text>')

# Shared SDA Waveform
path_shared = f"M 0,{y_shared_high} L {x_edges[0]},{y_shared_high}"
for i in range(8):
    startX = x_edges[i]
    endX = x_edges[i+1]
    bit = actual_sda_bits[i]
    yVal = y_shared_high if bit == 1 else y_shared_low
    path_shared += f" L {startX},{yVal} L {endX},{yVal}"
path_shared += f" L {svg_w},{y_shared_high}"
svg_blocks.append(f'<path d="{path_shared}" fill="none" stroke="#10B981" stroke-width="2" />')
svg_blocks.append(f'<text x="{pad_left - 15}" y="{y_shared_low}" fill="#10B981" font-family="monospace" font-size="8" text-anchor="end">Shared SDA Bus</text>')

# Shared SCL Waveform
path_scl = f"M 0,{y_scl_high} L {x_edges[0]},{y_scl_high}"
for i in range(8):
    startX = x_edges[i]
    midX = startX + 35
    endX = x_edges[i+1]
    path_scl += f" L {startX},{y_scl_low} L {midX},{y_scl_low} L {midX},{y_scl_high} L {endX},{y_scl_high}"
path_scl += f" L {svg_w},{y_scl_high}"
svg_blocks.append(f'<path d="{path_scl}" fill="none" stroke="#6366F1" stroke-width="1.5" />')
svg_blocks.append(f'<text x="{pad_left - 15}" y="{y_scl_low}" fill="#6366F1" font-family="monospace" font-size="8" text-anchor="end">SCL (Clock)</text>')

# Highlight dropout step
if lost_step_a != -1:
    xDropout = x_edges[lost_step_a] + 35
    svg_blocks.append(f'<line x1="{xDropout}" y1="10" x2="{xDropout}" y2="190" stroke="#EF6868" stroke-dasharray="2,2" stroke-width="1" />')
    svg_blocks.append(f'<text x="{xDropout}" y="15" fill="#EF6868" font-family="monospace" font-size="7" font-weight="bold" text-anchor="middle">A BACKED OFF</text>')

if lost_step_b != -1:
    xDropout = x_edges[lost_step_b] + 35
    svg_blocks.append(f'<line x1="{xDropout}" y1="10" x2="{xDropout}" y2="190" stroke="#EF6868" stroke-dasharray="2,2" stroke-width="1" />')
    svg_blocks.append(f'<text x="{xDropout}" y="15" fill="#EF6868" font-family="monospace" font-size="7" font-weight="bold" text-anchor="middle">B BACKED OFF</text>')

# Time Cursor
if st.session_state.arb_animating and step <= 9:
    cursor_x = x_edges[0] + step * 70 + 35
    svg_blocks.append(f'<line x1="{cursor_x}" y1="10" x2="{cursor_x}" y2="190" stroke="#3B82F6" stroke-width="1.5" />')

# Compile SVG
svg_content = f'<svg viewBox="0 0 {svg_w} {svg_h}" width="100%">{"".join(svg_blocks)}</svg>'

# Render Waveform
st.markdown('<div class="pipeline-step">Physical Waveform Arbitration Trace (Shared Open-Drain Bus)</div>', unsafe_allow_html=True)
with st.container():
    st.markdown('<div class="panel-box" style="margin-bottom: 0.5rem;">', unsafe_allow_html=True)
    st.markdown(f'<div style="background:#0F172A; padding:0; overflow-x:auto;">{svg_content}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ====================================================
# LIVE LOGS AND ARBITRATION STATES
# ====================================================
log_col, state_col = st.columns(2)

with log_col:
    st.markdown('<div class="pipeline-step">Bus Logging Terminal</div>', unsafe_allow_html=True)
    
    logs = ["[0.0ms] Multi-Master Sync: Both Master A and Master B pull SDA LOW simultaneously."]
    logs.append("[0.1ms] Both clock generators sync up on the shared SCL line.")
    
    cur_a = True
    cur_b = True
    for i in range(8):
      if step >= i + 1:
        bit_a = bits_a[i] if cur_a else 1
        bit_b = bits_b[i] if cur_b else 1
        shared = actual_sda_bits[i]
        
        logs.append(f"[Bit {7-i}] A drives {bit_a}, B drives {bit_b}. Shared SDA Bus resolves to {shared}.")
        
        if cur_a and lost_step_a == i:
          logs.append("[COLLISION] Master A wrote 1 but sensed LOW on SDA. Master A lost arbitration and backed off.")
          cur_a = False
        if cur_b and lost_step_b == i:
          logs.append("[COLLISION] Master B wrote 1 but sensed LOW on SDA. Master B lost arbitration and backed off.")
          cur_b = False
          
    if step >= 9:
      logs.append("[SUCCESS] Arbitration phase complete. Single active master owns the bus trace.")

    st.markdown(f'<div class="terminal-box">{"<br>".join(logs)}</div>', unsafe_allow_html=True)

with state_col:
    st.markdown('<div class="pipeline-step">Arbitration States</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="panel-box" style="height: 200px; margin:0; display:flex; flex-direction:column; justify-content:center; gap:0.5rem;">', unsafe_allow_html=True)
        
        status_a_html = '<span style="color:#10B981;font-weight:bold;">Active / Won</span>' if lost_step_a == -1 else f'<span style="color:#EF6868;">Lost (Backed off at Bit {7-lost_step_a})</span>'
        status_b_html = '<span style="color:#10B981;font-weight:bold;">Active / Won</span>' if lost_step_b == -1 else f'<span style="color:#EF6868;">Lost (Backed off at Bit {7-lost_step_b})</span>'
        
        st.markdown(f"""
        <div style="font-family:monospace; font-size:0.85rem;">
            <div style="margin-bottom:0.75rem;">
                <span style="color:#64748B; font-size:0.65rem; display:block;">MASTER A STATE</span>
                <span>{status_a_html}</span>
            </div>
            <div>
                <span style="color:#64748B; font-size:0.65rem; display:block;">MASTER B STATE</span>
                <span>{status_b_html}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

# ====================================================
# ANIMATION LOOP DRIVER
# ====================================================
if st.session_state.arb_animating:
    if st.session_state.arb_anim_step < 9:
        time.sleep(0.18)
        st.session_state.arb_anim_step += 1
        st.rerun()
    else:
        st.session_state.arb_animating = False
        st.rerun()
