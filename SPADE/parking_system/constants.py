"""
Constants used across the parking management system
"""

# Available parking environments
AVAILABLE_ENVIRONMENTS = [
    "Outdoor", 
    "Indoor", 
    "Both", 
    "Indoor-Preferred", 
    "Outdoor-Preferred"
]

# Available pricing options
AVAILABLE_PRICING_OPTIONS = [
    "Low", 
    "Medium", 
    "High"
]

# MQTT Topics
MQTT_PARKED_TOPIC = "parked"
MQTT_DISPLAY_VALUE_TOPIC = "{}_display_value"

# Default credentials
DEFAULT_AGENT_PASSWORD = "agent_password"
DEFAULT_DOMAIN = "isep.lan"

# Distance thresholds (in cm)
PARKING_OCCUPIED_THRESHOLD = 30