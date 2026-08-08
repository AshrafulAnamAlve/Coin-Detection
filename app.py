import streamlit as st
import cv2
import numpy as np

# Graphics Algorithms

def put_pixel(img, x, y, color):
    h, w = img.shape[:2]
    for i in range(-1, 2):
        for j in range(-1, 2):
            if 0 <= y + i < h and 0 <= x + j < w:
                img[y + i, x + j] = color


# Midpoint Circle Algorithm
def midpoint_circle(img, cx, cy, r, color):
    x = 0
    y = r
    p = 1 - r

    while x <= y:
        put_pixel(img, cx + x, cy + y, color)
        put_pixel(img, cx - x, cy + y, color)
        put_pixel(img, cx + x, cy - y, color)
        put_pixel(img, cx - x, cy - y, color)
        put_pixel(img, cx + y, cy + x, color)
        put_pixel(img, cx - y, cy + x, color)
        put_pixel(img, cx + y, cy - x, color)
        put_pixel(img, cx - y, cy - x, color)

        x += 1
        if p < 0:
            p = p + 2 * x + 1
        else:
            y -= 1
            p = p + 2 * x - 2 * y + 1


# Bresenham Line Algorithm
def bresenham_line(img, x1, y1, x2, y2, color):
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x2 > x1 else -1
    sy = 1 if y2 > y1 else -1

    x = x1
    y = y1

    if dx > dy:
        p = 2 * dy - dx
        for _ in range(dx + 1):
            put_pixel(img, x, y, color)
            x += sx
            if p < 0:
                p += 2 * dy
            else:
                y += sy
                p += 2 * dy - 2 * dx
    else:
        p = 2 * dx - dy
        for _ in range(dy + 1):
            put_pixel(img, x, y, color)
            y += sy
            if p < 0:
                p += 2 * dx
            else:
                x += sx
                p += 2 * dx - 2 * dy


def draw_center_mark(img, cx, cy, size, color):
    bresenham_line(img, cx - size, cy - size, cx + size, cy + size, color)
    bresenham_line(img, cx - size, cy + size, cx + size, cy - size, color)

st.title("Coin Detection and Counting System")
st.write("Upload an image of coins on a plain background.")

min_area = st.slider("Minimum coin area", 100, 5000, 800, step=100)

file = st.file_uploader("Upload image", type=["jpg", "jpeg", "png"])

if file is not None:

    data = np.asarray(bytearray(file.read()), dtype=np.uint8)
    image = cv2.imdecode(data, cv2.IMREAD_COLOR)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    blur = cv2.GaussianBlur(gray, (7, 7), 0)

    _, thresh = cv2.threshold(
        blur,
        0,
        255,
        cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
    )

    kernel = np.ones((5, 5), np.uint8)

    clean = cv2.morphologyEx(
        thresh,
        cv2.MORPH_OPEN,
        kernel,
        iterations=2
    )

    contours, _ = cv2.findContours(
        clean,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    count = 0
    output = image.copy()

    for cnt in contours:
        if cv2.contourArea(cnt) > min_area:
            count += 1

            (x, y), radius = cv2.minEnclosingCircle(cnt)
            cx, cy, r = int(x), int(y), int(radius)

            midpoint_circle(output, cx, cy, r, (0, 255, 0))

            draw_center_mark(
                output,
                cx,
                cy,
                int(r / 3),
                (255, 0, 0)
            )

            cv2.putText(
                output,
                str(count),
                (cx - 10, cy - r - 8),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                2
            )

    st.subheader("Original image")
    st.image(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    st.subheader("Detected coins (Midpoint Circle + Bresenham Line)")
    st.image(cv2.cvtColor(output, cv2.COLOR_BGR2RGB))

    st.subheader("After thresholding")
    st.image(clean)

    st.success(f"Total coins detected: {count}")