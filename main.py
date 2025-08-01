import cv2
import numpy as np
import torch
import time
import sys
import os
from ultralytics import YOLO

device = "cuda:0" if torch.cuda.is_available() else "cpu"


model = YOLO("yolo11n.pt")


def process_lane(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blur, 50, 150)

    height, width = edges.shape
    mask = np.zeros_like(edges)

    polygon = np.array([[
        (0, height),
        (width, height),
        (width // 2 + 50, height // 2 + 50),
        (width // 2 - 50, height // 2 + 50)
    ]], np.int32)

    cv2.fillPoly(mask, polygon, 255)
    cropped_edges = cv2.bitwise_and(edges, mask)

    lines = cv2.HoughLinesP(cropped_edges, 1, np.pi / 180, threshold=50,
                            minLineLength=50, maxLineGap=50)

    line_image = np.zeros_like(frame)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(line_image, (x1, y1), (x2, y2), (0, 255, 0), 5)

    return cv2.addWeighted(frame, 0.8, line_image, 1, 1)


cap = cv2.VideoCapture('project_video.mp4')

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    start_time = time.time()

    lane_frame = process_lane(frame)
    results = model.predict(lane_frame, device=device, classes=[2, 3, 5, 7])
    plot_frame = results[0].plot()

    end_time = time.time()
    fps = 1 / (end_time - start_time)
    cv2.putText(plot_frame, f'FPS: {fps:.2f}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)

    cv2.imshow('ADAS: Lane + Vehicle Detection', plot_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


