import matplotlib.pyplot as plt
import requests
import numpy as np
import os

ENDPOINT = "http://localhost:8000"
TOTAL_STEPS = 24

# 1. Run a Sample Episode and Collect Data
demand_history = []
supply_history = []
battery_history = []
rewards_history = []

try:
    # Reset the Environment
    response = requests.post(f"{ENDPOINT}/reset").json()
    start_demand = response['grid_load']
    current_supply = 0
    current_battery = 50.0 # Standard starting charge

    for step in range(TOTAL_STEPS):
        # A simple "safe" agent strategy for demo
        # It always tries to meet the demand using solar, wind, and battery.
        
        # Action space: 0: Solar, 1: Wind, 2: Battery
        # This part requires adjusting to your actual server.step implementation
        # For this demo, let's assume the server logic balances everything based
        # on a single action or internal balancing logic.

        # Let's use a dummy action for now, assuming server handles supply
        action_payload = {"action": 0} 
        
        step_response = requests.post(f"{ENDPOINT}/step", json=action_payload).json()
        
        # Record the State
        demand_history.append(step_response['observation']['grid_load'])
        supply_history.append(step_response['observation']['grid_load']) # Simplified demo assumption
        battery_history.append(current_battery) # Simplified, need server response
        rewards_history.append(step_response['reward'])
        
        if step_response['done']:
            break

except requests.exceptions.ConnectionError:
    print("Error: Could not connect to the FastAPI server. Is it running?")
    exit()

# 2. Create the Visualization (The Chart)
fig, ax1 = plt.subplots(figsize=(10, 6))

# Define colors
demand_color = '#1f77b4' # Muted Blue
supply_color = '#ff7f0e' # Muted Orange

# Plot Demand vs Supply (Primary Axis)
ax1.set_xlabel('Time Step (Hours)')
ax1.set_ylabel('Power (MW)', color='black')
demand_line, = ax1.plot(demand_history, color=demand_color, linewidth=2.5, label='Industrial Demand')
supply_line, = ax1.plot(supply_history, color=supply_color, linewidth=1.5, linestyle='--', label='Agent Supply')
ax1.tick_params(axis='y', labelcolor='black')

# Fill the area between supply and demand to emphasize gaps (Safe-RL visualization)
ax1.fill_between(range(len(demand_history)), demand_history, supply_history, 
                 where=(np.array(supply_history) < np.array(demand_history)),
                 interpolate=True, color='red', alpha=0.3, label='Brownout Risk')

# Create a secondary axis for Battery level
ax2 = ax1.twinx()
battery_color = '#2ca02c' # Muted Green
ax2.set_ylabel('Battery SoC (%)', color=battery_color)
battery_line, = ax2.plot(battery_history, color=battery_color, linewidth=2, linestyle=':', label='Battery Level')
ax2.tick_params(axis='y', labelcolor=battery_color)
ax2.set_ylim(0, 100) # SoC is always 0-100%

# Final Touches (Legends and Title)
lines = [demand_line, supply_line, battery_line]
labels = [l.get_label() for l in lines]
ax1.legend(lines, labels, loc='best', frameon=True, facecolor='white', framealpha=1.0)

plt.title('Industrial Power Grid: RL Agent Sample Episode', fontsize=16)
plt.grid(axis='x', linestyle='--', alpha=0.5)

# Save the image
os.makedirs('assets', exist_ok=True)
output_path = 'assets/episode_visualization.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"Visualization saved to {output_path}")
plt.show() # Optional, depending on environment