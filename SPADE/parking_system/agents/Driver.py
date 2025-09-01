import sys
import os

# Add the parent directory to the path to import constants
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, OneShotBehaviour
from spade.message import Message


class Driver(Agent):
    """
    Agent representing a driver looking for a parking spot
    """
    
    def __init__(self, jid: str, password: str, parking_manager_jid):
        super().__init__(jid, password)
        self.parking_manager_jid = parking_manager_jid
        self.assigned_spot_queue = None
        self.has_park = False
        self.parking_spot_jid = ""
        self.parking_env = ""
        self.parking_pricing = ""
        self.parking_zone_jid = ""
        self.parking_lat = ""
        self.parking_lon = ""

    def set_assigned_spot_queue(self, assigned_spot_queue):
        """Set the queue for assigned spots"""
        self.assigned_spot_queue = assigned_spot_queue

    class RequestParkingBehaviour(OneShotBehaviour):
        """
        Behaviour to request a parking spot from the system
        """
        
        def __init__(self, owner, lat, lon, environment, price):
            super().__init__()
            self.owner = owner
            self.lat = lat
            self.lon = lon
            self.environment = environment
            self.price = price

        async def run(self):
            """Execute the parking request process"""
            # Create a request message to the parking manager
            # Example: "Request Outdoor-Preferred Low 40.7128 -74.0060"
            msg = Message(to=self.owner.parking_manager_jid)
            msg.body = f"Request {self.environment} {self.price} {self.lat} {self.lon}"
            
            # Send the request message
            await self.send(msg)
            
            # Wait for the response from the parking manager
            response_msg = await self.receive(timeout=15)
            if response_msg:
                # Check if a spot was found
                if response_msg.body != "NoSpotAvailable":
                    # Process the response - get the parking zone manager ID
                    parking_zone_manager_id = response_msg.body
                    print(f"Received parking zone manager ID: {parking_zone_manager_id}")
                    
                    # Request a spot from the specific parking zone
                    msg = Message(to=parking_zone_manager_id)
                    msg.body = "Request"
                    await self.send(msg)
                    
                    # Wait for the response with the assigned spot
                    response_msg = await self.receive(timeout=15)
                    if response_msg:
                        # Process the response with the assigned spot details
                        try:
                            parts = response_msg.body.split()
                            if len(parts) >= 5:
                                parking_spot_id = parts[0]
                                self.owner.parking_pricing = parts[1]
                                self.owner.parking_env = parts[2]
                                self.owner.parking_lat = parts[3]
                                self.owner.parking_lon = parts[4]
                                self.owner.parking_zone_jid = str(response_msg.sender)
                                self.owner.parking_spot_jid = parking_spot_id
                                self.owner.has_park = True
                                
                                # Put the assigned spot in the queue if it exists
                                if self.owner.assigned_spot_queue is not None:
                                    self.owner.assigned_spot_queue.put(parking_spot_id)
                        except (ValueError, IndexError) as e:
                            print(f"Error processing parking spot assignment: {e}")
                else:
                    print("No parking spots available matching the criteria")

    async def execute_behaviour2(self, lat: float, lon: float, environment: str, price: str):
        """Execute the parking request behaviour"""
        request_behaviour = self.RequestParkingBehaviour(self, lat, lon, environment, price)
        self.add_behaviour(request_behaviour)