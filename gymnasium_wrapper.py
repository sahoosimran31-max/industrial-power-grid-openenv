import gymnasium as gym
from gymnasium import spaces
import numpy as np
import requests

class PowerGridGymEnv(gym.Env):
    def __init__(self, endpoint="http://localhost:8000"):
        super(PowerGridGymEnv, self).__init__()
        self.endpoint = endpoint
        
        # Define Action Space: [0: Solar, 1: Wind, 2: Battery]
        self.action_space = spaces.Discrete(3)
        
        # Define Observation Space: [Demand, Supply, Battery]
        # We use a box of floats from 0 to 100 (or your max range)
        self.observation_space = spaces.Box(low=0, high=200, shape=(3,), dtype=np.float32)

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        response = requests.post(f"{self.endpoint}/reset").json()
        
        # Convert your API response to a numpy array for Gym
        obs = np.array([response['grid_load'], 0.0, 50.0], dtype=np.float32)
        return obs, {}

    def step(self, action):
        # Send action to your FastAPI server
        payload = {
            "action": {
                "action": int(action),
                "message": "step_action"  # Non-empty message for OpenEnv
            }
        }
        response = requests.post(f"{self.endpoint}/step", json=payload).json()
        
        obs = np.array([
            float(response['observation']['is_demand_met']), 
            response['observation']['carbon_footprint'], 
            1.0 if response['observation']['grid_stability'] == "STABLE" else 0.0
        ], dtype=np.float32)
        
        reward = response.get('reward', 0.0)
        done = response.get('terminated', False)  # OpenEnv uses 'terminated'
        
        return obs, reward, done, False, {}

    