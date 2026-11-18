#include "sensor_manager.h"

SensorManager::SensorManager() : dht(PIN_DHT22, DHT22) {
    data.temperature = 28.0f;
    data.humidity = 60.0f;
    data.gasRaw = 500.0f;
    data.gasFiltered = 500.0f;
    data.distanceCm = CONVEYOR_MAX_DIST_CM;
    data.siloCapacityPct = 0;
    data.dhtValid = false;
}

void SensorManager::begin() {
    dht.begin();
    pinMode(PIN_MQ2_ADC, INPUT);
    pinMode(PIN_TRIG_US, OUTPUT);
    pinMode(PIN_ECHO_US, INPUT);
    digitalWrite(PIN_TRIG_US, LOW);

    float initialGas = (float)analogRead(PIN_MQ2_ADC);
    data.gasRaw = initialGas;
    data.gasFiltered = initialGas;
}

void SensorManager::updateFastSensors() {
    data.gasRaw = (float)analogRead(PIN_MQ2_ADC);
    data.gasFiltered = applyEMA(data.gasRaw, data.gasFiltered, EMA_ALPHA);
}

// Update khusus sensor ultrasonik untuk kebutuhan loop PID konveyor (50 ms)
void SensorManager::updateUltrasonic() {
    float dist = readUltrasonicDistance();
    if (dist > 0.0f && dist <= (CONVEYOR_MAX_DIST_CM + 10.0f)) {
        data.distanceCm = dist;
        data.siloCapacityPct = calculateCapacity(dist);
    }
}

void SensorManager::updateSlowSensors() {
    float t = dht.readTemperature();
    float h = dht.readHumidity();

    if (!isnan(t) && !isnan(h) && t > 0.0f && t < 80.0f && h >= 0.0f && h <= 100.0f) {
        data.temperature = t;
        data.humidity = h;
        data.dhtValid = true;
    } else {
        data.dhtValid = false;
    }
}

SensorData SensorManager::getData() const {
    return data;
}

float SensorManager::getDistanceCm() const {
    return data.distanceCm;
}

float SensorManager::applyEMA(float current, float previous, float alpha) {
    return (alpha * current) + ((1.0f - alpha) * previous);
}

float SensorManager::readUltrasonicDistance() {
    digitalWrite(PIN_TRIG_US, LOW);
    delayMicroseconds(2);
    digitalWrite(PIN_TRIG_US, HIGH);
    delayMicroseconds(10);
    digitalWrite(PIN_TRIG_US, LOW);

    // Timeout 12.000 µs (~200 cm, sangat cukup untuk konveyor 45 cm, tidak membuat loop lambat)
    unsigned long duration = pulseIn(PIN_ECHO_US, HIGH, 12000);
    if (duration == 0) {
        return CONVEYOR_MAX_DIST_CM; // Timeout = anggap tidak ada barang
    }

    float distance = (duration * 0.0343f) / 2.0f;
    return distance;
}

int SensorManager::calculateCapacity(float distance) {
    if (distance >= SILO_DEPTH_EMPTY_CM) return 0;
    if (distance <= SILO_DEPTH_FULL_CM)  return 100;

    float pct = ((SILO_DEPTH_EMPTY_CM - distance) / (SILO_DEPTH_EMPTY_CM - SILO_DEPTH_FULL_CM)) * 100.0f;
    return constrain((int)pct, 0, 100);
}
