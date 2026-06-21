import streamlit as st
import math

# Set page config
st.set_page_config(
    page_title="PrajnaEdge - Timer: The Race Against Time",
    page_icon="⏱️",
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
        content: "⏱️";
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
</style>
""", unsafe_allow_html=True)

st.title("EdgeCase: The Race Against Time")
st.subheader("Configuring Hardware Timer Registers & Waveform Generation")
st.caption("Interact with clock prescalers, auto-reload value (ARR), and compare match threshold (CCR) to see how digital signals are structured in hardware.")

# ====================================================
# CONFIGURATION PANEL (REGISTER SETTINGS)
# ====================================================
st.markdown('<div class="pipeline-step">Register Configurations</div>', unsafe_allow_html=True)
with st.container():
    st.markdown('<div class="panel-box">', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    
    with c1:
        f_osc = st.selectbox(
            "Clock Source Frequency",
            [1000000, 8000000, 16000000],
            format_func=lambda x: f"{x // 1000000} MHz ({'Internal Osc' if x==1000000 else 'HSE Crystal' if x==8000000 else 'PLL Speed'})",
            key="tb_clk"
        )
        psc = st.slider("Prescaler (PSC Register Value)", 0, 1000, 9, key="tb_psc")
        
    with c2:
        bits = st.selectbox("Counter Register Size", [8, 16], format_func=lambda x: f"{x}-bit (Max: {2**x - 1})", key="tb_bits")
        max_arr = 255 if bits == 8 else 2000
        arr = st.slider("Auto-Reload (ARR Register)", 1, max_arr, 99, key="tb_arr")
        
    with c3:
        ccr = st.slider("Compare Value (CCR Register)", 0, arr, min(49, arr), key="tb_ccr")
        
    st.markdown('</div>', unsafe_allow_html=True)

# ====================================================
# CALCULATIONS
# ====================================================
div_ratio = psc + 1
f_cnt = f_osc / div_ratio
f_arr = f_cnt / (arr + 1)
period_ms = 1000 / f_arr
duty_percent = (ccr / arr * 100) if arr > 0 else 0

st.markdown('<div class="pipeline-step">Calculated Technical Metrics</div>', unsafe_allow_html=True)
with st.container():
    st.markdown('<div class="panel-box">', unsafe_allow_html=True)
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f'<div class="metric-box"><div class="metric-label">Divider Ratio (PSC+1)</div><div class="metric-val">{div_ratio}</div></div>', unsafe_allow_html=True)
    with m2:
        f_cnt_str = f"{f_cnt/1000000:.2f} MHz" if f_cnt >= 1000000 else f"{f_cnt/1000:.2f} kHz"
        st.markdown(f'<div class="metric-box"><div class="metric-label">Counter Frequency (f_CNT)</div><div class="metric-val">{f_cnt_str}</div></div>', unsafe_allow_html=True)
    with m3:
        f_arr_str = f"{f_arr/1000:.2f} kHz" if f_arr >= 1000 else f"{f_arr:.2f} Hz"
        st.markdown(f'<div class="metric-box"><div class="metric-label">Overflow Frequency (Interrupt)</div><div class="metric-val">{f_arr_str} ({period_ms:.3f} ms)</div></div>', unsafe_allow_html=True)
    with m4:
        st.markdown(f'<div class="metric-box"><div class="metric-label">Compare Match Duty Cycle</div><div class="metric-val">{duty_percent:.1f}% (CCR/ARR)</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ====================================================
# WAVEFORM DISPLAY
# ====================================================
st.markdown('<div class="pipeline-step">Hardware Counting & Signal Generation Waveform</div>', unsafe_allow_html=True)

# Render SVG
width = 900
height = 240
padding = 40
chart_y_top = 30
chart_y_bottom = 120
chart_height = chart_y_bottom - chart_y_top
period_width = 200

svg_blocks = []
grid_pattern = """
<defs>
  <pattern id="tb-grid" width="20" height="20" patternUnits="userSpaceOnUse">
    <path d="M 20 0 L 0 0 0 20" fill="none" stroke="rgba(148,163,184,0.03)" stroke-width="1"/>
  </pattern>
</defs>
<rect width="100%" height="100%" fill="url(#tb-grid)" rx="6" />
"""
svg_blocks.append(grid_pattern)

# ARR line
svg_blocks.append(f'<line x1="{padding}" y1="{chart_y_top}" x2="{width - padding}" y2="{chart_y_top}" stroke="rgba(239, 68, 68, 0.4)" stroke-dasharray="3,3" stroke-width="1.5" />')
svg_blocks.append(f'<text x="{width - padding + 5}" y="{chart_y_top + 4}" fill="rgba(239, 68, 68, 0.8)" font-family="monospace" font-size="10">ARR ({arr})</text>')

# CCR line
ccr_y = chart_y_bottom - (ccr / arr) * chart_height if arr > 0 else chart_y_bottom
svg_blocks.append(f'<line x1="{padding}" y1="{ccr_y}" x2="{width - padding}" y2="{ccr_y}" stroke="rgba(59, 130, 246, 0.6)" stroke-dasharray="4,2" stroke-width="1.5" />')
svg_blocks.append(f'<text x="{width - padding + 5}" y="{ccr_y + 4}" fill="rgba(59, 130, 246, 0.9)" font-family="monospace" font-size="10">CCR ({ccr})</text>')

# 0 line
svg_blocks.append(f'<line x1="{padding}" y1="{chart_y_bottom}" x2="{width - padding}" y2="{chart_y_bottom}" stroke="rgba(148, 163, 184, 0.15)" stroke-width="1" />')
svg_blocks.append(f'<text x="{padding - 25}" y="{chart_y_bottom + 4}" fill="#64748B" font-family="monospace" font-size="10">0</text>')

# Generate Sawtooth CNT
path_d = ""
overflows = []
matches = []
start_x = padding
end_x = width - padding

for x in range(start_x, end_x + 1):
    cycle_x = (x - start_x) % period_width
    progress = cycle_x / period_width
    y = chart_y_bottom - progress * chart_height
    
    if x == start_x:
        path_d += f"M {x} {y}"
    else:
        prev_cycle_x = (x - 1 - start_x) % period_width
        if cycle_x < prev_cycle_x:
            path_d += f" L {x} {chart_y_bottom} M {x} {chart_y_bottom - chart_height}"
            overflows.append(x)
        else:
            path_d += f" L {x} {y}"
            
    # CCR Match detection
    prev_cnt = (prev_cycle_x / period_width) * arr
    curr_cnt = progress * arr
    if prev_cnt <= ccr < curr_cnt:
        matches.append(x)

svg_blocks.append(f'<path d="{path_d}" fill="none" stroke="#E2E8F0" stroke-width="2" />')

# PWM Out line
out_y_top = 150
out_y_bottom = 190
pwm_path_d = ""

for x in range(start_x, end_x + 1):
    cycle_x = (x - start_x) % period_width
    progress = cycle_x / period_width
    curr_cnt = progress * arr
    is_high = curr_cnt < ccr
    y = out_y_top if is_high else out_y_bottom
    
    if x == start_x:
        pwm_path_d += f"M {x} {y}"
    else:
        prev_cycle_x = (x - 1 - start_x) % period_width
        prev_cnt = (prev_cycle_x / period_width) * arr
        prev_high = prev_cnt < ccr
        if is_high != prev_high:
            pwm_path_d += f" L {x} {out_y_bottom if prev_high else out_y_top} L {x} {y}"
        else:
            pwm_path_d += f" L {x} {y}"

svg_blocks.append(f'<line x1="{padding}" y1="{out_y_bottom}" x2="{width - padding}" y2="{out_y_bottom}" stroke="rgba(148, 163, 184, 0.15)" stroke-width="1" />')
svg_blocks.append(f'<text x="{padding - 30}" y="{out_y_bottom - 10}" fill="#10B981" font-family="monospace" font-size="10">PWM</text>')
svg_blocks.append(f'<text x="{padding - 30}" y="{out_y_top + 10}" fill="#10B981" font-family="monospace" font-size="10">OUT</text>')
svg_blocks.append(f'<path d="{pwm_path_d}" fill="none" stroke="#10B981" stroke-width="2" />')

# Event circles
for mx in matches:
    svg_blocks.append(f'<line x1="{mx}" y1="{chart_y_top}" x2="{mx}" y2="{chart_y_bottom}" stroke="rgba(59, 130, 246, 0.2)" stroke-width="1" stroke-dasharray="2,2" />')
    svg_blocks.append(f'<circle cx="{mx}" cy="{chart_y_bottom - (ccr / arr) * chart_height if arr > 0 else chart_y_bottom}" r="4" fill="#3B82F6" />')
    svg_blocks.append(f'<path d="M {mx - 5} 140 L {mx} 133 L {mx + 5} 140 Z" fill="#3B82F6" />')

for ox in overflows:
    svg_blocks.append(f'<line x1="{ox}" y1="{chart_y_top}" x2="{ox}" y2="{chart_y_bottom}" stroke="rgba(239, 68, 68, 0.2)" stroke-width="1" stroke-dasharray="2,2" />')
    svg_blocks.append(f'<circle cx="{ox}" cy="{chart_y_bottom}" r="4" fill="#EF6868" />')
    svg_blocks.append(f'<text x="{ox - 24}" y="{chart_y_top - 6}" fill="#EF6868" font-family="monospace" font-size="8">OVERFLOW</text>')

svg_code = "\n".join(svg_blocks)
st.markdown(f'<div class="edgecase-visual"><svg viewBox="0 0 {width} {height}" style="overflow:visible;">{svg_code}</svg></div>', unsafe_allow_html=True)
