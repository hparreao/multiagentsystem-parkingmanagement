#include <WiFi.h>
#include <PubSubClient.h>
#include "SevSeg.h"

// TODO: Replace with your WiFi credentials
const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";

// TODO: Replace with your MQTT broker information
const char* mqttServer = "YOUR_MQTT_BROKER_IP";
const int mqttPort = 1883;
const char* mqttSetTopic = "pz1_set_topic";
const char* mqttValueTopic = "pz1_display_value";

WiFiClient espClient;
PubSubClient client(espClient);
SevSeg sevseg;

bool isTopicSet = false;

void setup() {
  // Connect to Wi-Fi
  Serial.begin(115200);
  Serial.println("IM ALIVE");
  WiFi.mode(WIFI_STA); // Optional
  WiFi.begin(ssid, password);
  Serial.println("\nConnecting");

  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(100);
  }
  Serial.println("WiFi connected");

  IPAddress ip;
  if (WiFi.hostByName(mqttServer, ip)) {
    Serial.print("Ping successful. IP address: ");
    Serial.println(ip);
  } else {
    Serial.println("Ping failed");
  }

  // Connect to MQTT Broker
  client.setServer(mqttServer, mqttPort);
  client.setCallback(callback);

  Serial.println("Connecting to MQTT Broker...");

  while (!client.connected()) {
    if (client.connect("ESP32Client")) {
      Serial.println("MQTT connected");
      client.subscribe(mqttSetTopic);
    } else {
      Serial.print("MQTT connection failed, retrying in 5 seconds...");
      delay(5000);
    }
  }

  // Initialize the seven-segment display
  byte sevenSegments = 1;
  byte CommonPins[] = {};
  byte LEDsegmentPins[] = {13, 32, 14, 27, 26, 25, 33};
  bool resistorsOnSegments = true;
  sevseg.begin(COMMON_ANODE, sevenSegments, CommonPins, LEDsegmentPins, resistorsOnSegments);
  sevseg.setBrightness(80);
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
}

void callback(char* topic, byte* payload, unsigned int length) {
  // Convert the received payload to a string
  payload[length] = '\0';
  String message = String((char*)payload);

  // Check if the received topic matches the set topic
  if (String(topic) == mqttSetTopic) {
    // Update the mqttValueTopic with the new topic
    mqttValueTopic = message.c_str();
    isTopicSet = true;
    client.unsubscribe(mqttSetTopic);
    client.subscribe(mqttValueTopic);
    Serial.print("New MQTT topic set: ");
    Serial.println(mqttValueTopic);
  }
  // Check if the received topic matches the subscribed value topic
  else if (isTopicSet && String(topic) == mqttValueTopic) {
    // Update the display with the received value
    int value = message.toInt();
    Serial.println(message);
    sevseg.setNumber(value);
    sevseg.refreshDisplay();
  }
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect("ESP32Client")) {
      Serial.println("connected");
      if (!isTopicSet) {
        client.subscribe(mqttSetTopic);
      } else {
        client.subscribe(mqttValueTopic);
      }
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" retrying in 5 seconds");
      delay(5000);
    }
  }
}