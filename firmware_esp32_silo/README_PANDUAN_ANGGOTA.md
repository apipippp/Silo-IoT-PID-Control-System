# PANDUAN PENGGUNAAN FIRMWARE ESP32 (UNTUK ANGGOTA KELOMPOK)
**Tugas Besar IoT & Sistem Kendali - Semester 5**  
**Judul: Sistem Kendali Silo & Konveyor Otomatis Berbasis PID & IoT**

---

## 1. Cara Membuka di Arduino IDE
1. Buka folder `firmware_esp32_silo`.
2. Klik ganda pada file **`firmware_esp32_silo.ino`**.
3. Arduino IDE akan otomatis membuka file utama beserta seluruh file `.h` dan `.cpp` sebagai **tab-tab terpisah di bagian atas**.
4. Pilih Board: **ESP32 Dev Module** (atau DOIT ESP32 DEVKIT V1).
5. Pilih Port COM yang sesuai dengan kabel data ESP32 Anda.

---

## 2. Library yang Wajib Di-Install di Arduino IDE
Buka menu **Tools > Manage Libraries...** (atau shortcut `Ctrl + Shift + I`), lalu cari dan install library berikut:

1. **`DHT sensor library`** by Adafruit (jika diminta install dependensi `Adafruit Unified Sensor`, klik *Install All*).
2. **`ESP32Servo`** by Kevin Harrington (library resmi servo hardware timer ESP32).
3. **`LiquidCrystal_I2C`** by Frank de Brabander (untuk layar LCD I2C 16x2).
4. **`ArduinoJson`** by Benoit Blanchon (versi 6.x atau 7.x, untuk serialisasi JSON UART ke Raspi).

---

## 3. Struktur File & Pembagian Modul

Kode sengaja dipecah agar rapi, modular, dan mudah dipelajari per bagian:

| Nama File | Bagian / Tugas | Keterangan Singkat |
|---|---|---|
| **`config.h`** | **Konfigurasi Global** | Berisi seluruh nomor pinout, angka batas hysteresis, dimensi konveyor, titik henti webcam, dan nilai gain PID ($K_p, K_i, K_d$). |
| **`conveyor_pid`** (.h & .cpp) | **Algoritma Kendali PID Konveyor** | **[FITUR UTAMA SISTEM KENDALI]** Menghitung modulasi PWM motor DC agar barang melambat secara mulus (*smooth deceleration*) dan berhenti tepat di depan webcam. |
| **`sensor_manager`** (.h & .cpp) | **Akuisisi Data Sensor** | Membaca Ultrasonik secara cepat (20 Hz) untuk PID, membaca DHT22, dan memfilter MQ-2 dengan *Exponential Moving Average* (EMA). |
| **`actuator_controller`** (.h & .cpp) | **Kontrol Aktuator Fisik** | Mengendalikan 2 Kipas via 1 Relay, sudut servo ventilasi atap (0°–90°), dan arah/kecepatan PWM konveyor L298N. |
| **`control_logic`** (.h & .cpp) | **Otak Hysteresis Silo** | Menjalankan logika Hysteresis suhu & gas. Mengambil keputusan status silo (`NORMAL`, `WARN_TEMP`, `WARN_GAS`, atau `CRITICAL`). |
| **`display_manager`** (.h & .cpp) | **Tampilan Layar LCD** | Mengatur teks LCD 16x2 I2C dengan 2 tampilan layar bergantian: Layar 1 (Iklim Silo), Layar 2 (Jarak, Error PID, PWM & Fase Konveyor). |
| **`communication`** (.h & .cpp) | **Jembatan UART ke Raspi 3** | Mengirimkan paket JSON telemetri tiap 1 detik ke Raspberry Pi 3 via pin RX2/TX2, serta menerima perintah kendali (`SCAN_PASS`, `STOP_CONVEYOR`, dll). |
| **`firmware_esp32_silo.ino`** | **Program Utama (Main)** | Hanya berisi `setup()` dan `loop()` non-blocking (menggunakan `millis()`, tanpa `delay()`). |

---

## 4. Teori & Cara Kerja Algoritma PID Konveyor

