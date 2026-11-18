#include "conveyor_pid.h"

ConveyorPID::ConveyorPID() {
    setpoint = WEBCAM_STOP_POINT_CM;
    prevError = 0.0f;
    integral = 0.0f;
    lastTime = 0;
    lastError = 0.0f;
    lastOutputPWM = PWM_STOP;
    currentPhase = CONV_PHASE_IDLE;
    drainStartTime = 0;
}

void ConveyorPID::begin() {
    setpoint = WEBCAM_STOP_POINT_CM;
    prevError = 0.0f;
    integral = 0.0f;
    lastTime = millis();
    currentPhase = CONV_PHASE_IDLE;
}

// ============================================================================
// ALGORITMA PID DISKRIT UNTUK KENDALI PWM MOTOR KONVEYOR
// ============================================================================
int ConveyorPID::calculatePID(float currentDist, float dt) {
    if (dt <= 0.0f) dt = 0.05f; // Hindari pembagian dengan nol

    // 1. Hitung Nilai Galat / Error (Jarak Barang ke Titik Webcam)
    // Sensor berada di ujung silo. Saat barang mendekat, currentDist mengecil menuju setpoint.
    float error = currentDist - setpoint;
    lastError = error;

    // Jika barang sudah berada di dalam batas toleransi berhenti (Deadband)
    if (abs(error) <= STOP_TOLERANCE_CM) {
        integral = 0.0f; // Reset integral agar tidak wind-up saat diam
        return PWM_STOP;
    }

    // 2. Komponen Proporsional (P-Term)
    float pTerm = PID_KP * error;

    // 3. Komponen Integral (I-Term) dengan Anti-Windup Clamping
    integral += error * dt;
    integral = constrain(integral, -50.0f, 50.0f); // Cegah akumulasi berlebih
    float iTerm = PID_KI * integral;

    // 4. Komponen Derivatif (D-Term) untuk Pengereman Mulus (Anti-Overshoot)
    float dTerm = PID_KD * ((error - prevError) / dt);
    prevError = error;

    // 5. Total Sinyal Kontrol Matematis u(t)
    float controlSignal = pTerm + iTerm + dTerm;

    // 6. Konversi Sinyal Kontrol ke Rentang Fisik PWM Motor Kuning (L298N)
    int targetPWM = PWM_STOP;
    if (controlSignal > 0.0f) {
        // Terapkan batas ambang batas gesekan (Stiction) agar motor tidak berdengung
        int calculated = PWM_MIN_MOVING + (int)controlSignal;
        targetPWM = constrain(calculated, PWM_MIN_MOVING, PWM_MAX_SPEED);
    } else {
        targetPWM = PWM_STOP;
    }

    return targetPWM;
}

// ============================================================================
// STATE MACHINE & ORKESTRASI PERGERAKAN KONVEYOR
// ============================================================================
void ConveyorPID::compute(float currentDistanceCm, ActuatorController& actuators) {
    unsigned long now = millis();
    float dt = (now - lastTime) / 1000.0f;
    lastTime = now;

    // ------------------------------------------------------------------------
    // FASE A: SEDANG MENGALIRKAN BARANG YANG LOLOS SCAN MASUK KE SILO
    // ------------------------------------------------------------------------
    if (currentPhase == CONV_PHASE_DRAINING) {
        // Jalankan konveyor dengan kecepatan tetap selama 2.5 detik hingga barang jatuh ke silo
        if (now - drainStartTime < 2500) {
            actuators.setConveyor(true, PWM_MAX_SPEED);
            lastOutputPWM = PWM_MAX_SPEED;
            return;
        } else {
            // Waktu pengosongan selesai, kembali ke mode siap deteksi
            currentPhase = CONV_PHASE_IDLE;
        }
    }

    // ------------------------------------------------------------------------
    // FASE B: EVALUASI POSISI BARANG BERDASARKAN JARAK ULTRASONIK
    // ------------------------------------------------------------------------
    
    // Cek apakah tidak ada barang (jarak membaca ujung terjauh konveyor atau error)
    if (currentDistanceCm >= CONVEYOR_MAX_DIST_CM || currentDistanceCm <= 0.0f) {
        currentPhase = CONV_PHASE_IDLE;
        integral = 0.0f;
        actuators.setConveyor(false, PWM_STOP);
        lastOutputPWM = PWM_STOP;
        return;
    }

    // Jika ada barang yang sedang mendekat menuju titik webcam (Jarak > Setpoint)
    if (currentDistanceCm > (setpoint + STOP_TOLERANCE_CM)) {
        currentPhase = CONV_PHASE_APPROACHING;
        
        // Hitung modulasi kecepatan PID (semakin dekat semakin melambat)
        int pwm = calculatePID(currentDistanceCm, dt);
        lastOutputPWM = pwm;
        actuators.setConveyor(true, pwm);
    }
    // Jika barang sudah tiba tepat di depan webcam (Dalam radius toleransi)
    else if (abs(currentDistanceCm - setpoint) <= STOP_TOLERANCE_CM) {
        currentPhase = CONV_PHASE_AT_WEBCAM;
        lastOutputPWM = PWM_STOP;
        actuators.setConveyor(false, PWM_STOP); // Rem seketika!
    }
    // Jika barang terlanjur lewat melewati titik webcam menuju silo
    else {
        // Alirkan saja barang terus ke depan
        currentPhase = CONV_PHASE_APPROACHING;
        actuators.setConveyor(true, PWM_MIN_MOVING);
        lastOutputPWM = PWM_MIN_MOVING;
    }
}

// ============================================================================
// PERINTAH KONTROL DARI RASPBERRY PI 3 (SETELAH AI SELESAI SCAN)
// ============================================================================
void ConveyorPID::resumeAfterScan(ActuatorController& actuators) {
    currentPhase = CONV_PHASE_DRAINING;
    drainStartTime = millis();
    actuators.setConveyor(true, PWM_MAX_SPEED);
    lastOutputPWM = PWM_MAX_SPEED;
}

void ConveyorPID::manualStop(ActuatorController& actuators) {
    currentPhase = CONV_PHASE_IDLE;
    integral = 0.0f;
    actuators.setConveyor(false, PWM_STOP);
    lastOutputPWM = PWM_STOP;
}

void ConveyorPID::manualRun(ActuatorController& actuators, int speed) {
    currentPhase = CONV_PHASE_DRAINING;
    drainStartTime = millis() + 60000; // Manual run panjang
    actuators.setConveyor(true, speed);
    lastOutputPWM = speed;
}

ConveyorPhase ConveyorPID::getPhase() const {
    return currentPhase;
}

const char* ConveyorPID::getPhaseString() const {
    switch (currentPhase) {
        case CONV_PHASE_IDLE:        return "IDLE";
        case CONV_PHASE_APPROACHING: return "APPROACH";
        case CONV_PHASE_AT_WEBCAM:   return "AT_WEBCAM";
        case CONV_PHASE_DRAINING:    return "DRAIN_SILO";
        default:                     return "UNKNOWN";
    }
}

float ConveyorPID::getError() const {
    return lastError;
}

int ConveyorPID::getLastPWM() const {
    return lastOutputPWM;
}

bool ConveyorPID::isItemAtWebcam() const {
    return (currentPhase == CONV_PHASE_AT_WEBCAM);
}
