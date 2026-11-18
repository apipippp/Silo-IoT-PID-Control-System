# language: Python, file: test_detection.py, target: Laptop (Windows/Mac/Linux) & Raspberry Pi 3
# Cara install dependensi di laptop:
# pip install opencv-python numpy

import os
import sys
import time
import ssl
import urllib.request
import cv2
import numpy as np

# File model Caffe MobileNet-SSD (ringan & cepat)
PROTOTXT_URL = "https://raw.githubusercontent.com/chuanqi305/MobileNet-SSD/master/deploy.prototxt"
MODEL_URL = "https://github.com/chuanqi305/MobileNet-SSD/raw/master/mobilenet_iter_73000.caffemodel"
PROTOTXT_FILE = "deploy.prototxt"
MODEL_FILE = "mobilenet_iter_73000.caffemodel"

# 20 Kelas objek bawaan PASCAL VOC
CLASSES = [
    "background", "aeroplane", "bicycle", "bird", "boat",
    "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
    "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
    "sofa", "train", "tvmonitor"
]

# Warna acak konsisten untuk tiap kelas objek
np.random.seed(42)
COLORS = np.random.uniform(50, 255, size=(len(CLASSES), 3))

CONF_THRESHOLD = 0.45


def download_file(url, filename):
    if not os.path.exists(filename):
        print(f"[DOWNLOAD] Mengunduh {filename}...")
        # Bypass verifikasi SSL untuk mencegah issue sertifikat di Windows
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        
        with urllib.request.urlopen(url, context=ctx) as response, open(filename, 'wb') as out_file:
            data = response.read()
            out_file.write(data)
        print(f"[OK] {filename} berhasil diunduh.")


def main():
    try:
        download_file(PROTOTXT_URL, PROTOTXT_FILE)
        download_file(MODEL_URL, MODEL_FILE)
    except Exception as e:
        print(f"[ERROR] Gagal mengunduh model: {e}")
        return

    print("[INIT] Memuat model ke OpenCV DNN...")
    net = cv2.dnn.readNetFromCaffe(PROTOTXT_FILE, MODEL_FILE)
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

    # Buka webcam laptop (DirectShow di Windows untuk inisialisasi instan)
    if sys.platform.startswith("win"):
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    else:
        cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("[FALLBACK] Mencoba backend default webcam...")
        cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("[ERROR] Kamera tidak terdeteksi pada index 0!")
        return

    # Resolusi tampilan
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    cv2.namedWindow("Object Detection Test", cv2.WINDOW_NORMAL)
    print("\n" + "="*50)
    print("DETEKSI OBJEK AKTIF")
    print("Arahkan objek (botol, orang, kursi, tv/layar, tanaman, dll) ke webcam.")
    print("Tekan tombol 'q' pada jendela kamera untuk keluar.")
    print("="*50 + "\n")

    prev_time = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[WARN] Gagal membaca frame dari webcam.")
            break

        h, w = frame.shape[:2]

        # Konversi frame ke input blob 300x300 untuk MobileNet-SSD
        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)
        net.setInput(blob)
        detections = net.forward()

        # Iterasi hasil deteksi
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > CONF_THRESHOLD:
                idx = int(detections[0, 0, i, 1])
                label = CLASSES[idx]
                color = COLORS[idx]

                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")

                # Pastikan bounding box berada dalam batas frame
                startX, startY = max(0, startX), max(0, startY)
                endX, endY = min(w, endX), min(h, endY)

                # Gambar kotak objek
                cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)

                # Label teks
                text = f"{label}: {confidence * 100:.1f}%"
                y = startY - 10 if startY - 10 > 20 else startY + 20
                cv2.rectangle(frame, (startX, y - 18), (startX + len(text) * 9, y + 4), color, -1)
                cv2.putText(frame, text, (startX + 2, y - 3),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 0), 1, cv2.LINE_AA)

        # Hitung FPS real-time
        curr_time = time.time()
        fps = 1.0 / (curr_time - prev_time) if (curr_time - prev_time) > 0 else 0
        prev_time = curr_time

        # Overlay FPS
        cv2.putText(frame, f"FPS: {fps:.1f}", (15, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

        cv2.imshow("Object Detection Test", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
