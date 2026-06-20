import streamlit as st
import time

# Set page config
st.set_page_config(
    page_title="PrajnaEdge - I2C: The Shared Bus",
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
        height: 200px;
        overflow-y: auto;
        line-height: 1.5;
        color: #A5F3FC;
    }
</style>
""", unsafe_allow_html=True)

st.title("EdgeCase: The Shared Bus")
st.subheader("I2C Protocol Signaling, Addressing & Handshakes")
st.caption("Select a transaction type and toggle device presence to watch I2C start/stop framing and ACK/NACK verification in real-time.")

# Initialize Session State
if "i2c_op" not in st.session_state:
    st.session_state.i2c_op = "temp"
if "i2c_ack" not in st.session_state:
    st.session_state.i2c_ack = True
if "i2c_animating" not in st.session_state:
    st.session_state.i2c_animating = False
if "i2c_anim_step" not in st.session_state:
    st.session_state.i2c_anim_step = 22

# ====================================================
# CONFIGURATION PANEL
# ====================================================
st.markdown('<div class="pipeline-step">Transaction Setup</div>', unsafe_allow_html=True)
with st.container():
    st.markdown('<div class="panel-box">', unsafe_allow_html=True)
    op_col, presence_col, mode_col = st.columns([1.5, 1.5, 1])
    
    with op_col:
        st.markdown('<div class="panel-title" style="color:#3B82F6;">Target Peripheral Operation</div>', unsafe_allow_html=True)
        op_sel = st.selectbox(
            "Transaction Select",
            ["temp", "eeprom", "oled"],
            format_func=lambda x: {
                "temp": "Read Temp Sensor (Address 0x48)",
                "eeprom": "Write EEPROM (Address 0x50, Data 0x3F)",
                "oled": "Write OLED Display (Address 0x3C, Cmd 0xAF)"
            }[x],
            key="sb_op"
        )
        st.session_state.i2c_op = op_sel

    with presence_col:
        st.markdown('<div class="panel-title" style="color:#FFF;">Device Presence</div>', unsafe_allow_html=True)
        ack_active = st.checkbox("Target Device Responding (ACK)", value=st.session_state.i2c_ack, key="cb_ack")
        st.session_state.i2c_ack = ack_active
        st.caption("Uncheck to simulate NACK error (e.g. device is missing or powered off).")

    with mode_col:
        st.markdown('<div class="panel-title" style="color:#10B981;">Physical Bus Mode</div>', unsafe_allow_html=True)
        st.markdown('<div class="agreement-item agreement-ok" style="font-weight:bold;text-align:center;">Wired-AND Open-Drain Bus Active</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# Parse parameters
addr = 0x48
rwb = 1
data_byte = 0x2C
desc = ""
if st.session_state.i2c_op == "temp":
    addr = 0x48
    rwb = 1
    data_byte = 0x2C
    desc = "Instruction: i2c_read(0x48) -> Read temperature register (expect 0x2C)"
elif st.session_state.i2c_op == "eeprom":
    addr = 0x50
    rwb = 0
    data_byte = 0x3F
    desc = "Instruction: i2c_write(0x50, 0x3F) -> Write data byte 0x3F to EEPROM memory address"
elif st.session_state.i2c_op == "oled":
    addr = 0x3C
    rwb = 0
    data_byte = 0xAF;
    desc = "Instruction: i2c_write(0x3C, 0xAF) -> Write command byte 0xAF to OLED graphics controller"

# ====================================================
# SYSTEM CONTROLS
# ====================================================
st.markdown('<div class="pipeline-step">System Controls</div>', unsafe_allow_html=True)
with st.container():
    st.markdown('<div class="panel-box">', unsafe_allow_html=True)
    c_desc, c_btn = st.columns([3, 1])
    with c_desc:
        st.markdown(f'<div style="font-family:monospace;font-size:0.85rem;color:#FFF;height:38px;display:flex;align-items:center;">{desc}</div>', unsafe_allow_html=True)
    with c_btn:
        transmit_clicked = st.button("TRANSMIT", use_container_width=True)
        if transmit_clicked:
            st.session_state.i2c_animating = True
            st.session_state.i2c_anim_step = 0
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# Setup bit arrays
addr_bits = [(addr >> b) & 1 for b in range(6, -1, -1)]
rw_bit = rwb
slave_ack_bit = 0 if st.session_state.i2c_ack else 1
data_bits = [(data_byte >> b) & 1 for b in range(7, -1, -1)]
master_ack_bit = 0

step = st.session_state.i2c_anim_step
is_responding = st.session_state.i2c_ack
total_pulses = 18 if is_responding else 9

# SCL rising edge coordinates for sampling ticks
x_edges = [120 + p * 35 for p in range(total_pulses)]

# ====================================================
# SVG WAVEFORMS
# ====================================================
svg_w = 920
svg_h = 180
pad_left = 80
scl_y_high = 45
scl_y_low = 65
sda_y_high = 105
sda_y_low = 125

svg_blocks = []

# SCL Clock Waveform
scl_path = f"M 0,{scl_y_high} L 100,{scl_y_high}"
if step > 0:
    scl_path += f" L 120,{scl_y_high}"
    for p in range(total_pulses):
        xs = x_edges[p]
        xm = xs + 17.5
        xe = xs + 35
        scl_path += f" L {xs},{scl_y_low} L {xm},{scl_y_low} L {xm},{scl_y_high} L {xe},{scl_y_high}"
    scl_path += f" L {svg_w},{scl_y_high}"
else:
    scl_path += f" L {svg_w},{scl_y_high}"
svg_blocks.append(f'<path d="{scl_path}" fill="none" stroke="#3B82F6" stroke-width="2" />')
svg_blocks.append(f'<text x="{pad_left - 15}" y="{scl_y_low - 2}" fill="#3B82F6" font-family="monospace" font-size="8" text-anchor="end">SCL</text>')

# SDA Data Waveform
sda_path = f"M 0,{sda_y_high}"
if step > 0:
    # START condition
    sda_path += f" L 100,{sda_y_high} L 100,{sda_y_low} L 120,{sda_y_low}"
    
    current_sda_val = 0
    for p in range(total_pulses):
        xs = x_edges[p]
        xe = xs + 35
        
        val = 1
        if p < 7:
            val = addr_bits[p]
        elif p == 7:
            val = rw_bit
        elif p == 8:
            val = slave_ack_bit
        elif p < 17:
            val = data_bits[p - 9]
        elif p == 17:
            val = master_ack_bit
            
        y_val = sda_y_high if val == 1 else sda_y_low
        sda_path += f" L {xs},{y_val} L {xe},{y_val}"
        current_sda_val = val
        
    # STOP condition
    stop_x_start = 120 + total_pulses * 35 + 10
    stop_x_end = stop_x_start + 15
    stop_y_val = sda_y_high if current_sda_val == 1 else sda_y_low
    sda_path += f" L {stop_x_start},{stop_y_val} L {stop_x_start},{sda_y_low} L {stop_x_end},{sda_y_high} L {svg_w},{sda_y_high}"
else:
    sda_path += f" L {svg_w},{sda_y_high}"
svg_blocks.append(f'<path d="{sda_path}" fill="none" stroke="#10B981" stroke-width="2" />')
svg_blocks.append(f'<text x="{pad_left - 15}" y="{sda_y_low - 2}" fill="#10B981" font-family="monospace" font-size="8" text-anchor="end">SDA</text>')

# Draw Sampling Ticks
for p in range(total_pulses):
    if step >= p + 2:
        xs = x_edges[p] + 17.5
        val = 1
        if p < 7:
            val = addr_bits[p]
        elif p == 7:
            val = rw_bit
        elif p == 8:
            val = slave_ack_bit
        elif p < 17:
            val = data_bits[p - 9]
        elif p == 17:
            val = master_ack_bit

        color = "#EF6868" if (p == 8 and not is_responding) else "#E2E8F0"
        svg_blocks.append(f'<line x1="{xs}" y1="35" x2="{xs}" y2="145" stroke="{color}" stroke-dasharray="2,2" stroke-width="0.8" />')
        svg_blocks.append(f'<circle cx="{xs}" cy="{scl_y_high}" r="2.5" fill="#3B82F6" />')
        svg_blocks.append(f'<circle cx="{xs}" cy="{sda_y_high if val == 1 else sda_y_low}" r="3" fill="{color}" stroke="#0F172A" />')
        
        label = str(val)
        if p == 8: label = "ACK" if val == 0 else "NACK"
        if p == 17: label = "ACK"
        svg_blocks.append(f'<text x="{xs}" y="156" fill="{color}" font-family="monospace" font-size="7" text-anchor="middle" font-weight="bold">{label}</text>')

# Cursor
if st.session_state.i2c_animating and step <= total_pulses + 2:
    cursor_x = 100
    if step == 1: cursor_x = 100
    elif step >= 2 and step <= total_pulses + 1:
        cursor_x = x_edges[step - 2] + 17.5
    else:
        cursor_x = 120 + total_pulses * 35 + 15
    svg_blocks.append(f'<line x1="{cursor_x}" y1="15" x2="{cursor_x}" y2="155" stroke="#3B82F6" stroke-width="1.5" />')

# Compile SVG
svg_content = f'<svg viewBox="0 0 {svg_w} {svg_h}" width="100%">{"".join(svg_blocks)}</svg>'

# Render Waveform
st.markdown('<div class="pipeline-step">Physical Waveform Trace (Shared SDA / SCL Lines)</div>', unsafe_allow_html=True)
with st.container():
    st.markdown('<div class="panel-box" style="margin-bottom: 0.5rem;">', unsafe_allow_html=True)
    st.markdown(f'<div style="background:#0F172A; padding:0; overflow-x:auto;">{svg_content}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.caption("I2C wire traces: START and STOP signaling on SDA (while SCL is HIGH), clock pulses on SCL, and data bits sampled on SCL rising edges.")

# ====================================================
# LIVE LOGS AND DATA RECOVERY OUTCOME
# ====================================================
log_col, out_col = st.columns(2)

with log_col:
    st.markdown('<div class="pipeline-step">Protocol Transaction Log</div>', unsafe_allow_html=True)
    
    logs = ["[0.0ms] Bus Idle. SDA and SCL pulled HIGH via resistors."]
    if step >= 1:
      logs.append("[0.2ms] START Condition: SDA pulled LOW while SCL is HIGH.")
    for p in range(total_pulses):
      if step >= p + 2:
        if p < 7:
          logs.append(f"[Address Bit {6 - p}] Master writes address bit -> SDA = {addr_bits[p]}. sampled on SCL rise.")
        elif p == 7:
          logs.append(f"[Read/Write] Master writes direction bit -> SDA = {rw_bit} ({'Read' if rw_bit == 1 else 'Write'}).")
        elif p == 8:
          if is_responding:
            logs.append("[9th Clock] Handshake: Target slave pulls SDA LOW (ACK). Address verified.")
          else:
            logs.append("[9th Clock] Handshake: SDA remains HIGH (NACK). No responding slave detected at address!")
        elif p < 17:
          bit_idx = p - 9
          sender = "Slave" if rwb == 1 else "Master"
          logs.append(f"[Data Bit {7 - bit_idx}] {sender} drives SDA = {data_bits[bit_idx]}. sampled on SCL rise.")
        elif p == 17:
          receiver = "Master" if rwb == 1 else "Slave"
          logs.append(f"[Data Handshake] {receiver} pulls SDA LOW (ACK) to confirm byte receipt.")
          
    if step >= 20 or (step >= 11 and not is_responding):
      if not is_responding:
        logs.append("[2.2ms] Aborting transaction due to NACK.")
      logs.append("[STOP Condition] SDA pulled LOW->HIGH while SCL is HIGH. Bus released.")

    st.markdown(f'<div class="terminal-box">{"<br>".join(logs)}</div>', unsafe_allow_html=True)

with out_col:
    st.markdown('<div class="pipeline-step">Data Recovery Outcome</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="panel-box" style="height: 200px; margin:0; display:flex; flex-direction:column; justify-content:center; gap:0.5rem;">', unsafe_allow_html=True)
        
        # Shift Register Preview
        rx_register_bits = ["_"] * 8
        if step >= 2:
            if step <= 9:
                for idx in range(step - 1):
                    rx_register_bits[idx] = str(addr_bits[idx])
            elif step == 10:
                for idx in range(7): rx_register_bits[idx] = str(addr_bits[idx])
                rx_register_bits[7] = str(rw_bit)
            elif step >= 11 and step <= 19:
                for idx in range(step - 11):
                    rx_register_bits[idx] = str(data_bits[idx])
            else:
                for idx in range(8): rx_register_bits[idx] = str(data_bits[idx])
                
        cells_html = []
        for bit in rx_register_bits:
            cls = "register-cell"
            if bit != "_":
                cls += " fifo-active-rx" if is_responding else " fifo-active"
            cells_html.append(f"""
            <div class="{cls}" style="display:inline-block; margin-right:0.25rem;">
                <div class="register-label">D</div>
                <div class="register-val">{bit}</div>
            </div>
            """)
            
        st.markdown('<div style="font-family:monospace; font-size:0.75rem; color:#64748B; text-transform:uppercase;">Shift Register (Input Buffer):</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="register-container" style="margin:0;">{"".join(cells_html)}</div>', unsafe_allow_html=True)
        
        recovered_str = "..."
        if step >= 20:
            recovered_str = "Address Match! Target responding. Recovered status: Success."
        elif step >= 11 and not is_responding:
            recovered_str = f"ERROR: Not Acknowledged (NACK). Address 0x{addr:02X} is non-existent."
            
        st.markdown(f"""
        <div style="font-family:monospace; margin-top:0.4rem; font-size:0.85rem;">
            <div>
                <span style="color:#64748B; font-size:0.65rem; display:block;">TARGET ADDRESS</span>
                <span style="font-weight:bold; color:#FFF;">0x{addr:02X} ({'READ' if rwb == 1 else 'WRITE'})</span>
            </div>
            <div style="margin-top:0.4rem;">
                <span style="color:#64748B; font-size:0.65rem; display:block;">TRANSACTION STATUS</span>
                <span style="font-weight:bold; color:{'#10B981' if is_responding else '#EF6868'};">{recovered_str}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

# ====================================================
# ANIMATION LOOP DRIVER
# ====================================================
if st.session_state.i2c_animating:
    max_steps = 22 if is_responding else 12
    if st.session_state.i2c_anim_step < max_steps:
        time.sleep(0.15)
        st.session_state.i2c_anim_step += 1
        st.rerun()
    else:
        st.session_state.i2c_animating = False
        st.rerun()
