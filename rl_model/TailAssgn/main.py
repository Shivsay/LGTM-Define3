import gym
from gym import spaces
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import torch
import torch.nn as nn
import torch.optim as optim
import random
from collections import deque

# -------------------------
# Data Loading and Helpers
# -------------------------
# For example, load flight legs from a CSV (assumed to have columns: flight_id, flight_date, aircraft_type, dep_time, dep_airport, STA, arr_airport)
# flights_df = pd.read_csv('flight_legs.csv')  
# For demonstration, here is a small dummy dataset:
# Load flight legs from CSV
flights_df = pd.read_csv('C:/Users/acer/Desktop/Hackathon/TailAssgn/Flight_legs.csv', 
                         usecols=["Flt ID", "Flt Dt (Z)", "A/C Type", "STD", "Dep Arp", "STA", "Arv Arp"])
flights_df.columns = ["flight_id", "flight_date", "aircraft_type", "dep_time", "dep_airport", "STA", "arr_airport"]
flights_df.dropna(inplace=True)

# Load available airplanes from CSV
airplanes_df = pd.read_csv('C:/Users/acer/Desktop/Hackathon/TailAssgn/aircraft.csv', 
                           usecols=["R6g", "A/C Type"])
airplanes_df.columns = ["reg_no", "aircraft_type"]
airplanes_df.dropna(inplace=True)
airplanes = airplanes_df.to_dict(orient='records')

# Helper to parse time strings (assuming format "%H:%M")
def parse_time(time_str):
    return datetime.strptime(time_str, "%H%M/%d")

# -------------------------
# Gym Environment for Tail Assignment
# -------------------------
class TailAssignmentEnv(gym.Env):
    """
    A simplified environment where the agent assigns a flight (current index) to one of the available airplanes.
    State is a dummy vector here (extend it to include flight features).
    """
    def __init__(self, flights_df, airplanes, min_turnaround=45):
        super(TailAssignmentEnv, self).__init__()
        self.flights_df = flights_df.reset_index(drop=True)
        self.airplanes = airplanes
        self.num_airplanes = len(airplanes)
        self.current_flight = 0
        self.min_turnaround = timedelta(minutes=min_turnaround)
        # For simplicity, each airplane's schedule is stored in a dict (reg_no -> last flight assigned)
        self.schedule = {plane['reg_no']: None for plane in self.airplanes}
        # Observation: For demo, a fixed-size vector (you should expand this to include relevant flight features)
        self.observation_space = spaces.Box(low=0, high=1, shape=(10,), dtype=np.float32)
        # Action: which airplane (0 to num_airplanes-1)
        self.action_space = spaces.Discrete(self.num_airplanes)

    def reset(self):
        self.current_flight = 0
        self.schedule = {plane['reg_no']: None for plane in self.airplanes}
        return self._get_obs()

    def _get_obs(self):
        # Return dummy observation for current flight (replace with meaningful features)
        return np.array([0.5]*10, dtype=np.float32)

    def step(self, action):
        flight = self.flights_df.iloc[self.current_flight]
        chosen_plane = self.airplanes[action]
        reward = 0
        
        # Check if chosen airplane type matches flight requirement
        if chosen_plane['aircraft_type'] != flight['aircraft_type']:
            reward = -10  # heavy penalty for mismatch
        else:
            last_flight = self.schedule[chosen_plane['reg_no']]
            if last_flight is None:
                reward = 1  # free assignment reward
                self.schedule[chosen_plane['reg_no']] = flight
            else:
                # Check if the previous flight's arrival airport matches the current flight's departure airport
                if last_flight['arr_airport'] != flight['dep_airport']:
                    reward = -5  # penalty for location mismatch
                else:
                    # Check turnaround time
                    last_sta = parse_time(last_flight['STA'])
                    curr_dep = parse_time(flight['dep_time'])
                    if (curr_dep - last_sta) < self.min_turnaround:
                        reward = -5  # penalty for insufficient turnaround
                    else:
                        reward = 1
                        self.schedule[chosen_plane['reg_no']] = flight
        
        self.current_flight += 1
        done = self.current_flight >= len(self.flights_df)
        obs = self._get_obs() if not done else np.zeros(10, dtype=np.float32)
        return obs, reward, done, {}

