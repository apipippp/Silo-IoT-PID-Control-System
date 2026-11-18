#include "communication.h"

Communication::Communication() : RaspiSerial(2) {
    rxBuffer = "";
}

void Communication::begin() {
    Serial.begin(UART_BAUDRATE);
    RaspiSerial.begin(UART_BAUDRATE, SERIAL_8N1, PIN_UART_RX2, PIN_UART_TX2);

    Serial.println("\n[SISTEM] Komunikasi Serial ESP32 Siap.");
    Serial.println("[SISTEM] Port Serial2 terhubung ke Raspberry Pi 3 (RX2=16, TX2=17).");
}

void Communication::sendTelemetry(const SensorData& sensors, const ActuatorStatus& actuators, const ControlLogic& logic, const ConveyorPID& conveyor) {
    StaticJsonDocument<288> doc;

    doc["temp"]        = serialized(String(sensors.temperature, 1));
    doc["hum"]         = serialized(String(sensors.humidity, 1));
    doc["gas"]         = (int)sensors.gasFiltered;
    doc["dist_cm"]     = serialized(String(sensors.distanceCm, 1));
    doc["pid_err"]     = serialized(String(conveyor.getError(), 1));
    doc["conv_phase"]  = conveyor.getPhaseString();
    doc["conv_pwm"]    = conveyor.getLastPWM();
    doc["silo_state"]  = logic.getStateString();
    doc["fans"]        = actuators.fansActive ? 1 : 0;
    doc["vent_deg"]    = actuators.ventilationAngle;

    String output;
    serializeJson(doc, output);
    output += "\n";

    RaspiSerial.print(output);

    Serial.print("[TELEMETRY -> RASPI]: ");
    Serial.print(output);
}

void Communication::processIncomingCommands(ActuatorController& actuators, ConveyorPID& conveyor) {
    while (RaspiSerial.available() > 0) {
        char c = (char)RaspiSerial.read();
        if (c == '\n') {
            rxBuffer.trim();
            if (rxBuffer.length() > 0) {
                parseAndExecuteCommand(rxBuffer, actuators, conveyor);
            }
            rxBuffer = "";
        } else if (c != '\r') {
            rxBuffer += c;
        }
    }

    while (Serial.available() > 0) {
        char c = (char)Serial.read();
        if (c == '\n') {
            rxBuffer.trim();
            if (rxBuffer.length() > 0) {
                Serial.print("[MANUAL COMMAND]: ");
                Serial.println(rxBuffer);
                parseAndExecuteCommand(rxBuffer, actuators, conveyor);
            }
            rxBuffer = "";
        } else if (c != '\r') {
            rxBuffer += c;
        }
    }
}

void Communication::parseAndExecuteCommand(const String& cmdString, ActuatorController& actuators, ConveyorPID& conveyor) {
    StaticJsonDocument<200> doc;
    DeserializationError error = deserializeJson(doc, cmdString);

    String cmd = "";
    int val = -1;

    if (!error) {
        if (doc.containsKey("cmd")) {
            cmd = doc["cmd"].as<String>();
        }
        if (doc.containsKey("val")) {
            val = doc["val"].as<int>();
        }
    } else {
        cmd = cmdString;
    }

    cmd.toUpperCase();

    // 1. Perintah dari Raspi setelah Webcam selesai scan objek
    if (cmd == "SCAN_PASS" || cmd == "SCAN_DONE" || cmd == "RESUME_CONVEYOR" || cmd == "RUN_CONVEYOR") {
        conveyor.resumeAfterScan(actuators);
        Serial.println("[AKSI]: Scan Selesai! Konveyor dialirkan masuk ke silo.");
    }
    else if (cmd == "STOP_CONVEYOR" || cmd == "CONV_STOP") {
        conveyor.manualStop(actuators);
        Serial.println("[AKSI]: Konveyor DIHENTIKAN manual.");
    }
    else if (cmd == "VENT_OPEN") {
        actuators.setVentilationAngle(SERVO_ANGLE_FULL);
        Serial.println("[AKSI]: Ventilasi dibuka 90° manual.");
    }
    else if (cmd == "VENT_CLOSE") {
        actuators.setVentilationAngle(SERVO_ANGLE_CLOSED);
        Serial.println("[AKSI]: Ventilasi ditutup 0° manual.");
    }
    else if (cmd == "FAN_ON") {
        actuators.setFans(true);
        Serial.println("[AKSI]: 2 Fan dinyalakan manual.");
    }
    else if (cmd == "FAN_OFF") {
        actuators.setFans(false);
        Serial.println("[AKSI]: 2 Fan dimatikan manual.");
    }
    else {
        Serial.print("[WARNING]: Perintah tidak dikenali: ");
        Serial.println(cmd);
    }
}
