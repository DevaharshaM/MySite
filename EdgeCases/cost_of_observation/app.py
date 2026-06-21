import streamlit as st
import math

# Page configuration
st.set_page_config(
    page_title="PrajnaEdge - ADC: The Cost of Observation",
    page_icon="⚠️",
    layout="wide"
)

# Custom dark theme styles
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
        content: "⚠️";
        color: #E2E8F0;
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
    .edgecase-visual {
        background: #0F172A;
        border: 1px solid rgba(148, 163, 184, 0.12);
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 1.5rem;
        overflow-x: auto;
    }
    .edgecase-visual svg {
        display: block;
        width: 100%;
        min-width: 600px;
    }
    .agreement-item {
        font-family: monospace;
        font-size: 0.72rem;
        padding: 0.6rem;
        margin-bottom: 0.5rem;
        border-radius: 6px;
        line-height: 1.4;
    }
    .agreement-ok {
        background: rgba(16, 185, 129, 0.08);
        color: #10B981;
        border: 1px solid rgba(16, 185, 129, 0.2);
    }
    .agreement-fail {
        background: rgba(239, 68, 68, 0.08);
        color: #EF6868;
        border: 1px solid rgba(239, 68, 68, 0.2);
    }
    .agreement-warn {
        background: rgba(245, 158, 11, 0.08);
        color: #F59E0B;
        border: 1px solid rgba(245, 158, 11, 0.2);
    }
