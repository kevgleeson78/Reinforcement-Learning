from copy import deepcopy
import numpy as np
import random
import os.path
import pandas as pd
from FlaskApp import FlaskTest

AGENT = "A"
GOAL = "G"
EMPTY = "*"
TRAP = "#"
episodes_form = 0
max_steps_form = 0
per_step_cost = 0
goal_reward = 0
gamma_form = 0
epsilon_form = 0

grid = [
    [EMPTY, EMPTY, EMPTY, GOAL],
    [EMPTY, EMPTY, EMPTY, TRAP],
    [EMPTY, EMPTY, EMPTY, EMPTY],
    [EMPTY, EMPTY, EMPTY, EMPTY],
    [AGENT, EMPTY, EMPTY, EMPTY],
]

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


def init():


    completeName = os.path.join("static/", "test.txt")

    f = open(completeName,"w+")

    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

    ACTIONS = [UP, DOWN, LEFT, RIGHT]


    start_state = State(grid=grid, agent_pos=[4, 0])
    f.write("%d," % (start_state.agent_pos[0]))
    f.write("%d," % (start_state.agent_pos[1]))

    def act(state, action):

        def new_agent_pos(state, action):
            p = deepcopy(state.agent_pos)

            if action == UP:
                p[0] = max(0, p[0] - 1)
            elif action == DOWN:
                p[0] = min(len(state.grid) - 1, p[0] + 1)
            elif action == LEFT:
                p[1] = max(0, p[1] - 1)
            elif action == RIGHT:
                p[1] = min(len(state.grid[0]) - 1, p[1] + 1)
            else:
                raise ValueError(f"Unknown action {action}")
            return p

        p = new_agent_pos(state, action)


        f.write("%d," % (p[0]))
        f.write("%d," % (p[1]))
        grid_item = state.grid[p[0]][p[1]]

        new_grid = deepcopy(state.grid)

        if grid_item == TRAP:
            reward = -100
            is_done = True
            f.write("%d," % (start_state.agent_pos[0]))
            f.write("%d," % (start_state.agent_pos[1]))
            new_grid[p[0]][p[1]] += AGENT
        elif grid_item == GOAL:
            reward = int(goal_reward)
            is_done = True
            f.write("%d," % (start_state.agent_pos[0]))
            f.write("%d," % (start_state.agent_pos[1]))
            new_grid[p[0]][p[1]] += AGENT
        elif grid_item == EMPTY:
            reward = int(per_step_cost)
            is_done = False
            old = state.agent_pos
            new_grid[old[0]][old[1]] = EMPTY
            new_grid[p[0]][p[1]] = AGENT
        elif grid_item == AGENT:
            reward = int(per_step_cost)
            is_done = False
        else:
            raise ValueError(f"Unknown grid item {grid_item}")

        return State(grid=new_grid, agent_pos=p), reward, is_done



    random.seed(42) # for reproducibility

    N_STATES = 20

    N_EPISODES = int(episodes_form)


    MAX_EPISODE_STEPS = int(max_steps_form)

    MIN_ALPHA = 0.1

    alphas = np.linspace(1.0, MIN_ALPHA, N_EPISODES)

    gamma = float(gamma_form)#.8
    eps = float(epsilon_form)#.09
    q_table1 = np.zeros((N_STATES,len(ACTIONS)))
    print (q_table1)
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

    if os.path.exists("static/Dataframe.csv"):
        os.remove('static/Dataframe.csv')

    for e in range(N_EPISODES):


        total_reward = 0
        alpha = alphas[e]
        state = start_state
        for _ in range(MAX_EPISODE_STEPS):

            test = pd.DataFrame(list(q_table.values()))

            number_of_steps = 0
            action = choose_action(state)
            next_state, reward, done = act(state, action)

            total_reward += reward
            print(state.agent_pos[0])
            q(state)[action] = q(state, action) + \
                               alpha * (reward + gamma * np.max(q(next_state, action)) - q(state, action))
            state = next_state
            number_of_steps +=_
            print(action, state, "step number->", number_of_steps +1)

            if number_of_steps +1 == MAX_EPISODE_STEPS:
                f.write("%d," % (state.agent_pos[0]))
                f.write("%d," % (state.agent_pos[1]))

            with open('static/Dataframe.csv', 'a') as f1:

                f1.write(test.to_csv(header=None))

                f1.close()
            if done:
                break

       # print(test)
       # test.to_csv("static/Dataframe.csv", sep='\t', encoding='utf-8')
        print(f"Episode {e + 1}: total reward -> {total_reward}")

    f.close()


