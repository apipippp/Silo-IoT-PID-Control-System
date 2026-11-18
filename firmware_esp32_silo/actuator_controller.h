#ifndef ACTUATOR_CONTROLLER_H
#define ACTUATOR_CONTROLLER_H

#include <Arduino.h>
#include <ESP32Servo.h>
#include "config.h"

// Status Aktuator untuk kemudahan pemantauan
struct ActuatorStatus {
    bool fansActive;         // Status 2 Kipas (True = Nyala, False = Mati)
    int  ventilationAngle;   // Sudut bukaan ventilasi servo (0° - 90°)
    bool conveyorRunning;    // Status konveyor (True = Jalan, False = Berhenti)
    int  conveyorSpeed;      // Kecepatan PWM konveyor (0 - 255)
};

class ActuatorController {
public:
    ActuatorController();
    void begin();

    // Kontrol 2 Kipas via 1 Relay
    void setFans(bool enable);

    // Kontrol Katup Ventilasi Atap Silo
    void setVentilationAngle(int angle);

    // Kontrol Motor DC Konveyor (L298N)
    void setConveyor(bool run, int speed = CONVEYOR_SPEED_NORMAL);

    // Ambil status terkini seluruh aktuator
    ActuatorStatus getStatus() const;

private:
    Servo ventServo;
    ActuatorStatus status;
};

#endif // ACTUATOR_CONTROLLER_H
