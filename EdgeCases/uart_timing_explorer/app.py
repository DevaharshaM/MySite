import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Set page layout
st.set_page_config(page_title="UART Timing Explorer", layout="centered")

st.title("⬢ UART Timing Explorer")
st.write("Simulate clock drift and sample point alignment on an asynchronous serial link.")

# Sidebar controls
st.sidebar.header("UART Parameters")
tx_baud = st.sidebar.selectbox("TX Baud Rate", [9600, 19200, 115200], index=0)
drift_percent = st.sidebar.slider("RX Clock Drift (%)", -15.0, 15.0, 0.0, 0.5)
parity = st.sidebar.selectbox("Parity", ["None (8N1)", "Even (8E1)", "Odd (8O1)"], index=0)
stop_bits = st.sidebar.selectbox("Stop Bits", [1, 2], index=0)

# Main layout controls
text_input = st.text_input("Text to Transmit", value="UART", max_chars=16)

# Simulation logic
if text_input:
    # Calculations
    rx_baud = tx_baud * (1.0 + (drift_percent / 100.0))
    T_tx = 1.0
    T_rx = txBaud_duration = tx_baud / rx_baud  # RX bit duration in TX time units
    
    # Map parity string
    parity_mode = "none"
    if "Even" in parity:
        parity_mode = "even"
    elif "Odd" in parity:
        parity_mode = "odd"

    # Get first character for waveform visualization
    first_char = text_input[0] if len(text_input) > 0 else ' '
    first_char_code = ord(first_char)
    
    # Calculate bits
    data_bits = [(first_char_code >> i) & 1 for i in range(8)]
    
    parity_bit = None
    if parity_mode != "none":
        one_count = sum(data_bits)
        if parity_mode == "even":
            parity_bit = 0 if one_count % 2 == 0 else 1
        else:
            parity_bit = 1 if one_count % 2 == 0 else 0
            
    # Build TX frame bits
    tx_frame = [0] + data_bits  # Start bit (0) + data
    if parity_bit is not None:
        tx_frame.append(parity_bit)
    tx_frame.extend([1] * stop_bits)  # Stop bit(s)
    
    total_bits = len(tx_frame)
    
    # Simulate sampling for all characters
    decoded_chars = []
    total_errors = 0
    framing_error_first = False
    parity_error_first = False
    first_char_samples = []

    for idx, char in enumerate(text_input):
        char_code = ord(char)
        c_data = [(char_code >> i) & 1 for i in range(8)]
        
        c_parity = None
        if parity_mode != "none":
            one_count = sum(c_data)
            if parity_mode == "even":
                c_parity = 0 if one_count % 2 == 0 else 1
            else:
                c_parity = 1 if one_count % 2 == 0 else 0
                
        c_frame = [0] + c_data
        if c_parity is not None:
            c_frame.append(c_parity)
        c_frame.extend([1] * stop_bits)
        
        # RX samples at (0.5 + i) * T_rx
        rx_bits = []
        c_samples = []
        for i in range(len(c_frame)):
            sample_time = (0.5 + i) * T_rx
            bit_idx = int(np.floor(sample_time / T_tx))
            sampled_val = 1
            if 0 <= bit_idx < len(c_frame):
                sampled_val = c_frame[bit_idx]
            rx_bits.append(sampled_val)
            c_samples.append((sample_time, sampled_val, bit_idx))
            
        if idx == 0:
            first_char_samples = c_samples
            
        # Parse RX bits
        rx_data = rx_bits[1:9]
        rx_parity = rx_bits[9] if parity_mode != "none" else None
        rx_stop_idx = 10 if parity_mode != "none" else 9
        rx_stop_bits = rx_bits[rx_stop_idx : rx_stop_idx + stop_bits]
        
        # Verify errors
        framing_error = any(sb != 1 for sb in rx_stop_bits) or rx_bits[0] != 0
        parity_error = False
        if parity_mode != "none" and rx_parity is not None:
            expected_parity = 0 if sum(rx_data) % 2 == 0 else 1
            if parity_mode == "odd":
                expected_parity = 1 if sum(rx_data) % 2 == 0 else 0
            if rx_parity != expected_parity:
                parity_error = True
                
        if idx == 0:
            framing_error_first = framing_error
            parity_error_first = parity_error
            
        # Decode character
        rx_char_code = 0
        for i in range(8):
            if rx_data[i] == 1:
                rx_char_code |= (1 << i)
                
        if framing_error or parity_error:
            total_errors += 1
            decoded_chars.append(f"~~{char}~~")
        else:
            decoded_chars.append(chr(rx_char_code))
            
    # Visualize using Matplotlib
    fig, ax = plt.subplots(figsize=(10, 3.5), facecolor='#0F172A')
    ax.set_facecolor('#0F172A')
    
    # Plot grid boundaries for TX bits
    for i in range(total_bits + 1):
        ax.axvline(i, color='#1E293B', linestyle='-', linewidth=1)
        if i < total_bits:
            label = ""
            if i == 0:
                label = "START"
            elif 1 <= i <= 8:
                label = f"D{i-1}"
            elif i == 9 and parity_mode != "none":
                label = "PAR"
            else:
                label = f"STOP"
            ax.text(i + 0.5, 1.25, label, color='#64748B', fontsize=8, ha='center', fontfamily='monospace')
            
    # Construct Waveform coordinates
    x_wave = [0]
    y_wave = [1]
    for i in range(total_bits):
        val = tx_frame[i]
        x_wave.extend([i, i + 1])
        y_wave.extend([val, val])
    x_wave.append(total_bits + 0.5)
    y_wave.append(1)
    
    # Plot waveform line
    ax.plot(x_wave, y_wave, color='#FFF', linewidth=2.5)
    
    # Plot sampling lines
    for idx, (s_time, s_val, b_idx) in enumerate(first_char_samples):
        # Correct sample check
        in_bounds = 0 <= b_idx < len(tx_frame)
        actual_val = tx_frame[b_idx] if in_bounds else 1
        is_correct = s_val == actual_val
        color = '#3B82F6' if is_correct else '#EF4444'
        style = '--' if is_correct else ':'
        
        ax.axvline(s_time, color=color, linestyle=style, linewidth=1.5)
        ax.plot(s_time, 0.5, marker='o', color=color, markersize=6)
        ax.text(s_time, -0.25, f"S{idx}", color=color, fontsize=8, ha='center', fontfamily='monospace')
        
    # Set labels and styles
    ax.set_xlim(-0.5, total_bits + 0.5)
    ax.set_ylim(-0.5, 1.5)
    ax.set_yticks([0, 1])
    ax.set_yticklabels(["LOW (0)", "HIGH (1)"], color='#64748B', fontfamily='monospace')
    ax.set_xticks([])
    
    # Remove borders
    for spine in ax.spines.values():
        spine.set_visible(False)
        
    plt.tight_layout()
    st.pyplot(fig)
    
    # Report Section
    st.subheader("Receiver Diagnostic Report")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Receiver Status**")
        if total_errors == 0:
            st.success("Locked & Synchronized (0 Errors)")
        else:
            errors_list = []
            if framing_error_first:
                errors_list.append("Framing Error")
            if parity_error_first:
                errors_list.append("Parity Mismatch")
            if not errors_list:
                errors_list.append("Data Corruption")
            st.error(f"Error: {' / '.join(errors_list)} ({total_errors} char errors)")
            
    with col2:
        st.markdown("**Decoded Output**")
        st.code(" ".join(decoded_chars))
