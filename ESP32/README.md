# ESP32 Parking Module Requirements

## Hardware Components
- ESP32 Development Board
- HC-SR04 Ultrasonic Sensor (1 or 2 depending on configuration)
- Jumper Wires
- Breadboard (optional)
- 7-Segment Display (for display modules)

## Required Libraries
- WiFi.h (built-in)
- HTTPClient.h (built-in)
- ArduinoJson (install via Library Manager)
- PubSubClient (for MQTT, install via Library Manager)
- SevSeg (for 7-segment displays, install via Library Manager)

## Wiring Diagram

### Parking Module (Single Sensor)
- HC-SR04 VCC -> ESP32 5V
- HC-SR04 GND -> ESP32 GND
- HC-SR04 Trig -> ESP32 GPIO 5
- HC-SR04 Echo -> ESP32 GPIO 18

### Parking Module (Double Sensor)
- HC-SR04 #1 VCC -> ESP32 5V
- HC-SR04 #1 GND -> ESP32 GND
- HC-SR04 #1 Trig -> ESP32 GPIO 5
- HC-SR04 #1 Echo -> ESP32 GPIO 18
- HC-SR04 #2 VCC -> ESP32 5V
- HC-SR04 #2 GND -> ESP32 GND
- HC-SR04 #2 Trig -> ESP32 GPIO 27
- HC-SR04 #2 Echo -> ESP32 GPIO 26

### Display Module
- 7-Segment Display pins connected to ESP32 GPIO pins as defined in the code

## Installation Instructions

1. Install Arduino IDE
2. Install ESP32 board support in Arduino IDE
3. Install required libraries via Library Manager:
   - ArduinoJson
   - PubSubClient
   - SevSeg
4. Navigate to the appropriate directory:
   - `parkingmodulescript/` for single parking sensor
   - `parkingmodulescript/double/` for double parking sensors
   - `displaymodulescript/` for single display
   - `displaymodulescript/double/` for double displays
5. Copy the `.ino.template` file to `.ino` and modify the TODO sections with your actual values:
   - WiFi credentials
   - Server IP address
   - MQTT broker IP address
   - GPS coordinates
6. Upload to ESP32

## Configuration

Before uploading the code to your ESP32, you must update the following values in the code:

1. **WiFi Credentials**:
   ```cpp
   const char* ssid = "YOUR_WIFI_SSID";
   const char* password = "YOUR_WIFI_PASSWORD";
   ```

2. **Server IP Address**:
   ```cpp
   const char* server_ip = "http://YOUR_SERVER_IP:8000/parking_module/ps1";
   ```

3. **MQTT Broker IP** (for display modules):
   ```cpp
   const char* mqttServer = "YOUR_MQTT_BROKER_IP";
   ```

4. **GPS Coordinates**:
   ```cpp
   float latitude = YOUR_LATITUDE_VALUE;
   float longitude = YOUR_LONGITUDE_VALUE;
   ```

Replace all placeholder values with your actual configuration details.