import sys
import os
from math import radians, sin, cos, sqrt, atan2

# Add the parent directory to the path to import constants
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from parking_system.constants import AVAILABLE_ENVIRONMENTS, AVAILABLE_PRICING_OPTIONS


class ParkingManager(Agent):
    """
    Agent that manages the entire parking system and coordinates between parking zones
    """
    
    class ListenBehaviour(CyclicBehaviour):
        """
        Behaviour to listen for messages from parking zone managers and drivers
        """
        
        def __init__(self, owner):
            super().__init__()
            self.owner = owner

        async def run(self):
            """Main behaviour loop"""
            # Wait for incoming messages from ParkingZoneManager agents
            msg = await self.receive(timeout=5)

            if msg:
                sender_jid = str(msg.sender)

                if msg.body.startswith("Request"):
                    environment, pricing, lat, lon = self.extract_request_params(msg.body)
                    response = self.find_vacant_parking_spot(environment, pricing, lat, lon)
                    if response:
                        response_msg = Message(to=sender_jid)
                        response_msg.body = response
                        await self.send(response_msg)
                    else:
                        # Send error response if no spot found
                        response_msg = Message(to=sender_jid)
                        response_msg.body = "NoSpotAvailable"
                        await self.send(response_msg)
                else:
                    # Process the message and extract the number of vacant spaces and additional information
                    try:
                        parts = msg.body.split()
                        if len(parts) >= 5:
                            vacant_spaces, lat, lon, price_hour, environment = parts[:5]
                            # Convert the necessary values to the desired types
                            vacant_spaces = int(vacant_spaces)
                            lat = float(lat)
                            lon = float(lon)
                            price_hour = float(price_hour)
                            self.update_vacant_spaces(sender_jid, vacant_spaces, environment, lat, lon, price_hour)
                    except (ValueError, IndexError) as e:
                        print(f"Error processing message: {e}")

        def extract_request_params(self, request_msg):
            """Extract parameters from a driver's request message"""
            # Example: "Request Outdoor-Preferred Low 40.7128 -74.0060"
            params = request_msg.split()[1:]  # Remove the "Request" part
            environment = params[0] if params and params[0] in AVAILABLE_ENVIRONMENTS else None
            pricing = params[1] if len(params) > 1 and params[1] in AVAILABLE_PRICING_OPTIONS else None
            lat = float(params[2]) if len(params) > 2 else None
            lon = float(params[3]) if len(params) > 3 else None
            return environment, pricing, lat, lon

        def update_vacant_spaces(self, parking_zone_manager_jid, vacant_spaces, environment, lat, lon, price_hour):
            """Update the number of vacant spaces for a parking zone manager"""
            # Update the internal data structure with the number of vacant spaces
            parking_zone_manager = (parking_zone_manager_jid, environment, lat, lon, price_hour)
            self.owner.vacant_spaces[parking_zone_manager] = vacant_spaces

            # Print the updated vacant space count for the parking zone manager
            print(f"Parking zone manager {parking_zone_manager_jid} has {vacant_spaces} vacant spaces")

        def find_vacant_parking_spot(self, environment=None, pricing=None, lat=None, lon=None):
            """Find the best vacant parking spot based on criteria"""
            matched_spots = []

            # Evaluate all parking zones with vacant spaces
            for parking_zone_manager, vacant_spots in self.owner.vacant_spaces.items():
                if vacant_spots > 0:
                    parking_zone_manager_jid, parking_zone_environment, parking_zone_pricing, parking_zone_lat, parking_zone_lon = parking_zone_manager
                    score = self.calculate_score(
                        parking_zone_environment, 
                        parking_zone_pricing, 
                        parking_zone_lat,
                        parking_zone_lon, 
                        environment,
                        pricing, 
                        lat, 
                        lon
                    )
                    matched_spots.append((parking_zone_manager, score))

            if matched_spots:
                # Sort the matched spots based on the score in descending order
                matched_spots.sort(key=lambda x: x[1], reverse=True)
                return matched_spots[0][0][0]  # Return the JID of the best match

            return None

        def calculate_score(self, spot_environment, spot_pricing, spot_lat, spot_lon, client_environment,
                            client_pricing, client_lat, client_lon):
            """Calculate a score for a parking spot based on environment, pricing, and proximity"""
            # Environment matching score
            environment_weight = 0
            if client_environment:
                if spot_environment == client_environment:
                    environment_weight = 3
                elif spot_environment.endswith("-Preferred") and spot_environment.startswith(client_environment.split("-")[0]):
                    environment_weight = 2
                else:
                    environment_weight = 1
            
            # Pricing matching score
            pricing_weight = 0
            if client_pricing:
                pricing_values = {"Low": 0.25, "Medium": 1.0, "High": 2.0}
                spot_pricing_value = pricing_values.get(spot_pricing, 1.0)
                client_pricing_value = pricing_values.get(client_pricing, 1.0)
                
                if spot_pricing_value <= client_pricing_value:
                    pricing_weight = 3
                elif spot_pricing_value <= client_pricing_value * 1.5:
                    pricing_weight = 2
                else:
                    pricing_weight = 1
            
            # Proximity score
            proximity_weight = self.calculate_proximity_weight(spot_lat, spot_lon, client_lat, client_lon)
            
            return environment_weight + pricing_weight + proximity_weight

        def calculate_proximity_weight(self, spot_lat, spot_lon, client_lat, client_lon):
            """Calculate a proximity weight based on the distance between spot and client"""
            if spot_lat is not None and spot_lon is not None and client_lat is not None and client_lon is not None:
                distance = self.calculate_distance(spot_lat, spot_lon, client_lat, client_lon)
                # Higher weight for closer distances
                if distance <= 0.1:  # 100 meters
                    return 6
                elif distance <= 0.25:  # 250 meters
                    return 5
                elif distance <= 0.5:  # 500 meters
                    return 4
                elif distance <= 1.0:  # 1 kilometer
                    return 3
                elif distance <= 2.0:  # 2 kilometers
                    return 2
                elif distance <= 5.0:  # 5 kilometers
                    return 1
                else:
                    return 0
            else:
                return 0

        def calculate_distance(self, lat1, lon1, lat2, lon2):
            """Calculate the distance between two locations using the Haversine formula"""
            # Convert degrees to radians
            lat1_rad = radians(lat1)
            lon1_rad = radians(lon1)
            lat2_rad = radians(lat2)
            lon2_rad = radians(lon2)

            # Earth's radius in kilometers
            earth_radius = 6371.0

            # Haversine formula
            dlon = lon2_rad - lon1_rad
            dlat = lat2_rad - lat1_rad
            a = sin(dlat / 2) ** 2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2) ** 2
            c = 2 * atan2(sqrt(a), sqrt(1 - a))
            distance = earth_radius * c

            return distance

    def __init__(self, jid: str, password: str, verify_security: bool = False):
        super().__init__(jid, password, verify_security)
        self.vacant_spaces = {}  # Dictionary to store vacant space counts for parking zone managers

    async def setup(self):
        """Agent setup - add the listening behaviour"""
        listen_behaviour = self.ListenBehaviour(self)
        self.add_behaviour(listen_behaviour)