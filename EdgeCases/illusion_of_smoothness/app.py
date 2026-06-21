import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Set dark theme for matplotlib
plt.style.use('dark_background')
fig_color = '#0F172A'
panel_color = '#1E293B'
border_color = 'rgba(148,163,184,0.12)'

st.set_page_config(
    page_title="EdgeCase: The Illusion of Smoothness",
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
    .agreement-item {
        border-radius: 6px;
        padding: 0.6rem;
        margin-bottom: 0.75rem;
        border: 1px solid transparent;
        font-family: 'DM Sans', sans-serif;
    }
    .agreement-ok {
        background: rgba(16, 185, 129, 0.08);
        border-color: rgba(16, 185, 129, 0.2);
        color: #10B981;
    }
    .agreement-warn {
        background: rgba(245, 158, 11, 0.08);
        border-color: rgba(245, 158, 11, 0.2);
        color: #F59E0B;
    }
    .agreement-fail {
        background: rgba(239, 68, 68, 0.08);
        border-color: rgba(239, 68, 68, 0.2);
        color: #EF6868;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("EdgeCase: The Illusion of Smoothness")
st.subheader("How Sequence Timing & Filters Create Continuous Waves")

st.markdown(
    "Adjust the waveform type, resolution, update frequency, and filter cutoff to witness how discrete staircases are integrated into smooth analog curves."
)

# 2-Column Controls
st.markdown('<div class="panel-box">', unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    wave_type = st.selectbox("Waveform Type", ["Sine Wave", "Triangle Wave", "Sawtooth Wave", "Square Wave"])
    res = st.selectbox("DAC Resolution", [3, 4, 8], format_func=lambda x: f"{x}-bit ({2**x} Levels)")

with col2:
    f_update = st.slider("Update Frequency (Hz)", min_value=10, max_value=120, value=30, step=5)
    f_cutoff = st.slider("RC Filter Cutoff (Hz)", min_value=5, max_value=100, value=40, step=5)
st.markdown('</div>', unsafe_allow_html=True)

# Signal parameters (Fixed fundamental signal frequency = 3 Hz)
f_sig = 3
vref = 3.3
sig_center = 1.65
sig_amp = 1.2
steps = 2**res - 1

# Filter evaluations
isFilterTooHigh = f_cutoff > f_update * 0.7
isFilterTooLow = f_cutoff < f_sig * 1.5

# Diagnostics Grid
st.markdown("### System Diagnostic Alert")
if isFilterTooHigh:
    st.markdown(
        f'<div class="agreement-item agreement-warn"><strong>⚠ INSUFFICIENT FILTERING</strong><br>Filter cutoff ({f_cutoff} Hz) is too close to update rate ({f_update} Hz). High-frequency switching staircases remain visible on the output.</div>',
        unsafe_allow_html=True
    )
elif isFilterTooLow:
    st.markdown(
        f'<div class="agreement-item agreement-fail"><strong>✗ SEVERE ATTENUATION</strong><br>Filter cutoff ({f_cutoff} Hz) is too low. The filter blocks our target signal ({f_sig} Hz), leading to massive amplitude loss and phase delay.</div>',
        unsafe_allow_html=True
    )
else:
    st.markdown(
        f'<div class="agreement-item agreement-ok"><strong>✓ RECONSTRUCTION LOCK</strong><br>Cutoff frequency is balanced. High-frequency steps are completely smoothed out while preserving signal amplitude.</div>',
        unsafe_allow_html=True
    )

# Math waveforms calculation
t = np.linspace(0, 1.0, 300)

def get_ideal_wave(times):
    if wave_type == "Sine Wave":
        return sig_center + sig_amp * np.sin(2 * np.pi * f_sig * times)
    elif wave_type == "Triangle Wave":
        period = 1 / f_sig
        phase = (times % period) / period
        val = np.where(phase < 0.5, 4 * phase - 1, 3 - 4 * phase)
        return sig_center + sig_amp * val
    elif wave_type == "Sawtooth Wave":
        period = 1 / f_sig
        phase = (times % period) / period
        return sig_center + sig_amp * (2 * phase - 1)
    else:  # Square Wave
        val = np.where(np.sin(2 * np.pi * f_sig * times) >= 0, 1, -1)
        return sig_center + sig_amp * val

ideal_v = get_ideal_wave(t)

# Stepped DAC output simulation
step_times = np.linspace(0, 1.0, f_update + 1)
step_v_ideal = get_ideal_wave(step_times)
step_codes = np.round((step_v_ideal / vref) * steps)
step_codes = np.clip(step_codes, 0, steps)
step_v_quant = (step_codes / steps) * vref

# Interpolate to create staircase for plotting
staircase_v = []
for ti in t:
    idx = int(ti * f_update)
    clamped_idx = min(idx, len(step_v_quant) - 1)
    staircase_v.append(step_v_quant[clamped_idx])
staircase_v = np.array(staircase_v)

# Low pass filter simulation (RC integration)
dt = 1.0 / len(t)
tau = 1.0 / (2 * np.pi * f_cutoff)
alpha = dt / (tau + dt)

filtered_v = []
y_lpf = get_ideal_wave(0)
for val in staircase_v:
    y_lpf = alpha * val + (1 - alpha) * y_lpf
    filtered_v.append(y_lpf)
filtered_v = np.array(filtered_v)

# Plotting waveforms
fig, ax = plt.subplots(figsize=(8, 3.5), facecolor=fig_color)
ax.set_facecolor(fig_color)

# Ideal wave (dashed gray)
ax.plot(t, ideal_v, color='rgba(148,163,184,0.2)', lw=1.5, ls='--', label='Ideal Continuous Wave')

# Stepped DAC output (red stepped line)
ax.step(t, staircase_v, where='post', color='#EF6868', lw=1.5, alpha=0.8, label='Raw Stepped DAC')

# Filtered Output (green line)
ax.plot(t, filtered_v, color='#10B981', lw=2.5, label='Reconstructed Analog')

ax.set_xlim(0, 1.0)
ax.set_ylim(-0.2, 3.5)
ax.set_xlabel("Time (Seconds)", color='#64748B', fontsize=9)
ax.set_ylabel("Voltage (V)", color='#64748B', fontsize=9)
ax.set_title("Waveform Reconstruction Comparison", color='white', fontsize=11, fontweight='bold')
ax.tick_params(colors='#64748B', labelsize=8)
ax.grid(True, color='rgba(148,163,184,0.05)', linestyle='-')
ax.legend(loc='upper right', facecolor='#1E293B', edgecolor='rgba(148,163,184,0.1)', fontsize=8)

st.pyplot(fig)
plt.close(fig)
