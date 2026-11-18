# Modul Deteksi Objek & Tracking Conveyor

Modul pengujian computer vision untuk tracking material pada sistem konveyor (bagian dari Supply Chain Management Silo IoT).

## Struktur Folder
```text
├── yolo_detection.py      # Program deteksi objek YOLOv8 (80 kelas COCO, paling akurat di laptop)
├── test_detection.py       # Program deteksi alternatif MobileNet-SSD (versi ultra-ringan CPU)
├── conveyor_tracker.py     # Program tracking objek dengan garis virtual counter
├── requirements.txt        # Dependensi Python
└── README.md

## Cara Menjalankan

### 1. Di Laptop (Windows/Mac/Linux)
```bash
cd conveyor_object_detection
pip install -r requirements.txt
python yolo_detection.py
```

### 2. Di Raspberry Pi 3
```bash
cd conveyor_object_detection
sudo apt update
sudo apt install -y python3-opencv python3-numpy
python3 test_detection.py
```

## Kontrol
- **q**: Keluar dari program
- **r**: Reset counter objek (pada `conveyor_tracker.py`)
