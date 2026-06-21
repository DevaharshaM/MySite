import streamlit as st

# Page configuration
st.set_page_config(
    page_title="PrajnaEdge - PWM: Painting with Time",
    page_icon="🔆",
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
        content: "🔆";
        color: #10B981;
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

st.title("EdgeCase: Painting with Time")
st.subheader("Pulse Width Modulation (PWM) and Average Power Integration")
st.caption("Adjust the frequency and duty cycle to inspect how digital pulses simulate analog voltages, driving physical loads like LEDs and DC motors.")

# ====================================================
# CONFIGURATION PANEL
# ====================================================
st.markdown('<div class="pipeline-step">PWM Waveform Configuration</div>', unsafe_allow_html=True)
with st.container():
    st.markdown('<div class="panel-box">', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        freq = st.selectbox(
            "PWM Frequency",
            [50, 500, 2000, 10000],
            format_func=lambda x: f"{x} Hz ({'Servo Motor' if x==50 else 'Standard Arduino PWM' if x==500 else 'Audible motor drive' if x==2000 else 'Ultrasonic dimming'})",
            key="pwm_freq"
        )
    with c2:
        duty = st.slider("Duty Cycle (0% to 100%)", 0, 100, 50, key="pwm_duty")
    st.markdown('</div>', unsafe_allow_html=True)

# ====================================================
# LOADS PANEL
# ====================================================
spin_duration = f"{max(0.1, 2.0 - (duty/100)*1.9):.2f}s"
spin_animation = f"animation: spin {spin_duration} linear infinite;" if duty > 0 else ""
led_opacity = duty / 100.0

st.markdown('<div class="pipeline-step">Output Loads Simulation</div>', unsafe_allow_html=True)
st.markdown("""
<div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap:1.5rem; margin-bottom:1.5rem;">
  <div>
    <div class="pipeline-step">Output Load 1: Dimmable LED</div>
    <div class="panel-box" style="height:150px; display:flex; flex-direction:column; justify-content:center; align-items:center; background:#0F172A;">
      <svg width="60" height="80" viewBox="0 0 60 80" style="overflow:visible;">
        <path d="M 15 45 L 15 35 C 15 20 45 20 45 35 L 45 45 Z" fill="#1E293B" stroke="rgba(148, 163, 184, 0.12)" stroke-width="2" />
        <path d="M 15 45 L 15 35 C 15 20 45 20 45 35 L 45 45 Z" fill="#10B981" opacity="{led_opacity}" style="filter: drop-shadow(0px 0px 12px #10B981);" />
        <rect x="20" y="45" width="20" height="6" fill="#64748B" rx="1" />
        <line x1="25" y1="51" x2="25" y2="75" stroke="#94A3B8" stroke-width="2" />
        <line x1="35" y1="51" x2="35" y2="75" stroke="#94A3B8" stroke-width="2" />
      </svg>
      <div style="font-family:monospace; font-size:0.75rem; color:#E2E8F0; margin-top:0.75rem;">LED Brightness: {duty}%</div>
    </div>
  </div>
  <div>
    <div class="pipeline-step">Output Load 2: DC Fan Motor</div>
    <div class="panel-box" style="height:150px; display:flex; flex-direction:column; justify-content:center; align-items:center; background:#0F172A;">
      <svg width="90" height="90" viewBox="0 0 100 100" style="overflow:visible;">
        <style>
          @keyframes spin {{
            from {{ transform: rotate(0deg); }}
            to {{ transform: rotate(360deg); }}
          }}
          .spinning-fan {{
            transform-origin: 50px 50px;
            {spin_animation}
          }}
        </style>
        <circle cx="50" cy="50" r="45" fill="none" stroke="rgba(148, 163, 184, 0.12)" stroke-width="2" />
        <circle cx="50" cy="50" r="10" fill="#334155" />
        <g class="spinning-fan">
          <path d="M 50 40 C 40 30 40 10 50 10 C 60 10 60 30 50 40 Z" fill="#E2E8F0" />
          <path d="M 60 50 C 70 40 90 40 90 50 C 90 60 70 60 60 50 Z" fill="#E2E8F0" />
          <path d="M 50 60 C 60 70 60 90 50 90 C 40 90 40 70 50 60 Z" fill="#E2E8F0" />
          <path d="M 40 50 C 30 60 10 60 10 50 C 10 40 30 40 40 50 Z" fill="#E2E8F0" />
        </g>
      </svg>
      <div style="font-family:monospace; font-size:0.75rem; color:#E2E8F0; margin-top:0.75rem;">Fan RPM: ~{int(3000 * (duty/100))} RPM</div>
    </div>
  </div>
</div>
""".format(led_opacity=led_opacity, duty=duty, spin_animation=spin_animation), unsafe_allow_html=True)

# ====================================================
# WAVEFORM DISPLAY
# ====================================================
st.markdown('<div class="pipeline-step">Inspected Pulse Waveform (Time domain)</div>', unsafe_allow_html=True)

width = 900
height = 140
padding = 40
cycle_width = 175
high_y = 20
low_y = height - 20
start_x = padding
end_x = width - padding

svg_blocks = []
svg_blocks.append('<rect width="100%" height="100%" fill="none" rx="6" />')
svg_blocks.append(f'<line x1="{padding}" y1="{low_y}" x2="{width - padding}" y2="{low_y}" stroke="rgba(148, 163, 184, 0.15)" stroke-width="1" />')
svg_blocks.append(f'<line x1="{padding}" y1="{high_y}" x2="{width - padding}" y2="{high_y}" stroke="rgba(148, 163, 184, 0.15)" stroke-dasharray="3,3" stroke-width="1" />')
svg_blocks.append(f'<text x="{padding - 30}" y="24" fill="#64748B" font-family="monospace" font-size="10">3.3V</text>')
svg_blocks.append(f'<text x="{padding - 30}" y="{height - 16}" fill="#64748B" font-family="monospace" font-size="10">0V</text>')

path_d = ""
for x in range(start_x, end_x + 1):
    cycle_x = (x - start_x) % cycle_width
    progress = cycle_x / cycle_width
    is_high = progress < (duty / 100.0)
    y = high_y if is_high else low_y
    
    if x == start_x:
        path_d += f"M {x} {y}"
    else:
        prev_cycle_x = (x - 1 - start_x) % cycle_width
        prev_progress = prev_cycle_x / cycle_width
        prev_high = prev_progress < (duty / 100.0)
        
        if is_high != prev_high:
            path_d += f" L {x} {low_y if prev_high else high_y} L {x} {y}"
        else:
            path_d += f" L {x} {y}"

svg_blocks.append(f'<path d="{path_d}" fill="none" stroke="#10B981" stroke-width="2.5" />')

svg_code = "\n".join(svg_blocks)
st.markdown(f'<div class="edgecase-visual"><svg viewBox="0 0 {width} {height}" style="overflow:visible;">{svg_code}</svg></div>', unsafe_allow_html=True)

# ====================================================
# STATS PANEL
# ====================================================
period_s = 1 / freq
period_ms = period_s * 1000
period_us = period_s * 1000000

ton_ms = period_ms * (duty / 100.0)
ton_us = period_us * (duty / 100.0)

toff_ms = period_ms * ((100 - duty) / 100.0)
toff_us = period_us * ((100 - duty) / 100.0)

v_avg = 3.3 * (duty / 100.0)

st.markdown('<div class="pipeline-step">Timing & Signal Metrics</div>', unsafe_allow_html=True)
with st.container():
    st.markdown('<div class="panel-box">', unsafe_allow_html=True)
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f'<div class="metric-box"><div class="metric-label">Signal Period (T)</div><div class="metric-val">{period_ms:.2f} ms ({int(period_us)} µs)</div></div>', unsafe_allow_html=True)
    with m2:
        st.markdown(f'<div class="metric-box"><div class="metric-label">On-Time / Pulse Width (T_on)</div><div class="metric-val">{ton_ms:.2f} ms ({int(ton_us)} µs)</div></div>', unsafe_allow_html=True)
    with m3:
        st.markdown(f'<div class="metric-box"><div class="metric-label">Off-Time (T_off)</div><div class="metric-val">{toff_ms:.2f} ms ({int(toff_us)} µs)</div></div>', unsafe_allow_html=True)
    with m4:
        st.markdown(f'<div class="metric-box"><div class="metric-label">Equivalent DC Voltage</div><div class="metric-val">{v_avg:.2f} V (at 3.3V reference)</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
