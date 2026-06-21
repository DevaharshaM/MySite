import streamlit as st
import math

# Page configuration
st.set_page_config(
    page_title="PrajnaEdge - ADC: Capturing Reality",
    page_icon="📡",
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
        content: "📡";
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
    .metric-box {
        background: #0F172A;
        border: 1px solid rgba(148, 163, 184, 0.08);
        border-radius: 6px;
        padding: 0.75rem;
    }
    .metric-label {
        font-family: monospace;
        font-size: 0.65rem;
        color: #64748B;
        text-transform: uppercase;
        margin-bottom: 0.25rem;
    }
    .metric-val {
        font-family: monospace;
        font-size: 0.95rem;
        color: #FFF;
        font-weight: bold;
    }
    .terminal-box {
        background: #0F172A;
        border: 1px solid rgba(148, 163, 184, 0.12);
        border-radius: 8px;
        padding: 0.8rem;
        font-family: monospace;
        font-size: 0.72rem;
        height: 180px;
        overflow-y: auto;
        line-height: 1.5;
        color: #A5F3FC;
    }
</style>
""", unsafe_allow_html=True)

st.title("EdgeCase: Capturing Reality")
st.subheader("Slicing Time & Quantizing Voltages into Binary Reality")
st.caption("Adjust signal frequency, amplitude, ADC resolution, and sampling rate to see how reality is sliced in time and quantized in levels.")

# ====================================================
# CONFIGURATION PANEL
# ====================================================
st.markdown('<div class="pipeline-step">Signal & Converter Configuration</div>', unsafe_allow_html=True)
with st.container():
    st.markdown('<div class="panel-box">', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    
    with c1:
        sig_type = st.selectbox(
            "Signal Type",
            ["sine", "triangle", "sawtooth", "noisy"],
            format_func=lambda x: f"{x.capitalize()} Wave",
            key="cr_type"
        )
        f_sig = st.slider("Signal Frequency (Hz)", 1, 10, 3, key="cr_freq")
        
    with c2:
        amp = st.slider("Signal Amplitude (V)", 0.5, 1.65, 1.25, step=0.1, key="cr_amp")
        res = st.selectbox("ADC Resolution", [3, 4, 8], format_func=lambda x: f"{x}-bit ({2**x} Levels)", key="cr_res")
        
    with c3:
        f_sample = st.slider("Sampling Rate (Hz)", 5, 80, 20, key="cr_rate")
        
    st.markdown('</div>', unsafe_allow_html=True)

# ====================================================
# CALCULATIONS
# ====================================================
steps = 2**res - 1
lsb = (3.3 / steps) * 1000  # in mV
sample_period_ms = 1000 / f_sample
nyquist = 2 * f_sig
satisfies_nyquist = f_sample >= nyquist

st.markdown('<div class="pipeline-step">Sensing Metrics</div>', unsafe_allow_html=True)
with st.container():
    st.markdown('<div class="panel-box">', unsafe_allow_html=True)
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f'<div class="metric-box"><div class="metric-label">Step Size (LSB)</div><div class="metric-val">{lsb:.1f} mV</div></div>', unsafe_allow_html=True)
    with m2:
        st.markdown(f'<div class="metric-box"><div class="metric-label">Sampling Period</div><div class="metric-val">{sample_period_ms:.1f} ms</div></div>', unsafe_allow_html=True)
    with m3:
        st.markdown(f'<div class="metric-box"><div class="metric-label">Nyquist Threshold</div><div class="metric-val">{nyquist} Hz</div></div>', unsafe_allow_html=True)
    with m4:
        nyq_status = '<span style="color:#10B981;">✓ Met</span>' if satisfies_nyquist else '<span style="color:#EF6868;">✗ Violated</span>'
        st.markdown(f'<div class="metric-box"><div class="metric-label">Nyquist Criteria</div><div class="metric-val">{nyq_status}</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ====================================================
# WAVEFORM GENERATION & PLOT
# ====================================================
st.markdown('<div class="pipeline-step">Reconstructed Waveform (Green) vs. Original Analog (Gray)</div>', unsafe_allow_html=True)

width = 900
height = 240
padding = 40
plotW = width - 2 * padding
plotH = height - 2 * padding

# Evaluate physical voltage centered at 1.65V
def get_analog_voltage(t):
    center = 1.65
    if sig_type == "sine":
        return center + amp * math.sin(2 * math.pi * f_sig * t)
    elif sig_type == "triangle":
        period = 1 / f_sig
        phase = (t % period) / period
        val = (4 * phase - 1) if phase < 0.5 else (3 - 4 * phase)
        return center + amp * val
    elif sig_type == "sawtooth":
        period = 1 / f_sig
        phase = (t % period) / period
        return center + amp * (2 * phase - 1)
    else:
        # noisy
        s1 = math.sin(2 * math.pi * f_sig * t)
        s2 = 0.3 * math.sin(2 * math.pi * (f_sig * 2.3) * t + 1.2)
        n = 0.15 * math.sin(100 * t)
        return center + (amp / 1.3) * (s1 + s2 + n)

def get_x(t):
    return padding + t * plotW

def get_y(v):
    clamped_v = max(0.0, min(3.3, v))
    return height - padding - (clamped_v / 3.3) * plotH

svg_blocks = []
grid_pattern = """
<defs>
  <pattern id="cr-grid" width="20" height="20" patternUnits="userSpaceOnUse">
    <path d="M 20 0 L 0 0 0 20" fill="none" stroke="rgba(148,163,184,0.03)" stroke-width="1"/>
  </pattern>
</defs>
<rect width="100%" height="100%" fill="url(#cr-grid)" rx="6" />
"""
svg_blocks.append(grid_pattern)

# Ruler lines
svg_blocks.append(f'<line x1="{padding}" y1="{padding}" x2="{width - padding}" y2="{padding}" stroke="rgba(148, 163, 184, 0.15)" stroke-width="1" />')
svg_blocks.append(f'<text x="{padding - 28}" y="{padding + 4}" fill="#64748B" font-family="monospace" font-size="9">3.3V</text>')

svg_blocks.append(f'<line x1="{padding}" y1="{height - padding}" x2="{width - padding}" y2="{height - padding}" stroke="rgba(148, 163, 184, 0.15)" stroke-width="1" />')
svg_blocks.append(f'<text x="{padding - 28}" y="{height - padding + 4}" fill="#64748B" font-family="monospace" font-size="9">0V</text>')

svg_blocks.append(f'<line x1="{padding}" y1="{height / 2}" x2="{width - padding}" y2="{height / 2}" stroke="rgba(148, 163, 184, 0.08)" stroke-width="1" stroke-dasharray="2,2" />')
svg_blocks.append(f'<text x="{padding - 33}" y="{height / 2 + 4}" fill="#64748B" font-family="monospace" font-size="9">1.65V</text>')

# Continuous analog curve
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

svg_blocks.append(f'<path d="{analog_path}" fill="none" stroke="rgba(148, 163, 184, 0.3)" stroke-width="2" />')

# Sample logic
total_samples = int(f_sample)
sample_points = []
reconstructed_points = []
log_lines = []

for i in range(total_samples + 1):
    t = i / f_sample
    if t > 1.0:
        break
    v_anal = get_analog_voltage(t)
    raw_code = round((v_anal / 3.3) * steps)
    code = max(0, min(steps, raw_code))
    v_quant = (code / steps) * 3.3
    
    x = get_x(t)
    y_quant = get_y(v_quant)
    
    sample_points.append({"x": x, "y": y_quant, "t": t, "v_anal": v_anal, "v_quant": v_quant, "code": code})
    
    if i == 0:
        reconstructed_points.append({"x": x, "y": y_quant})
    else:
        reconstructed_points.append({"x": x, "y": sample_points[i-1]["y"]})
        reconstructed_points.append({"x": x, "y": y_quant})
        
    time_ms = t * 1000
    bin_code = bin(code)[2:].zfill(res)
    hex_code = hex(code)[2:].upper().zfill(2)
    log_lines.append(f"[{time_ms:.1f}ms] Vin = {v_anal:.3f}V -> ADC: {code} (0b{bin_code} / 0x{hex_code}) -> Vout = {v_quant:.3f}V")

# Timing vertical markers
for pt in sample_points:
    svg_blocks.append(f'<line x1="{pt["x"]}" y1="{padding}" x2="{pt["x"]}" y2="{height - padding}" stroke="rgba(59, 130, 246, 0.15)" stroke-width="1" stroke-dasharray="3,3" />')

# Step staircase green trace
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
    svg_blocks.append(f'<circle cx="{pt["x"]}" cy="{pt["y"]}" r="3.5" fill="#EF6868" />')
    svg_blocks.append(f'<circle cx="{pt["x"]}" cy="{pt["y"]}" r="6" fill="none" stroke="#EF6868" stroke-width="1" opacity="0.4" />')

svg_code = "\n".join(svg_blocks)
st.markdown(f'<div class="edgecase-visual"><svg viewBox="0 0 {width} {height}" style="overflow:visible;">{svg_code}</svg></div>', unsafe_allow_html=True)

# ====================================================
# LOGS TABLE
# ====================================================
st.markdown('<div class="pipeline-step">Digital Output Buffer Log</div>', unsafe_allow_html=True)
log_html = "".join([f"<div>{line}</div>" for line in log_lines])
st.markdown(f'<div class="terminal-box">{log_html}</div>', unsafe_allow_html=True)
