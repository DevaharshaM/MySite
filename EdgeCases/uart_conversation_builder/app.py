import streamlit as st
import time

# Set page config
st.set_page_config(
    page_title="PrajnaEdge - Build a UART Conversation",
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
    .code-display {
        font-family: monospace;
        background: #0F172A;
        padding: 0.6rem 1rem;
        border-radius: 6px;
        border: 1px solid rgba(148, 163, 184, 0.08);
        font-size: 1.1rem;
        color: #A5F3FC;
    }
    .code-highlight {
        color: #FFFFFF;
        background: rgba(59, 130, 246, 0.3);
        padding: 0.1rem 0.3rem;
        border-radius: 3px;
        border-bottom: 2px solid #3B82F6;
        font-weight: bold;
    }
    .text-corrupted {
        color: #EF6868;
        font-weight: bold;
        background: rgba(239, 68, 68, 0.15);
        padding: 0.1rem 0.3rem;
        border-radius: 3px;
        border: 1px dashed rgba(239, 68, 68, 0.3);
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
    .fifo-container {
        display: flex;
        gap: 0.4rem;
        margin-top: 0.5rem;
    }
    .fifo-block {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 38px;
        height: 38px;
        border: 1px solid rgba(148, 163, 184, 0.15);
        border-radius: 4px;
        background: #0F172A;
        font-family: monospace;
        font-size: 1rem;
        font-weight: bold;
        color: #94A3B8;
    }
    .fifo-active {
        border-color: #3B82F6;
        background: rgba(59, 130, 246, 0.1);
        color: #FFFFFF;
        box-shadow: 0 0 8px rgba(59, 130, 246, 0.2);
    }
    .fifo-active-rx {
        border-color: #10B981;
        background: rgba(16, 185, 129, 0.1);
        color: #FFFFFF;
        box-shadow: 0 0 8px rgba(16, 185, 129, 0.2);
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
    .flow-step {
        display: inline-block;
        font-family: monospace;
        font-size: 0.8rem;
        padding: 0.25rem 0.5rem;
        background: #0F172A;
        border: 1px solid rgba(148, 163, 184, 0.1);
        border-radius: 4px;
        margin-right: 0.4rem;
        margin-bottom: 0.4rem;
    }
</style>
""", unsafe_allow_html=True)

st.title("EdgeCase: The Journey of a Byte")
st.subheader("What really happens when you send \"Hello\"?")
st.caption("Walk through the hidden layers of registers, serial frames, electrical signals, and sampling points.")

# Initialize Session State
if "message" not in st.session_state:
    st.session_state.message = "Hello"
if "selected_idx" not in st.session_state:
    st.session_state.selected_idx = 0
if "animating" not in st.session_state:
    st.session_state.animating = False
if "current_stage" not in st.session_state:
    st.session_state.current_stage = 10
if "temp_message" not in st.session_state:
    st.session_state.temp_message = "Hello"

# ====================================================
# CONFIGURATION SETTINGS (TX & RX ALWAYS VISIBLE)
# ====================================================
st.markdown('<div class="pipeline-step">System Configurations</div>', unsafe_allow_html=True)
with st.container():
    st.markdown('<div class="panel-box">', unsafe_allow_html=True)
    tx_col, rx_col, agree_col = st.columns([1, 1, 1])
    
    with tx_col:
        st.markdown('<div class="panel-title" style="color:#3B82F6;">Transmitter (TX Contract)</div>', unsafe_allow_html=True)
        tx_baud = st.selectbox("TX Baud Rate", [9600, 19200, 115200], index=0)
        tx_data_bits = st.selectbox("TX Data Bits", [5, 6, 7, 8], index=3)
        tx_parity = st.selectbox("TX Parity", ["None", "Even", "Odd"], index=0)
        tx_stop_bits = st.selectbox("TX Stop Bits", [1, 2], index=0)

    with rx_col:
        st.markdown('<div class="panel-title" style="color:#E2E8F0;">Receiver (RX Contract)</div>', unsafe_allow_html=True)
        rx_baud = st.selectbox("RX Baud Rate", [4800, 9600, 14400, 19200, 115200], index=1)
        rx_data_bits = st.selectbox("RX Data Bits", [5, 6, 7, 8], index=3)
        rx_parity = st.selectbox("RX Parity", ["None", "Even", "Odd"], index=0)
        rx_stop_bits = st.selectbox("RX Stop Bits", [1, 2], index=0)

    with agree_col:
        st.markdown('<div class="panel-title" style="color:#10B981;">Agreement Verification</div>', unsafe_allow_html=True)
        
        # Agreement Logic
        baud_ok = (tx_baud == rx_baud)
        bits_ok = (tx_data_bits == rx_data_bits)
        parity_ok = (tx_parity == rx_parity)
        stops_ok = (tx_stop_bits == rx_stop_bits)
        
        verify_items = [
            ("Baud Rate", baud_ok, f"{tx_baud} vs {rx_baud} bps"),
            ("Data Bits", bits_ok, f"{tx_data_bits} vs {rx_data_bits} bits"),
            ("Parity Check", parity_ok, f"{tx_parity} vs {rx_parity}"),
            ("Stop Bits", stops_ok, f"{tx_stop_bits} vs {rx_stop_bits}")
        ]
        
        for name, ok, desc in verify_items:
            icon = "✓" if ok else "✗"
            cls = "agreement-ok" if ok else "agreement-fail"
            st.markdown(f'<div class="agreement-item {cls}">{icon} {name}: {desc}</div>', unsafe_allow_html=True)
            
    st.markdown('</div>', unsafe_allow_html=True)

# ====================================================
# MESSAGE INPUT & SEND BUTTON
# ====================================================
st.markdown('<div class="pipeline-step">System Controls</div>', unsafe_allow_html=True)
with st.container():
    st.markdown('<div class="panel-box">', unsafe_allow_html=True)
    msg_col, char_col, action_col = st.columns([2, 1, 1])
    
    with msg_col:
        # Tied to st.session_state.temp_message so typing doesn't instantly rerun the pipeline
        message_input = st.text_input("Enter Message (Press Enter/SEND to Transmit)", value=st.session_state.temp_message, max_chars=12)
        st.session_state.temp_message = message_input
        
    with char_col:
        # Show dropdown options for already transmitted message
        char_options = [f"Index {idx}: '{char}'" for idx, char in enumerate(st.session_state.message)]
        # Clamp index
        if st.session_state.selected_idx >= len(char_options):
            st.session_state.selected_idx = 0
        selected_option = st.selectbox("Inspect Byte Details", char_options, index=st.session_state.selected_idx)
        selected_idx = int(selected_option.split(":")[0].split(" ")[1])
        st.session_state.selected_idx = selected_idx
        
        selected_char = st.session_state.message[selected_idx]
        selected_char_code = ord(selected_char)

    with action_col:
        st.markdown('<div style="height: 28px;"></div>', unsafe_allow_html=True)
        send_clicked = st.button("SEND MESSAGE", use_container_width=True)
        
    if send_clicked:
        st.session_state.message = st.session_state.temp_message
        if not st.session_state.message:
            st.session_state.message = " "
        st.session_state.selected_idx = 0
        st.session_state.animating = True
        st.session_state.current_stage = 1
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# Helper function to generate stage badges/glows
def get_stage_style(stage_num):
    is_animating = st.session_state.animating
    curr_stage = st.session_state.current_stage
    
    if is_animating:
        if stage_num < curr_stage:
            return "", ""
        elif stage_num == curr_stage:
            label = '<span style="color:#3B82F6; font-family:monospace; font-size:0.75rem; font-weight:bold; margin-left:1rem; border:1px solid #3B82F6; padding:0.15rem 0.4rem; border-radius:4px; background:rgba(59,130,246,0.1); letter-spacing:0.05em;">PROCESSING...</span>'
            style = "border-color: #3B82F6; box-shadow: 0 0 15px rgba(59, 130, 246, 0.35); background: rgba(59, 130, 246, 0.02);"
            return label, style
        else:
            label = '<span style="color:#64748B; font-family:monospace; font-size:0.75rem; margin-left:1rem;">(WAITING)</span>'
            style = "opacity: 0.15; filter: grayscale(100%); pointer-events: none;"
            return label, style
    else:
        return "", ""

# ====================================================
# STAGE 1: APPLICATION (SOFTWARE VARIABLE)
# ====================================================
label, style = get_stage_style(1)
st.markdown(f'<div class="pipeline-step">Stage 1: Application (Software variable) {label}</div>', unsafe_allow_html=True)
with st.container():
    st.markdown(f'<div class="panel-box" style="{style}">', unsafe_allow_html=True)
    prefix = st.session_state.message[:selected_idx]
    hl_char = f'<span class="code-highlight">{selected_char}</span>'
    suffix = st.session_state.message[selected_idx+1:]
    st.markdown(f'<div class="code-display">uart_write("{prefix}{hl_char}{suffix}");</div>', unsafe_allow_html=True)
    st.caption("The user application requests data transmission. The highlighted character is currently selected for inspection.")
    st.markdown('</div>', unsafe_allow_html=True)

# ====================================================
# STAGE 2: UART DRIVER (HANDOFF)
# ====================================================
label, style = get_stage_style(2)
st.markdown(f'<div class="pipeline-step">Stage 2: UART Driver (Handoff) {label}</div>', unsafe_allow_html=True)
with st.container():
    st.markdown(f'<div class="panel-box" style="{style}">', unsafe_allow_html=True)
    st.markdown(f"""
    <div style="font-family:monospace; font-size:0.8rem; background:#0f172a; padding:0.6rem 1rem; border-radius:6px; border:1px solid rgba(148,163,184,0.08);">
        <span style="color:#64748B;">DRIVER STATE:</span> Pushing byte <span style="color:#3B82F6; font-weight:bold;">0x{selected_char_code:02X}</span> to hardware register
    </div>
    """, unsafe_allow_html=True)
    st.caption("The device driver intercepts the call, verifies if the peripheral is ready, and copies the data byte into the hardware transmitter port.")
    st.markdown('</div>', unsafe_allow_html=True)

# ====================================================
# STAGE 3: TX FIFO (QUEUE BUFFER)
# ====================================================
label, style = get_stage_style(3)
st.markdown(f'<div class="pipeline-step">Stage 3: TX FIFO (Queue buffer) {label}</div>', unsafe_allow_html=True)
with st.container():
    st.markdown(f'<div class="panel-box" style="{style}">', unsafe_allow_html=True)
    fifo_blocks = []
    for idx, char in enumerate(st.session_state.message):
        cls = "fifo-block fifo-active" if idx == selected_idx else "fifo-block"
        fifo_blocks.append(f'<div class="{cls}">{char}</div>')
    st.markdown(f"""
    <div style="font-family:monospace; font-size:0.7rem; color:#64748B; text-transform:uppercase;">Hardware FIFO Buffer:</div>
    <div class="fifo-container">{"".join(fifo_blocks)}</div>
    """, unsafe_allow_html=True)
    st.caption("A hardware memory queue (FIFO) buffers bytes to prevent timing gaps if the CPU is busy with other tasks.")
    st.markdown('</div>', unsafe_allow_html=True)

# ====================================================
# STAGE 4: SERIALIZATION (ASCII & BINARY MAPPING)
# ====================================================
label, style = get_stage_style(4)
st.markdown(f'<div class="pipeline-step">Stage 4: Serialization (ASCII & Binary Mapping) {label}</div>', unsafe_allow_html=True)
with st.container():
    st.markdown(f'<div class="panel-box" style="{style}">', unsafe_allow_html=True)
    char_bin_bits = [int(x) for x in format(selected_char_code, '08b')]
    lsb_bits = [str((selected_char_code >> b) & 1) for b in range(8)]
    st.markdown(f"""
    <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(180px, 1fr)); gap:1rem; font-family:monospace;">
        <div style="background:#0F172A; padding:0.5rem; border-radius:4px; border:1px solid rgba(148,163,184,0.08);">
            <span style="color:#64748B; font-size:0.7rem; display:block;">CHARACTER</span>
            <span style="color:#FFF; font-weight:bold; font-size:1.1rem;">'{selected_char}'</span>
        </div>
        <div style="background:#0F172A; padding:0.5rem; border-radius:4px; border:1px solid rgba(148,163,184,0.08);">
            <span style="color:#64748B; font-size:0.7rem; display:block;">ASCII DECIMAL</span>
            <span style="color:#3B82F6; font-weight:bold; font-size:1.1rem;">{selected_char_code}</span>
        </div>
        <div style="background:#0F172A; padding:0.5rem; border-radius:4px; border:1px solid rgba(148,163,184,0.08);">
            <span style="color:#64748B; font-size:0.7rem; display:block;">BINARY BYTE</span>
            <span style="color:#10B981; font-weight:bold; font-size:1.1rem;">{"".join(map(str, char_bin_bits))}</span>
        </div>
        <div style="background:#0F172A; padding:0.5rem; border-radius:4px; border:1px solid rgba(148,163,184,0.08);">
            <span style="color:#64748B; font-size:0.7rem; display:block;">LSB FIRST ORDER</span>
            <span style="color:#F59E0B; font-weight:bold; font-size:1.1rem;">{" → ".join(lsb_bits)}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.caption("Software concepts translate into discrete physical values (0s and 1s) ordered LSB-first.")
    st.markdown('</div>', unsafe_allow_html=True)

# ====================================================
# STAGE 5: SHIFT REGISTER (PARALLEL-IN SERIAL-OUT)
# ====================================================
label, style = get_stage_style(5)
st.markdown(f'<div class="pipeline-step">Stage 5: Shift Register (Parallel-In Serial-Out) {label}</div>', unsafe_allow_html=True)
with st.container():
    st.markdown(f'<div class="panel-box" style="{style}">', unsafe_allow_html=True)
    cells_html = []
    for b in range(tx_data_bits):
        bit_val = (selected_char_code >> b) & 1
        cells_html.append(f"""
        <div class="register-cell">
            <div class="register-label">D{b}</div>
            <div class="register-val">{bit_val}</div>
        </div>
        """)
    st.markdown(f"""
    <div style="font-family:monospace; font-size:0.7rem; color:#64748B; text-transform:uppercase;">Transmitter Shift Register (PISO):</div>
    <div class="register-container">
        {"".join(cells_html)}
        <div style="display:flex; align-items:center; margin-left:0.5rem; color:#3B82F6; font-weight:bold; font-family:monospace; font-size:0.8rem;">➔ serial out</div>
    </div>
    """, unsafe_allow_html=True)
    st.caption("Data is loaded in parallel from the buffer, then shifted out bit-by-bit onto the electrical trace.")
    st.markdown('</div>', unsafe_allow_html=True)

# ====================================================
# STAGES 6 & 7: PROTOCOL FRAME BUILDER & PHYSICAL WIRE (SVG RENDERED)
# ====================================================
is_animating = st.session_state.animating
curr_stage = st.session_state.current_stage

label6 = ""
label7 = ""
combined_style = ""
highlight_frame = False
highlight_waveform = False

if is_animating:
    if curr_stage < 6:
        label6 = '<span style="color:#64748B; font-family:monospace; font-size:0.75rem; margin-left:1rem;">(WAITING)</span>'
        label7 = '<span style="color:#64748B; font-family:monospace; font-size:0.75rem; margin-left:1rem;">(WAITING)</span>'
        combined_style = "opacity: 0.15; filter: grayscale(100%); pointer-events: none;"
    elif curr_stage == 6:
        label6 = '<span style="color:#3B82F6; font-family:monospace; font-size:0.75rem; font-weight:bold; margin-left:1rem; border:1px solid #3B82F6; padding:0.15rem 0.4rem; border-radius:4px; background:rgba(59,130,246,0.1);">PROCESSING...</span>'
        label7 = '<span style="color:#64748B; font-family:monospace; font-size:0.75rem; margin-left:1rem;">(WAITING)</span>'
        combined_style = "border-color: #3B82F6; box-shadow: 0 0 15px rgba(59, 130, 246, 0.35); background: rgba(59, 130, 246, 0.02);"
        highlight_frame = True
    elif curr_stage == 7:
        label7 = '<span style="color:#3B82F6; font-family:monospace; font-size:0.75rem; font-weight:bold; margin-left:1rem; border:1px solid #3B82F6; padding:0.15rem 0.4rem; border-radius:4px; background:rgba(59,130,246,0.1);">PROCESSING...</span>'
        combined_style = "border-color: #3B82F6; box-shadow: 0 0 15px rgba(59, 130, 246, 0.35); background: rgba(59, 130, 246, 0.02);"
        highlight_waveform = True

# Build TX frame bits info
char_bits = []
for b in range(tx_data_bits):
    char_bits.append((selected_char_code >> b) & 1)

tx_parity_bit = None
if tx_parity != "None":
    bit_sum = sum(char_bits)
    if tx_parity == "Even":
        tx_parity_bit = bit_sum % 2
    else:
        tx_parity_bit = 0 if bit_sum % 2 != 0 else 1

# List of frame slots for drawing
tx_frame_bits = []
tx_frame_bits.append({"type": "idle", "label": "IDLE", "val": 1, "desc": "Line free"})
tx_frame_bits.append({"type": "start", "label": "START", "val": 0, "desc": "Frame Alert"})
for b in range(tx_data_bits):
    tx_frame_bits.append({"type": "data", "label": f"D{b}", "val": char_bits[b], "desc": "Payload LSB" if b==0 else ("Payload MSB" if b==tx_data_bits-1 else "Payload bit")})
if tx_parity_bit is not None:
    tx_frame_bits.append({"type": "parity", "label": "PARITY", "val": tx_parity_bit, "desc": "Error Check"})
for s in range(tx_stop_bits):
    tx_frame_bits.append({"type": "stop", "label": "STOP", "val": 1, "desc": "Frame End"})
tx_frame_bits.append({"type": "idle", "label": "IDLE", "val": 1, "desc": "Line free"})

# Generate TX states array
tx_states = [b["val"] for b in tx_frame_bits]

# Emulate RX sampling
T_tx = 1.0
T_rx = tx_baud / rx_baud
rx_sample_count = 1 + rx_data_bits + (1 if rx_parity != "None" else 0) + rx_stop_bits
rx_samples_info = []

for i in range(rx_sample_count):
    rx_time = (0.5 + i) * T_rx
    tx_time = 1.0 + rx_time  # physical time offset (Start falling edge begins at physical index 1)
    tx_idx = int(tx_time)
    sampled_val = 1
    if 0 <= tx_idx < len(tx_states):
        sampled_val = tx_states[tx_idx]
    
    # Verify correctness based on original TX states
    correct = True
    if tx_idx >= len(tx_states):
        correct = False # outside boundary
    else:
        if i == 0 and sampled_val != 0:
            correct = False
        elif 1 <= i <= rx_data_bits:
            tx_bit_pos = i - 1
            if tx_bit_pos < tx_data_bits:
                expected_tx_val = char_bits[tx_bit_pos]
            else:
                expected_tx_val = 1
            if sampled_val != expected_tx_val:
                correct = False
        elif i >= 1 + rx_data_bits + (1 if rx_parity != "None" else 0):
            if sampled_val != 1:
                correct = False

    rx_samples_info.append({
        "idx": i,
        "tx_time": tx_time,
        "val": sampled_val,
        "correct": correct
    })

# Draw SVG
svg_w = 900
svg_h = 320
pad_left = 70
pad_right = 30
disp_w = svg_w - pad_left - pad_right
n_slots = len(tx_states)
dx = disp_w / n_slots

colors = {
    "idle": "#475569",
    "start": "#EF4444",
    "data": "#3B82F6",
    "parity": "#F59E0B",
    "stop": "#10B981"
}

svg_blocks = []
blocks_opacity = "0.3" if highlight_waveform else "1.0"
waveform_opacity = "0.3" if highlight_frame else "1.0"
waveform_stroke_width = "4" if highlight_waveform else "2"
waveform_stroke_color = "#3B82F6" if highlight_waveform else "#FFFFFF"

# 1. Draw Frame Blocks
for i, b in enumerate(tx_frame_bits):
    x = pad_left + i * dx
    c = colors[b["type"]]
    stroke_w = "2.5" if (highlight_frame and b["type"] != "idle") else "1.5"
    fill_opacity = "0.15" if highlight_frame else "0.08"
    svg_blocks.append(f"""
    <!-- Block {b["label"]} -->
    <rect x="{x + 2}" y="15" width="{dx - 4}" height="70" rx="4" fill="none" stroke="{c}" stroke-width="{stroke_w}" opacity="{blocks_opacity}" />
    <rect x="{x + 2}" y="15" width="{dx - 4}" height="70" rx="4" fill="{c}" opacity="{fill_opacity if blocks_opacity == "1.0" else "0.02"}" />
    <text x="{x + dx/2}" y="32" fill="#94A3B8" font-family="monospace" font-size="8" text-anchor="middle" font-weight="bold" opacity="{blocks_opacity}">{b["label"]}</text>
    <text x="{x + dx/2}" y="56" fill="{ '#EF6868' if b["val"]==0 else '#10B981' }" font-family="monospace" font-size="18" text-anchor="middle" font-weight="bold" opacity="{blocks_opacity}">{b["val"]}</text>
    <text x="{x + dx/2}" y="76" fill="#64748B" font-family="monospace" font-size="6.5" text-anchor="middle" opacity="{blocks_opacity}">{b["desc"]}</text>
    """)

# 2. Draw Waveform Step Line
path_d = f"M 0,135 L {pad_left},135"
for i in range(n_slots):
    val = tx_states[i]
    prev_val = tx_states[i-1] if i > 0 else 1
    y = 135 if val == 1 else 175
    x_start = pad_left + i * dx
    x_end = pad_left + (i + 1) * dx
    if val != prev_val:
        y_prev = 135 if prev_val == 1 else 175
        path_d += f" L {x_start},{y_prev} L {x_start},{y}"
    path_d += f" L {x_end},{y}"
path_d += f" L {svg_w},135"

svg_blocks.append(f"""
<!-- Waveform Signal -->
<path d="{path_d}" fill="none" stroke="{waveform_stroke_color}" stroke-width="{waveform_stroke_width}" opacity="{waveform_opacity}" />
<text x="{pad_left - 8}" y="139" fill="#64748B" font-family="monospace" font-size="8" text-anchor="end" opacity="{waveform_opacity}">HIGH (3.3V)</text>
<text x="{pad_left - 8}" y="179" fill="#64748B" font-family="monospace" font-size="8" text-anchor="end" opacity="{waveform_opacity}">LOW (0V)</text>
""")

# Draw Slot Dividers & Grid lines
for i in range(n_slots + 1):
    x = pad_left + i * dx
    svg_blocks.append(f'<line x1="{x}" y1="15" x2="{x}" y2="195" stroke="#334155" stroke-dasharray="1,4" stroke-width="0.75" />')

# 3. Draw RX Sampling Timeline (only visible at Stage 8 or higher)
rx_visible = not (is_animating and curr_stage < 8)

if rx_visible:
    svg_blocks.append(f"""
    <!-- RX Axis line -->
    <line x1="{pad_left}" y1="235" x2="{svg_w - pad_right}" y2="235" stroke="#475569" stroke-width="1" />
    <text x="{pad_left - 8}" y="238" fill="#64748B" font-family="monospace" font-size="8" text-anchor="end">RX SAMPLES</text>
    """)

    for s in rx_samples_info:
        x_sample = pad_left + s["tx_time"] * dx
        if x_sample > (svg_w - pad_right):
            continue
        
        y_wave = 135 if s["val"] == 1 else 175
        color = "#3B82F6" if s["correct"] else "#EF6868"
        dash = "2,3" if s["correct"] else "1,1"
        
        svg_blocks.append(f"""
        <!-- Sample S{s["idx"]} -->
        <line x1="{x_sample}" y1="120" x2="{x_sample}" y2="235" stroke="{color}" stroke-dasharray="{dash}" stroke-width="1" />
        <circle cx="{x_sample}" cy="{y_wave}" r="4" fill="{color}" stroke="#0F172A" stroke-width="1" />
        <circle cx="{x_sample}" cy="235" r="3" fill="{color}" />
        <text x="{x_sample}" y="252" fill="{color}" font-family="monospace" font-size="9" text-anchor="middle" font-weight="bold">S{s["idx"]}</text>
        <text x="{x_sample}" y="266" fill="#FFF" font-family="monospace" font-size="9" text-anchor="middle" font-weight="bold">({s["val"]})</text>
        """)

# Combine SVG
svg_content = f"""
<svg viewBox="0 0 {svg_w} {svg_h}" width="100%">
    {"".join(svg_blocks)}
</svg>
"""

# Render combined stage container
st.markdown(f'<div class="pipeline-step">Stage 6: UART Frame Builder (TX Pin state) {label6}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="pipeline-step">Stage 7: Physical Wire (Waveform) {label7}</div>', unsafe_allow_html=True)
with st.container():
    st.markdown(f'<div class="panel-box" style="{combined_style}">', unsafe_allow_html=True)
    st.markdown(f'<div style="background:#0F172A; padding:0; overflow-x:auto;">{svg_content}</div>', unsafe_allow_html=True)
    st.caption("Voltage values on the physical trace directly echo the UART frame contract. Dashed lines illustrate receiver sampling offsets.")
    st.markdown('</div>', unsafe_allow_html=True)

# ====================================================
# STAGE 8: RX PIN & RECEIVER (SAMPLING & DEMODULATION)
# ====================================================
label, style = get_stage_style(8)
st.markdown(f'<div class="pipeline-step">Stage 8: RX Pin & Receiver (Sampling & Demodulation) {label}</div>', unsafe_allow_html=True)
with st.container():
    st.markdown(f'<div class="panel-box" style="{style}">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">Receiver Processing Flow (First Frame Byte)</div>', unsafe_allow_html=True)
    
    # State sequence strings
    flow_steps = []
    
    # Start detection check
    rx_start_val = rx_samples_info[0]["val"]
    if rx_start_val == 0:
        flow_steps.append('<span class="flow-step" style="color:#10B981;">✓ Waiting: Idle line HIGH</span>')
        flow_steps.append('<span class="flow-step" style="color:#10B981;">✓ Start Bit Detected (LOW)</span>')
    else:
        flow_steps.append('<span class="flow-step" style="color:#EF6868;">✗ Waiting: Idle Mismatch</span>')
        flow_steps.append('<span class="flow-step" style="color:#EF6868;">✗ Start Bit Error (HIGH)</span>')

    # Data bits
    rx_data_bits_vals = [s["val"] for s in rx_samples_info[1:1+rx_data_bits]]
    flow_steps.append(f'<span class="flow-step" style="color:#3B82F6;">➔ Sampling {rx_data_bits} Payload Bits: [{",".join(map(str, rx_data_bits_vals))}]</span>')

    # Parity check
    if rx_parity != "None":
        rx_par_idx = 1 + rx_data_bits
        rx_parity_val = rx_samples_info[rx_par_idx]["val"] if rx_par_idx < len(rx_samples_info) else 1
        rx_sum = sum(rx_data_bits_vals)
        expected_rx_par = rx_sum % 2 if rx_parity == "Even" else (0 if rx_sum % 2 != 0 else 1)
        if rx_parity_val == expected_rx_par:
            flow_steps.append(f'<span class="flow-step" style="color:#10B981;">✓ Parity Matched ({rx_parity} = {rx_parity_val})</span>')
        else:
            flow_steps.append(f'<span class="flow-step" style="color:#EF6868;">✗ Parity Error (Sampled {rx_parity_val}, expected {expected_rx_par})</span>')

# Stop bits check
    rx_stop_start_idx = 1 + rx_data_bits + (1 if rx_parity != "None" else 0)
    rx_stop_vals = [s["val"] for s in rx_samples_info[rx_stop_start_idx:rx_stop_start_idx+rx_stop_bits]]
    stops_valid = all(v == 1 for v in rx_stop_vals)
    if stops_valid:
        flow_steps.append(f'<span class="flow-step" style="color:#10B981;">✓ Stop Bit(s) Verified (HIGH)</span>')
    else:
        flow_steps.append(f'<span class="flow-step" style="color:#EF6868;">✗ Framing Error (Stop bit LOW)</span>')

    # Decoded character value
    reconstructed_code = 0
    for b in range(rx_data_bits):
        if b < len(rx_data_bits_vals) and rx_data_bits_vals[b] == 1:
            reconstructed_code |= (1 << b)

    if (not parity_ok) or (not bits_ok) or (not stops_valid) or (rx_start_val != 0):
        flow_steps.append(f'<span class="flow-step" style="background:#EF6868; color:#FFF; font-weight:bold;">➔ Character Corrupted: \'?\'</span>')
    else:
        char_out = chr(reconstructed_code) if 32 <= reconstructed_code <= 126 else '?'
        flow_steps.append(f'<span class="flow-step" style="background:#10B981; color:#0F172A; font-weight:bold;">➔ Character Recovered: \'{char_out}\'</span>')

    st.markdown(" ".join(flow_steps), unsafe_allow_html=True)
    st.caption("The receiver checks timing offsets, decodes the voltage transitions, and validates the parity/stop framing.")
    st.markdown('</div>', unsafe_allow_html=True)

# ====================================================
# STAGE 9: RX FIFO (HARDWARE INPUT BUFFER)
# ====================================================
label, style = get_stage_style(9)
st.markdown(f'<div class="pipeline-step">Stage 9: RX FIFO (Hardware Input buffer) {label}</div>', unsafe_allow_html=True)
with st.container():
    st.markdown(f'<div class="panel-box" style="{style}">', unsafe_allow_html=True)
    
    # Run full message decoding loop
    recovered_chars = []
    has_any_error = False

    for char in st.session_state.message:
        val = ord(char)
        # Serialize under TX parameters
        tx_c_bits = [(val >> b) & 1 for b in range(tx_data_bits)]
        tx_c_par = None
        if tx_parity != "None":
            s_sum = sum(tx_c_bits)
            tx_c_par = s_sum % 2 if tx_parity == "Even" else (0 if s_sum % 2 != 0 else 1)
        
        tx_c_frame = [0] + tx_c_bits
        if tx_c_par is not None:
            tx_c_frame.append(tx_c_par)
        for _ in range(tx_stop_bits):
            tx_c_frame.append(1)
        
        # Idle pads
        tx_c_full = [1] + tx_c_frame + [1]
        
        # Sample under RX parameters
        rx_c_sampled = []
        for i in range(rx_sample_count):
            rx_time = (0.5 + i) * T_rx
            tx_time = 1.0 + rx_time
            tx_idx = int(tx_time)
            s_val = 1
            if 0 <= tx_idx < len(tx_c_full):
                s_val = tx_c_full[tx_idx]
            rx_c_sampled.append(s_val)

        # Parse RX bits
        rx_c_start = rx_c_sampled[0]
        rx_c_data = rx_c_sampled[1:1+rx_data_bits]
        rx_c_parity_val = rx_c_sampled[1+rx_data_bits] if rx_parity != "None" else None
        
        rx_c_stop_start = 1 + rx_data_bits + (1 if rx_parity != "None" else 0)
        rx_c_stops = rx_c_sampled[rx_c_stop_start:rx_c_stop_start+rx_stop_bits]
        
        # Framing check
        f_err = (rx_c_start != 0) or any(v != 1 for v in rx_c_stops)
        
        # Parity check
        p_err = False
        if rx_parity != "None" and rx_c_parity_val is not None:
            rx_sum = sum(rx_c_data)
            expected_p = rx_sum % 2 if rx_parity == "Even" else (0 if rx_sum % 2 != 0 else 1)
            if rx_c_parity_val != expected_p:
                p_err = True

        if f_err or p_err:
            has_any_error = True
            recovered_chars.append('?')
        else:
            # Reconstruct byte value
            rec_val = 0
            for b in range(rx_data_bits):
                if b < len(rx_c_data) and rx_c_data[b] == 1:
                    rec_val |= (1 << b)
            char_out = chr(rec_val) if 32 <= rec_val <= 126 else '?'
            recovered_chars.append(char_out)

    # Draw RX FIFO queue blocks
    rx_fifo_blocks = []
    for idx, char in enumerate(recovered_chars):
        cls = "fifo-block fifo-active-rx" if idx == selected_idx else "fifo-block"
        if char == '?':
            rx_fifo_blocks.append(f'<div class="{cls}" style="border-color:#EF6868; color:#EF6868; background:rgba(239,68,68,0.08);">?</div>')
        else:
            rx_fifo_blocks.append(f'<div class="{cls}">{char}</div>')

    st.markdown(f"""
    <div style="font-family:monospace; font-size:0.7rem; color:#64748B; text-transform:uppercase;">Receiver FIFO Queue buffer:</div>
    <div class="fifo-container">{"".join(rx_fifo_blocks)}</div>
    """, unsafe_allow_html=True)
    st.caption("Decoded bytes are queued into the receiver FIFO buffer, waiting to be read by the system's driver.")
    st.markdown('</div>', unsafe_allow_html=True)

# ====================================================
# STAGE 10: APPLICATION (RECONSTRUCTED OUTPUT)
# ====================================================
label, style = get_stage_style(10)
st.markdown(f'<div class="pipeline-step">Stage 10: Application (Reconstructed Output) {label}</div>', unsafe_allow_html=True)
with st.container():
    st.markdown(f'<div class="panel-box" style="{style}">', unsafe_allow_html=True)
    
    # Highlight corrupted character indexes
    reconstructed_msg_chars = []
    for idx, char in enumerate(recovered_chars):
        if char == '?':
            reconstructed_msg_chars.append('<span class="text-corrupted">?</span>')
        else:
            reconstructed_msg_chars.append(char)
    reconstructed_message_str = "".join(reconstructed_msg_chars)

    out_col1, out_col2 = st.columns(2)
    with out_col1:
        st.markdown(f'<div style="font-family:monospace; font-size:0.75rem; color:#64748B;">TRANSMITTED MESSAGE:</div>', unsafe_allow_html=True)
        st.markdown(f'<div style="font-size:1.5rem; font-family:monospace; background:#0F172A; padding:0.6rem; border-radius:6px; border:1px solid rgba(148,163,184,0.1); font-weight:bold;">{st.session_state.message}</div>', unsafe_allow_html=True)
    
    with out_col2:
        st.markdown(f'<div style="font-family:monospace; font-size:0.75rem; color:#64748B;">RECOVERED MESSAGE:</div>', unsafe_allow_html=True)
        st.markdown(f'<div style="font-size:1.5rem; font-family:monospace; background:#0F172A; padding:0.6rem; border-radius:6px; border:1px solid rgba(148,163,184,0.1); font-weight:bold;">{reconstructed_message_str}</div>', unsafe_allow_html=True)
        
    st.caption("The software application reads the byte queue, completing the communication loop.")
    st.markdown('</div>', unsafe_allow_html=True)

# ====================================================
# CORE EDUCATIONAL MESSAGE
# ====================================================
st.info("""
**Core Educational Message:**
* UART does not synchronize processors. It synchronizes **expectations**.
* The transmitter and receiver can run at completely independent CPU clock frequencies (e.g. 16 MHz vs 1 GHz).
* As long as they agree on the baud rate, parity, data bits, and stop bits contract, they coordinate timing and reconstruct the serial stream successfully.
""")

# ====================================================
# ANIMATION LOOP DRIVER
# ====================================================
if st.session_state.animating:
    if st.session_state.current_stage < 10:
        time.sleep(0.6)
        st.session_state.current_stage += 1
        st.rerun()
    else:
        st.session_state.animating = False
        st.rerun()
