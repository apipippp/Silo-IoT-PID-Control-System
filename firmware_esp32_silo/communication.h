#ifndef COMMUNICATION_H
#define COMMUNICATION_H

#include <Arduino.h>
#include <ArduinoJson.h>
#include "config.h"
#include "sensor_manager.h"
#include "actuator_controller.h"
#include "control_logic.h"
#include "conveyor_pid.h"

class Communication {
public:
    Communication();
    void begin();

    // Kirim paket data telemetri JSON ke Raspberry Pi 3
    void sendTelemetry(const SensorData& sensors, const ActuatorStatus& actuators, const ControlLogic& logic, const ConveyorPID& conveyor);

    // Cek dan proses perintah yang masuk dari Raspberry Pi 3
    void processIncomingCommands(ActuatorController& actuators, ConveyorPID& conveyor);

private:
    HardwareSerial RaspiSerial;
    String rxBuffer;

    void parseAndExecuteCommand(const String& cmdString, ActuatorController& actuators, ConveyorPID& conveyor);
};

#endif // COMMUNICATION_H
