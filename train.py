import gymnasium as gym
from gymnasium_wrapper import PowerGridGymEnv # Ensure this matches your filename

# 1. Initialize the environment
# Make sure your FastAPI server is running on port 8001!
env = PowerGridGymEnv(endpoint="http://localhost:8001")

print("Starting AI Stability Test...")

for episode in range(1, 6):
    obs, _ = env.reset()
    done = False
    score = 0
    step_count = 0

    while not done and step_count < 20:
        # 2. Pick a random action (0, 1, or 2)
        action = env.action_space.sample()
        
        # 3. Apply the action
        obs, reward, done, truncated, info = env.step(action)
        
        score += reward
        step_count += 1
        
        print(f"Episode: {episode} | Step: {step_count} | Action: {action} | Reward: {reward}")

    print(f"✅ Episode {episode} Finished. Total Score: {score}")

print("\n🔥 All systems green! Your environment is ready for training.")