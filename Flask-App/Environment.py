from copy import deepcopy
from time import sleep
import numpy as np
import np.random as random
# Adapted from Source
#  https://medium.com/@curiousily/solving-an-mdp-with-q-learning-from-scratch-deep-reinforcement-learning-for-hackers-part-1-45d1d360c120

AGENT = "A"
GOAL = "G"
EMPTY = "*"

grid = [AGENT , EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, GOAL]

for row in grid:
    print(' '.join(row))


class State:

    def __init__(self, grid, agent_pos):
        self.grid = grid
        self.agent_pos = agent_pos

    def __eq__(self, other):
        return isinstance(other, State) and self.grid == other.grid and self.agent_pos == other.agent_pos

    def __hash__(self):
        return hash(str(self.grid) + str(self.agent_pos))

    def __str__(self):
        return f"State(grid={self.grid}, agent_pos={self.agent_pos})"


LEFT = 0
RIGHT = 1

ACTIONS = [LEFT, RIGHT]

start_state = State(grid=grid, agent_pos=[0])


def act(state, action):

    def new_agent_pos(state, action):
        p = deepcopy(state.agent_pos)
       # print(len(p))
        if action == RIGHT:
            p[0] = max(len(state.grid[0]) - 1, p[0] + 1)
        elif action == LEFT:
            p[0] =  max(0,p[0]-1)
        else:
            raise ValueError(f"Unknown action {action}")
        return p

    p = new_agent_pos(state, action)
   ## print(p)
    grid_item = state.grid[p[0]]

    new_grid = deepcopy(state.grid)


    if grid_item == GOAL:
        reward = 1000
        is_done = True
        new_grid[p[0]] += AGENT
    elif grid_item == EMPTY:
        reward = -1
        is_done = False
        old = state.agent_pos
        new_grid[old[0]] = EMPTY
        new_grid[p[0]] = AGENT
    elif grid_item == AGENT:
        reward = -1
        is_done = False
    else:
        raise ValueError(f"Unknown grid item {grid_item}")

    return State(grid=new_grid, agent_pos=p), reward, is_done



random.seed(42) # for reproducibility

N_STATES = 10
N_EPISODES = 2000

MAX_EPISODE_STEPS = 1000

MIN_ALPHA = 0.02

alphas = np.linspace(1.0, MIN_ALPHA, N_EPISODES)
gamma = .2
eps = 0.3

q_table = dict()


def q(state, action=None):

    if state not in q_table:
        q_table[state] = np.zeros(len(ACTIONS))

    if action is None:
        return q_table[state]

    return q_table[state][action]


def choose_action(state):
    if random.uniform(0, 1) < eps:
        return random.choice(ACTIONS)
    else:
        return np.argmax(q(state))


for e in range(N_EPISODES):

    state = start_state
    total_reward = 0
    alpha = alphas[e]

    for _ in range(MAX_EPISODE_STEPS):
        number_of_steps = 0
        action = choose_action(state)
        next_state, reward, done = act(state, action)
        total_reward += reward

        q(state)[action] = q(state, action) + \
                           alpha * (reward + gamma *  np.max(q(next_state)) - q(state, action))
        state = next_state
        number_of_steps +=_
        print(action, state, "step number->", number_of_steps)
        sleep(.05)

        if done:
            break
    print(f"Episode {e + 1}: total reward -> {total_reward}")
    print("Total_steps ->", number_of_steps)