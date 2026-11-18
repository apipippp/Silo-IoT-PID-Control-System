# language: Python, file: conveyor_tracker.py, target: Laptop & Raspberry Pi 3
import os
import sys
import time
import json
import ssl
import urllib.request
import cv2
import numpy as np

PROTOTXT_URL = "https://raw.githubusercontent.com/chuanqi305/MobileNet-SSD/master/deploy.prototxt"
MODEL_URL = "https://github.com/chuanqi305/MobileNet-SSD/raw/master/mobilenet_iter_73000.caffemodel"
PROTOTXT_FILE = "deploy.prototxt"
MODEL_FILE = "mobilenet_iter_73000.caffemodel"

CLASSES = [
    "background", "aeroplane", "bicycle", "bird", "boat",
    "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
    "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
    "sofa", "train", "tvmonitor"
]
CONF_THRESHOLD = 0.45
LINE_RATIO = 0.5


def download_file(url, filename):
    if not os.path.exists(filename):
        print(f"[DOWNLOAD] Mengunduh {filename}...")
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        with urllib.request.urlopen(url, context=ctx) as response, open(filename, 'wb') as out_file:
            out_file.write(response.read())
        print(f"[OK] {filename} siap.")


class CentroidTracker:
    def __init__(self, max_disappeared=15, max_distance=60):
        self.next_id = 0
        self.objects = {}
        self.disappeared = {}
        self.max_disappeared = max_disappeared
        self.max_distance = max_distance

    def register(self, centroid):
        self.objects[self.next_id] = centroid
        self.disappeared[self.next_id] = 0
        self.next_id += 1
        return self.next_id - 1

    def deregister(self, object_id):
        del self.objects[object_id]
        del self.disappeared[object_id]

    def update(self, rects):
        if len(rects) == 0:
            for obj_id in list(self.disappeared.keys()):
                self.disappeared[obj_id] += 1
                if self.disappeared[obj_id] > self.max_disappeared:
                    self.deregister(obj_id)
            return self.objects

        input_centroids = np.zeros((len(rects), 2), dtype="int")
        for i, (startX, startY, endX, endY) in enumerate(rects):
            input_centroids[i] = (int((startX + endX) / 2.0), int((startY + endY) / 2.0))

        if len(self.objects) == 0:
            for i in range(len(input_centroids)):
                self.register(input_centroids[i])
        else:
            object_ids = list(self.objects.keys())
            object_centroids = list(self.objects.values())

            dists = np.linalg.norm(np.array(object_centroids)[:, np.newaxis] - input_centroids, axis=2)
            rows = dists.min(axis=1).argsort()
            cols = dists.argmin(axis=1)[rows]

            used_rows, used_cols = set(), set()
            for (row, col) in zip(rows, cols):
                if row in used_rows or col in used_cols:
                    continue
                if dists[row, col] > self.max_distance:
                    continue

                obj_id = object_ids[row]
                self.objects[obj_id] = input_centroids[col]
                self.disappeared[obj_id] = 0
                used_rows.add(row)
                used_cols.add(col)

            unused_rows = set(range(0, dists.shape[0])).difference(used_rows)
            unused_cols = set(range(0, dists.shape[1])).difference(used_cols)

            for row in unused_rows:
                obj_id = object_ids[row]
                self.disappeared[obj_id] += 1
                if self.disappeared[obj_id] > self.max_disappeared:
                    self.deregister(obj_id)

            for col in unused_cols:
                self.register(input_centroids[col])

        return self.objects


def main():
    download_file(PROTOTXT_URL, PROTOTXT_FILE)
    download_file(MODEL_URL, MODEL_FILE)

    net = cv2.dnn.readNetFromCaffe(PROTOTXT_FILE, MODEL_FILE)
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW) if sys.platform.startswith("win") else cv2.VideoCapture(0)
    if not cap.isOpened():
        cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[ERROR] Kamera tidak terdeteksi.")
        return

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    tracker = CentroidTracker()
    track_positions = {}
    crossed_ids = set()
    total_count = 0
    flash_frames = 0

    print("[READY] Conveyor Line Tracker aktif. Tekan 'q' untuk keluar, 'r' untuk reset.")
    prev_time = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        h, w = frame.shape[:2]
        line_y = int(h * LINE_RATIO)

        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)
        net.setInput(blob)
        detections = net.forward()

        rects = []
        labels_map = {}

        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > CONF_THRESHOLD:
                idx = int(detections[0, 0, i, 1])
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")
                rects.append((startX, startY, endX, endY))
                labels_map[len(rects) - 1] = CLASSES[idx]

                cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 200, 255), 2)

        objects = tracker.update(rects)

        for obj_id, centroid in objects.items():
            cx, cy = centroid
            cv2.circle(frame, (cx, cy), 4, (0, 0, 255), -1)
            cv2.putText(frame, f"ID {obj_id}", (cx - 10, cy - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 255), 1)

            if obj_id in track_positions:
                prev_y = track_positions[obj_id][1]
                if prev_y < line_y <= cy and obj_id not in crossed_ids:
                    crossed_ids.add(obj_id)
                    total_count += 1
                    flash_frames = 6
                    print(f"[COUNT] Item passed! Total: {total_count} (ID {obj_id})")

            track_positions[obj_id] = centroid

        line_color = (0, 255, 0) if flash_frames > 0 else (0, 255, 255)
        if flash_frames > 0:
            flash_frames -= 1
        cv2.line(frame, (0, line_y), (w, line_y), line_color, 2)

        curr_time = time.time()
        fps = 1.0 / (curr_time - prev_time) if (curr_time - prev_time) > 0 else 0
        prev_time = curr_time

        cv2.putText(frame, f"TOTAL COUNT: {total_count} | FPS: {fps:.1f}", (15, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

        cv2.imshow("Conveyor Line Tracker", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('r'):
            total_count = 0
            crossed_ids.clear()
            print("[RESET] Hitungan di-reset ke 0.")

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
