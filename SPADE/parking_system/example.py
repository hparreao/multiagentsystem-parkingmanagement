"""
Example script demonstrating how to use the parking management system
"""

import asyncio
import requests
import time

# Configuration
BASE_URL = "http://localhost:8000"

async def main():
    print("Parking Management System - Example Usage")
    print("=" * 40)
    
    # 1. Create a parking manager
    print("1. Creating parking manager...")
    response = requests.post(f"{BASE_URL}/parking_manager/pm1")
    print(f"Response: {response.json()}")
    time.sleep(1)
    
    # 2. Create parking zones
    print("\n2. Creating parking zones...")
    response = requests.post(f"{BASE_URL}/parking_zone/pz1/pm1?lat=41.1776&lon=-8.6077&price_hour=2.5&environment=Outdoor")
    print(f"Zone 1: {response.json()}")
    
    response = requests.post(f"{BASE_URL}/parking_zone/pz2/pm1?lat=41.1782&lon=-8.6076&price_hour=3.0&environment=Indoor")
    print(f"Zone 2: {response.json()}")
    time.sleep(1)
    
    # 3. Create parking spots
    print("\n3. Creating parking spots...")
    spot_data = {"lat": 41.1776, "lon": -8.6077}
    response = requests.post(f"{BASE_URL}/parking_module/ps1/pz1", json=spot_data)
    print(f"Spot 1: {response.json()}")
    
    spot_data = {"lat": 41.1782, "lon": -8.6076}
    response = requests.post(f"{BASE_URL}/parking_module/ps2/pz2", json=spot_data)
    print(f"Spot 2: {response.json()}")
    time.sleep(1)
    
    # 4. Create a driver
    print("\n4. Creating driver...")
    response = requests.post(f"{BASE_URL}/driver/d1")
    print(f"Driver: {response.json()}")
    time.sleep(1)
    
    # 5. Send sonar data (simulating parking spot occupancy)
    print("\n5. Sending sonar data...")
    sonar_data = {"sonar_value": 35}  # Vacant ( > 30cm)
    response = requests.post(f"{BASE_URL}/parking_module/ps1", json=sonar_data)
    print(f"Spot 1 status: {response.json()}")
    
    sonar_data = {"sonar_value": 15}  # Occupied ( < 30cm)
    response = requests.post(f"{BASE_URL}/parking_module/ps2", json=sonar_data)
    print(f"Spot 2 status: {response.json()}")
    time.sleep(1)
    
    # 6. Request a parking spot
    print("\n6. Requesting parking spot...")
    response = requests.get(f"{BASE_URL}/driver/d1?lat=41.1776&lon=-8.6077&environment=Outdoor&pricing=Low")
    if response.status_code == 200:
        result = response.json()
        if "Error" in result:
            print(f"Error: {result['Error']}")
        else:
            print(f"Assigned spot: {result}")
    else:
        print(f"Error: {response.status_code} - {response.text}")

if __name__ == "__main__":
    asyncio.run(main())