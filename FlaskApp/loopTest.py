from datetime import datetime
from copy import deepcopy


import numpy as np
import random
import os.path
import pandas as pd


AGENT = 'A'
GOAL = 'G'
EMPTY = '*'
TRAP = '#'
algorithm_form = ""
episodes_form = 0
max_steps_form = 0
per_step_cost = 0
goal_reward = 0
gamma_form = 0
epsilon_form = 0
epsilon_form_decay = 0
alpha_form = 0
alpha_form_decay = 0

grid = [
    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
    [AGENT, TRAP, TRAP, TRAP, TRAP, GOAL],
]

for row in grid:
    print(' '.join(row))


class State:

    def __init__(self, grid, agent_pos):
        self.grid = grid
        self.agent_pos = agent_pos

    def __eq__(self, other):
        return isinstance(other, State) and self.grid == other.grid \
               and self.agent_pos == other.agent_pos

    def __hash__(self):
        return hash(str(self.grid) + str(self.agent_pos))

    def __str__(self):
        return 'State(grid={self.grid}, agent_pos={self.agent_pos})'


def init():



    completeName = os.path.join('static/Data', 'test.txt')

    f = open(completeName, 'w+')

    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

    ACTIONS = [UP, DOWN, LEFT, RIGHT]

    start_state = State(grid=grid, agent_pos=[5, 0])
    f.write('%d,' % start_state.agent_pos[0])
    f.write('%d,' % start_state.agent_pos[1])

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
                raise ValueError('Unknown action {action}')
            return p

        p = new_agent_pos(state, action)

        f.write('%d,' % p[0])
        f.write('%d,' % p[1])
        grid_item = state.grid[p[0]][p[1]]

        new_grid = deepcopy(state.grid)

        if grid_item == TRAP:
            reward = -100
            is_done = True
            goal_reached = False
            f.write('%d,' % start_state.agent_pos[0])
            f.write('%d,' % start_state.agent_pos[1])
            new_grid[p[0]][p[1]] += AGENT
        elif grid_item == GOAL:
            reward = int(goal_reward)
            is_done = True
            goal_reached = True
            f.write('%d,' % start_state.agent_pos[0])
            f.write('%d,' % start_state.agent_pos[1])
            new_grid[p[0]][p[1]] += AGENT
        elif grid_item == EMPTY:
            reward = float(per_step_cost)
            is_done = False
            goal_reached = False
            old = state.agent_pos
            new_grid[old[0]][old[1]] = EMPTY
            new_grid[p[0]][p[1]] = AGENT
        elif grid_item == AGENT:
            reward = float(per_step_cost)
            is_done = False
            goal_reached = False
        else:
            raise ValueError('Unknown grid item {grid_item}')

        return (State(grid=new_grid, agent_pos=p), reward, is_done, goal_reached)



    N_EPISODES = int(episodes_form)

    MAX_EPISODE_STEPS = int(max_steps_form)

    # Minimum Alpha value for numpy array

    MIN_ALPHA = 0.0001

    # Actual alpha value to be added to form on front end

    alpha = float(alpha_form)
    gamma = float(gamma_form)  # .8
    eps = float(epsilon_form)  # .09
    # The decay rate add to form on front end

    alphaDecay = float(alpha_form_decay)
    alphas = np.linspace(alpha, MIN_ALPHA, N_EPISODES)
    epsis = np.linspace(eps, MIN_ALPHA, N_EPISODES)



    # Epsilon deacy rate add to form on front end

    epsilon_decay = float(epsilon_form_decay)

    q_table = dict()
    print(eps)
    def q(state, action=None):

        if state not in q_table:
            q_table[state] = np.zeros(len(ACTIONS))

        if action is None:
            return q_table[state]

        return q_table[state][action]
    random.seed(145)
    def choose_action(state):


        if random.uniform(0, 1) < eps:
            return random.choice(ACTIONS)
        else:
            return np.argmax(q(state))

    if os.path.exists('static/Data/Dataframe.csv'):
        os.remove('static/Data/Dataframe.csv')

    def check(gr,alpha,eps):
        if gr:


            #eps = epsis[e]
            eps *= epsilon_decay
            alpha = alphas[e]
            alpha *= alphaDecay

        return alpha,eps
    q_learning_list = []
    sarsa_list = []
    if algorithm_form == "q-learning":
        for e in range(N_EPISODES):

            total_reward = 0
            #eps = epsis[e]

            state = start_state
            number_of_steps = 0
            for _ in range(MAX_EPISODE_STEPS):

                print(eps)
                action = choose_action(state)
                (next_state, reward, done, goal_reached) = act(state, action)

                alpha , eps = check(done,alpha,eps)
                #print(alpha)
                max_next_action = np.max(q(next_state))
                target = reward + gamma * max_next_action
                end_eq = target - q(state)[action]
                q(state)[action] += alpha * end_eq
                total_reward += reward
                state = next_state



                number_of_steps += 1


                if number_of_steps + 1 == MAX_EPISODE_STEPS:
                    f.write('%d,' % state.agent_pos[0])
                    f.write('%d,' % state.agent_pos[1])

                # To remove a row with all zero values in a dataframe
                # Every terminal state was adding a new row with all zero  values
                # Adapted from https://stackoverflow.com/questions/20490274/how-to-reset-index-in-a-pandas-data-frame
                # Adapted from https://stackoverflow.com/questions/22649693/drop-rows-with-all-zeros-in-pandas-data-frame

                empty_keys = {k: v for k, v in q_table.items() if sum(v) == 0}
                for k in empty_keys:
                    del q_table[k]

                with open('static/Data/Dataframe.csv', 'a',newline='') as f1:
                    f1.write(pd.DataFrame(list(q_table.values())).to_csv(header=None))


                if done:
                    break

            with open('static/Data/q_learning.json', 'w') as al:

                q_learning_list.append(total_reward)
                df = pd.DataFrame(q_learning_list)
                al.write(df.to_json())

            print(e)





    if algorithm_form == "sarsa":


        for e in range(N_EPISODES):
            state = start_state
            action = choose_action(state)

            # print(alpha)
            total_reward = 0
            number_of_steps = 0
          # eps = epsis[e]


            for _ in range(MAX_EPISODE_STEPS):

                (next_state, reward, done,goal_reached) = act(state, action)
                next_action = choose_action(next_state)
                alpha, eps = check(done,alpha,eps)
               # print(eps)
                target = reward + gamma * q(next_state)[next_action]
                eq_end = target - q(state)[action]
                q(state)[action] += alpha * eq_end

                number_of_steps += 1
                if number_of_steps + 1 == MAX_EPISODE_STEPS:
                    f.write('%d,' % state.agent_pos[0])
                    f.write('%d,' % state.agent_pos[1])

                # To remove a row with all zero values in a dataframe
                # Every terminal state was adding a new row with all zero  values
                # Adapted from https://stackoverflow.com/questions/20490274/how-to-reset-index-in-a-pandas-data-frame
                # Adapted from https://stackoverflow.com/questions/22649693/drop-rows-with-all-zeros-in-pandas-data-frame

                empty_keys = {k: v for k, v in q_table.items() if sum(v) == 0}
                for k in empty_keys:
                    del q_table[k]

                with open('static/Data/Dataframe.csv', 'a',newline='') as f1:
                    f1.write(pd.DataFrame(list(q_table.values())).to_csv(header=None))

                total_reward += reward
                action = next_action

                state = next_state
                if done:
                    break


            with open('static/Data/sarsa.json', 'w') as al:
                sarsa_list.append(total_reward)
                df = pd.DataFrame(sarsa_list)
                al.write(df.to_json())

            print(e)

    f.close()