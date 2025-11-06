import cv2
from webcolors import hex_to_rgb, CSS3_NAMES_TO_HEX

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


# Open webcam
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (640, 480))
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    h, w, _ = frame.shape
    cx, cy = w // 2, h // 2

    # Define region size around center
    box_size = 20
    x1, y1 = cx - box_size, cy - box_size
    x2, y2 = cx + box_size, cy + box_size

    # Take region around center
    region = rgb_frame[y1:y2, x1:x2]
    avg_color = region.mean(axis=(0, 1)).astype(int)

    color_name, color_hex, (r, g, b) = closest_color(avg_color)

    # Draw a filled rectangle (color sample box)
    cv2.rectangle(frame, (10, 10), (200, 110), (int(b), int(g), int(r)), -1)

    # Text details (in black)
    text_color = (0, 0, 0)
    cv2.putText(frame, f"Name: {color_name}", (15, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, text_color, 2)
    cv2.putText(frame, f"HEX: {color_hex.upper()}", (15, 70),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, text_color, 2)
    cv2.putText(frame, f"RGB: ({r},{g},{b})", (15, 100),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, text_color, 2)

    # Draw a green rectangle at the center region
    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    cv2.imshow("Color Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
