#ifndef CONTROL_LOGIC_H
#define CONTROL_LOGIC_H

#include <Arduino.h>
#include "config.h"
#include "sensor_manager.h"
#include "actuator_controller.h"

// Definisi Status Keamanan Lingkungan Silo
enum SiloState {
    SILO_STATE_NORMAL,       // Suhu, kelembaban, dan gas dalam batas normal
    SILO_STATE_WARNING_TEMP, // Suhu atau kelembaban melampaui batas aman
    SILO_STATE_WARNING_GAS,  // Konsentrasi gas pembusukan tinggi terdeteksi
    SILO_STATE_CRITICAL      // Suhu tinggi DAN gas tinggi secara bersamaan!
};

class ControlLogic {
public:
    ControlLogic();

    // Memproses data sensor dan menentukan tindakan aktuator
    void evaluate(const SensorData& sensors, ActuatorController& actuators);

    // Getter status
    SiloState getState() const;
    const char* getStateString() const;
    bool isTempAlert() const;
    bool isGasAlert() const;

private:
    SiloState currentState;
    
    // Flag Hysteresis Memori (Menyimpan status saat ini agar tidak chattering)
    bool tempAlertActive;
    bool humAlertActive;
    bool gasAlertActive;

    // Evaluasi Hysteresis
    void updateHysteresis(const SensorData& sensors);
};

#endif // CONTROL_LOGIC_H
