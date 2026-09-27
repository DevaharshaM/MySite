def generate_stepped_points(history):
    pts = []
    step_x = 200.0 / (len(history) - 1)
    for i, val in enumerate(history):
        x = i * step_x
        y = 6 if val == 1 else 24
        if i > 0:
            prev_y = 6 if history[i-1] == 1 else 24
            if prev_y != y:
                pts.append(f"{x:.1f},{prev_y}")
        pts.append(f"{x:.1f},{y}")
    return " ".join(pts)

history = [0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0]
print("Generated points:", generate_stepped_points(history))
