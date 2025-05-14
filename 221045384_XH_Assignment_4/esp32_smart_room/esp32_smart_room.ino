#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

const char* ssid = "Wie Wil Weet";
const char* password = "0614084796";
const char* serverUrl = "http://192.168.0.4:5000/api/control";

const int fanPin = 10;   // GPIO for fan (via transistor/MOSFET)
const int ledPin = 2;
const int ldrPin = A0;
const int pirPin = 3;    // GPIO for PIR motion sensor

bool autoMode = true;
bool ledOn = false;
bool fanOn = false;
bool motionDetected = false;

void setup() {
  Serial.begin(115200);
  pinMode(ledPin, OUTPUT);
  pinMode(fanPin, OUTPUT);
  pinMode(pirPin, INPUT);

  digitalWrite(ledPin, LOW);
  digitalWrite(fanPin, LOW);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");
}

void loop() {
  motionDetected = digitalRead(pirPin);

  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverUrl);
    int httpCode = http.GET();

    if (httpCode == 200) {
      String payload = http.getString();
      Serial.println("Payload: " + payload);

      DynamicJsonDocument doc(256);
      deserializeJson(doc, payload);

      autoMode = doc["auto"];
      ledOn = doc["led_on"];
      fanOn = doc["fan_on"];  // Manual fan toggle from Flet UI
    }

    http.end();
  }

  int ldrValue = analogRead(ldrPin);
  Serial.print("LDR Value: ");
  Serial.println(ldrValue);
  Serial.print("Motion Detected: ");
  Serial.println(motionDetected ? "Yes" : "No");

  // LED logic
  if (autoMode) {
    digitalWrite(ledPin, (ldrValue < 1000) ? HIGH : LOW);
  } else {
    digitalWrite(ledPin, ledOn ? HIGH : LOW);
  }

  // Fan logic
  if (autoMode) {
    digitalWrite(fanPin, motionDetected ? HIGH : LOW);
  } else {
    digitalWrite(fanPin, fanOn ? HIGH : LOW);
  }

  delay(1000);
}
