#include "actuator_controller.h"

// Kebanyakan modul relay optocoupler Arduino adalah ACTIVE-LOW (LOW = Nyala, HIGH = Mati)
// Jika relay Anda tipe Active-HIGH, cukup balik definisi ini.
#define RELAY_ACTIVE_LEVEL   LOW
#define RELAY_INACTIVE_LEVEL HIGH

ActuatorController::ActuatorController() {
    status.fansActive = false;
    status.ventilationAngle = SERVO_ANGLE_CLOSED;
    status.conveyorRunning = false;
    status.conveyorSpeed = CONVEYOR_SPEED_STOP;
}

void ActuatorController::begin() {
    // 1. Inisialisasi Relay Kipas (1 Relay mengontrol 2 Kipas DC 12V)
    pinMode(PIN_RELAY_FAN, OUTPUT);
    digitalWrite(PIN_RELAY_FAN, RELAY_INACTIVE_LEVEL); // Matikan saat start
    status.fansActive = false;

    // 2. Inisialisasi Servo SG90 (ESP32Servo Library)
    ESP32PWM::allocateTimer(0);
    ESP32PWM::allocateTimer(1);
    ventServo.setPeriodHertz(50); // Standar servo 50 Hz
    ventServo.attach(PIN_SERVO_VENT, 500, 2400); // Lebar pulsa mikrodetik SG90
    setVentilationAngle(SERVO_ANGLE_CLOSED);      // Posisi awal: Tertutup rapat (0°)

    // 3. Inisialisasi Driver Motor L298N Konveyor
    pinMode(PIN_L298N_IN1, OUTPUT);
    pinMode(PIN_L298N_IN2, OUTPUT);
    pinMode(PIN_L298N_ENA, OUTPUT);
    setConveyor(false, CONVEYOR_SPEED_STOP);      // Posisi awal: Konveyor diam
}

// ============================================================================
// KONTROL KIPAS (2 FAN DIKENDALIKAN SEKALIGUS LEWAT 1 RELAY)
// ============================================================================
void ActuatorController::setFans(bool enable) {
    if (enable) {
        digitalWrite(PIN_RELAY_FAN, RELAY_ACTIVE_LEVEL);
        status.fansActive = true;
    } else {
        digitalWrite(PIN_RELAY_FAN, RELAY_INACTIVE_LEVEL);
        status.fansActive = false;
    }
}

// ============================================================================
// KONTROL SERVO VENTILASI ATAP SILO (SUDUT 0° - 90°)
// ============================================================================
void ActuatorController::setVentilationAngle(int angle) {
    int safeAngle = constrain(angle, 0, 90);
    ventServo.write(safeAngle);
    status.ventilationAngle = safeAngle;
}

// ============================================================================
// KONTROL MOTOR KONVEYOR (MAJU / BERHENTI / PENGATURAN KECEPATAN PWM)
// ============================================================================
void ActuatorController::setConveyor(bool run, int speed) {
    if (run) {
        // Konveyor Maju
        digitalWrite(PIN_L298N_IN1, HIGH);
        digitalWrite(PIN_L298N_IN2, LOW);
        int safeSpeed = constrain(speed, 0, 255);
        analogWrite(PIN_L298N_ENA, safeSpeed);
        status.conveyorRunning = true;
        status.conveyorSpeed = safeSpeed;
    } else {
        // Konveyor Berhenti (Rem Listrik)
        digitalWrite(PIN_L298N_IN1, LOW);
        digitalWrite(PIN_L298N_IN2, LOW);
        analogWrite(PIN_L298N_ENA, 0);
        status.conveyorRunning = false;
        status.conveyorSpeed = 0;
    }
}

ActuatorStatus ActuatorController::getStatus() const {
    return status;
}
