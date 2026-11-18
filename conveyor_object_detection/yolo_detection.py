# language: Python, file: yolo_detection.py, target: Laptop & Edge, Python 3.9+
# dependencies: pip install ultralytics opencv-python

import os
import argparse
import sys
import time
import threading
import urllib.request
import cv2
import numpy as np
from ultralytics import YOLO

WINDOW_NAME = "YOLOv8 Detection"

# Resolusi path absolut direktori skrip ini
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

TWS_MODEL_URL = "https://raw.githubusercontent.com/MORSHEDMDMONOARUL/ExamShield/main/runs/detect/examshield_yolov8s/weights/best.pt"
DEFAULT_TWS_FILENAME = "earphone_tws.pt"


def resolve_model_path(model_input):
    """Mencari lokasi file model secara otomatis baik dari folder root maupun sub-folder"""
    # 1. Cek langsung dari CWD
    if os.path.exists(model_input):
        return os.path.abspath(model_input)

    # 2. Cek di dalam folder skrip (conveyor_object_detection/)
    in_script_dir = os.path.join(SCRIPT_DIR, model_input)
    if os.path.exists(in_script_dir):
        return in_script_dir

    # 3. Cek hanya dengan nama filenya di folder skrip
    basename = os.path.basename(model_input)
    in_script_base = os.path.join(SCRIPT_DIR, basename)
    if os.path.exists(in_script_base):
        return in_script_base

    # 4. Jika tetap tidak ada dan nama filenya adalah model TWS default, unduh otomatis
    if basename == DEFAULT_TWS_FILENAME:
        print(f"[DOWNLOAD] File {DEFAULT_TWS_FILENAME} belum ada. Mengunduh (~22.5 MB)...")
        urllib.request.urlretrieve(TWS_MODEL_URL, in_script_base)
        print("[OK] Model berhasil diunduh ke:", in_script_base)
        return in_script_base

    return model_input


