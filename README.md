Real-Time Color Detection using OpenCV

This project uses your webcam to detect and display the closest color name, HEX, and RGB values of the color appearing at the center of the video frame. It provides a live color recognition experience using OpenCV and the webcolors library.

📸 Features

Real-time color detection using your webcam.

Detects the average color of a small region in the center of the frame.

Displays:

Closest color name (from CSS3 color names).

HEX code and RGB values of the detected color.

Visual color sample box showing the detected color.

Press q to exit the program.

🧠 How It Works

The webcam captures video frames.

The frame is converted from BGR to RGB format.

A small square region at the center of the frame is analyzed.

The average color of that region is calculated.

The code finds the closest matching color name from the CSS3 color dataset using Euclidean distance.

The detected color info is displayed in real-time on the video feed.