# -------------------------
# PyTorch DQN Agent
# -------------------------
class DQN(nn.Module):
    def __init__(self, obs_size, n_actions):
        super(DQN, self).__init__()
        self.net = nn.Sequential(
            nn.Linear(obs_size, 64),
            nn.ReLU(),
            nn.Linear(64, 64),
            nn.ReLU(),
            nn.Linear(64, n_actions)
        )
    def forward(self, x):
        return self.net(x)

# Hyperparameters
OBS_SIZE = 10
N_ACTIONS = len(airplanes)
BATCH_SIZE = 32
GAMMA = 0.99
EPS_START = 1.0
EPS_END = 0.02
EPS_DECAY = 1000
LEARNING_RATE = 1e-3
MEMORY_SIZE = 10000
TARGET_UPDATE = 10

# Experience Replay Memory
class ReplayMemory:
    def __init__(self, capacity):
        self.capacity = capacity
        self.memory = deque(maxlen=capacity)
    def push(self, transition):
        self.memory.append(transition)
    def sample(self, batch_size):
        return random.sample(self.memory, batch_size)
    def __len__(self):
        return len(self.memory)

# Initialize environment, networks, optimizer, memory
env = TailAssignmentEnv(flights_df, airplanes)
policy_net = DQN(OBS_SIZE, N_ACTIONS)
target_net = DQN(OBS_SIZE, N_ACTIONS)
target_net.load_state_dict(policy_net.state_dict())
target_net.eval()

optimizer = optim.Adam(policy_net.parameters(), lr=LEARNING_RATE)
memory = ReplayMemory(MEMORY_SIZE)

steps_done = 0

def select_action(state):
    global steps_done
    eps_threshold = EPS_END + (EPS_START - EPS_END) * np.exp(-steps_done / EPS_DECAY)
    steps_done += 1
    if random.random() < eps_threshold:
        return torch.tensor([[random.randrange(N_ACTIONS)]], dtype=torch.long)
    else:
        with torch.no_grad():
            state_v = torch.tensor(state, dtype=torch.float32).unsqueeze(0)
            return policy_net(state_v).max(1)[1].view(1, 1)

def optimize_model():
    if len(memory) < BATCH_SIZE:
        return
    transitions = memory.sample(BATCH_SIZE)
    batch = list(zip(*transitions))
    state_batch = torch.tensor(np.array(batch[0]), dtype=torch.float32)
    action_batch = torch.tensor(batch[1]).unsqueeze(1)  # Ensure action_batch has the correct shape
    reward_batch = torch.tensor(batch[2], dtype=torch.float32)
    non_final_mask = torch.tensor(tuple(map(lambda d: d is not None, batch[3])), dtype=torch.bool)
    non_final_next_states = torch.tensor(np.array([s for s in batch[3] if s is not None]), dtype=torch.float32)
    
    state_action_values = policy_net(state_batch).gather(1, action_batch)
    next_state_values = torch.zeros(BATCH_SIZE)
    if non_final_next_states.size(0) > 0:
        next_state_values[non_final_mask] = target_net(non_final_next_states).max(1)[0].detach()
    expected_state_action_values = (next_state_values * GAMMA) + reward_batch
    
    loss = nn.MSELoss()(state_action_values.squeeze(), expected_state_action_values)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

# -------------------------
# Training Loop
# -------------------------
num_episodes = 200

for i_episode in range(num_episodes):
    state = env.reset()
    total_reward = 0
    while True:
        action = select_action(state)
        next_state, reward, done, _ = env.step(action.item())
        total_reward += reward
        memory.push((state, action, reward, next_state if not done else None))
        state = next_state
        optimize_model()
        if done:
            break
    if i_episode % TARGET_UPDATE == 0:
        target_net.load_state_dict(policy_net.state_dict())
    print(f"Episode {i_episode} Total Reward: {total_reward}")

# -------------------------
# Testing the Trained Agent
# -------------------------
state = env.reset()
while True:
    action = select_action(state)
    state, reward, done, _ = env.step(action.item())
    if done:
        break

print("Final flight assignment schedule:")
print(env.schedule)
