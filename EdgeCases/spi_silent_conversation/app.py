import streamlit as st
import time
import random

# Set page config
st.set_page_config(
    page_title="PrajnaEdge - SPI: The Silent Conversation",
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
        height: 220px;
        overflow-y: auto;
        line-height: 1.5;
        color: #A5F3FC;
    }
</style>
""", unsafe_allow_html=True)

st.title("EdgeCase: The Silent Conversation")
st.subheader("Chip Select Contention & Tri-State Collisions")
st.caption("Toggle individual Slave Chip Select lines to observe normal addressing, floating lines, and physical electrical conflicts on the shared MISO bus.")

# Initialize Session State
if "cs_flash" not in st.session_state:
    st.session_state.cs_flash = False
if "cs_sensor" not in st.session_state:
    st.session_state.cs_sensor = False
if "cs_adc" not in st.session_state:
    st.session_state.cs_adc = False
if "cs_display" not in st.session_state:
    st.session_state.cs_display = False
if "sc_animating" not in st.session_state:
    st.session_state.sc_animating = False
if "sc_anim_step" not in st.session_state:
    st.session_state.sc_anim_step = 20
if "sc_logs" not in st.session_state:
    st.session_state.sc_logs = []

# ====================================================
# CONFIGURATION PANEL (CHIP SELECT CONTROL)
# ====================================================
st.markdown('<div class="pipeline-step">Bus Selection Control</div>', unsafe_allow_html=True)
with st.container():
    st.markdown('<div class="panel-box">', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        st.markdown('<div class="panel-title" style="color:#10B981;">Flash Memory</div>', unsafe_allow_html=True)
        # Active low: unchecked = high/disabled, checked = low/enabled
        cs_flash_active = st.checkbox("Assert CS_Flash (Pull Low)", value=st.session_state.cs_flash, key="cb_flash")
        st.session_state.cs_flash = cs_flash_active
        st.caption("SPI Device 0 · Responds: `0xA5` (10100101)")

    with c2:
        st.markdown('<div class="panel-title" style="color:#3B82F6;">Temp Sensor</div>', unsafe_allow_html=True)
        cs_sensor_active = st.checkbox("Assert CS_Sensor (Pull Low)", value=st.session_state.cs_sensor, key="cb_sensor")
        st.session_state.cs_sensor = cs_sensor_active
        st.caption("SPI Device 1 · Responds: `0x3C` (00111100)")

    with c3:
        st.markdown('<div class="panel-title" style="color:#F59E0B;">ADC Converter</div>', unsafe_allow_html=True)
        cs_adc_active = st.checkbox("Assert CS_ADC (Pull Low)", value=st.session_state.cs_adc, key="cb_adc")
        st.session_state.cs_adc = cs_adc_active
        st.caption("SPI Device 2 · Responds: `0x5A` (01011010)")

    with c4:
        st.markdown('<div class="panel-title" style="color:#EC4899;">OLED Display</div>', unsafe_allow_html=True)
        cs_display_active = st.checkbox("Assert CS_Display (Pull Low)", value=st.session_state.cs_display, key="cb_display")
        st.session_state.cs_display = cs_display_active
        st.caption("SPI Device 3 · Responds: `0xF0` (11110000)")

    st.markdown('</div>', unsafe_allow_html=True)

# Count asserted devices
asserted_devices = []
if cs_flash_active: asserted_devices.append("Flash")
if cs_sensor_active: asserted_devices.append("Sensor")
if cs_adc_active: asserted_devices.append("ADC")
if cs_display_active: asserted_devices.append("Display")

num_asserted = len(asserted_devices)

# Display state summaries
st.markdown('<div class="pipeline-step">System Status</div>', unsafe_allow_html=True)
with st.container():
    st.markdown('<div class="panel-box">', unsafe_allow_html=True)
    c_status, c_action = st.columns([3, 1])
    with c_status:
        if num_asserted == 0:
            st.markdown('<div class="agreement-item agreement-warning" style="font-weight:bold;text-align:center;font-size:1rem;">⚠️ Bus Idle (Floating Tri-State). MISO Reads 0xFF (Pull-up).</div>', unsafe_allow_html=True)
        elif num_asserted == 1:
            st.markdown(f'<div class="agreement-item agreement-ok" style="font-weight:bold;text-align:center;font-size:1rem;">✓ Active Slave: {asserted_devices[0]} (Single Device Driving MISO)</div>', unsafe_allow_html=True)
        else:
            conflict_names = " & ".join(asserted_devices)
            st.markdown(f'<div class="agreement-item agreement-fail" style="font-weight:bold;text-align:center;font-size:1rem;">💥 CRITICAL: BUS CONTENTION! Multiple Slaves driving MISO: {conflict_names}</div>', unsafe_allow_html=True)
    with c_action:
        sc_transmit_btn = st.button("RUN SIMULATION", use_container_width=True)
        if sc_transmit_btn:
            st.session_state.sc_animating = True
            st.session_state.sc_anim_step = 0
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# Bit definitions
# Flash:   10100101 (0xA5)
# Sensor:  00111100 (0x3C)
# ADC:     01011010 (0x5A)
# Display: 11110000 (0xF0)
device_bits = {
    "Flash": [1, 0, 1, 0, 0, 1, 0, 1],
    "Sensor": [0, 0, 1, 1, 1, 1, 0, 0],
    "ADC": [0, 1, 0, 1, 1, 0, 1, 0],
    "Display": [1, 1, 1, 1, 0, 0, 0, 0]
}

# Determine MISO bit values and contention at each position
miso_display_bits = []
miso_errors = [] # indices of conflict
for bit_idx in range(8):
    driven_values = []
    for dev in asserted_devices:
        driven_values.append(device_bits[dev][bit_idx])
    
    if num_asserted == 0:
        # Floating high due to pull-up
        miso_display_bits.append(1)
    elif num_asserted == 1:
        miso_display_bits.append(driven_values[0])
    else:
        # Contention
        unique_vals = set(driven_values)
        if len(unique_vals) == 1:
            # All active devices driving the same level: no physical crash, but bad design
            miso_display_bits.append(driven_values[0])
        else:
            # Collision! Value is indeterminate (represented as 'X' or noisy waveform, outputs random/corrupted)
            miso_display_bits.append("X")
            miso_errors.append(bit_idx)

# ====================================================
# SVG BUS SCHEMATIC AND SIGNAL WAVEFORMS
# ====================================================
# Draw a combined bus topology SVG and waveform SVG
svg_w = 950
svg_h = 240
pad_left = 110
pad_right = 30
disp_w = svg_w - pad_left - pad_right

x_edges = [pad_left + 45 + i * 35 for i in range(16)]
step = st.session_state.sc_anim_step

svg_blocks = []

# 1. Individual Chip Select lines
# CS0: Flash
cs0_active = cs_flash_active
cs0_color = "#10B981" if cs0_active else "#475569"
cs0_y = 20
cs0_path = f"M {pad_left},{cs0_y} L {x_edges[0]},{cs0_y} L {x_edges[0]},{cs0_y + 10 if cs0_active else cs0_y} L {x_edges[14]},{cs0_y + 10 if cs0_active else cs0_y} L {x_edges[14]},{cs0_y} L {svg_w},{cs0_y}"
svg_blocks.append(f'<path d="{cs0_path}" fill="none" stroke="{cs0_color}" stroke-width="1.5" />')
svg_blocks.append(f'<text x="{pad_left - 15}" y="{cs0_y + 3}" fill="{cs0_color}" font-family="monospace" font-size="8" text-anchor="end">CS_Flash (CS0)</text>')

# CS1: Sensor
cs1_active = cs_sensor_active
cs1_color = "#3B82F6" if cs1_active else "#475569"
cs1_y = 45
cs1_path = f"M {pad_left},{cs1_y} L {x_edges[0]},{cs1_y} L {x_edges[0]},{cs1_y + 10 if cs1_active else cs1_y} L {x_edges[14]},{cs1_y + 10 if cs1_active else cs1_y} L {x_edges[14]},{cs1_y} L {svg_w},{cs1_y}"
svg_blocks.append(f'<path d="{cs1_path}" fill="none" stroke="{cs1_color}" stroke-width="1.5" />')
svg_blocks.append(f'<text x="{pad_left - 15}" y="{cs1_y + 3}" fill="{cs1_color}" font-family="monospace" font-size="8" text-anchor="end">CS_Sensor (CS1)</text>')

# CS2: ADC
cs2_active = cs_adc_active
cs2_color = "#F59E0B" if cs2_active else "#475569"
cs2_y = 70
cs2_path = f"M {pad_left},{cs2_y} L {x_edges[0]},{cs2_y} L {x_edges[0]},{cs2_y + 10 if cs2_active else cs2_y} L {x_edges[14]},{cs2_y + 10 if cs2_active else cs2_y} L {x_edges[14]},{cs2_y} L {svg_w},{cs2_y}"
svg_blocks.append(f'<path d="{cs2_path}" fill="none" stroke="{cs2_color}" stroke-width="1.5" />')
svg_blocks.append(f'<text x="{pad_left - 15}" y="{cs2_y + 3}" fill="{cs2_color}" font-family="monospace" font-size="8" text-anchor="end">CS_ADC (CS2)</text>')

# CS3: Display
cs3_active = cs_display_active
cs3_color = "#EC4899" if cs3_active else "#475569"
cs3_y = 95
cs3_path = f"M {pad_left},{cs3_y} L {x_edges[0]},{cs3_y} L {x_edges[0]},{cs3_y + 10 if cs3_active else cs3_y} L {x_edges[14]},{cs3_y + 10 if cs3_active else cs3_y} L {x_edges[14]},{cs3_y} L {svg_w},{cs3_y}"
svg_blocks.append(f'<path d="{cs3_path}" fill="none" stroke="{cs3_color}" stroke-width="1.5" />')
svg_blocks.append(f'<text x="{pad_left - 15}" y="{cs3_y + 3}" fill="{cs3_color}" font-family="monospace" font-size="8" text-anchor="end">CS_Display (CS3)</text>')

# 2. SCLK Line (pulses)
sclk_y_high = 120
sclk_y_low = 135
sclk_path = f"M 0,{sclk_y_low} L {x_edges[0]},{sclk_y_low}"
curr_y = sclk_y_low
for x in x_edges[:14]:
    next_y = sclk_y_high if curr_y == sclk_y_low else sclk_y_low
    sclk_path += f" L {x},{curr_y} L {x},{next_y}"
    curr_y = next_y
sclk_path += f" L {svg_w},{sclk_y_low}"
svg_blocks.append(f'<path d="{sclk_path}" fill="none" stroke="#6366F1" stroke-width="1.5" />')
svg_blocks.append(f'<text x="{pad_left - 15}" y="{sclk_y_low - 2}" fill="#6366F1" font-family="monospace" font-size="8" text-anchor="end">SCLK (Clock)</text>')

# 3. MOSI Line (Master output)
mosi_y_high = 155
mosi_y_low = 170
mosi_path = f"M 0,{mosi_y_low} L {x_edges[0]},{mosi_y_low}"
# Draw a dummy MOSI data train (01010101)
for i in range(8):
    y_val = mosi_y_high if (i % 2 == 0) else mosi_y_low
    mosi_path += f" L {x_edges[2*i]},{y_val} L {x_edges[2*i+1]},{y_val}"
mosi_path += f" L {svg_w},{mosi_y_low}"
svg_blocks.append(f'<path d="{mosi_path}" fill="none" stroke="#94A3B8" stroke-width="1.5" />')
svg_blocks.append(f'<text x="{pad_left - 15}" y="{mosi_y_low - 2}" fill="#94A3B8" font-family="monospace" font-size="8" text-anchor="end">MOSI (Data Out)</text>')

# 4. MISO Line (Slave input with potential conflicts)
miso_y_high = 190
miso_y_low = 205
miso_y_mid = 197.5

miso_path = f"M 0,{miso_y_high} L {x_edges[0]},{miso_y_high}"

miso_path_blocks = []
for i in range(8):
    val = miso_display_bits[i]
    x_start = x_edges[2*i]
    x_end = x_edges[2*i+1]
    
    if val == 1:
        miso_path_blocks.append(f'<path d="M {x_start},{miso_y_high} L {x_end},{miso_y_high}" fill="none" stroke="#10B981" stroke-width="2" />')
    elif val == 0:
        miso_path_blocks.append(f'<path d="M {x_start},{miso_y_low} L {x_end},{miso_y_low}" fill="none" stroke="#10B981" stroke-width="2" />')
    elif val == "X":
        # Collision waveform: double lines or red noise/shading
        miso_path_blocks.append(f"""
        <path d="M {x_start},{miso_y_high} L {x_end},{miso_y_high}" fill="none" stroke="#EF6868" stroke-width="2" />
        <path d="M {x_start},{miso_y_low} L {x_end},{miso_y_low}" fill="none" stroke="#EF6868" stroke-width="2" />
        <path d="M {x_start},{miso_y_high} L {x_end},{miso_y_low}" fill="none" stroke="#EF6868" stroke-width="1.5" stroke-dasharray="2,2" />
        <path d="M {x_start},{miso_y_low} L {x_end},{miso_y_high}" fill="none" stroke="#EF6868" stroke-width="1.5" stroke-dasharray="2,2" />
        <rect x="{x_start}" y="{miso_y_high}" width="{x_end - x_start}" height="{miso_y_low - miso_y_high}" fill="rgba(239, 104, 104, 0.15)" />
        <text x="{(x_start+x_end)/2}" y="{miso_y_mid + 3}" fill="#EF6868" font-family="monospace" font-size="8" font-weight="bold" text-anchor="middle">CONFLICT</text>
        """)

# Connect intermediate gaps
for i in range(7):
    x_mid_start = x_edges[2*i+1]
    x_mid_end = x_edges[2*i+2]
    val_prev = miso_display_bits[i]
    val_next = miso_display_bits[i+1]
    
    y1 = miso_y_high if val_prev == 1 or val_prev == "X" else miso_y_low
    y2 = miso_y_high if val_next == 1 or val_next == "X" else miso_y_low
    color = "#EF6868" if (val_prev == "X" or val_next == "X") else "#10B981"
    
    miso_path_blocks.append(f'<path d="M {x_mid_start},{y1} L {x_mid_end},{y2}" fill="none" stroke="{color}" stroke-width="2" />')

# Connect start and end transitions
miso_start_color = "#10B981" if (num_asserted <= 1) else "#EF6868"
if num_asserted == 0:
    miso_start_color = "#F59E0B" # Floating warning
miso_path_blocks.append(f'<path d="M 0,{miso_y_high} L {x_edges[0]},{miso_y_high}" fill="none" stroke="{miso_start_color}" stroke-width="1.5" />')

y_last = miso_y_high if miso_display_bits[-1] == 1 or miso_display_bits[-1] == "X" else miso_y_low
miso_path_blocks.append(f'<path d="M {x_edges[15]},{y_last} L {svg_w},{y_last}" fill="none" stroke="{miso_start_color}" stroke-width="1.5" />')

# Append MISO path blocks
svg_blocks.extend(miso_path_blocks)
svg_blocks.append(f'<text x="{pad_left - 15}" y="{miso_y_low - 2}" fill="{miso_start_color}" font-family="monospace" font-size="8" text-anchor="end">MISO (Data In)</text>')

# 5. Glowing Time Sweep Cursor
if st.session_state.sc_animating and step < 16:
    cursor_x = x_edges[0] + step * 35
    svg_blocks.append(f'<line x1="{cursor_x}" y1="10" x2="{cursor_x}" y2="225" stroke="#3B82F6" stroke-width="1.5" />')

# Compile SVG
svg_content = f'<svg viewBox="0 0 {svg_w} {svg_h}" width="100%">{"".join(svg_blocks)}</svg>'

# Render Waveform
st.markdown('<div class="pipeline-step">Physical Waveform Trace (Shared Bus State)</div>', unsafe_allow_html=True)
with st.container():
    st.markdown('<div class="panel-box" style="margin-bottom: 0.5rem;">', unsafe_allow_html=True)
    st.markdown(f'<div style="background:#0F172A; padding:0; overflow-x:auto;">{svg_content}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.caption("Shared bus traces: CS selection lines (colored if asserted low), SCLK pulses, MOSI data stream, and MISO bus state (green = normal, orange = floating idle, red = contention collision).")

# ====================================================
# LIVE LOGS AND DATA RECOVERY OUTCOME
# ====================================================
log_col, out_col = st.columns(2)

with log_col:
    st.markdown('<div class="pipeline-step">Bus Logging Terminal</div>', unsafe_allow_html=True)
    
    logs = []
    if num_asserted == 0:
        logs.append("[0.0ms] Master pulls all CS lines High (deasserted).")
        logs.append("[0.2ms] SCLK active, driving 8 clock pulses.")
        logs.append("[0.5ms] MISO wire is placed in high-impedance (tri-state) mode by all slaves.")
        logs.append("[0.8ms] Physical bus pull-up resistor pulls MISO voltage up to VCC (+3.3V).")
        for idx in range(8):
            if step >= idx * 2:
                logs.append(f"[Bit {7-idx}] Master samples MISO High -> Read 1 (Tri-stated).")
        if step >= 16:
            logs.append("[2.5ms] Clock pulses complete. Transaction ended.")
            logs.append("[Outcome] Master successfully read 0xFF (tri-stated bus).")
            
    elif num_asserted == 1:
        dev_name = asserted_devices[0]
        dev_hex = "0xA5" if dev_name == "Flash" else ("0x3C" if dev_name == "Sensor" else ("0x5A" if dev_name == "ADC" else "0xF0"))
        logs.append(f"[0.0ms] Master pulls CS_{dev_name} Low (asserted). All other CS lines remain High.")
        logs.append(f"[0.2ms] peripheral '{dev_name}' wakes up, enables output driver on MISO trace.")
        logs.append("[0.4ms] SCLK clock line begins pulsing.")
        for idx in range(8):
            if step >= idx * 2:
                val = device_bits[dev_name][idx]
                logs.append(f"[Bit {7-idx}] {dev_name} drives MISO: {val} -> Master samples: {val}.")
        if step >= 16:
            logs.append("[2.5ms] Clock pulses complete. CS deasserted.")
            logs.append(f"[Outcome] Communication clean. Master successfully read {dev_hex} from {dev_name}.")
            
    else:
        # Contention
        conflict_names = ", ".join(asserted_devices[:-1]) + " and " + asserted_devices[-1]
        logs.append(f"[CRITICAL] Master asserts multiple CS lines simultaneously: {conflict_names}!")
        logs.append("[0.1ms] Multiple output drivers enabled on the shared MISO physical trace.")
        logs.append("[0.2ms] SCLK begins pulsing. Peripherals attempt to transmit concurrent bytes.")
        
        for idx in range(8):
            if step >= idx * 2:
                # check if there is a conflict
                vals = [device_bits[dev][idx] for dev in asserted_devices]
                unique_vals = set(vals)
                if len(unique_vals) == 1:
                    logs.append(f"[Bit {7-idx}] All devices driving {vals[0]} -> Master samples: {vals[0]} (No collision).")
                else:
                    colliding_details = " vs ".join([f"{d}={device_bits[d][idx]}" for d in asserted_devices])
                    logs.append(f"[COLLISION] Bit {7-idx} conflict: {colliding_details}.")
                    logs.append(f"            MISO line voltage collapses. Logic state indeterminate.")
        
        if step >= 16:
            logs.append("[2.5ms] Transaction terminated.")
            logs.append("[CRITICAL] Bus contention caused short circuits. Current spike > 50mA recorded.")
            logs.append("[CRITICAL] Data read is corrupted/indeterminate. High hardware damage risk!")

    st.markdown(f'<div class="terminal-box">{"<br>".join(logs)}</div>', unsafe_allow_html=True)

with out_col:
    st.markdown('<div class="pipeline-step">Electrical Bus Status</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="panel-box" style="height: 220px; margin:0; display:flex; flex-direction:column; justify-content:center; gap:0.5rem;">', unsafe_allow_html=True)
        
        # Display MISO current voltage and state
        if num_asserted == 0:
            st.markdown('<div style="font-family:monospace; font-size:0.75rem; color:#64748B;">MISO BUS VOLTAGE LEVEL:</div>', unsafe_allow_html=True)
            st.markdown('<div style="font-family:monospace; font-size:1.5rem; color:#F59E0B; font-weight:bold;">~ 3.3V (Tri-State Pull-Up)</div>', unsafe_allow_html=True)
            st.markdown('<div style="font-family:monospace; font-size:0.72rem; color:#A5F3FC;">Current consumption: 0.0mA (Min)<br>Recovered Byte: 0xFF (Idle)</div>', unsafe_allow_html=True)
        elif num_asserted == 1:
            dev = asserted_devices[0]
            dev_hex = "0xA5" if dev == "Flash" else ("0x3C" if dev == "Sensor" else ("0x5A" if dev == "ADC" else "0xF0"))
            st.markdown(f'<div style="font-family:monospace; font-size:0.75rem; color:#64748B;">MISO BUS VOLTAGE ({dev}):</div>', unsafe_allow_html=True)
            st.markdown('<div style="font-family:monospace; font-size:1.5rem; color:#10B981; font-weight:bold;">Clean Digital 0V / 3.3V Transitions</div>', unsafe_allow_html=True)
            st.markdown(f'<div style="font-family:monospace; font-size:0.72rem; color:#A5F3FC;">Current consumption: ~1.2mA (Nominal)<br>Recovered Byte: {dev_hex}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div style="font-family:monospace; font-size:0.75rem; color:#EF6868; font-weight:bold;">⚠️ ELECTRICAL HAZARD: SHORT CIRCUIT</div>', unsafe_allow_html=True)
            st.markdown('<div style="font-family:monospace; font-size:1.5rem; color:#EF6868; font-weight:bold;">~ 1.6V Intermediate (Contention)</div>', unsafe_allow_html=True)
            st.markdown('<div style="font-family:monospace; font-size:0.72rem; color:#EF6868;">Current consumption: &gt; 48.5mA (EXCESSIVE HEAT)<br>Recovered Byte: ERROR / GARBAGE</div>', unsafe_allow_html=True)
            
        st.markdown('</div>', unsafe_allow_html=True)

# ====================================================
# ANIMATION LOOP DRIVER
# ====================================================
if st.session_state.sc_animating:
    if st.session_state.sc_anim_step < 16:
        time.sleep(0.12)
        st.session_state.sc_anim_step += 1
        st.rerun()
    else:
        st.session_state.sc_animating = False
        st.rerun()
