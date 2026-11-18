#ifndef CONFIG_H
#define CONFIG_H

#include <Arduino.h>

// ============================================================================
// 1. PINOUT MIKROKONTROLER ESP32 (30-Pin / 38-Pin DevKit)
// ============================================================================

// --- SENSOR ---
#define PIN_DHT22           4   // Pin Data DHT22 (Suhu & Kelembaban)
#define PIN_MQ2_ADC        34   // Pin Analog ADC1 MQ-2 (Konsentrasi Gas)
#define PIN_TRIG_US         5   // Pin Trigger HC-SR04 (Ultrasonik)
#define PIN_ECHO_US        18   // Pin Echo HC-SR04 (Wajib via Voltage Divider 1k:2k)

// --- AKTUATOR ---
#define PIN_RELAY_FAN      19   // Pin Relay (1 Relay mengendalikan 2 Fan 12V)
#define PIN_SERVO_VENT     13   // Pin PWM Servo SG90 (Katup Atap Silo)

// --- DRIVER MOTOR L298N (KONVEYOR) ---
#define PIN_L298N_ENA      14   // Pin PWM Pengatur Kecepatan Konveyor
#define PIN_L298N_IN1      25   // Pin Arah Putar Konveyor 1
#define PIN_L298N_IN2      26   // Pin Arah Putar Konveyor 2

// --- KOMUNIKASI SERIAL UART (Ke Raspberry Pi 3) ---
#define PIN_UART_RX2       16   // RX2 ESP32 <- Terhubung ke TX Pin 8 Raspi
#define PIN_UART_TX2       17   // TX2 ESP32 -> Terhubung ke RX Pin 10 Raspi
#define UART_BAUDRATE  115200   // Kecepatan baud komunikasi serial

// --- I2C LCD 16x2 ---
#define LCD_I2C_ADDR     0x27   // Alamat I2C umum (ganti 0x3F jika tidak muncul)
#define LCD_COLS           16
#define LCD_ROWS            2

// ============================================================================
// 2. PARAMETER HYSTERESIS SISTEM KENDALI SILO
// ============================================================================
#define THRESHOLD_TEMP_HIGH    33.0f   // Suhu >= 33°C -> Kipas ON, Ventilasi Buka
#define THRESHOLD_TEMP_LOW     30.5f   // Suhu <= 30.5°C -> Kipas OFF, Ventilasi Tutup

#define THRESHOLD_HUM_HIGH     72.0f   // RH >= 72% -> Pemicu kelembaban kritis
#define THRESHOLD_HUM_LOW      65.0f   // RH <= 65% -> Kelembaban kembali normal

#define THRESHOLD_GAS_HIGH   1800.0f   // Gas Tinggi (Indikasi Bau Busuk / Metana)
#define THRESHOLD_GAS_LOW    1200.0f   // Gas Rendah (Udara Silo Bersih Kembali)

// ============================================================================
// 3. PARAMETER GEOMETRI KONVEYOR & TITIK HENTI WEBCAM (cm)
// ============================================================================
// Sensor ultrasonik dipasang di ujung silo menghadap sepanjang konveyor:
#define CONVEYOR_MAX_DIST_CM   45.0f   // Jarak terjauh ujung konveyor (tidak ada barang jika dist >= 45)
#define WEBCAM_STOP_POINT_CM   15.0f   // SETPOINT (SP): Titik henti tepat di depan lensa webcam
#define STOP_TOLERANCE_CM       0.8f   // Toleransi deadband berhenti (± 0.8 cm)

// Parameter Dimensi Silo (cm) jika dipakai untuk level silo
#define SILO_DEPTH_EMPTY_CM    30.0f   
#define SILO_DEPTH_FULL_CM      5.0f   

// ============================================================================
// 4. PARAMETER PID KENDALI KECEPATAN KONVEYOR
// ============================================================================
// Nilai Gain Tuning PID (Silakan dituning halus saat uji coba fisik):
#define PID_KP                  8.5f   // Penguatan Proporsional (Merespons jarak sisa)
#define PID_KI                  0.2f   // Penguatan Integral (Menghilangkan sisa galat gesekan)
#define PID_KD                  3.0f   // Penguatan Derivatif (Mencegah overshoot / ngerem mulus)

// Batas Kecepatan PWM Motor Kuning (L298N)
#define PWM_MAX_SPEED            160   // Kecepatan maksimal (~6V aman untuk motor kuning)
#define PWM_MIN_MOVING            80   // Batas minimal PWM agar motor tidak mendengung akibat gesekan
#define PWM_STOP                   0   // Berhenti total

// Sudut Sudut Servo SG90
#define SERVO_ANGLE_CLOSED         0   // Katup atap tertutup rapat
#define SERVO_ANGLE_HALF          45   // Katup atap terbuka separuh (Sirkulasi suhu)
#define SERVO_ANGLE_FULL          90   // Katup atap terbuka penuh (Buang gas darurat)

#define EMA_ALPHA               0.15f  // Koefisien Filter EMA Gas

// ============================================================================
// 5. INTERVAL LOOP NON-BLOCKING (Dalam Milidetik)
// ============================================================================
#define INTERVAL_PID_MS           50   // Loop PID & Ultrasonik (20 Hz - Cepat & Responsif!)
#define INTERVAL_READ_FAST_MS    100   // Sampling MQ-2 (10 Hz)
#define INTERVAL_READ_SLOW_MS   2000   // Sampling DHT22 (0.5 Hz)
#define INTERVAL_LCD_UPDATE_MS  1000   // Update teks LCD (1 Hz)
#define INTERVAL_TELEMETRY_MS   1000   // Kirim data JSON ke Raspi (1 Hz)

#endif // CONFIG_H
