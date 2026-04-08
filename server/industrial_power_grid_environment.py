import random
from openenv_core import Environment

from server.models import IndustrialPowerGridObservation

class IndustrialPowerGridEnvironment(Environment):
    def __init__(self):
        # The 'Game' state
        self.solar = False
        self.wind = False
        self.battery = False
        self.current_demand = 1 # Start with a basic demand
        self._reward = 0.0
        self._done = False
    
    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        
        # INITIALIZE YOUR VARIABLES HERE
        self.solar = False
        self.wind = False
        self.current_demand = 50.0 
        self.is_demand_met = False
        self.carbon_footprint = 0.8
        self.grid_stability = "STABLE"

        return self.state

    def step(self, action_data):
        # Debug: Log what we receive
        print(f"DEBUG: action_data type = {type(action_data)}")
        print(f"DEBUG: action_data = {action_data}")
        
        action = action_data.action
        print(f"DEBUG: extracted action = {action}")
        
        # Logic for toggling
        if action == 0: 
            self.solar = not self.solar
        elif action == 1: 
            self.wind = not self.wind
        elif action == 2: 
            self.battery = not self.battery

        total_supply = sum([self.solar, self.wind, self.battery])
        
        # MEANINGFUL REWARD LOGIC
        if total_supply == self.current_demand:
            self._reward = 1.0  # Perfect Score!
            self._done = True
        elif total_supply > self.current_demand:
            self._reward = 0.5  # Partial Reward (Wasteful but demand met)
            self._done = False
        else:
            self._reward = -0.1 # Penalty (Blackout)
            self._done = False
        
        return self.state

    def get_observation(self):
        total_supply = sum([self.solar, self.wind, self.battery])
        return {
            "is_demand_met": total_supply >= self.current_demand,
            "carbon_footprint": 0.2 if self.solar and self.wind else 0.8,
            "grid_stability": "STABLE" if total_supply == self.current_demand else "WARNING"
        }

    @property
    def state(self) -> IndustrialPowerGridObservation:
        return IndustrialPowerGridObservation(
            is_demand_met=getattr(self, "is_demand_met", False),
            carbon_footprint=getattr(self, "carbon_footprint", 0.0),
            grid_stability=getattr(self, "grid_stability", "STABLE"),
            reward=self._reward,
            done=self._done
        )
    
    @property
    def reward(self) -> float:
        """Return the current reward."""
        return self._reward
    
    @property
    def done(self) -> bool:
        """Check if episode is done."""
        return self._done