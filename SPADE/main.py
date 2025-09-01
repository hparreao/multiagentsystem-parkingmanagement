from pydantic import BaseModel
from fastapi import FastAPI
import asyncio
import time
import sys
import os

# Add the parking_system package to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from parking_system.agents.Driver import Driver
from parking_system.agents.ParkingManager import ParkingManager
from parking_system.agents.ParkingSpotModule import ParkingSpotModule
from parking_system.agents.ParkingZoneManager import ParkingZoneManager

app = FastAPI()

agents = {}  # to keep track of created agents

AVAILABLE_ENVIRONMENTS = ["Outdoor", "Indoor", "Both", "Indoor-Preferred", "Outdoor-Preferred"]
AVAILABLE_PRICING_OPTIONS = ["Low", "Medium", "High"]


@app.get("/parking_preferences")
async def get_available_parking_preferences():
    return {"Environments": AVAILABLE_ENVIRONMENTS, "Pricing": AVAILABLE_PRICING_OPTIONS}


class SpotData(BaseModel):
    lat: float
    lon: float


@app.post("/parking_module/{pmodule_id}/{zone_id}")
async def create_spot(pmodule_id: str, zone_id: str, spot_data: SpotData):
    lat = spot_data.lat
    lon = spot_data.lon

    spot = ParkingSpotModule(f"{pmodule_id}@isep.lan", "agent_password", f"{zone_id}@isep.lan", lat, lon)
    await spot.start()
    agents[pmodule_id] = spot
    return {"Agent": pmodule_id, "Status": "Created"}


class ExecuteBehaviourRequest(BaseModel):
    sonar_value: int


@app.post("/parking_module/{pmodule_id}")
async def send_sonar(pmodule_id: str, request: ExecuteBehaviourRequest):
    sonar_value = request.sonar_value
    if pmodule_id in agents:
        asyncio.create_task(agents[pmodule_id].execute_behaviour(sonar_value))
        return {"Agent": pmodule_id, "Behaviour": "OneShotBehaviour Executed"}
    else:
        return {"Error": "No such agent exists"}


@app.post("/parking_zone/{zone_id}/{manager_id}")
async def create_zone(zone_id: str, manager_id: str, lat: float, lon: float, price_hour: float, environment: str):
    zone = ParkingZoneManager(f"{zone_id}@isep.lan", "agent_password", f"{manager_id}@isep.lan", lat, lon, price_hour,
                              environment, zone_id)
    await zone.start()
    agents[zone_id] = zone
    return {"Agent": zone_id, "Status": "Created"}


@app.post("/parking_manager/{manager_id}")
async def create_manager(manager_id: str):
    manager = ParkingManager(f"{manager_id}@isep.lan", "agent_password")
    await manager.start()
    agents[manager_id] = manager
    return {"Agent": manager_id, "Status": "Created"}


@app.get("/driver/{driver_id}")
async def execute_behaviour(driver_id: str, lat: float, lon: float, environment: str, pricing: str):
    if driver_id in agents:
        asyncio.create_task(agents[driver_id].execute_behaviour2(lat, lon, environment, pricing))
        while not agents[driver_id].has_park:
            await asyncio.sleep(0.1)

        return {"zone": agents[driver_id].parking_zone_jid, "module_id": agents[driver_id].parking_spot_jid,
                "lat": float(agents[driver_id].parking_lat),
                "lon": float(agents[driver_id].parking_lon),
                "pricing": float(agents[driver_id].parking_pricing), "environment": agents[driver_id].parking_env}
    else:
        return {"Error": "No such agent exists"}


@app.post("/driver/{driver_id}")
async def create_driver(driver_id: str):
    driver = Driver(f"{driver_id}@isep.lan", "agent_password", "pm1@isep.lan")
    await driver.start()
    agents[driver_id] = driver
    return {"Agent": driver_id, "Status": "Created"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)