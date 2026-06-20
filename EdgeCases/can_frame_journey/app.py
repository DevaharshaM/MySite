import streamlit as st
import time

# Set page config
st.set_page_config(
    page_title="PrajnaEdge - CAN: The Journey of a Frame",
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
    .terminal-box {
        background: #0F172A;
        border: 1px solid rgba(148, 163, 184, 0.12);
        border-radius: 8px;
        padding: 0.8rem;
        font-family: monospace;
        font-size: 0.75rem;
        height: 220px;
        overflow-y: auto;
        line-height: 1.5;
        color: #A5F3FC;
    }
    .stepper-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1.5rem;
        padding: 0.5rem 0;
    }
    .step-circle {
        width: 28px;
        height: 28px;
        border-radius: 50%;
        border: 2px solid #64748B;
        display: flex;
        align-items: center;
        justify-content: center;
        font-family: monospace;
        font-size: 0.75rem;
        font-weight: bold;
        color: #64748B;
        background-color: #0F172A;
    }
    .step-active {
        border-color: #3B82F6 !important;
        color: #3B82F6 !important;
    }
    .step-done {
        border-color: #10B981 !important;
        color: #10B981 !important;
    }
    .step-line {
        flex-grow: 1;
        height: 2px;
        background-color: rgba(148, 163, 184, 0.12);
        margin: 0 4px;
    }
    .line-done {
        background-color: #10B981 !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("EdgeCase: The Journey of a CAN Frame")
st.subheader("CAN Controller Message Pipeline Simulator")
st.caption("Follow a CAN frame step-by-step from the application layer, through configuration registers, Message RAM mapping, framing, physical transmission, and final delivery.")

# Initialize Session State
if "jf_id" not in st.session_state:
    st.session_state.jf_id = "0x1F4"
if "jf_data" not in st.session_state:
    st.session_state.jf_data = "0xDE 0xAD 0xBE 0xEF"
if "jf_animating" not in st.session_state:
    st.session_state.jf_animating = False
if "jf_step" not in st.session_state:
    st.session_state.jf_step = 20

# ====================================================
# CONFIGURATION PANEL
# ====================================================
st.markdown('<div class="pipeline-step">Frame Settings</div>', unsafe_allow_html=True)
with st.container():
    st.markdown('<div class="panel-box">', unsafe_allow_html=True)
    c1, c2 = st.columns([1, 1])
    
    with c1:
        st.markdown('<div class="panel-title" style="color:var(--blue);">Message Identifier</div>', unsafe_allow_html=True)
        val_id = st.text_input("ID (Hex)", value="0x1F4", key="txt_jf_id")
        st.session_state.jf_id = val_id
        
    with c2:
        st.markdown('<div class="panel-title" style="color:#10B981;">Data Payload</div>', unsafe_allow_html=True)
        val_data = st.text_input("Bytes (Hex, space-separated)", value="0xDE 0xAD 0xBE 0xEF", key="txt_jf_data")
        st.session_state.jf_data = val_data

    st.markdown('</div>', unsafe_allow_html=True)

# Stages definition
stages = [
    { "title": "Application", "desc": "The software application calls the driver function: `can_transmit(0x1F4, [0xDE, 0xAD, 0xBE, 0xEF])`. The core processor prepares to hand over control." },
    { "title": "CAN Controller", "desc": "The driver writes the transmit request command to the CAN Controller peripheral register (TXBAR - Transmit Buffer Add Request register), setting up transmission flags." },
    { "title": "Message RAM", "desc": "The peripheral writes the frame description into a dedicated **Message RAM** partition. *Connection to 'The Hidden Geography of Firmware'*: On microcontrollers like STM32H7, Message RAM sits in a specific SRAM block. A misalignment in the register base offset triggers a hardware bus fault or silent frame drops." },
    { "title": "Frame Builder", "desc": "The CAN controller IP packages the identifier, DLC (Data Length Code = 4), and the hex payload into a structured serial frame, ready for physical bitwise streaming." },
    { "title": "Arbitration", "desc": "The transceiver checks if the bus is idle, then asserts SOF and transmits the 11 ID bits (00111110100) onto the bus, listening to ensure no higher-priority message collides." },
    { "title": "Bit Stuffing", "desc": "As bits flow, the hardware controller monitors the stream. If it detects five consecutive 1s or 0s, it automatically inserts an opposite bit (stuff bit) to keep the receiver clocks synchronized." },
    { "title": "CRC Generator", "desc": "The hardware calculates a 15-bit Cyclic Redundancy Check (CRC) over the address and payload, appending the checksum to the frame for error validation." },
    { "title": "Differential Bus", "desc": "The CAN transceiver drives the physical twisted-pair wire. Logic 0 pushes CANH to 3.5V and CANL to 1.5V (Dominant). Logic 1 leaves both lines floating at 2.5V (Recessive)." },
    { "title": "Receiving Node", "desc": "The receiving transceiver senses the differential voltage. Validating the CRC, it overrides the ACK slot with a dominant 0 to acknowledge correct delivery." },
    { "title": "App Delivery", "desc": "The receiving CAN controller copies the received payload from its FIFO Message RAM buffer to CPU registers, triggering an RX interrupt so the destination application can process the data." }
]

step = st.session_state.jf_step

# ====================================================
# PIPELINE STEPPER DISPLAY
# ====================================================
st.markdown('<div class="pipeline-step">Pipeline Progress</div>', unsafe_allow_html=True)

stepper_parts = []
for i in range(10):
    active_class = ""
    if i == step:
        active_class = "step-active"
    elif i < step:
        active_class = "step-done"
        
    bullet = "✓" if i < step else str(i + 1)
    
    stepper_parts.append(f'<div class="step-circle {active_class}" title="{stages[i]["title"]}">{bullet}</div>')
    if i < 9:
        line_class = "line-done" if i < step else ""
        stepper_parts.append(f'<div class="step-line {line_class}"></div>')

stepper_html = f'<div class="stepper-container" style="background:#1E293B; border-radius:8px; border:1px solid rgba(148, 163, 184, 0.12); padding:1rem 1.5rem;">' + "".join(stepper_parts) + '</div>'
st.markdown(stepper_html, unsafe_allow_html=True)

# ====================================================
# DETAILED VIEW AND LOGS
# ====================================================
detail_col, log_col = st.columns([1, 1.2])

with detail_col:
    st.markdown('<div class="pipeline-step">Current Stage Mechanics</div>', unsafe_allow_html=True)
    if step < 10:
        s = stages[step]
        st.markdown(f"""
        <div class="panel-box" style="min-height:220px;">
            <div style="font-family:'Syne',sans-serif; font-size:1.1rem; font-weight:bold; color:#FFFFFF; margin-bottom:0.5rem;">{step+1}. {s['title']}</div>
            <p style="font-size:0.85rem; color:#CBD5E1; line-height:1.6;">{s['desc']}</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="panel-box" style="min-height:220px; display:flex; flex-direction:column; justify-content:center; align-items:center; text-align:center;">
            <div style="font-family:'Syne',sans-serif; font-size:1.2rem; font-weight:bold; color:#10B981; margin-bottom:0.5rem;">✓ Transaction Finished</div>
            <p style="font-size:0.85rem; color:#64748B;">Click TRANSMIT to run a new message pipeline simulation.</p>
        </div>
        """, unsafe_allow_html=True)

# Build Logs
log_lines = [f"[{time.strftime('%H:%M:%S', time.localtime())}] System idle. Ready for transmit."]
if step <= 10:
    log_lines = [f"[{time.strftime('%H:%M:%S', time.localtime())}] Transmit sequence started."]
    for idx in range(min(step + 1, 10)):
        s_title = stages[idx]['title']
        t_str = time.strftime('%H:%M:%S', time.localtime())
        log_line = f"[{t_str}] Stage {idx+1}: {s_title} - "
        
        if idx == 0: log_line += f"Preparing packet ID {st.session_state.jf_id}, payload [{st.session_state.jf_data}]"
        elif idx == 2: log_line += "Wrote descriptor boundaries to CAN Message RAM"
        elif idx == 4: log_line += "Starting bit-arbitration with ID bits"
        elif idx == 7: log_line += "Driving physical lines CANH/CANL"
        elif idx == 8: log_line += "ACK assertion detected (Dominant 0 in slot)"
        else: log_line += "OK"
        
        log_lines.append(log_line)

if step >= 10:
    log_lines.append(f"[{time.strftime('%H:%M:%S', time.localtime())}] [SYSTEM] Frame transaction completed successfully.")

with log_col:
    st.markdown('<div class="pipeline-step">Controller Signal Log</div>', unsafe_allow_html=True)
    log_html = "".join([f"<div>{l}</div>" for l in log_lines])
    st.markdown(f'<div class="terminal-box">{log_html}</div>', unsafe_allow_html=True)

# System Controls
st.markdown('<div style="margin-top:1rem; display:flex; justify-content:flex-end;">', unsafe_allow_html=True)
c_desc_empty, c_btn_run = st.columns([3, 1])
with c_btn_run:
    transmit_clicked = st.button("TRANSMIT", use_container_width=True)
    if transmit_clicked:
        st.session_state.jf_animating = True
        st.session_state.jf_step = 0
        st.rerun()

# Driver loop
if st.session_state.jf_animating and step < 10:
    time.sleep(2.0)
    st.session_state.jf_step += 1
    st.rerun()
elif step >= 10:
    st.session_state.jf_animating = False
