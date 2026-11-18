#ifndef DISPLAY_MANAGER_H
#define DISPLAY_MANAGER_H

#include <Arduino.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include "config.h"
#include "sensor_manager.h"
#include "actuator_controller.h"
#include "control_logic.h"
#include "conveyor_pid.h"

class DisplayManager {
public:
    DisplayManager();
    void begin();
    
    // Perbarui tampilan LCD (non-blocking)
    void update(const SensorData& sensors, const ActuatorStatus& actuators, const ControlLogic& logic, const ConveyorPID& conveyor);

private:
    LiquidCrystal_I2C lcd;
    int currentScreen;
    unsigned long lastScreenSwitch;

    void renderScreen1(const SensorData& sensors, const ControlLogic& logic);
    void renderScreen2(const SensorData& sensors, const ConveyorPID& conveyor, const ActuatorStatus& actuators);
};

#endif // DISPLAY_MANAGER_H
