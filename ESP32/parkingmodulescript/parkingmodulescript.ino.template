#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

// TODO: Replace with your WiFi credentials
const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";

// Device and manager identification
const char* device_id = "ps1";  // Parking Spot ID
const char* manager_id = "pz1"; // Parking Zone ID

// TODO: Replace with your server IP and port
const char* server_ip = "http://YOUR_SERVER_IP:8000/parking_module/ps1";

const int trigPin = 5;
const int echoPin = 18;

// define sound speed in cm/uS
#define SOUND_SPEED 0.034
#define CM_TO_INCH 0.393701

long duration;
float distanceCm;

// the following variables are unsigned longs because the time, measured in
// milliseconds, will quickly become a bigger number than can be stored in an int.
unsigned long lastTime = 0;
// Timer set to 10 minutes (600000)
// unsigned long timerDelay = 600000;
// Set timer to 5 seconds (5000)
unsigned long timerDelay = 5000;

// GPS coordinates (replace with actual values)
float latitude = 0.0;
float longitude = 0.0;

void setup() {
  Serial.begin(115200);
  pinMode(trigPin, OUTPUT); // Sets the trigPin as an Output
  pinMode(echoPin, INPUT); // Sets the echoPin as an Input
  delay(1000);

  WiFi.mode(WIFI_STA); // Optional
  WiFi.begin(ssid, password);
  Serial.println("\nConnecting");

  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(100);
  }

  Serial.println("\nConnected to the WiFi network");
  Serial.print("Local ESP32 IP: ");
  Serial.println(WiFi.localIP());

  std::string endpoint = server_ip + std::string("/") + manager_id;
  const char* endpoint_char = endpoint.c_str();
  WiFiClient client;
  HTTPClient http;
  StaticJsonDocument<200> doc;
  doc["lat"] = latitude;   // Replace latitude with your actual value
  doc["lon"] = longitude;  // Replace longitude with your actual value
  String payload;
  serializeJson(doc, payload);

  if (http.begin(client, endpoint_char)) {
    http.addHeader("Content-Type", "application/json");
    int httpResponseCode = http.POST(payload);

    if (httpResponseCode > 0) {
      Serial.print("HTTP Response code: ");
      Serial.println(httpResponseCode);
      String response = http.getString();
      Serial.println(response);
    } else {
      Serial.print("Error code: ");
      Serial.println(httpResponseCode);
    }

    // Free resources
    http.end();
  } else {
    Serial.println("Unable to connect to the server");
  }
}

void sendDataToServer(int distance) {
  WiFiClient client;
  HTTPClient http;

  // Create the JSON payload
  StaticJsonDocument<200> doc;
  doc["sonar_value"] = distance;
  String payload;
  serializeJson(doc, payload);

  // Make the POST request
  if (http.begin(client, server_ip)) {
    http.addHeader("Content-Type", "application/json");
    int httpResponseCode = http.POST(payload);

    if (httpResponseCode > 0) {
      Serial.print("HTTP Response code: ");
      Serial.println(httpResponseCode);
      String response = http.getString();
      Serial.println(response);
    } else {
      Serial.print("Error code: ");
      Serial.println(httpResponseCode);
    }

    // Free resources
    http.end();
  } else {
    Serial.println("Unable to connect to the server");
  }
}

void loop() {
  // Clears the trigPin
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  // Sets the trigPin on HIGH state for 10 microseconds
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  // Reads the echoPin, returns the sound wave travel time in microseconds
  duration = pulseIn(echoPin, HIGH);

  // Calculate the distance
  distanceCm = duration * SOUND_SPEED / 2;

  // Convert to inches
  float distanceInch = distanceCm * CM_TO_INCH;

  // Prints the distance in the Serial Monitor
  Serial.print("Distance (cm): ");
  Serial.println(distanceCm);

  // Send the distance value to the server
  int distanceInt = static_cast<int>(distanceCm);
  sendDataToServer(distanceInt);

  delay(timerDelay);
}