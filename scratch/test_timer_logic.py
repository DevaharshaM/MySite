def simulate_tick(source, timerId, mode, state):
    # state is a dict: {'th': int, 'tl': int, 'tf': int, 'pin': int, 'history': list}
    if mode == 1:
        # 16-bit counter
        count = (state['th'] << 8) | state['tl']
        count += 1
        if count > 0xFFFF:
            count = 0
            state['tf'] = 1
            state['pin'] = 1 if state['pin'] == 0 else 0
            event = "16-BIT OVERFLOW ROLLOVER (FFFFH -> 0000H)"
        else:
            state['tf'] = 0
            event = f"Count: {count:04X}H"
        state['th'] = (count >> 8) & 0xFF
        state['tl'] = count & 0xFF
    elif mode == 2:
        # 8-bit auto-reload
        # tl increments, th stays fixed as reload value
        tl = state['tl'] + 1
        if tl > 0xFF:
            state['tf'] = 1
            state['pin'] = 1 if state['pin'] == 0 else 0
            # Auto-reload!
            state['tl'] = state['th']
            event = f"8-BIT OVERFLOW! Auto-reloaded TL{timerId} from TH{timerId} ({state['th']:02X}H)"
        else:
            state['tf'] = 0
            state['tl'] = tl
            event = f"TL{timerId} count: {tl:02X}H"
    return event

# Test Mode 1
s1 = {'th': 0xFF, 'tl': 0xF8, 'tf': 0, 'pin': 0, 'history': []}
print("Testing Mode 1:")
for i in range(10):
    ev = simulate_tick('timer', 0, 1, s1)
    print(f"Step {i+1}: {ev}, TH0={s1['th']:02X}H, TL0={s1['tl']:02X}H, TF0={s1['tf']}, Pin={s1['pin']}")

# Test Mode 2
s2 = {'th': 0xD0, 'tl': 0xFD, 'tf': 0, 'pin': 0, 'history': []}
print("\nTesting Mode 2 (Auto-Reload):")
for i in range(5):
    ev = simulate_tick('timer', 0, 2, s2)
    print(f"Step {i+1}: {ev}, TH0={s2['th']:02X}H, TL0={s2['tl']:02X}H, TF0={s2['tf']}, Pin={s2['pin']}")
