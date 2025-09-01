import random
import time
from datetime import datetime
import sys
import os

# Add the parent directory to the path to import constants
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, OneShotBehaviour
from spade.message import Message
from parking_system.constants import PARKING_OCCUPIED_THRESHOLD


class ParkingSpotModule(Agent):
    """
    Agent representing a physical parking spot with ultrasonic sensor
    """

    def __init__(self, agent_jid, agent_password, manager_jid, lat, lon):
        super().__init__(jid=agent_jid, password=agent_password)
        self.manager_jid = manager_jid
        self.cash = random.randrange(100, 200)
        self.private_value = None
        self.time_arrived = None
        self.is_vacant = True
        self.lat = lat
        self.lon = lon

    class InformBehaviour(OneShotBehaviour):
        """
        Behaviour to inform the parking zone manager about vacancy status
        """

        def __init__(self, owner, sonar_value):
            super().__init__()
            self.owner = owner
            self.sonar_value = sonar_value

        async def run(self):
            # Determine if the parking spot is vacant based on the sonar value
            is_vacant = self.sonar_value > PARKING_OCCUPIED_THRESHOLD
            
            msg = Message(to=self.owner.manager_jid)
            
            # Create a message to inform the parking spot manager about the vacancy status
            if is_vacant:
                if self.owner.is_vacant != is_vacant:
                    if self.owner.time_arrived:
                        duration = datetime.now() - self.owner.time_arrived
                        duration_minutes = duration.total_seconds() / 60
                        self.owner.time_arrived = None
                        msg.body = f"Vacant {duration_minutes}"
                    else:
                        msg.body = "Vacant"
                else:
                    msg.body = "Vacant"
            else:
                if self.owner.is_vacant != is_vacant:
                    self.owner.time_arrived = datetime.now()

                msg.body = "Occupied"

            self.owner.is_vacant = is_vacant
            # Send the message
            await self.send(msg)

    class BidBehaviour(CyclicBehaviour):
        """
        Behaviour to participate in parking spot auctions
        """

        def __init__(self, owner):
            super().__init__()
            self.owner = owner

        async def run(self):
            msg = await self.receive(timeout=5)
            if msg:
                if "AuctionStart" in msg.body:
                    self.owner.private_value = random.randrange(30, 45)
                    if self.owner.private_value > self.owner.cash:
                        self.owner.private_value = self.owner.cash

                    initial_bid = int(msg.body.split()[-1])

                    if self.owner.private_value > initial_bid:
                        # Send initial bid
                        bid_msg = Message(to=self.owner.manager_jid)
                        bid_msg.body = f"Bid {initial_bid} {self.owner.lat} {self.owner.lon}"
                        await self.send(bid_msg)
                elif "BidRequest" in msg.body:
                    # Increase bid
                    random_step = random.randrange(1, 5)
                    current_bid = int(msg.body.split()[-1])
                    new_bid = current_bid + random_step
                    # Fixed the logical operator from & to and
                    if self.owner.cash >= new_bid and new_bid <= self.owner.private_value:
                        time.sleep(0.5)
                        bid_msg = Message(to=self.owner.manager_jid)
                        bid_msg.body = f"Bid {new_bid} {self.owner.lat} {self.owner.lon}"
                        await self.send(bid_msg)
                    else:
                        bid_msg = Message(to=self.owner.manager_jid)
                        bid_msg.body = "Poor"
                        await self.send(bid_msg)

                elif "AuctionEnd" in msg.body:
                    # Auction end logic here
                    winner_bid, winner_jid = msg.body.split()[1:]
                    if f"{self.owner.jid.localpart}@{self.owner.jid.domain}" == winner_jid:
                        self.owner.cash -= int(winner_bid)
                        print(f"Updated cash ({winner_jid}: {self.owner.cash})")

    async def setup(self):
        bid_behaviour = self.BidBehaviour(self)
        self.add_behaviour(bid_behaviour)

    async def execute_behaviour(self, sonar_value: int):
        inform_behaviour = self.InformBehaviour(self, sonar_value)
        self.add_behaviour(inform_behaviour)