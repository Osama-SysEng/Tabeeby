/*
  TABEEBY Microcontroller Firmware
  Arduino-compatible medical IoT device firmware
*/

#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>

const char* ssid = "TABEEBY_IOT";
const char* password = "SECURE_PASSWORD";
const char* mqtt_server = "iot-service.tabeeby.health";
const int mqtt_port = 1883;

WiFiClient espClient;
PubSubClient client(espClient);

// Sensor pins
#define HEART_RATE_PIN A0
#define TEMP_PIN A1
#define SPO2_PIN A2

unsigned long lastMsg = 0;
const long interval = 60000; // 1 minute

void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    String clientId = "TABEEBY-DEVICE-" + String(random(0xffff), HEX);
    if (client.connect(clientId.c_str())) {
      Serial.println("connected");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

void setup() {
  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server, mqtt_port);

  pinMode(HEART_RATE_PIN, INPUT);
  pinMode(TEMP_PIN, INPUT);
  pinMode(SPO2_PIN, INPUT);
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  unsigned long now = millis();
  if (now - lastMsg > interval) {
    lastMsg = now;

    // Read sensors
    int heartRate = analogRead(HEART_RATE_PIN);
    float temperature = (analogRead(TEMP_PIN) * 3.3 / 4095.0) * 100;
    int spo2 = analogRead(SPO2_PIN);

    // Create JSON payload
    StaticJsonDocument<256> doc;
    doc["device_id"] = "TABEEBY-MCU-001";
    doc["patient_id"] = "PATIENT-UUID";
    doc["timestamp"] = now;
    doc["readings"]["heart_rate"] = map(heartRate, 0, 4095, 50, 150);
    doc["readings"]["temperature"] = temperature;
    doc["readings"]["spo2"] = map(spo2, 0, 4095, 90, 100);

    char payload[256];
    serializeJson(doc, payload);

    client.publish("tabeeby/iot/vitals", payload);
    Serial.println("Data published");
  }
}
