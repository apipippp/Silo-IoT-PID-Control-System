# SISTEM KENDALI & MONITORING LINGKUNGAN SILO RAW MATERIAL BERBASIS IOT & CLOSED-LOOP PID CONVEYOR

> **Tugas Besar Mata Kuliah Sistem Kendali & Internet of Things (IoT) — Semester 5**  
> **Platform Hardware:** ESP32 DevKit V1 (30/38 Pin) & Raspberry Pi 3 Model B  
> **Arsitektur Firmware:** Modular C++ (Header/Source Separation) & Non-Blocking Scheduler  

---

## DAFTAR ISI
1. [Ringkasan Proyek](#1-ringkasan-proyek)
2. [Arsitektur Sistem & Distribusi Daya](#2-arsitektur-sistem--distribusi-daya)
3. [Skematik Pinout & Wiring](#3-skematik-pinout--wiring)
4. [Alur Kerja Sistem (Workflow & State Machine)](#4-alur-kerja-sistem-workflow--state-machine)
5. [Metode Pemrosesan Sinyal & Filtrasi Data](#5-metode-pemrosesan-sinyal--filtrasi-data)
6. [Metode Sistem Kendali & Analisis Matematis](#6-metode-sistem-kendali--analisis-matematis)
   * 6.1 [Kendali Hysteresis Lingkungan Silo](#61-kendali-hysteresis-lingkungan-silo-non-linear-deadband)
   * 6.2 [Kendali PID Diskrit Konveyor Barang](#62-kendali-pid-diskrit-konveyor-linear-closed-loop)
   * 6.3 [Pembuktian Teoretis Eliminasi Galat Tunak ($e_{ss} = 0$)](#63-pembuktian-teoretis-eliminasi-galat-tunak-e_ss--0)
   * 6.4 [Metode Penalaan Ziegler-Nichols](#64-metode-penalaan-ziegler-nichols)
7. [Protokol Komunikasi Telemetri UART ke Raspberry Pi 3](#7-protokol-komunikasi-telemetri-uart-ke-raspberry-pi-3)
8. [Struktur Modul Kode Sumber](#8-struktur-modul-kode-sumber)
9. [Panduan Instalasi & Uji Coba](#9-panduan-instalasi--uji-coba)

---

## 1. RINGKASAN PROYEK

Proyek ini mengintegrasikan dua domain rekayasa utama: **Sistem Kendali Tertutup (*Closed-Loop Control*)** dan **Sistem Cerdas Internet of Things (IoT)** pada miniatur pabrik penyimpanan bahan baku curah (*raw material silo*) dan konveyor penyortir otomatis:

1. **Sistem Kendali Lingkungan Silo:** Menjaga kestabilan iklim mikro (suhu dan kelembaban) serta mengevakuasi gas pembusukan biologis (metana/amonia via MQ-2) menggunakan ventilasi atap proporsional (Servo SG90) dan paket 2 kipas exhaust/sirkulasi 12V DC melalui modul relay.
2. **Sistem Kendali Posisi & Kecepatan Konveyor:** Mengatur pergerakan sabuk konveyor pengumpan bahan baku menggunakan motor DC gearbox dan driver H-Bridge L298N dengan algoritma **Closed-Loop PID Control**. Kecepatan konveyor melambat secara mulus (*smooth deceleration*) saat mendekati titik inspeksi kamera webcam, berhenti presisi di tengah lensa, menunggu hasil klasifikasi AI (YOLOv8 di Raspberry Pi 3), lalu mengalirkan barang masuk ke dalam silo.

---

## 2. ARSITEKTUR SISTEM & DISTRIBUSI DAYA

Sistem menggunakan **Single Power Supply Architecture** bersumber dari 1 Adaptor 12V DC dengan pembagian rel daya terisolasi (*Isolated Power Rails*) guna mencegah *electrical noise* dan *voltage drop*:

```
                            [ ADAPTOR 12V DC (3A / 5A) ]
                                          |
        +---------------------------------+---------------------------------+
        |                                 |                                 |
        v                                 v                                 v
[ REL 12V MURNI ]              [ STEPDOWN 1 (LM2596) ]           [ STEPDOWN 2 (LM2596) ]
• Motor DC (L298N VMS)         • Output: 5.15V - 5.20V           • Output: 5.00V Stabil
• 2x Fan 12V (via Relay)       • Khusus Raspberry Pi 3           • Suplai Beban 5V:
                                 (Terhindar dari undervoltage)     - ESP32 (Pin VIN)
                                                                   - Servo SG90
                                                                   - Sensor MQ-2 (Heater)
                                                                   - Modul Relay, LCD, HC-SR04
        |                                 |                                 |
        +---------------------------------+---------------------------------+
                                          |
                              [ COMMON GROUND BUS (GND) ]
                    (Semua kutub negatif wajib terhubung bersama!)
```

---

## 3. SKEMATIK PINOUT & WIRING

### A. Tabel Sambungan Pin ESP32 (DevKit 30/38 Pin)

| Kategori | Nama Komponen | Pin Komponen | Pin ESP32 | Sumber Daya ($V_{CC}$) | Catatan Teknis |
|---|---|---|:---:|:---:|---|
| **Sensor** | **MQ-2** | Pin $A_0$ | **GPIO 34** | Rel 5V Stepdown 2 | Masuk ke ADC1 (0–4095, bebas konflik WiFi) |
| **Sensor** | **DHT22** | Pin Data | **GPIO 4** | Rel 5V Stepdown 2 | Beri resistor pull-up 4.7kΩ ke 3.3V |
| **Sensor** | **HC-SR04** | Pin Trig | **GPIO 5** | Rel 5V Stepdown 2 | Output pulsa pemicu 10 µs |
| **Sensor** | **HC-SR04** | Pin Echo | **GPIO 18** | Rel 5V Stepdown 2 | **Wajib Voltage Divider (1kΩ : 2kΩ)** ke 3.3V |
| **Aktuator**| **Modul Relay** | Pin IN | **GPIO 19** | Rel 5V Stepdown 2 | Mengendalikan 2 Fan 12V secara paralel |
| **Aktuator**| **Servo SG90** | Pin Sinyal (Oranye)| **GPIO 13** | Rel 5V Stepdown 2 | Sinyal PWM sudut katup ventilasi (0°–90°) |
| **Aktuator**| **L298N Motor**| Pin ENA | **GPIO 14** | Rel 12V Adaptor | Modulasi PWM kecepatan (skala 0–255) |
| **Aktuator**| **L298N Motor**| Pin IN1 | **GPIO 25** | Rel 12V Adaptor | Logika arah maju konveyor |
| **Aktuator**| **L298N Motor**| Pin IN2 | **GPIO 26** | Rel 12V Adaptor | Logika arah konveyor |
| **Display** | **LCD 16x2 I2C**| Pin SDA | **GPIO 21** | Rel 5V Stepdown 2 | Jalur Data Serial I2C (Wire) |
| **Display** | **LCD 16x2 I2C**| Pin SCL | **GPIO 22** | Rel 5V Stepdown 2 | Jalur Clock Serial I2C (Wire) |
| **Komunikasi**| **Raspberry Pi 3**| Pin 8 (TXD Raspi)| **GPIO 16 (RX2)**| — | Menerima perintah kendali dari AI |
| **Komunikasi**| **Raspberry Pi 3**| Pin 10 (RXD Raspi)| **GPIO 17 (TX2)**| — | Mengirim string telemetri JSON ke AI |
| **Ground**  | **Semua Komponen**| Ground (-) | **GND ESP32** | — | **Wajib disatukan ke Common Ground Bus** |

---

## 4. ALUR KERJA SISTEM (WORKFLOW & STATE MACHINE)

```
                            [ MULAI (Power ON) ]
                                     |
               Inisialisasi Serial, Sensor, Aktuator, LCD & PID
                                     |
                   +-----------------+-----------------+
                   |                                   |
         [ LOOP KENDALI SILO ]               [ LOOP PID KONVEYOR (50ms) ]
                   |                                   |
       Baca MQ-2 (EMA Filter 100ms)         Baca Ultrasonik Jarak Barang (PV)
       Baca DHT22 (Validasi 2000ms)                    |
                   |                        Hitung Galat: e[k] = PV - Setpoint
        Evaluasi Hysteresis Suhu & Gas                 |
                   |                        +----------+----------+
    +--------------+--------------+         |                     |
    |              |              |    e > Deadband         |e| <= Deadband
 [NORMAL]     [WARN_TEMP]    [WARN_GAS]     |                     |
Fan: OFF      Fan: ON        Fan: ON    PID Modulasi PWM      Motor STOP (PWM = 0)
Vent: 0°      Vent: 45°      Vent: 90°  Konveyor Melambat     Kirim "AT_WEBCAM" ke Raspi
    |              |              |         |                     |
    +--------------+--------------+         +--------+            v
                   |                                 |   [ SCANNING WEBCAM YOLO ]
                   v                                 |   Raspi proses inspeksi AI
    Update LCD 16x2 & Telemetri UART                 |            |
         ke Raspberry Pi 3 (1 Hz)                    |   Kirim "SCAN_PASS" via UART
                                                     |            |
                                                     |            v
                                                     |    [ FASE DRAINING ]
                                                     |   Konveyor jalan 2.5 detik
                                                     |   Barang jatuh ke dalam silo
                                                     |            |
                                                     +<-----------+
```

---

## 5. METODE PEMROSESAN SINYAL & FILTRASI DATA

### 5.1 Exponential Moving Average (EMA) pada Sensor Gas MQ-2
Konversi Analog-to-Digital (ADC) pada ESP32 memiliki derau frekuensi tinggi (*high-frequency switching noise*). Untuk menghaluskan fluktuasi tanpa membebani memori RAM mikroprosesor (tanpa *circular array*), diimplementasikan algoritma **Low-Pass IIR / Exponential Moving Average (EMA)**:

$$y[k] = \alpha \cdot x[k] + (1 - \alpha) \cdot y[k-1]$$

* $x[k]$ = Nilai mentah ADC gas saat ini (0–4095).
* $y[k-1]$ = Nilai gas terfilter pada siklus sebelumnya.
* $\alpha = 0.15$ = Faktor pemulusan (*smoothing factor*). Nilai ini memberikan respon dinamis yang mulus namun tetap tanggap mendeteksi semburan gas bocor seketika.

### 5.2 Outlier & NaN Rejection pada Sensor DHT22
Protokol 1-Wire DHT22 rentan terhadap *packet frame error* yang menghasilkan nilai `NaN` atau lonjakan ekstrem. Algoritma menyaring data dengan aturan validasi:
$$\text{Data Diterima jika: } (\text{data} \neq \text{NaN}) \land (0^\circ\text{C} < T < 80^\circ\text{C}) \land (0\% \le RH \le 100\%)$$
Jika pembacaan korup, sistem mempertahankan nilai suhu/kelembaban siklus sebelumnya.

---

## 6. METODE SISTEM KENDALI & ANALISIS MATEMATIS

### 6.1 Kendali Hysteresis Lingkungan Silo (Non-Linear Deadband)
Paket 2 Kipas DC 12V dikendalikan oleh modul **Relay Mekanik**. Karakteristik relay adalah sakelar bistabil (ON/OFF) yang tidak boleh dipicu oleh algoritma linier kontinu (seperti PWM frekuensi tinggi) karena dapat merusak kontak tembaga relay. 

Diterapkan **Kendali Hysteresis (Dua Ambang Batas)** untuk mencegah osilasi sakelar (*chattering/contact bouncing*):

```
Suhu Naik   -------------------------> [ ON: 33.0 °C ] (Relay Kipas Menyala)
                                           |
    [ Zona Hysteresis / Deadband ]        | Kipas TETAP MENYALA di zona ini
                                           v
Suhu Turun  <------------------------- [ OFF: 30.5 °C ] (Relay Kipas Mati)
```

* **Hysteresis Suhu:** ON pada $T \ge 33.0^\circ\text{C}$, OFF pada $T \le 30.5^\circ\text{C}$ (Deadband = $2.5^\circ\text{C}$).
* **Hysteresis Gas MQ-2:** ON pada $\text{ADC} \ge 1800$, OFF pada $\text{ADC} \le 1200$ (Deadband = 600 ADC).

---

### 6.2 Kendali PID Diskrit Konveyor (Linear Closed-Loop)
Pada konveyor barang, aktuator adalah **Driver H-Bridge L298N** yang mendukung modulasi lebar pulsa (*Pulse Width Modulation*). Diterapkan sistem kendali lingkar tertutup berbasis **PID Diskrit** pada laju sampling $f_s = 20\text{ Hz}$ ($\Delta t = 50\text{ ms}$):

```
       r(t) = 15 cm        e(t)       +------------+  u(t) PWM   +-------------+  v(t)  +----------+
[ Setpoint Webcam ] --->( Σ )-------> | PID C(s)   | ----------> | Driver      | -----> | Konveyor | ----+ y(t)
                         - ^          | Controller |             | L298N Motor |        | Plant    |     | Jarak
                           |          +------------+             +-------------+        +----------+     |
                           +-------------------------[ Sensor HC-SR04 ]<---------------------------------+
```

#### Persamaan Selisih Hingga (*Finite Difference Equation*):
1. **Galat Jarak Saat Ini:**
   $$e[k] = y[k] - r[k] = \text{JarakAktual}[k] - 15.0\text{ cm}$$
2. **Aksi Proporsional ($P$):** Menghasilkan gaya gerak awal sebanding dengan sisa jarak barang:
   $$P[k] = K_p \cdot e[k]$$
3. **Aksi Integral ($I$) dengan Anti-Windup:** Menjumlahkan riwayat akumulasi galat guna mengatasi gaya gesek statis (*stiction*) sabuk konveyor:
   $$I[k] = \text{clamp}\left(I[k-1] + K_i \cdot e[k] \cdot \Delta t, -50, +50\right)$$
4. **Aksi Derivatif ($D$):** Membaca laju perubahan galat sebagai rem dinamis peredam inersia beban:
   $$D[k] = K_d \cdot \frac{e[k] - e[k-1]}{\Delta t}$$
5. **Total Sinyal Kontrol & Saturasi Fisik:**
   $$u[k] = P[k] + I[k] + D[k]$$
   $$\text{PWM}_{\text{out}} = \begin{cases} 
   0, & \text{jika } |e[k]| \le 0.8\text{ cm (Deadband Stop)} \\
   \text{constrain}(80 + u[k], 80, 160), & \text{jika } e[k] > 0.8\text{ cm}
   \end{cases}$$

---

### 6.3 Pembuktian Teoretis Eliminasi Galat Tunak ($e_{ss} = 0$)
Sesuai materi kuliah **Lecture 7 (Steady-State Error & System Types)**, konveyor pengatur posisi memiliki fungsi alih lingkar terbuka $G_p(s) = \frac{K_m}{s(\tau_m s + 1)}$.

Dengan menyertakan kontroler PID $C(s) = K_p + \frac{K_i}{s} + K_d s$:
$$\lim_{s \to 0} C(s) \cdot G_p(s) = \lim_{s \to 0} \left( \frac{K_i}{s} \right) \left( \frac{K_m}{s} \right) = \infty \quad \text{(Sistem Tipe-2 terhadap Posisi)}$$

Berdasarkan **Teorema Nilai Akhir (*Final Value Theorem*)**:
$$e_{ss} = \lim_{s \to 0} s \cdot E(s) = \lim_{s \to 0} \frac{s \cdot R(s)}{1 + C(s)G(s)}$$
Untuk masukan undak posisi $R(s) = \frac{A}{s}$:
$$e_{ss} = \lim_{s \to 0} \frac{A}{1 + \infty} = 0$$

> **Kesimpulan Ilmiah:** Terbukti secara analitik bahwa keberadaan suku integral ($K_i$) mutlak menjamin barang berhenti tepat di koordinat lensa kamera tanpa menyisakan galat tunak ($e_{ss} = 0$).

---

### 6.4 Metode Penalaan Ziegler-Nichols
Berdasarkan pendekatan **Kurva Reaksi Ziegler-Nichols (Z-N Process Reaction Curve)** yang disesuaikan dengan karakteristik motor mini meja praktikum:
* **$K_p = 8.5$:** Memberikan percepatan awal yang mantap saat barang berada di ujung konveyor ($e = 30\text{ cm}$).
* **$K_i = 0.2\text{ s}^{-1}$:** Memberikan torsi dorong tambahan halus tanpa menyebabkan osilasi integral.
* **$K_d = 3.0\text{ s}$:** Mencegah terjadinya lonjakan hentakan (*zero percent overshoot*, $\%OS \approx 0\%$) saat barang memasuki zona henti webcam.

---

## 7. PROTOKOL KOMUNIKASI TELEMETRI UART KE RASPBERRY PI 3

Komunikasi antara ESP32 dan Raspberry Pi 3 berjalan asinkron via **Hardware Serial2 (Baudrate: 115200 bps, 8-N-1)**:

### A. Format Paket Telemetri ESP32 $\rightarrow$ Raspi 3 (1 Hz):
```json
{
  "temp": 31.4,
  "hum": 68.0,
  "gas": 1420,
  "dist_cm": 15.1,
  "pid_err": 0.1,
  "conv_phase": "AT_WEBCAM",
  "conv_pwm": 0,
  "silo_state": "NORMAL",
  "fans": 0,
  "vent_deg": 0
}
```

### B. Format Perintah Kontrol Raspi 3 $\rightarrow$ ESP32:
* **`{"cmd": "SCAN_PASS"}`:** Perintah bahwa inspeksi kamera YOLOv8 selesai & lolos; ESP32 mengalirkan konveyor selama 2.5 detik ke dalam silo.
* **`{"cmd": "STOP_CONVEYOR"}`:** Perintah penghentian darurat konveyor.
* **`{"cmd": "RUN_CONVEYOR", "val": 150}`:** Perintah override konveyor manual.
* **`{"cmd": "VENT_OPEN"}` / `{"cmd": "VENT_CLOSE"}`:** Override katup servo manual.
* **`{"cmd": "FAN_ON"}` / `{"cmd": "FAN_OFF"}`:** Override relay 2 kipas manual.

---

## 8. STRUKTUR MODUL KODE SUMBER

Folder `firmware_esp32_silo/` dirancang menggunakan arsitektur modular C++:

```
firmware_esp32_silo/
├── firmware_esp32_silo.ino   # File master setup() & loop() non-blocking scheduler
├── config.h                  # Pusat konfigurasi pinout, ambang batas & gain PID
├── sensor_manager.h          # Header modul pembacaan sensor terpadu
├── sensor_manager.cpp        # Implementasi EMA Filter MQ-2 & Outlier DHT22
├── actuator_controller.h     # Header kontroler rel fisik aktuator
├── actuator_controller.cpp   # Implementasi kendali 1 Relay Fan, Servo, & L298N
├── conveyor_pid.h            # Header algoritma Closed-Loop PID Konveyor
├── conveyor_pid.cpp          # Implementasi finite difference PID, anti-windup & stiction
├── control_logic.h           # Header state machine lingkungan silo
├── control_logic.cpp         # Implementasi Hysteresis Suhu, Lembab & Gas
├── display_manager.h         # Header display visual LCD 16x2 I2C
├── display_manager.cpp       # Implementasi 2 layar bergantian (Iklim & Status PID)
├── communication.h           # Header antarmuka UART JSON ke Raspberry Pi 3
├── communication.cpp         # Implementasi pengiriman telemetri & command parser
└── README.md                 # Dokumentasi teknis & panduan lengkap
```

---

## 9. PANDUAN INSTALASI & UJI COBA

### 1. Dependensi Library Arduino IDE:
Install library berikut via menu **Tools > Manage Libraries**:
* **`DHT sensor library`** by Adafruit
* **`Adafruit Unified Sensor`** by Adafruit
* **`ESP32Servo`** by Kevin Harrington
* **`LiquidCrystal_I2C`** by Frank de Brabander
* **`ArduinoJson`** by Benoit Blanchon (v6 atau v7)

### 2. Langkah Kompilasi & Flash:
1. Hubungkan ESP32 ke port USB laptop.
2. Buka file **`firmware_esp32_silo.ino`** di Arduino IDE.
3. Pilih board: **ESP32 Dev Module**.
4. Klik tombol **Upload** (Tanda panah ke kanan).

### 3. Pengujian Mandiri via Serial Monitor:
1. Buka Serial Monitor pada baudrate **115200**.
2. Letakkan tangan/benda di depan ultrasonik $\rightarrow$ Amati nilai `dist_cm`, `pid_err`, dan penurunan nilai `conv_pwm` secara otomatis hingga berhenti tepat di 15 cm (`AT_WEBCAM`).
3. Ketik perintah `SCAN_PASS` pada kolom input Serial Monitor $\rightarrow$ Konveyor akan otomatis berputar selama 2.5 detik untuk menjatuhkan barang ke dalam silo.
