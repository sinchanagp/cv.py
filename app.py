import cv2
import numpy as np
import streamlit as st
from webcolors import CSS3_NAMES_TO_HEX, hex_to_rgb

st.set_page_config(page_title="Color Detector", layout="wide")
st.title("🎨 Smart Color Detection")

# ---------- Closest Color Finder ----------
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

# --------- Camera Input ---------
img = st.camera_input("📷 Take a picture to begin")

if img:
    # Convert to OpenCV format
    file_bytes = np.asarray(bytearray(img.read()), dtype=np.uint8)
    frame = cv2.imdecode(file_bytes, 1)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    st.write("👉 **Tap anywhere on the image to detect color**")

    # Display image
    clicked_image = st.image(frame_rgb, caption="Tap on the image to detect color", use_column_width=True)

    # Use query params to capture click events (mobile supported)
    event = st.experimental_get_query_params()

    if "x" in event and "y" in event:
        x = int(event["x"][0])
        y = int(event["y"][0])

        # Keep inside bounds
        y = min(y, frame_rgb.shape[0] - 1)
        x = min(x, frame_rgb.shape[1] - 1)

        # Extract color from clicked pixel
        r, g, b = frame_rgb[y, x]

        # Get closest named color
        color_name, hex_code, (nr, ng, nb) = closest_color((r, g, b))

        st.subheader("🎯 Detected Color Information")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 📌 Exact Clicked Color")
            st.write(f"RGB: **({r}, {g}, {b})**")
            st.write(
                f"<div style='width:120px;height:120px;border-radius:10px;background-color:rgb({r},{g},{b});border:2px solid #000;'></div>",
                unsafe_allow_html=True,
            )

        with col2:
            st.markdown("### 🌈 Closest Named Color")
            st.write(f"Name: **{color_name}**")
            st.write(f"HEX: **{hex_code}**")
            st.write(
                f"<div style='width:120px;height:120px;border-radius:10px;background-color:{hex_code};border:2px solid #000;'></div>",
                unsafe_allow_html=True,
            )

        st.success("Tap another point on the image to detect a new color!")