### A. Konsep Matematis:
Sensor ultrasonik diletakkan di sisi dalam silo menghadap lurus sepanjang lintasan konveyor.
* **$SP$ (Setpoint):** Jarak titik henti tepat di depan lensa webcam (didefinisikan di `config.h`: `WEBCAM_STOP_POINT_CM = 15.0f`).
* **$PV$ (Process Variable):** Jarak barang aktual yang terbaca oleh ultrasonik saat ini.
* **Galat / Error:** 
  $$e(t) = PV - SP = \text{Jarak} - 15.0\text{ cm}$$

### B. Cara Kerja Komponen PID:
1. **Proporsional ($P = K_p \times e$):**
   * Saat barang masih jauh (misal jarak 40 cm, $e = 25$): $P$ menghasilkan nilai besar $\rightarrow$ Motor bergerak cepat.
   * Saat barang mendekati webcam ($e \to 0$): $P$ mengecil $\rightarrow$ Motor otomatis melambat.
2. **Derivatif ($D = K_d \times \frac{\Delta e}{\Delta t}$):**
   * Membaca laju perubahan kecepatan barang. Bertindak sebagai "rem otomatis" agar konveyor tidak bablas (*anti-overshoot*) akibat inersia beban.
3. **Integral ($I = K_i \times \sum e \cdot \Delta t$):**
   * Memberikan gaya dorong mikro tambahan jika motor macet akibat gaya gesek (*stiction*) saat hampir sampai di titik henti.
4. **Zona Berhenti (Deadband):**
   * Jika $|e| \le 0.8\text{ cm}$, sinyal PWM langsung diputus ke `0` (**Motor Berhenti Tepat di Tengah Lensa Kamera**).

### C. Alur Kerja Scanning dengan Raspberry Pi 3:
1. Barang diletakkan di konveyor $\rightarrow$ PID mendeteksi barang dan memperlambat lajunya hingga berhenti tepat di depan webcam.
2. ESP32 otomatis mengunci posisi barang dan mengirim status `conv_phase: "AT_WEBCAM"` ke Raspberry Pi 3.
3. Raspberry Pi 3 mengambil foto dan melakukan deteksi objek via YOLOv8.
4. Setelah barang dinyatakan lolos scan, Raspi 3 mengirim perintah UART: `{"cmd": "SCAN_PASS"}`.
5. ESP32 menerima perintah tersebut $\rightarrow$ menjalankan konveyor selama 2.5 detik hingga barang jatuh ke dalam silo $\rightarrow$ kembali siap mendeteksi barang berikutnya!

---

## 5. Cara Tuning Nilai PID (Jika Gerakan Kurang Pas di Alat Fisik)

Jika saat diuji di meja praktikum gerakannya belum pas, buka file **`config.h`** dan sesuaikan nilai konstanta berikut:

```cpp
#define PID_KP   8.5f   // Naikkan jika motor terasa terlalu lelet merespons barang jauh
#define PID_KI   0.2f   // Naikkan sedikit jika motor sering berhenti sebelum sampai webcam
#define PID_KD   3.0f   // Naikkan jika barang sering kebablasan/mengerem terlalu mendadak
```

---

## 6. Uji Coba Manual via Serial Monitor Laptop

1. Buka Serial Monitor di Arduino IDE pada baudrate **115200**.
2. Setiap 1 detik, data lengkap sistem kendali akan muncul:
   ```json
   {"temp":29.4,"hum":62.0,"gas":840,"dist_cm":15.1,"pid_err":0.1,"conv_phase":"AT_WEBCAM","conv_pwm":0,"silo_state":"NORMAL","fans":0,"vent_deg":0}
   ```
3. Ketika barang sudah berhenti di depan webcam, kalian bisa mengetik perintah berikut di Serial Monitor untuk mensimulasikan perintah Raspi:
   * Ketik **`SCAN_PASS`** lalu tekan Enter $\rightarrow$ Konveyor akan otomatis jalan mengalirkan barang ke silo selama 2.5 detik!
   * Ketik **`STOP_CONVEYOR`** $\rightarrow$ Konveyor berhenti darurat.
   * Ketik **`FAN_ON`** / **`FAN_OFF`** $\rightarrow$ Menguji 2 kipas.
   * Ketik **`VENT_OPEN`** / **`VENT_CLOSE`** $\rightarrow$ Menguji buka-tutup servo atap.
