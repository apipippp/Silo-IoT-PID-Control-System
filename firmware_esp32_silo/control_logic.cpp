#include "control_logic.h"

ControlLogic::ControlLogic() {
    currentState = SILO_STATE_NORMAL;
    tempAlertActive = false;
    humAlertActive  = false;
    gasAlertActive  = false;
}

// ============================================================================
// 1. UPDATE STATUS HYSTERESIS TIAP SENSOR (ANTI-CHATTERING)
// ============================================================================
void ControlLogic::updateHysteresis(const SensorData& sensors) {
    // --- HYSTERESIS SUHU ---
    if (!tempAlertActive && sensors.temperature >= THRESHOLD_TEMP_HIGH) {
        tempAlertActive = true;  // Trigger ON saat tembus batas atas
    } else if (tempAlertActive && sensors.temperature <= THRESHOLD_TEMP_LOW) {
        tempAlertActive = false; // Reset OFF baru terjadi setelah turun ke batas bawah
    }

    // --- HYSTERESIS KELEMBABAN ---
    if (!humAlertActive && sensors.humidity >= THRESHOLD_HUM_HIGH) {
        humAlertActive = true;
    } else if (humAlertActive && sensors.humidity <= THRESHOLD_HUM_LOW) {
        humAlertActive = false;
    }

    // --- HYSTERESIS GAS MQ-2 ---
    if (!gasAlertActive && sensors.gasFiltered >= THRESHOLD_GAS_HIGH) {
        gasAlertActive = true;
    } else if (gasAlertActive && sensors.gasFiltered <= THRESHOLD_GAS_LOW) {
        gasAlertActive = false;
    }
}

// ============================================================================
// 2. MATRIKS KEPUTUSAN KENDALI & AKTUASI SILO
// ============================================================================
void ControlLogic::evaluate(const SensorData& sensors, ActuatorController& actuators) {
    // Perbarui status hysteresis masing-masing parameter
    updateHysteresis(sensors);

    bool climateAlert = (tempAlertActive || humAlertActive);

    // Evaluasi Kombinasi Status Silo:
    if (climateAlert && gasAlertActive) {
        // KONDISI 4: CRITICAL (Suhu/Lembab Tinggi DAN Gas Tinggi)
        currentState = SILO_STATE_CRITICAL;
        actuators.setVentilationAngle(SERVO_ANGLE_FULL); // Buka penuh 90°
        actuators.setFans(true);                         // Paket 2 Kipas ON
    } 
    else if (gasAlertActive) {
        // KONDISI 3: WARNING GAS (Bau Busuk / Pembusukan Biji)
        currentState = SILO_STATE_WARNING_GAS;
        actuators.setVentilationAngle(SERVO_ANGLE_FULL); // Buka penuh 90°
        actuators.setFans(true);                         // Paket 2 Kipas ON
    } 
    else if (climateAlert) {
        // KONDISI 2: WARNING SUHU / KELEMBABAN
        currentState = SILO_STATE_WARNING_TEMP;
        actuators.setVentilationAngle(SERVO_ANGLE_HALF); // Buka separuh 45°
        actuators.setFans(true);                         // Paket 2 Kipas ON
    } 
    else {
        // KONDISI 1: NORMAL (Semua Parameter Aman)
        currentState = SILO_STATE_NORMAL;
        actuators.setVentilationAngle(SERVO_ANGLE_CLOSED); // Tutup rapat 0°
        actuators.setFans(false);                          // Paket 2 Kipas OFF
    }
}

SiloState ControlLogic::getState() const {
    return currentState;
}

const char* ControlLogic::getStateString() const {
    switch (currentState) {
        case SILO_STATE_NORMAL:       return "NORMAL";
        case SILO_STATE_WARNING_TEMP: return "WARN_TEMP";
        case SILO_STATE_WARNING_GAS:  return "WARN_GAS";
        case SILO_STATE_CRITICAL:     return "CRITICAL";
        default:                      return "UNKNOWN";
    }
}

bool ControlLogic::isTempAlert() const {
    return tempAlertActive;
}

bool ControlLogic::isGasAlert() const {
    return gasAlertActive;
}
