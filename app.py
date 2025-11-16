import cv2
import numpy as np
import streamlit as st
from webcolors import CSS3_NAMES_TO_HEX, hex_to_rgb

st.set_page_config(page_title="Real-Time Color Detection", layout="wide")
st.title("🎨 Real-Time Color Detection App (OpenCV + Streamlit)")

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

    return closest_name, closest_hex.upper(), hex_to_rgb(closest_hex)

start_camera = st.checkbox("Start Camera")
frame_window = st.image([])

cap = cv2.VideoCapture(0)

while start_camera:
    ret, frame = cap.read()
    if not ret:
        st.error("Camera not detected.")
        break

    frame = cv2.resize(frame, (640, 480))
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    h, w, _ = rgb.shape
    cx, cy = w // 2, h // 2

    box = 20
    x1, y1 = cx - box, cy - box
    x2, y2 = cx + box, cy + box

    region = rgb[y1:y2, x1:x2]
    avg_color = region.mean(axis=(0, 1)).astype(int)

    color_name, hex_code, (r, g, b) = closest_color(avg_color)

    # Draw center square
    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # Text panel
    info = np.zeros((120, 640, 3), dtype=np.uint8)
    info[:] = (b, g, r)

    cv2.putText(info, f"Color: {color_name}", (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
    cv2.putText(info, f"RGB: ({r},{g},{b})", (10, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
    cv2.putText(info, f"HEX: {hex_code}", (350, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

    # Stack webcam + info
    output = np.vstack((frame, info))
    frame_window.image(cv2.cvtColor(output, cv2.COLOR_BGR2RGB))

cap.release()
