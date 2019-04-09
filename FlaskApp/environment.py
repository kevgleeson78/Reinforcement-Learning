"""
File Name: Environment.py
Version: 1.0
Author: Kevin Gleeson
Date: 09/04/2019
"""
# Import deep copy library
from copy import deepcopy
#import the numpy package
import numpy as np
# import the random package
import random
# path used for file creation
import os.path
# import the pandas package
import pandas as pd

"""
Declare Agent, Goal, Empty and trap chars.
To be used for the environment space
"""
AGENT = 'A'
GOAL = 'G'
EMPTY = '*'
TRAP = '#'

"""
Variables initialised for binding from the form on the html template.
"""
environment_form = ""
algorithm_form = ""
episodes_form = 0
max_steps_form = 0
per_step_cost = 0
goal_reward = 0
trap_reward = 0
gamma_form = 0
epsilon_form = 0
epsilon_form_decay = 0
alpha_form = 0
alpha_form_decay = 0

"""
Init function needed to run the script from the form submit event on the front end.
"""
def init():
    """
    Initialise the initial grid with all empty variables.
    """
    grid = [
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
    ]
    """
    The Cliff environment.
    """
    grid_cliff = [
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [AGENT, TRAP, TRAP, TRAP, TRAP, GOAL],
    ]
    """
    The standard environment.
    """
    grid_standard = [
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, GOAL],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, TRAP],
        [EMPTY, EMPTY, TRAP, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, TRAP, EMPTY, TRAP, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, TRAP, EMPTY],
        [AGENT, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
    ]
    """
    Condition to check the user input from the form drop down.
    If its grid_cliff set the gris to grid_cliff.
    """
    if environment_form == "grid_cliff":
        grid = grid_cliff
    """
    If the drop down is grid_standard set the grid to grid_standard.
    """
    if environment_form == "grid_standard":
        grid = grid_standard
    # Print out the environment to the console for testing.
    for row in grid:
        print(' '.join(row))
    """
    A class to hold the current state of the environment and agent position.
    """
    class State:
        #Initialise the class variables of grid and agent position
        def __init__(self, grid, agent_pos):
            self.grid = grid
            self.agent_pos = agent_pos

        def __eq__(self, other):
            return isinstance(other, State) and self.grid == other.grid \
                   and self.agent_pos == other.agent_pos
        # used for console display and debugging
        def __hash__(self):
            return hash(str(self.grid) + str(self.agent_pos))
        # used for console display and debugging
        def __str__(self):
            return 'State(grid={self.grid}, agent_pos={self.agent_pos})'

    #used for writing out the agent position to a text file.
    # The file gets overwritten when the init() function gets called from the html form.
    # Adapted from : https://stackoverflow.com/questions/1945920/why-doesnt-os-path-join-work-in-this-case
    completeName = os.path.join('static/Data', 'agentPos.txt')
    # Open the file or create one if it doesn't exist
    f = open(completeName, 'w+')

    # Set numeric values to the four actions of up, down, left and right
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
    # Store the four actions in an arrray
    ACTIONS = [UP, DOWN, LEFT, RIGHT]

    # The start position of the agent in the grid
    start_state = State(grid=grid, agent_pos=[5, 0])
    # Write out the start position to hte text file
    f.write('%d,' % start_state.agent_pos[0])
    f.write('%d,' % start_state.agent_pos[1])

    """
    The act function controlls the agent transition from one state to another.
    Along with assigning rewards for a particuler action based on the curretn state the agent is in.
    Returns the:
    Reward for the action taken.
    The new state.
    Boolean if the episode is over (done). 
    """
    def act(state, action):
        # The updated new agent position once transitioned
        def new_agent_pos(state, action):
            # A deep copy of teh state classs agent position to prevent a unwanted change in data
            p = deepcopy(state.agent_pos)
            # Checking the actions taken
            if action == UP:
                #Move up and Limit the movememt to the top of the grid
                p[0] = max(0, p[0] - 1)
            elif action == DOWN:
                #Move down and limit the movement to the bottom of the grid
                p[0] = min(len(state.grid) - 1, p[0] + 1)
            elif action == LEFT:
                # Move left and limit the movement to the far left of the grid
                p[1] = max(0, p[1] - 1)
            elif action == RIGHT:
                #Move right and limit the movement to the far right of the grid
                p[1] = min(len(state.grid[0]) - 1, p[1] + 1)
            else:
                #Exception handler for unknown action
                raise ValueError('Unknown action {action}')
            #Return the copy of the class
            return p
        # Get teh returned values from new_agent_pos function
        p = new_agent_pos(state, action)
        # Write out the new agent position to the text file
        f.write('%d,' % p[0])
        f.write('%d,' % p[1])
        #Update the gris state
        grid_item = state.grid[p[0]][p[1]]
        # A copy of the state class grid
        new_grid = deepcopy(state.grid)
    
        if grid_item == TRAP:
            reward = int(trap_reward)
            is_done = True
            f.write('%d,' % start_state.agent_pos[0])
            f.write('%d,' % start_state.agent_pos[1])
            new_grid[p[0]][p[1]] += AGENT

        elif grid_item == GOAL:
            reward = int(goal_reward)
            is_done = True
            f.write('%d,' % start_state.agent_pos[0])
            f.write('%d,' % start_state.agent_pos[1])
            new_grid[p[0]][p[1]] += AGENT

        elif grid_item == EMPTY:
            reward = float(per_step_cost)
            is_done = False
            old = state.agent_pos
            new_grid[old[0]][old[1]] = EMPTY
            new_grid[p[0]][p[1]] = AGENT

        elif grid_item == AGENT:
            reward = float(per_step_cost)
            is_done = False

        else:
            raise ValueError('Unknown grid item {grid_item}')

        return (State(grid=new_grid, agent_pos=p), reward, is_done)

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

    # Epsilon deacy rate add to form on front end

    epsilon_decay = float(epsilon_form_decay)

    # print(eps)

    # Q-Table dictionary
    q_table = dict()

    # Updating the Q-Table
    def q(state, action=None):

        if state not in q_table:
            q_table[state] = np.zeros(len(ACTIONS))

        if action is None:
            return q_table[state]

        return q_table[state][action]

    # For controlling the random value.
    # Time.now can be used here
    # random.seed(145)
    # Choosing an action based on the epsilon value
    def choose_action(state):
        if random.uniform(0, 1) < eps:
            return random.choice(ACTIONS)
        else:
            return np.argmax(q(state))

    # Check if the Dataframe csv file exists and remove if it does.
    if os.path.exists('static/Data/Q_Table.csv'):
        os.remove('static/Data/Q_Table.csv')

    # A function to check if the goal has been reached
    # This can be used to set the decay rate for alpha and epsilon
    def check_terminal_state(dn, alpha, eps):
        if dn:
            # eps = epsis[e]

            eps *= epsilon_decay
            alpha = alphas[e]
            alpha *= alphaDecay
        return alpha, eps

    # Two lists for sarsa and q-learning algorithms rewards after each episode.
    # These lists will bre written out to json files for graphing on the result page.
    q_learning_list = []
    sarsa_list = []

    if algorithm_form == "q-learning":
        for e in range(N_EPISODES):

            total_reward = 0
            # eps = epsis[e]

            state = start_state
            number_of_steps = 0
            for _ in range(MAX_EPISODE_STEPS):

                # print(eps)
                action = choose_action(state)
                (next_state, reward, done) = act(state, action)

                alpha, eps = check_terminal_state(done, alpha, eps)
                print(alpha)
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

                with open('static/Data/Q_Table.csv', 'a', newline='') as f1:
                    f1.write(pd.DataFrame(list(q_table.values())).to_csv(header=None))
                    f1.flush()

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

            print(alpha)
            total_reward = 0
            number_of_steps = 0
            # eps = epsis[e]

            for _ in range(MAX_EPISODE_STEPS):

                (next_state, reward, done) = act(state, action)
                next_action = choose_action(next_state)
                alpha, eps = check_terminal_state(done, alpha, eps)
                #  print(eps)
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

                with open('static/Data/Q_Table.csv', 'a', newline='') as f1:

                    f1.write(pd.DataFrame(list(q_table.values())).to_csv(header=None))
                    f1.flush()
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