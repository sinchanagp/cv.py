import cv2
import streamlit as st
import numpy as np
from webcolors import hex_to_rgb, CSS3_NAMES_TO_HEX
from PIL import Image

# Function to get closest color name
def closest_color(requested_color):
    r, g, b = map(int, requested_color)
    min_distance = float("inf")
    closest_name = None
    closest_hex = None
    for name, hex_value in CSS3_NAMES_TO_HEX.items():
        r_c, g_c, b_c = hex_to_rgb(hex_value)
        distance = (r_c - r) ** 2 + (g_c - g) ** 2 + (b_c - b) ** 2
        if distance < min_distance:
            min_distance = distance
            closest_name = name
            closest_hex = hex_value
    return closest_name, closest_hex, hex_to_rgb(closest_hex)

# Streamlit UI
st.title("🎨 Real-Time Color Detection App")
st.write("Place an object in front of your camera — the app detects the color at the center.")

# Start camera
run = st.checkbox('Start Camera')
FRAME_WINDOW = st.image([])

cap = cv2.VideoCapture(0)

while run:
    ret, frame = cap.read()
    if not ret:
        st.error("Camera not detected.")
        break

    frame = cv2.resize(frame, (640, 480))
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    h, w, _ = frame.shape
    cx, cy = w // 2, h // 2

    # Define region around center
    box_size = 20
    x1, y1 = cx - box_size, cy - box_size
    x2, y2 = cx + box_size, cy + box_size
    region = rgb_frame[y1:y2, x1:x2]
    avg_color = region.mean(axis=(0, 1)).astype(int)

    color_name, color_hex, (r, g, b) = closest_color(avg_color)

    # Draw region on frame
    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # Create color info box
    info_box = np.zeros((120, 400, 3), dtype=np.uint8)
    info_box[:] = [b, g, r]
    cv2.putText(info_box, f"Name: {color_name}", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
    cv2.putText(info_box, f"HEX: {color_hex.upper()}", (10, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
    cv2.putText(info_box, f"RGB: ({r},{g},{b})", (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)

    # Combine frames side-by-side
    combined = np.vstack((frame, cv2.resize(info_box, (640, 120))))
    FRAME_WINDOW.image(cv2.cvtColor(combined, cv2.COLOR_BGR2RGB))

else:
    cap.release()
    st.write("Camera stopped.")
