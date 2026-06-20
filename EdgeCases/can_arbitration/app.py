import streamlit as st
import time

# Set page config
st.set_page_config(
    page_title="PrajnaEdge - CAN: The Conversation of Dominance",
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

st.title("EdgeCase: The Conversation of Dominance")
st.subheader("CAN Bus Bitwise Arbitration Simulator")
st.caption("Configure 11-bit identifiers for Node 1, Node 2, and Node 3 to observe how dominant (0) bits override recessive (1) bits without destroying data.")

# Initialize Session State
if "can_id1" not in st.session_state:
    st.session_state.can_id1 = "0x3F4"
if "can_id2" not in st.session_state:
    st.session_state.can_id2 = "0x3A2"
if "can_id3" not in st.session_state:
    st.session_state.can_id3 = "0x5B1"
if "can_animating" not in st.session_state:
    st.session_state.can_animating = False
if "can_anim_step" not in st.session_state:
    st.session_state.can_anim_step = 20

# ====================================================
# CONFIGURATION PANEL
# ====================================================
st.markdown('<div class="pipeline-step">Identifier Setup</div>', unsafe_allow_html=True)
with st.container():
    st.markdown('<div class="panel-box">', unsafe_allow_html=True)
    c1, c2, c3, status_col = st.columns([1, 1, 1, 1.2])
    
    with c1:
        st.markdown('<div class="panel-title" style="color:#3B82F6;">Node 1 (Engine ECU)</div>', unsafe_allow_html=True)
        val_id1_str = st.text_input("ID 1 (Hex)", value="0x3F4", key="txt_id1")
        st.session_state.can_id1 = val_id1_str
        
    with c2:
        st.markdown('<div class="panel-title" style="color:#EC4899;">Node 2 (ABS Controller)</div>', unsafe_allow_html=True)
        val_id2_str = st.text_input("ID 2 (Hex)", value="0x3A2", key="txt_id2")
        st.session_state.can_id2 = val_id2_str

    with c3:
        st.markdown('<div class="panel-title" style="color:#A855F7;">Node 3 (Body Control)</div>', unsafe_allow_html=True)
        val_id3_str = st.text_input("ID 3 (Hex)", value="0x5B1", key="txt_id3")
        st.session_state.can_id3 = val_id3_str

    # Parse inputs
    def parse_hex(val_str, default_val):
        try:
            clean = val_str.strip()
            if not clean.startswith("0x"):
                clean = "0x" + clean
            parsed = int(clean, 16)
            if parsed < 0 or parsed > 0x7FF:
                return default_val
            return parsed
        except:
            return default_val

    id1 = parse_hex(st.session_state.can_id1, 0x3F4)
    id2 = parse_hex(st.session_state.can_id2, 0x3A2)
    id3 = parse_hex(st.session_state.can_id3, 0x5B1)

    # Convert to 11 bits
    bits1 = [(id1 >> i) & 1 for i in range(10, -1, -1)]
    bits2 = [(id2 >> i) & 1 for i in range(10, -1, -1)]
    bits3 = [(id3 >> i) & 1 for i in range(10, -1, -1)]

    # Calculate arbitration dropouts
    active1, active2, active3 = True, True, True
    lost_step1, lost_step2, lost_step3 = -1, -1, -1
    bus_bits = []

    for i in range(11):
        b1 = bits1[i] if active1 else 1
        b2 = bits2[i] if active2 else 1
        b3 = bits3[i] if active3 else 1
        
        shared_bit = b1 & b2 & b3
        bus_bits.append(shared_bit)

        if active1 and b1 == 1 and shared_bit == 0:
            active1 = False
            lost_step1 = i
        if active2 and b2 == 1 and shared_bit == 0:
            active2 = False
            lost_step2 = i
        if active3 and b3 == 1 and shared_bit == 0:
            active3 = False
            lost_step3 = i

    winner = 1
    if active2: winner = 2
    if active3: winner = 3

    with status_col:
        st.markdown('<div class="panel-title" style="color:#10B981;">Arbitration Status</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="agreement-item agreement-ok" style="font-weight:bold;text-align:center;font-size:0.8rem;">✓ Node {winner} Won.<br>Lowest numerical ID won.</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ====================================================
# SYSTEM CONTROLS
# ====================================================
st.markdown('<div class="pipeline-step">System Controls</div>', unsafe_allow_html=True)
with st.container():
    st.markdown('<div class="panel-box">', unsafe_allow_html=True)
    c_desc, c_btn = st.columns([3, 1])
    with c_desc:
        st.markdown('<div style="font-family:monospace;font-size:0.85rem;color:#FFF;height:38px;display:flex;align-items:center;">Click start to trace the arbitration logic across the nodes.</div>', unsafe_allow_html=True)
    with c_btn:
        arb_transmit_clicked = st.button("START ARBITRATION", use_container_width=True)
        if arb_transmit_clicked:
            st.session_state.can_animating = True
            st.session_state.can_anim_step = 0
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

step = st.session_state.can_anim_step

# ====================================================
# SVG TIMING WAVEFORMS
# ====================================================
svg_w = 950
svg_h = 280
pad_left = 110
y_1 = 35
y_2 = 95
y_3 = 155
y_shared = 225

step_w = (svg_w - pad_left - 40) / 11

svg_blocks = []

# Draw grids
for i in range(12):
    x = pad_left + i * step_w
    svg_blocks.append(f'<line x1="{x}" y1="10" x2="{x}" y2="{svg_h - 30}" stroke="rgba(148, 163, 184, 0.12)" stroke-dasharray="2,2"/>')
    if i < 11:
        svg_blocks.append(f'<text x="{x + step_w/2}" y="{svg_h - 10}" fill="#64748B" font-size="9" text-anchor="middle">Bit {10-i}</text>')

# Rows
rows = [
    {"name": "Node 1 TX", "y": y_1, "color": "#3B82F6", "bits": bits1, "lost": lost_step1},
    {"name": "Node 2 TX", "y": y_2, "color": "#EC4899", "bits": bits2, "lost": lost_step2},
    {"name": "Node 3 TX", "y": y_3, "color": "#A855F7", "bits": bits3, "lost": lost_step3},
    {"name": "Shared Bus", "y": y_shared, "color": "#10B981", "bits": bus_bits, "lost": -1}
]

for r in rows:
    svg_blocks.append(f'<text x="10" y="{r["y"] + 5}" fill="{r["color"]}" font-size="10" font-weight="bold" font-family="sans-serif">{r["name"]}</text>')
    
    # Path
    start_y = r["y"] + (-12 if r["bits"][0] == 1 else 12)
    path_data = f"M {pad_left} {start_y}"
    
    for i in range(11):
        startX = pad_left + i * step_w
        endX = pad_left + (i + 1) * step_w
        
        # If node dropped out, it stops driving and is recessive (1)
        val = r["bits"][i]
        if r["lost"] != -1 and i > r["lost"]:
            val = 1
            
        yVal = r["y"] + (-12 if val == 1 else 12)
        path_data += f" L {startX} {yVal} L {endX} {yVal}"
        
        # Mark dropout point
        if r["lost"] == i and step >= i:
            svg_blocks.append(f'<circle cx="{startX + step_w/2}" cy="{yVal}" r="5" fill="#EF6868"/>')
            svg_blocks.append(f'<text x="{startX + step_w/2}" y="{yVal - 8}" fill="#EF6868" font-size="8" text-anchor="middle" font-weight="bold">LOST</text>')
            
    svg_blocks.append(f'<path d="{path_data}" fill="none" stroke="{r["color"]}" stroke-width="2"/>')

# Cursor
if step < 11:
    cx = pad_left + step * step_w
    svg_blocks.append(f'<rect x="{cx}" y="10" width="{step_w}" height="{svg_h - 40}" fill="rgba(59, 130, 246, 0.08)" stroke="#3B82F6" stroke-dasharray="4,4"/>')

svg_content = f'<svg width="100%" height="{svg_h}" viewBox="0 0 {svg_w} {svg_h}">' + "".join(svg_blocks) + "</svg>"
st.markdown(f'<div class="panel-box" style="padding:0.75rem;background:#0F172A;">{svg_content}</div>', unsafe_allow_html=True)

# ====================================================
# LOGS AND SUMMARY
# ====================================================
log_col, sum_col = st.columns([1.5, 1])

# Build logs
log_lines = ["Initializing CAN arbitration sequence...", "Nodes check for bus idle. Bus is free.", "Simultaneously transmitting SOF (Start of Frame: Dominant 0)..."]
act1, act2, act3 = True, True, True
for i in range(min(step + 1, 11)):
    b1 = bits1[i]
    b2 = bits2[i]
    b3 = bits3[i]
    bus = bus_bits[i]
    
    line = f"Bit {10-i}: [N1: {b1 if act1 else '-'}, N2: {b2 if act2 else '-'}, N3: {b3 if act3 else '-'}] => Bus: {bus}"
    
    drops = []
    if act1 and b1 == 1 and bus == 0:
        act1 = False
        drops.append("N1 lost")
    if act2 and b2 == 1 and bus == 0:
        act2 = False
        drops.append("N2 lost")
    if act3 and b3 == 1 and bus == 0:
        act3 = False
        drops.append("N3 lost")
        
    if drops:
        line += f" | ({', '.join(drops)} - read 0, wrote 1)"
    log_lines.append(line)

if step >= 11:
    log_lines.append(f"Arbitration completed. Node {winner} wins bus control.")

with log_col:
    st.markdown('<div class="pipeline-step">Arbitration Log</div>', unsafe_allow_html=True)
    log_html = "".join([f"<div>{l}</div>" for l in log_lines])
    st.markdown(f'<div class="terminal-box">{log_html}</div>', unsafe_allow_html=True)

with sum_col:
    st.markdown('<div class="pipeline-step">Active States</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="panel-box" style="height:200px; display:flex; flex-direction:column; justify-content:center; gap:0.5rem; margin-bottom:0;">', unsafe_allow_html=True)
        
        s1_class = "agreement-ok" if (lost_step1 == -1 or step < lost_step1) else "agreement-fail"
        s1_txt = "ACTIVE" if (lost_step1 == -1 or step < lost_step1) else "DROPPED OUT"
        
        s2_class = "agreement-ok" if (lost_step2 == -1 or step < lost_step2) else "agreement-fail"
        s2_txt = "ACTIVE" if (lost_step2 == -1 or step < lost_step2) else "DROPPED OUT"
        
        s3_class = "agreement-ok" if (lost_step3 == -1 or step < lost_step3) else "agreement-fail"
        s3_txt = "ACTIVE" if (lost_step3 == -1 or step < lost_step3) else "DROPPED OUT"
        
        st.markdown(f'<div class="agreement-item {s1_class}">Node 1 (Engine ECU): {s1_txt}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="agreement-item {s2_class}">Node 2 (ABS Controller): {s2_txt}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="agreement-item {s3_class}">Node 3 (Body Control): {s3_txt}</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

# Animation driver
if st.session_state.can_animating and step < 11:
    time.sleep(1.2)
    st.session_state.can_anim_step += 1
    st.rerun()
elif step >= 11:
    st.session_state.can_animating = False
