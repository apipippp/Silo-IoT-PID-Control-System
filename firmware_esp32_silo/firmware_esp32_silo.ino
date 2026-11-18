/**
 * ============================================================================
 * PROYEK TUGAS BESAR IOT & SISTEM KENDALI - SEMESTER 5
 * ============================================================================
 * Judul     : Sistem Kendali & Monitoring Silo + Konveyor Berbasis PID & IoT
 * Deskripsi : Firmware Utama ESP32 (Arsitektur Modular Non-Blocking)
 * 
 * Modul Terpisah:
 * 1. config.h              -> Parameter Pinout, Hysteresis, Geometri Konveyor & PID Gain
 * 2. sensor_manager        -> Akuisisi DHT22, Filter EMA MQ-2, Ultrasonik Cepat
 * 3. actuator_controller   -> Kontrol 2 Kipas (1 Relay), Servo SG90, L298N PWM
 * 4. conveyor_pid          -> Kontroler PID Kecepatan & Titik Henti Webcam Konveyor
 * 5. control_logic         -> State Machine Hysteresis Suhu, Lembab & Gas Silo
 * 6. display_manager       -> LCD 16x2 I2C 2-Layar Bergantian
 * 7. communication         -> Protokol Serial UART JSON ke Raspberry Pi 3
 * ============================================================================
 */

#include <Arduino.h>
#include "config.h"
#include "sensor_manager.h"
#include "actuator_controller.h"
#include "conveyor_pid.h"
#include "control_logic.h"
#include "display_manager.h"
#include "communication.h"

// --- INSTANSIASI OBJEK MODULAR ---
SensorManager       sensorMgr;
ActuatorController  actuatorCtrl;
ConveyorPID         conveyorPID;
ControlLogic        logicCtrl;
DisplayManager      displayMgr;
Communication       comm;

// --- TIMER SCHEDULER NON-BLOCKING (MILLIS) ---
unsigned long prevPIDTime        = 0;
unsigned long prevFastSampleTime = 0;
unsigned long prevSlowSampleTime = 0;
unsigned long prevDisplayTime    = 0;
unsigned long prevTelemetryTime  = 0;

void setup() {
    // 1. Inisialisasi Komunikasi Serial (USB & RX2/TX2 ke Raspi 3)
    comm.begin();

    // 2. Inisialisasi Aktuator (Relay, Servo, Driver Motor L298N)
    actuatorCtrl.begin();

    // 3. Inisialisasi Modul Kendali PID Konveyor
    conveyorPID.begin();

    // 4. Inisialisasi Sensor (MQ-2, DHT22, HC-SR04)
    sensorMgr.begin();

    // 5. Inisialisasi Layar LCD 16x2 I2C
    displayMgr.begin();

    Serial.println("[SISTEM] Seluruh modul ESP32 berhasil diinisialisasi.");
    Serial.println("[SISTEM] Setpoint Webcam = " + String(WEBCAM_STOP_POINT_CM) + " cm.");
    Serial.println("[SISTEM] Memulai loop kendali otomatis...");
}

void loop() {
    unsigned long currentMillis = millis();

    // ------------------------------------------------------------------------
    // TUGAS 1: LOOP CEPAT PID KONVEYOR (Setiap 50 ms / 20 Hz)
    // ------------------------------------------------------------------------
    // Mengukur jarak ultrasonik secara cepat dan menghitung sinyal kontrol PWM
    // agar barang melambat secara mulus dan berhenti tepat di depan webcam!
    if (currentMillis - prevPIDTime >= INTERVAL_PID_MS) {
        prevPIDTime = currentMillis;
        sensorMgr.updateUltrasonic();
        conveyorPID.compute(sensorMgr.getDistanceCm(), actuatorCtrl);
    }

    // ------------------------------------------------------------------------
    // TUGAS 2: SAMPLING SENSOR CEPAT (MQ-2 Filter EMA tiap 100 ms)
    // ------------------------------------------------------------------------
    if (currentMillis - prevFastSampleTime >= INTERVAL_READ_FAST_MS) {
        prevFastSampleTime = currentMillis;
        sensorMgr.updateFastSensors();
    }

    // ------------------------------------------------------------------------
    // TUGAS 3: SAMPLING SENSOR LAMBAT (DHT22 Suhu/Lembab tiap 2000 ms)
    // ------------------------------------------------------------------------
    if (currentMillis - prevSlowSampleTime >= INTERVAL_READ_SLOW_MS) {
        prevSlowSampleTime = currentMillis;
        sensorMgr.updateSlowSensors();
    }

    // ------------------------------------------------------------------------
    // TUGAS 4: EVALUASI KENDALI HYSTERESIS SILO (Suhu, Gas, Kipas & Ventilasi)
    // ------------------------------------------------------------------------
    SensorData currentData = sensorMgr.getData();
    logicCtrl.evaluate(currentData, actuatorCtrl);

    // ------------------------------------------------------------------------
    // TUGAS 5: CEK PERINTAH MASUK DARI RASPBERRY PI 3 (UART / SERIAL)
    // ------------------------------------------------------------------------
    comm.processIncomingCommands(actuatorCtrl, conveyorPID);

    // ------------------------------------------------------------------------
    // TUGAS 6: PERBARUI TAMPILAN LAYAR LCD 16x2 I2C (Setiap 1000 ms)
    // ------------------------------------------------------------------------
    if (currentMillis - prevDisplayTime >= INTERVAL_LCD_UPDATE_MS) {
        prevDisplayTime = currentMillis;
        displayMgr.update(currentData, actuatorCtrl.getStatus(), logicCtrl, conveyorPID);
    }

    // ------------------------------------------------------------------------
    // TUGAS 7: KIRIM DATA TELEMETRI JSON KE RASPBERRY PI 3 (Setiap 1000 ms)
    // ------------------------------------------------------------------------
    if (currentMillis - prevTelemetryTime >= INTERVAL_TELEMETRY_MS) {
        prevTelemetryTime = currentMillis;
        comm.sendTelemetry(currentData, actuatorCtrl.getStatus(), logicCtrl, conveyorPID);
    }
}
