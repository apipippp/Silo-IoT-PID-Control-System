#ifndef SENSOR_MANAGER_H
#define SENSOR_MANAGER_H

#include <Arduino.h>
#include <DHT.h>
#include "config.h"

// Struktur data terpadu untuk menampung seluruh pembacaan sensor yang telah difilter
struct SensorData {
    float temperature;     // Suhu terfilter (°C)
    float humidity;        // Kelembaban terfilter (% RH)
    float gasRaw;          // Nilai mentah ADC gas MQ-2
    float gasFiltered;     // Nilai gas terfilter EMA
    float distanceCm;      // Jarak barang di konveyor (cm)
    int   siloCapacityPct; // Persentase isi silo (0% - 100%)
    bool  dhtValid;        // Penanda apakah DHT22 terbaca valid
};

class SensorManager {
public:
    SensorManager();
    void begin();
    
    // Fungsi pembacaan berkala
    void updateFastSensors();      // Dibaca tiap 100ms (MQ-2 EMA)
    void updateUltrasonic();       // Dibaca tiap 50ms (Khusus loop PID konveyor)
    void updateSlowSensors();      // Dibaca tiap 2000ms (DHT22 Suhu & Lembab)

    // Getter data
    SensorData getData() const;
    float getDistanceCm() const;

private:
    DHT dht;
    SensorData data;

    // Filter Helpers
    float applyEMA(float current, float previous, float alpha);
    float readUltrasonicDistance();
    int   calculateCapacity(float distance);
};

#endif // SENSOR_MANAGER_H
