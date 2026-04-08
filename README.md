---
title: Industrial Power Grid Environment Server
emoji: 🔋
colorFrom: gray
colorTo: indigo
sdk: docker
pinned: false
app_port: 8001
base_path: /web
tags:
  - openenv
  - reinforcement-learning
  - sustainability
---

# 🔋 Industrial Power Grid Environment

An autonomous Reinforcement Learning environment designed to simulate an industrial power grid. The goal is to balance energy supply from multiple sources (Solar, Wind, Battery) to meet factory demand while minimizing the total carbon footprint.

## 🚀 Quick Start

The simplest way to interact with the environment is using the Gymnasium wrapper provided in the repository:

```python
from gymnasium_wrapper import PowerGridGymEnv

# Initialize the environment (Ensure server is running on port 8001)
env = PowerGridGymEnv(endpoint="http://localhost:8001")

obs, info = env.reset()
print(f"Initial State: {obs}")

# Take a step with a random action (0: Solar, 1: Wind, 2: Battery)
action = env.action_space.sample()
obs, reward, terminated, truncated, info = env.step(action)

print(f"Action Taken: {action} | Reward: {reward}")

🛠️ Installation & Setup
1. Install Dependencies
Ensure you have your virtual environment active, then run:

Bash
pip install -r requirements.txt

2. Run the Environment ServerStart the FastAPI/OpenEnv server to host the simulation:Bash# Windows (PowerShell)
$env:PYTHONPATH = "."
python -m server.app --port 8001

# Linux/Mac
PYTHONPATH=. python3 -m server.app --port 8001

3. Run the AI Stability Test
In a second terminal, run the training script to verify the RL loop:

Bash

python train.py
📊 Environment Details

Action Space: Discrete(3)
Value   Action          Description
0       Toggle Solar     Activates/Deactivates Solar panel arrays
1       Toggle Wind      Activates/Deactivates Wind turbine clusters 
2       Toggle Battery   Switches between Charging/Discharging states

Observation 

Space: Box(3)

Index   Feature                   Unit  
0       Demand Met               Boolean (1.0 = Yes, 0.0 = No)
1       Carbon FootprintMetric   Tons (Lower is better)
2       Grid Stability           1.0 = Stable, 0.0 = Unstable


Reward Function

The agent is rewarded for maintaining a stable grid while reducing emissions:

Success: $+1.0$ (Demand met with 0 carbon)Sustainability Penalty: Reward is scaled by carbon footprint: $1.0 - (Carbon \times 0.5)$Failure: $-1.0$ (Grid blackout/demand not met)

🐳 Docker Support
Building the Image

Bash
docker build -t industrial_power_grid-env:latest -f server/Dockerfile .

Deploying to Hugging Face Spaces

Bash

openenv push --repo-id your-username/industrial-power-grid --private


📡 API Documentation
Once the server is running, you can explore the interactive API docs at:

http://localhost:8001/docs

## Project Structure

```
industrial_power_grid/
├── .dockerignore         # Docker build exclusions
├── __init__.py            # Module exports
├── README.md              # This file
├── openenv.yaml           # OpenEnv manifest
├── pyproject.toml         # Project metadata and dependencies
├── uv.lock                # Locked dependencies (generated)
├── client.py              # IndustrialPowerGridEnv client
├── models.py              # Action and Observation models
└── server/
    ├── __init__.py        # Server module exports
    ├── industrial_power_grid_environment.py  # Core environment logic
    ├── app.py             # FastAPI application (HTTP + WebSocket endpoints)
    └── Dockerfile         # Container image definition
```
