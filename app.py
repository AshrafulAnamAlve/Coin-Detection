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