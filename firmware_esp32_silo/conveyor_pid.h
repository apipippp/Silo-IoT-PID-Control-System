#ifndef CONVEYOR_PID_H
#define CONVEYOR_PID_H

#include <Arduino.h>
#include "config.h"
#include "actuator_controller.h"

// State Machine Tahapan Pergerakan Konveyor
enum ConveyorPhase {
    CONV_PHASE_IDLE,        // Tidak ada barang di konveyor
    CONV_PHASE_APPROACHING, // Barang terdeteksi & PID memperlambat ke titik webcam
    CONV_PHASE_AT_WEBCAM,   // Barang berhenti tepat di titik henti webcam
    CONV_PHASE_DRAINING     // Barang lolos scan, dialirkan jatuh ke dalam silo
};

class ConveyorPID {
public:
    ConveyorPID();
    void begin();

    // Hitung PID dan atur kecepatan motor L298N (dijalankan tiap 50 ms)
    void compute(float currentDistanceCm, ActuatorController& actuators);

    // Perintah eksternal (dari Raspberry Pi 3 atau tombol)
    void resumeAfterScan(ActuatorController& actuators); // Barang lolos scan -> jalan ke silo
    void manualStop(ActuatorController& actuators);
    void manualRun(ActuatorController& actuators, int speed = PWM_MAX_SPEED);

    // Getters untuk Telemetri & Debugging
    ConveyorPhase getPhase() const;
    const char*   getPhaseString() const;
    float         getError() const;
    int           getLastPWM() const;
    bool          isItemAtWebcam() const;

private:
    ConveyorPhase currentPhase;

    // Variabel Matematika PID
    float setpoint;        // Titik henti webcam (cm)
    float prevError;       // Galat siklus sebelumnya (e[k-1])
    float integral;        // Akumulasi galat integral
    unsigned long lastTime;// Waktu komputasi terakhir (millis)
    
    // Status & Output
    float lastError;
    int   lastOutputPWM;
    unsigned long drainStartTime; // Timer saat barang dialirkan ke silo

    // Fungsi Internal Hitung PID Diskrit
    int calculatePID(float currentDist, float dt);
};

#endif // CONVEYOR_PID_H
