#include <Wire.h>
#include "MAX30105.h"
#include "heartRate.h"
#include <TinyGPS++.h>
#include <SPI.h>
#include <RH_RF95.h>

MAX30105 particleSensor;
TinyGPSPlus gps;
RH_RF95 rf95;

const float freq = 868.0;

const byte RATE_SIZE = 4;
byte rates[RATE_SIZE];
byte rateSpot = 0;
long lastBeat = 0;

float beatsPerMinute = 0;
int beatAvg = 0;

unsigned long lastSendTime = 0;
const unsigned long sendInterval = 30000;

void setup() {
  Serial.begin(9600);
  delay(1000);

  if (!rf95.init()) {
    Serial.println("Erreur init LoRa");
    while (1);
  }
  rf95.setFrequency(freq);
  rf95.setTxPower(13);
  Serial.println("LoRa + GPS + BPM prêt");

  if (!particleSensor.begin(Wire, I2C_SPEED_FAST)) {
    Serial.println("MAX30105 non détecté.");
    while (1);
  }
  particleSensor.setup();
  particleSensor.setPulseAmplitudeRed(0x0A);
  particleSensor.setPulseAmplitudeGreen(0);
}

void loop() {
  while (Serial.available() > 0) {
    gps.encode(Serial.read());
  }

  long irValue = particleSensor.getIR();

  if (checkForBeat(irValue)) {
    long delta = millis() - lastBeat;
    lastBeat = millis();
    beatsPerMinute = 60 / (delta / 1000.0);

    if (beatsPerMinute < 255 && beatsPerMinute > 20) {
      rates[rateSpot++] = (byte)beatsPerMinute;
      rateSpot %= RATE_SIZE;
      beatAvg = 0;
      for (byte x = 0; x < RATE_SIZE; x++)
        beatAvg += rates[x];
      beatAvg /= RATE_SIZE;
    }
  }

  Serial.print("IR="); Serial.print(irValue);
  Serial.print(" BPM="); Serial.print(beatsPerMinute);
  Serial.print(" Avg BPM="); Serial.print(beatAvg);
  if (irValue < 50000) Serial.print(" (Pas de doigt)");
  Serial.println();

  if (millis() - lastSendTime > sendInterval) {
    lastSendTime = millis();

    float lat = -1, lon = -1;
    if (gps.location.isValid()) {
      lat = gps.location.lat();
      lon = gps.location.lng();
    } else {
      Serial.println("GPS invalide, valeurs -1 utilisées.");
    }

    String bpmStr;
    if (irValue < 50000) {
      bpmStr = "-1";
    } else {
      bpmStr = String(beatAvg);
    }

    String payload = String(lat, 6) + "," + String(lon, 6) + "," + bpmStr;
    Serial.print("Envoi LoRa : "); Serial.println(payload);

    rf95.send((uint8_t*)payload.c_str(), strlen(payload.c_str()));
    rf95.waitPacketSent();
    Serial.println("Envoyé.\n------------------------");
  }
}