</style>
""", unsafe_allow_html=True)

st.title("EdgeCase: The Cost of Observation")
st.subheader("Visualizing Signal Corruptions: Aliasing, Clipping & Quantization Noise")
st.caption("Adjust parameters below to trigger typical measurement errors: sample below 2x frequency to induce aliasing; drop reference voltage below amplitude to clip; lower resolution to increase quantization steps.")

# ====================================================
# CONFIGURATION PANEL
# ====================================================
st.markdown('<div class="pipeline-step">Measurement System Parameters</div>', unsafe_allow_html=True)
with st.container():
    st.markdown('<div class="panel-box">', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        f_sig = st.slider("Signal Frequency (Hz)", 1, 15, 5, key="co_freq")
        f_sample = st.slider("Sampling Rate (Hz)", 2, 30, 8, key="co_rate")
    with c2:
        res = st.selectbox("ADC Resolution", [3, 4, 12], format_func=lambda x: f"{x}-bit ({2**x} Levels)", key="co_res")
        vref = st.slider("Reference Voltage (V)", 1.0, 5.0, 2.5, step=0.1, key="co_vref")
    st.markdown('</div>', unsafe_allow_html=True)

# ====================================================
# DIAGNOSTICS & ALERTS
# ====================================================
sig_center = 1.65
sig_amp = 1.3
is_aliased = f_sample < 2 * f_sig
is_clipped = (sig_center + sig_amp > vref) or (sig_center - sig_amp < 0)
has_high_noise = res == 3
has_range_underutilization = vref >= 4.0

st.markdown('<div class="pipeline-step">System Diagnostic Lock Alerts</div>', unsafe_allow_html=True)
with st.container():
    st.markdown('<div class="panel-box">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if is_aliased:
            st.markdown(f'<div class="agreement-item agreement-fail"><strong>✗ ALIASING DETECTED</strong><br>Sample rate {f_sample} Hz is less than Nyquist rate ({2*f_sig} Hz). High-frequency details are folded back into a false lower frequency.</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="agreement-item agreement-ok"><strong>✓ NYQUIST LOCK</strong><br>Sample rate is sufficient to capture waveforms without folding distortion.</div>', unsafe_allow_html=True)
            
    with col2:
        if is_clipped:
            st.markdown(f'<div class="agreement-item agreement-fail"><strong>✗ SIGNAL CLIPPING</strong><br>Signal peak ({(sig_center + sig_amp):.2f}V) exceeds VREF ({vref:.1f}V). Voltage above VREF is saturated to maximum digital code.</div>', unsafe_allow_html=True)
        elif has_range_underutilization:
            st.markdown(f'<div class="agreement-item agreement-warn"><strong>⚠ UNDER-UTILIZED RANGE</strong><br>VREF ({vref:.1f}V) is much larger than signal peak. Digital counts use only a fraction of dynamic range.</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="agreement-item agreement-ok"><strong>✓ RANGE ALIGNED</strong><br>VREF perfectly envelopes the signal span without saturation or wasteful range.</div>', unsafe_allow_html=True)
            
    with col3:
        if has_high_noise:
            st.markdown('<div class="agreement-item agreement-warn"><strong>⚠ QUANTIZATION STEPS</strong><br>3-bit resolution mesh divides VREF into only 8 steps. Severe rounding error results in coarse signal steps.</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="agreement-item agreement-ok"><strong>✓ LOW QUANTIZATION NOISE</strong><br>Resolution is fine enough to approximate the curve smoothly.</div>', unsafe_allow_html=True)
            
    st.markdown('</div>', unsafe_allow_html=True)

# ====================================================
# WAVEFORM DISPLAY
# ====================================================
st.markdown('<div class="pipeline-step">Measured Reconstructed Signal (Green) vs. True Analog Wave (Gray)</div>', unsafe_allow_html=True)

width = 900
height = 240
padding = 40
plotW = width - 2 * padding
plotH = height - 2 * padding

def get_analog_voltage(t):
    return sig_center + sig_amp * math.sin(2 * math.pi * f_sig * t)

def get_x(t):
    return padding + t * plotW

def get_y(v):
    clamped_v = max(0.0, min(vref, v))
    return height - padding - (clamped_v / vref) * plotH

svg_blocks = []
svg_blocks.append('<rect width="100%" height="100%" fill="none" rx="6" />')

# Ruler lines
svg_blocks.append(f'<line x1="{padding}" y1="{padding}" x2="{width - padding}" y2="{padding}" stroke="rgba(148, 163, 184, 0.15)" stroke-width="1" />')
svg_blocks.append(f'<text x="{padding - 28}" y="{padding + 4}" fill="#64748B" font-family="monospace" font-size="9">{vref:.1f}V</text>')

svg_blocks.append(f'<line x1="{padding}" y1="{height - padding}" x2="{width - padding}" y2="{height - padding}" stroke="rgba(148, 163, 184, 0.15)" stroke-width="1" />')
svg_blocks.append(f'<text x="{padding - 28}" y="{height - padding + 4}" fill="#64748B" font-family="monospace" font-size="9">0V</text>')

# Continuous analog curve (showing clipping reference boundary)
analog_path = ""
steps_count = 300
for i in range(steps_count + 1):
    t = i / steps_count
    v = get_analog_voltage(t)
    x = get_x(t)
    y = get_y(v)
    if i == 0:
        analog_path += f"M {x} {y}"
    else:
        analog_path += f" L {x} {y}"

svg_blocks.append(f'<path d="{analog_path}" fill="none" stroke="rgba(148, 163, 184, 0.2)" stroke-width="2" />')

# Sample logic
steps = 2**res - 1
total_samples = int(f_sample)
sample_points = []
reconstructed_points = []

for i in range(total_samples + 1):
    t = i / f_sample
    if t > 1.0:
        break
    v_anal = get_analog_voltage(t)
    raw_code = round((v_anal / vref) * steps)
    code = max(0, min(steps, raw_code))
    v_quant = (code / steps) * vref
    
    x = get_x(t)
    y_quant = get_y(v_quant)
    
    sample_points.append({"x": x, "y": y_quant})
    
    if i == 0:
        reconstructed_points.append({"x": x, "y": y_quant})
    else:
        reconstructed_points.append({"x": x, "y": sample_points[i-1]["y"]})
        reconstructed_points.append({"x": x, "y": y_quant})

# Timing vertical markers
for pt in sample_points:
    svg_blocks.append(f'<line x1="{pt["x"]}" y1="{padding}" x2="{pt["x"]}" y2="{height - padding}" stroke="rgba(59, 130, 246, 0.12)" stroke-width="1" stroke-dasharray="3,3" />')

# Reconstructed Staircase green trace
staircase_path = ""
for idx, pt in enumerate(reconstructed_points):
    if idx == 0:
        staircase_path += f"M {pt['x']} {pt['y']}"
    else:
        staircase_path += f" L {pt['x']} {pt['y']}"
if len(sample_points) > 0:
    staircase_path += f" L {width - padding} {sample_points[-1]['y']}"

svg_blocks.append(f'<path d="{staircase_path}" fill="none" stroke="#10B981" stroke-width="2" />')

# Red sample dots
for pt in sample_points:
    svg_blocks.append(f'<circle cx="{pt["x"]}" cy="{pt["y"]}" r="3" fill="#EF6868" />')

svg_code = "\n".join(svg_blocks)
st.markdown(f'<div class="edgecase-visual"><svg viewBox="0 0 {width} {height}" style="overflow:visible;">{svg_code}</svg></div>', unsafe_allow_html=True)
