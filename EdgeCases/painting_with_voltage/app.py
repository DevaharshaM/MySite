import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Set dark theme for matplotlib
plt.style.use('dark_background')
fig_color = '#0F172A'
panel_color = '#1E293B'
border_color = 'rgba(148,163,184,0.12)'

st.set_page_config(
    page_title="EdgeCase: Painting with Voltage",
    layout="centered"
)

# Custom CSS for dark theme integration
st.markdown(
    """
    <style>
    .stApp {
        background-color: #0F172A;
        color: #E2E8F0;
    }
    .stSlider > div > div > div {
        background: #3B82F6;
    }
    .stSelectbox > div > div {
        background-color: #1E293B;
        border-color: rgba(148,163,184,0.2);
        color: white;
    }
    .panel-box {
        background-color: #1E293B;
        padding: 1.25rem;
        border-radius: 8px;
        border: 1px solid rgba(148, 163, 184, 0.12);
        margin-bottom: 1.5rem;
    }
    .metric-val {
        font-size: 1.2rem;
        font-weight: bold;
        color: #10B981;
    }
    .metric-label {
        font-size: 0.75rem;
        color: #64748B;
        text-transform: uppercase;
        margin-bottom: 0.25rem;
    }
    .terminal-text {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.75rem;
        color: #A5F3FC;
        background: #090D16;
        padding: 0.75rem;
        border-radius: 6px;
        border: 1px solid rgba(148, 163, 184, 0.1);
        min-height: 80px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("EdgeCase: Painting with Voltage")
st.subheader("Watch Numbers Become Analog Voltages")

st.markdown(
    "Adjust resolution, reference voltage, and digital input value to watch how a number transforms into an analog voltage level."
)

# 2-Column Controls
st.markdown('<div class="panel-box">', unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    res_opt = st.selectbox("DAC Resolution", [3, 4, 8, 12], format_func=lambda x: f"{x}-bit ({2**x} Levels)")
    vref = st.slider("Reference Voltage (VREF)", min_value=1.0, max_value=5.0, value=3.3, step=0.1)

steps = 2**res_opt - 1
with col2:
    code = st.slider("Digital Input Code", min_value=0, max_value=steps, value=steps // 2, step=1)
st.markdown('</div>', unsafe_allow_html=True)

# Math calculations
lsb = (vref / steps) * 1000  # mV
vout = (code / steps) * vref  # V
bin_str = bin(code)[2:].zfill(res_opt)
hex_str = "0x" + hex(code)[2:].upper().zfill(int(np.ceil(res_opt/4)))

# Layout columns for metrics & visual
m_col1, m_col2 = st.columns([1, 1])

with m_col1:
    st.markdown('<div class="panel-box">', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-label">Resolution Steps</div><div class="metric-val" style="color:#FFF;">{steps + 1} Levels</div>', unsafe_allow_html=True)
    st.markdown('<div style="height:10px;"></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-label">LSB Size (Step Width)</div><div class="metric-val" style="color:#3B82F6;">{lsb:.2f} mV</div>', unsafe_allow_html=True)
    st.markdown('<div style="height:10px;"></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-label">Binary Value</div><div class="metric-val" style="font-family:monospace; color:#FFF;">{bin_str}</div>', unsafe_allow_html=True)
    st.markdown('<div style="height:10px;"></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-label">Output Voltage (VOUT)</div><div class="metric-val">{vout:.3f} V</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with m_col2:
    # Drawing Gauge using Matplotlib
    fig, ax = plt.subplots(figsize=(4, 3), facecolor=fig_color)
    ax.set_facecolor(fig_color)
    
    # Semicircle gauge drawing
    theta = np.linspace(0, np.pi, 100)
    ax.plot(np.cos(theta), np.sin(theta), color='#263244', lw=8, solid_capstyle='round')
    
    # Filled slice based on output
    fraction = vout / vref
    theta_filled = np.linspace(np.pi, np.pi * (1 - fraction), 100)
    ax.plot(np.cos(theta_filled), np.sin(theta_filled), color='#10B981', lw=8, solid_capstyle='round')
    
    # Needle line
    angle = np.pi * (1 - fraction)
    ax.plot([0, 0.85 * np.cos(angle)], [0, 0.85 * np.sin(angle)], color='#EF6868', lw=3, solid_capstyle='round')
    ax.plot(0, 0, marker='o', color='#EF6868', markersize=8)
    
    # Text overlay
    ax.text(0, -0.2, f"{vout:.3f} V", color='white', fontsize=12, fontweight='bold', ha='center')
    ax.text(0, -0.38, "DAC OUTPUT", color='#64748B', fontsize=8, ha='center')
    
    # Scale tick markings
    for val in [0.0, 0.25, 0.5, 0.75, 1.0]:
        a = np.pi * (1 - val)
        ax.plot([0.85 * np.cos(a), 0.95 * np.cos(a)], [0.85 * np.sin(a), 0.95 * np.sin(a)], color='#64748B', lw=1)
        ax.text(1.15 * np.cos(a), 1.15 * np.sin(a), f"{val*vref:.1f}V", color='#64748B', fontsize=6, ha='center', va='center')
        
    ax.set_xlim(-1.3, 1.3)
    ax.set_ylim(-0.5, 1.3)
    ax.axis('off')
    st.pyplot(fig)
    plt.close(fig)

# Register Logs
st.markdown("### Output Register Write Log")
st.markdown(
    f"""<div class="terminal-text">
    [SPI/DMA Channel Active]<br>
    DAC_DHR12RD write register {hex_str} (Bin: {bin_str})<br>
    VOUT pin driven to: {vout:.3f} V
    </div>""",
    unsafe_allow_html=True
)
