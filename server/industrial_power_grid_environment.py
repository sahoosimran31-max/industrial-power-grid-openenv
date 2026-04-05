import random
from openenv_core import Environment

class IndustrialPowerGridEnvironment(Environment):
    def __init__(self):
        # The 'Game' state
        self.solar = False
        self.wind = False
        self.battery = False
        self.current_demand = 1 # Start with a basic demand
    
    def reset(self):
        # Task 1: Easy (Demand=1), Task 2: Med (Demand=2), Task 3: Hard (Demand=3)
        self.solar = False
        self.wind = False
        self.battery = False
        self.current_demand = random.randint(1, 3) 
        return self.get_observation()

    def step(self, action_data):
        action = action_data.action
        # Logic for toggling
        if action == 0: self.solar = not self.solar
        elif action == 1: self.wind = not self.wind
        elif action == 2: self.battery = not self.battery

        total_supply = sum([self.solar, self.wind, self.battery])
        
        # MEANINGFUL REWARD LOGIC
        if total_supply == self.current_demand:
            reward = 1.0  # Perfect Score!
            done = True
        elif total_supply > self.current_demand:
            reward = 0.5  # Partial Reward (Wasteful but demand met)
            done = False
        else:
            reward = -0.1 # Penalty (Blackout)
            done = False
            
        return self.get_observation(), reward, done

    def get_observation(self):
        total_supply = sum([self.solar, self.wind, self.battery])
        return {
            "is_demand_met": total_supply >= self.current_demand,
            "carbon_footprint": 0.2 if self.solar and self.wind else 0.8,
            "grid_stability": "STABLE" if total_supply == self.current_demand else "WARNING"
        }
