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