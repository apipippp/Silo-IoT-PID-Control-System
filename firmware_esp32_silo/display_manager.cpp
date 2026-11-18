#include "display_manager.h"

DisplayManager::DisplayManager() : lcd(LCD_I2C_ADDR, LCD_COLS, LCD_ROWS) {
    currentScreen = 0;
    lastScreenSwitch = 0;
}

void DisplayManager::begin() {
    Wire.begin();
    lcd.init();
    lcd.backlight();
    lcd.clear();

    lcd.setCursor(0, 0);
    lcd.print(" SILO MONITORING ");
    lcd.setCursor(0, 1);
    lcd.print("  CONVEYOR PID   ");
    delay(1500);
    lcd.clear();
}

void DisplayManager::update(const SensorData& sensors, const ActuatorStatus& actuators, const ControlLogic& logic, const ConveyorPID& conveyor) {
    if (millis() - lastScreenSwitch > 3500) {
        lastScreenSwitch = millis();
        currentScreen = (currentScreen + 1) % 2;
        lcd.clear();
    }

    if (currentScreen == 0) {
        renderScreen1(sensors, logic);
    } else {
        renderScreen2(sensors, conveyor, actuators);
    }
}

// Layar 1: Status Iklim Silo (Suhu, Lembab, Gas, State)
void DisplayManager::renderScreen1(const SensorData& sensors, const ControlLogic& logic) {
    char line0[17];
    char line1[17];

    snprintf(line0, sizeof(line0), "T:%.1fC H:%.0f%%", sensors.temperature, sensors.humidity);
    const char* st = logic.getStateString();
    snprintf(line1, sizeof(line1), "G:%.0f [%s]", sensors.gasFiltered, st);

    lcd.setCursor(0, 0);
    lcd.print(line0);
    lcd.setCursor(0, 1);
    lcd.print(line1);
}

// Layar 2: Status PID Konveyor (Jarak Aktual, Galat Error, PWM & Fase)
void DisplayManager::renderScreen2(const SensorData& sensors, const ConveyorPID& conveyor, const ActuatorStatus& actuators) {
    char line0[17];
    char line1[17];

    // Baris 0: Jarak sensor & Error ke titik webcam (SP: 15cm)
    snprintf(line0, sizeof(line0), "D:%.1f e:%.1fcm", sensors.distanceCm, conveyor.getError());

    // Baris 1: Nilai PWM dan Status Fase (APPROACH / AT_CAM / DRAIN)
    snprintf(line1, sizeof(line1), "PWM:%d [%s]", conveyor.getLastPWM(), conveyor.getPhaseString());

    lcd.setCursor(0, 0);
    lcd.print(line0);
    lcd.setCursor(0, 1);
    lcd.print(line1);
}
