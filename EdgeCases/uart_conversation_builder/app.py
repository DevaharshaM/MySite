import streamlit as st
import matplotlib.pyplot as plt

# Set page config
st.set_page_config(
    page_title="PrajnaEdge - Build a UART Conversation",
    page_icon="⚡",
    layout="wide"
)

# Custom Styling (Minimal, dark theme)
st.markdown("""
<style>
    .reportview-container {
        background: #0F172A;
        color: #E2E8F0;
    }
    .panel-header {
        font-family: 'Syne', sans-serif;
        font-weight: 700;
        font-size: 1.1rem;
        color: #FFFFFF;
        text-transform: uppercase;
        margin-top: 1.5rem;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .panel-header::before {
        content: "⚡";
        color: #3B82F6;
    }
    .text-corrupted {
        color: #EF6868;
        font-weight: bold;
        text-decoration: underline;
    }
    .diagnostic-ok {
        padding: 0.2rem 0.5rem;
        background: rgba(16, 185, 129, 0.1);
        color: #10B981;
        border: 1px solid rgba(16, 185, 129, 0.2);
        border-radius: 4px;
        font-family: monospace;
        font-size: 0.8rem;
    }
    .diagnostic-error {
        padding: 0.2rem 0.5rem;
        background: rgba(239, 68, 68, 0.1);
        color: #EF6868;
        border: 1px solid rgba(239, 68, 68, 0.2);
        border-radius: 4px;
        font-family: monospace;
        font-size: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)

st.title("EdgeCase: Build a UART Conversation")
st.caption("Explore how two independent processors coordinate time to serialize and transmit data over a single wire.")

# ====================================================
# PANEL 1: Message Input
# ====================================================
st.markdown('<div class="panel-header">Panel 1: Message Input & Serialization</div>', unsafe_allow_html=True)
message = st.text_input("Message to Transmit", value="Hello", max_chars=12)

# Serialization table
if message:
    mapping_data = []
    # Limit visualization to first 5 chars
    for char in message[:5]:
        val = ord(char)
        binary_str = format(val, '08b')
        lsb_first = [str((val >> b) & 1) for b in range(8)]
        mapping_data.append({
            "Character": char,
            "ASCII Decimal": val,
            "Binary Byte (MSB->LSB)": binary_str,
            "LSB First Order": " → ".join(lsb_first)
        })
    st.table(mapping_data)
    if len(message) > 5:
        st.info(f"... and {len(message) - 5} more characters")

# ====================================================
# PANEL 2: UART Frame Builder (TX Contract)
# ====================================================
st.markdown('<div class="panel-header">Panel 2: UART Frame Builder (TX Contract)</div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
with col1:
    tx_baud = st.selectbox("TX Baud Rate", [9600, 19200, 115200], index=0)
with col2:
    tx_data_bits = st.selectbox("TX Data Bits", [5, 6, 7, 8], index=3)
with col3:
    tx_parity = st.selectbox("TX Parity", ["None", "Even", "Odd"], index=0)
with col4:
    tx_stop_bits = st.selectbox("TX Stop Bits", [1, 2], index=0)

# Build first character's frame
first_char_code = ord(message[0]) if message else 32
tx_bits = []
# Start bit
tx_bits.append(("Start", 0, "red"))
# Data bits
char_bits = []
for b in range(tx_data_bits):
    bit_val = (first_char_code >> b) & 1
    char_bits.append(bit_val)
    tx_bits.append((f"D{b}", bit_val, "blue"))
# Parity
tx_parity_bit = None
if tx_parity != "None":
    bit_sum = sum(char_bits)
    if tx_parity == "Even":
        tx_parity_bit = bit_sum % 2
    else:
        tx_parity_bit = 0 if bit_sum % 2 != 0 else 1
    tx_bits.append(("Parity", tx_parity_bit, "orange"))
# Stop bits
for s in range(tx_stop_bits):
    tx_bits.append((f"Stop{s+1}" if tx_stop_bits > 1 else "Stop", 1, "green"))

# Visualize constructed frame boxes
frame_visuals = []
for label, val, color in tx_bits:
    frame_visuals.append(f"**[{label}: {val}]**")
st.markdown("  →  ".join(frame_visuals))

# ====================================================
# ADVANCED EXPERIMENT TOGGLE
# ====================================================
st.write("---")
adv_mode = st.checkbox("Advanced Mode: Unlock Receiver Mismatch Experiment")

rx_baud = tx_baud
rx_data_bits = tx_data_bits
rx_parity = tx_parity
rx_stop_bits = tx_stop_bits

if adv_mode:
    st.markdown('<div class="panel-header" style="color:#EF6868;">Advanced: Mismatched Receiver Settings (RX Contract)</div>', unsafe_allow_html=True)
    rx_col1, rx_col2, rx_col3, rx_col4 = st.columns(4)
    with rx_col1:
        rx_baud = rx_col1.selectbox("RX Baud Rate", [4800, 9600, 14400, 19200, 115200], index=1)
    with rx_col2:
        rx_data_bits = rx_col2.selectbox("RX Data Bits", [5, 6, 7, 8], index=3)
    with rx_col3:
        rx_parity = rx_col3.selectbox("RX Parity", ["None", "Even", "Odd"], index=0)
    with rx_col4:
        rx_stop_bits = rx_col4.selectbox("RX Stop Bits", [1, 2], index=0)

# ====================================================
# PANEL 3: Transmission Waveform
# ====================================================
st.markdown('<div class="panel-header">Panel 3: Electrical Waveform & Sampling Points (First Character)</div>', unsafe_allow_html=True)

# Build physical waveform data points
tx_waveform_states = [1] + [val for _, val, _ in tx_bits] + [1]
T_tx = 1.0
T_rx = tx_baud / rx_baud

# RX Samples starting from falling edge of Start Bit (occurs at physical time 1.0)
rx_sample_count = 1 + rx_data_bits + (1 if rx_parity != "None" else 0) + rx_stop_bits
rx_samples = []
for i in range(rx_sample_count):
    rx_time = (0.5 + i) * T_rx
    tx_time = 1.0 + rx_time
    tx_idx = int(tx_time)
    sampled_val = 1
    if 0 <= tx_idx < len(tx_waveform_states):
        sampled_val = tx_waveform_states[tx_idx]
    rx_samples.append((rx_time, tx_time, sampled_val, i))

# Plot the waveform using matplotlib
fig, ax = plt.subplots(figsize=(10, 2.5), facecolor='#0F172A')
ax.set_facecolor('#0F172A')

# Waveform line step plotting
x_vals = []
y_vals = []
for idx, val in enumerate(tx_waveform_states):
    x_vals.extend([idx, idx + 1])
    y_vals.extend([val, val])

ax.plot(x_vals, y_vals, color='#FFFFFF', linewidth=2, label="TX Voltage Line")

# Draw vertical grid boundaries for TX slots
for i in range(len(tx_waveform_states) + 1):
    ax.axvline(i, color='#334155', linestyle=':', alpha=0.5)

# Label the slots
slot_labels = ["IDLE", "START"] + [label for label, _, _ in tx_bits] + ["IDLE"]
for i, label in enumerate(slot_labels):
    ax.text(i + 0.5, -0.25, label, color='#64748B', fontsize=6, ha='center', fontfamily='monospace')

# Plot RX sampling points
for rx_time, tx_time, sampled_val, sample_idx in rx_samples:
    tx_idx = int(tx_time)
    actual_tx_val = tx_waveform_states[tx_idx] if 0 <= tx_idx < len(tx_waveform_states) else 1
    correct = (sampled_val == actual_tx_val)
    color = '#3B82F6' if correct else '#EF6868'
    ax.axvline(tx_time, color=color, linestyle='--', alpha=0.7, linewidth=1)
    ax.scatter([tx_time], [0.5], color=color, zorder=5, s=30)
    ax.text(tx_time, 1.25, f"S{sample_idx}", color=color, fontsize=7, ha='center', fontfamily='monospace')

# Style the axes
ax.set_xlim(0, len(tx_waveform_states))
ax.set_ylim(-0.4, 1.4)
ax.set_yticks([0, 1])
ax.set_yticklabels(["LOW (0)", "HIGH (1)"], color='#64748B', fontfamily='monospace', fontsize=8)
ax.tick_params(colors='#64748B', labelsize=8)
ax.spines['bottom'].set_color('#334155')
ax.spines['left'].set_color('#334155')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(False)

st.pyplot(fig)

# ====================================================
# PANEL 4: Receiver & Reconstruction
# ====================================================
st.markdown('<div class="panel-header">Panel 4: Receiver &amp; Reconstruction</div>', unsafe_allow_html=True)

recovered_chars = []
has_framing_err = False
has_parity_err = False

for char in message:
    val = ord(char)
    # Build TX frame bits for this character
    char_tx_bits = []
    for b in range(tx_data_bits):
        char_tx_bits.append((val >> b) & 1)
    char_tx_parity_bit = None
    if tx_parity != "None":
        sum_bits = sum(char_tx_bits)
        if tx_parity == "Even":
            char_tx_parity_bit = sum_bits % 2
        else:
            char_tx_parity_bit = 0 if sum_bits % 2 != 0 else 1
    
    char_tx_frame = [0] + char_tx_bits
    if char_tx_parity_bit is not None:
        char_tx_frame.append(char_tx_parity_bit)
    for _ in range(tx_stop_bits):
        char_tx_frame.append(1)
        
    # Sample bits using RX parameters
    rx_sampled_bits = []
    for i in range(rx_sample_count):
        rx_time = (0.5 + i) * T_rx
        tx_idx = int(rx_time)
        s_val = 1
        if 0 <= tx_idx < len(char_tx_frame):
            s_val = char_tx_frame[tx_idx]
        rx_sampled_bits.append(s_val)
        
    # Parse RX bits
    rx_start = rx_sampled_bits[0]
    rx_data = rx_sampled_bits[1:1+rx_data_bits]
    rx_parity_val = rx_sampled_bits[1+rx_data_bits] if rx_parity != "None" else None
    
    rx_stop_start = 1 + rx_data_bits + (1 if rx_parity != "None" else 0)
    rx_stops = rx_sampled_bits[rx_stop_start:rx_stop_start+rx_stop_bits]
    
    # Check framing errors
    framing_err = (rx_start != 0)
    for sb in rx_stops:
        if sb != 1:
            framing_err = True
            
    # Check parity errors
    parity_err = False
    if rx_parity != "None" and rx_parity_val is not None:
        rx_sum = sum(rx_data)
        expected_par = rx_sum % 2 if rx_parity == "Even" else (0 if rx_sum % 2 != 0 else 1)
        if rx_parity_val != expected_par:
            parity_err = True
            
    if framing_err:
        has_framing_err = True
    if parity_err:
        has_parity_err = True
        
    # Reconstruct byte
    rec_byte = 0
    for b in range(rx_data_bits):
        if b < len(rx_data) and rx_data[b] == 1:
            rec_byte |= (1 << b)
            
    if framing_err or parity_err:
        recovered_chars.append(f'<span class="text-corrupted">?</span>')
    else:
        recovered_chars.append(chr(rec_byte) if 32 <= rec_byte <= 126 else '?')

# Display recovered message
recovered_message_str = "".join(recovered_chars)

status_col, msg_col = st.columns(2)
with status_col:
    st.write("**Receiver Status**")
    if not has_framing_err and not has_parity_err:
        st.markdown('<span class="diagnostic-ok">LOCKED & SYNCHRONIZED</span>', unsafe_allow_html=True)
        st.caption("TX and RX configurations match perfectly. Signal expectations are aligned.")
    else:
        errors = []
        if has_framing_err:
            errors.append("Framing Error")
        if has_parity_err:
            errors.append("Parity Error")
        st.markdown(f'<span class="diagnostic-error">{" / ".join(errors)}</span>', unsafe_allow_html=True)
        st.caption("The receiver sampled at the wrong timings or calculated a parity mismatch due to configuration drift.")

with msg_col:
    st.write("**Recovered Message**")
    st.markdown(f'<div style="font-size:1.5rem; font-family:monospace; background:#0F172A; padding:0.5rem; border-radius:4px; border:1px solid #334155;">{recovered_message_str}</div>', unsafe_allow_html=True)

# Educational lesson
st.info("""
**Core Educational Message:**
* UART does not synchronize processors. It synchronizes **expectations**.
* The transmitter and receiver can run at completely independent CPU clock frequencies (e.g. 16 MHz vs 1 GHz).
* As long as they agree on the baud rate, parity, data bits, and stop bits contract, they reconstruct the serial stream successfully.
""")