class SmoothYOLOTracker:
    def __init__(self, cam_idx=1, width=1920, height=1080, model_path="earphone_tws.pt",
                 auto_exp=True, gain=0.0, boost=10, conf=0.25, imgsz=384):
        self.cam_idx = cam_idx
        self.target_w = width
        self.target_h = height
        self.conf = conf
        self.auto_exp = auto_exp
        self.curr_gain = float(gain)
        self.soft_brightness = int(boost)
        self.curr_exposure = -5.0
        self.imgsz = imgsz

        backend = cv2.CAP_DSHOW if sys.platform.startswith("win") else cv2.CAP_ANY
        self.cap = cv2.VideoCapture(cam_idx, backend)
        if not self.cap.isOpened():
            self.cap = cv2.VideoCapture(cam_idx)

        if not self.cap.isOpened():
            raise RuntimeError(f"Gagal membuka kamera pada index {cam_idx}")

        # Konfigurasi stream 1080p MJPG
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.target_w)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.target_h)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))

        # Set awal exposure & gain
        self._apply_exposure_mode()
        self._apply_hardware_gain(self.curr_gain)

        self.actual_w = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.actual_h = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.actual_fps = int(self.cap.get(cv2.CAP_PROP_FPS))
        print(f"[CAMERA] Stream: {self.actual_w}x{self.actual_h} @ {self.actual_fps} FPS (MJPG)")

        # Resolusi path model yang aman
        self.resolved_model = resolve_model_path(model_path)
        print(f"[INIT] Memuat model dari: {self.resolved_model}...")
        self.model = YOLO(self.resolved_model)
        print(f"[MODEL] Kelas terdaftar: {list(self.model.names.values())}")

        # Threading state
        self.running = True
        self.latest_proxy = None
        self.proxy_lock = threading.Lock()

        self.cached_boxes = []
        self.boxes_lock = threading.Lock()

        # Resolusi proxy AI 640x360 agar objek kecil di jarak 20-30cm terbaca tajam
        self.proxy_w = 640
        self.proxy_h = int(self.proxy_w * (self.actual_h / self.actual_w)) if self.actual_w > 0 else 360

        self.ai_thread = threading.Thread(target=self._ai_worker, daemon=True)
        self.ai_thread.start()

    def _apply_exposure_mode(self):
        if self.auto_exp:
            self.cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.75)
            print("[CAMERA] Mode Exposure: OTOMATIS (Terang alami)")
        else:
            self.cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)
            self.cap.set(cv2.CAP_PROP_EXPOSURE, self.curr_exposure)
            print(f"[CAMERA] Mode Exposure: MANUAL ({self.curr_exposure})")

    def _apply_hardware_gain(self, val):
        self.cap.set(cv2.CAP_PROP_GAIN, val)
        self.curr_gain = self.cap.get(cv2.CAP_PROP_GAIN)

    def open_driver_dialog(self):
        if sys.platform.startswith("win"):
            print("[CAMERA] Membuka panel kontrol driver Windows...")
            self.cap.set(cv2.CAP_PROP_SETTINGS, 1)

    def _ai_worker(self):
        ignored_classes = {"normal", "head_rotation", "paper_passing", "hand_gestures"}

        while self.running:
            small_img = None
            with self.proxy_lock:
                if self.latest_proxy is not None:
                    small_img = self.latest_proxy

            if small_img is None:
                time.sleep(0.005)
                continue

            results = self.model.predict(
                source=small_img,
                imgsz=self.imgsz,
                conf=self.conf,
                verbose=False
            )

            new_boxes = []
            if len(results) > 0 and results[0].boxes:
                boxes = results[0].boxes.xyxy.cpu().numpy()
                confs = results[0].boxes.conf.cpu().numpy()
                classes = results[0].boxes.cls.cpu().numpy().astype(int)

                for box, score, cls_id in zip(boxes, confs, classes):
                    name = self.model.names[cls_id]

                    if name in ignored_classes:
                        continue

                    display_name = "TWS / Earbuds" if name.lower() == "earphone" else name

                    norm_x1 = box[0] / self.proxy_w
                    norm_y1 = box[1] / self.proxy_h
                    norm_x2 = box[2] / self.proxy_w
                    norm_y2 = box[3] / self.proxy_h
                    new_boxes.append(((norm_x1, norm_y1, norm_x2, norm_y2), display_name, score))

            with self.boxes_lock:
                self.cached_boxes = new_boxes

            time.sleep(0.005)

    def run(self):
        cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
        disp_w, disp_h = 1280, 720
        cv2.resizeWindow(WINDOW_NAME, disp_w, disp_h)

        print("\n" + "="*65)
        print("PROGRAM DETEKSI TWS / EARBUDS AKTIF:")
        print("  Model khusus TWS telah dimuat (mengenali case & earbuds).")
        print("  [a]     : Beralih mode AUTO-EXPOSURE (Terang) / MANUAL (30 FPS)")
        print("  [p]     : Buka panel kontrol driver kamera Windows (seperti di OBS)")
        print("  [+ / -] : Naikkan / Turunkan Software Brightness Boost")
        print("  [q]     : Keluar")
        print("="*65 + "\n")

        prev_time = time.time()
        fps_smooth = 30.0

        while True:
            ret, frame = self.cap.read()
            if not ret:
                break

            if self.soft_brightness > 0:
                frame = cv2.convertScaleAbs(frame, alpha=1.05, beta=self.soft_brightness)

            proxy_frame = cv2.resize(frame, (self.proxy_w, self.proxy_h), interpolation=cv2.INTER_LINEAR)
            with self.proxy_lock:
                self.latest_proxy = proxy_frame

            display_frame = cv2.resize(frame, (disp_w, disp_h), interpolation=cv2.INTER_LINEAR)

            current_boxes = []
            with self.boxes_lock:
                current_boxes = list(self.cached_boxes)

            for (nx1, ny1, nx2, ny2), name, score in current_boxes:
                x1 = int(nx1 * disp_w)
                y1 = int(ny1 * disp_h)
                x2 = int(nx2 * disp_w)
                y2 = int(ny2 * disp_h)

                cv2.rectangle(display_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                label = f"{name} {score:.2f}"
                y_label = max(25, y1 - 8)
                cv2.putText(display_frame, label, (x1, y_label),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 0), 2, cv2.LINE_AA)

            curr_time = time.time()
            dt = curr_time - prev_time
            if dt > 0:
                fps_smooth = (fps_smooth * 0.9) + ((1.0 / dt) * 0.1)
            prev_time = curr_time

            model_basename = os.path.basename(self.resolved_model)
            mode_str = "AUTO" if self.auto_exp else f"MANUAL({self.curr_exposure:.1f})"
            hud1 = f"FPS: {fps_smooth:.1f} | Model: {model_basename} | Deteksi: {len(current_boxes)}"
            hud2 = "[a]=Auto/Man | [p]=Driver Panel | [+/-]=Boost"

            cv2.putText(display_frame, hud1, (20, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 255), 2, cv2.LINE_AA)
            cv2.putText(display_frame, hud2, (20, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1, cv2.LINE_AA)

            cv2.imshow(WINDOW_NAME, display_frame)
            key = cv2.waitKey(1) & 0xFF

            if key == ord('q'):
                break
            elif key == ord('a'):
                self.auto_exp = not self.auto_exp
                self._apply_exposure_mode()
            elif key == ord('p'):
                self.open_driver_dialog()
            elif key == ord('e'):
                self._apply_hardware_gain(min(128.0, self.curr_gain + 10.0))
                print(f"[SET] Gain: {self.curr_gain}")
            elif key == ord('d'):
                self._apply_hardware_gain(max(0.0, self.curr_gain - 10.0))
                print(f"[SET] Gain: {self.curr_gain}")
            elif key in [ord('='), ord('+')]:
                self.soft_brightness = min(100, self.soft_brightness + 5)
                print(f"[SET] Boost: +{self.soft_brightness}")
            elif key in [ord('-'), ord('_')]:
                self.soft_brightness = max(0, self.soft_brightness - 5)
                print(f"[SET] Boost: +{self.soft_brightness}")

        self.running = False
        self.ai_thread.join(timeout=1.0)
        self.cap.release()
        cv2.destroyAllWindows()


def auto_detect_camera():
    for idx in [1, 0, 2]:
        test_cap = cv2.VideoCapture(idx, cv2.CAP_DSHOW if sys.platform.startswith("win") else cv2.CAP_ANY)
        if test_cap.isOpened():
            test_cap.release()
            return idx
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="YOLOv8 Detection with Custom TWS Model")
    parser.add_argument("--cam", "-c", type=int, default=None, help="Index kamera")
    parser.add_argument("--model", "-m", default=DEFAULT_TWS_FILENAME,
                        help="Path model YOLO (default: earphone_tws.pt khusus TWS/Earbuds)")
    parser.add_argument("--manual", action="store_true", help="Mulai dalam mode manual exposure")
    parser.add_argument("--gain", "-g", type=float, default=0.0, help="Hardware gain awal (default: 0.0)")
    parser.add_argument("--boost", "-b", type=int, default=10, help="Digital boost awal (default: 10)")
    parser.add_argument("--conf", type=float, default=0.25, help="Confidence threshold (default: 0.25)")
    parser.add_argument("--imgsz", type=int, default=384, help="Ukuran tensor input AI (default: 384)")
    args = parser.parse_args()

    selected_cam = args.cam if args.cam is not None else auto_detect_camera()
    print(f"[SETUP] Membuka kamera Index {selected_cam}...")

    tracker = SmoothYOLOTracker(
        cam_idx=selected_cam,
        width=1920,
        height=1080,
        model_path=args.model,
        auto_exp=not args.manual,
        gain=args.gain,
        boost=args.boost,
        conf=args.conf,
        imgsz=args.imgsz
    )
    tracker.run()
