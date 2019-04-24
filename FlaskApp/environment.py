"""
File Name: Environment.py
Version: 1.0
Author: Kevin Gleeson
Date: 09/04/2019
"""
# Import deep copy library
from copy import deepcopy
# import the numpy package
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
    If its grid_cliff set the grid to grid_cliff.
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
        # Initialise the class variables of grid and agent position
        def __init__(self, grid, agent_pos):
            self.grid = grid
            self.agent_pos = agent_pos

        def __eq__(self, other):
            return isinstance(other, State) and self.grid == other.grid \
                   and self.agent_pos == other.agent_pos

        # Getting the agent and grid as strings
        def __hash__(self):
            return hash(str(self.grid) + str(self.agent_pos))

        # used for console display and debugging
        def __str__(self):
            return 'State(grid={self.grid}, agent_pos={self.agent_pos})'

    # used for writing out the agent position to a text file.
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
                # Move up and Limit the movememt to the top of the grid
                p[0] = max(0, p[0] - 1)
            elif action == DOWN:
                # Move down and limit the movement to the bottom of the grid
                p[0] = min(len(state.grid) - 1, p[0] + 1)
            elif action == LEFT:
                # Move left and limit the movement to the far left of the grid
                p[1] = max(0, p[1] - 1)
            elif action == RIGHT:
                # Move right and limit the movement to the far right of the grid
                p[1] = min(len(state.grid[0]) - 1, p[1] + 1)
            else:
                # Exception handler for unknown action
                raise ValueError('Unknown action {action}')
            # Return the copy of the class
            return p

        # Get the returned values from new_agent_pos function
        p = new_agent_pos(state, action)
        # Write out the new agent position to agentPos.txt
        # This is used for animating the agent on the front end canvas
        f.write('%d,' % p[0])
        f.write('%d,' % p[1])
        # Update the grid state
        grid_item = state.grid[p[0]][p[1]]
        # A copy of the state class grid
        new_grid = deepcopy(state.grid)
        # Condition to check if the grid item is a trap 
        if grid_item == TRAP:
            # assign the reward signal from the value set in hte form
            reward = int(trap_reward)
            # done to end the iteration
            is_done = True
            # re-write out the start postion to the agentPos text file
            f.write('%d,' % start_state.agent_pos[0])
            f.write('%d,' % start_state.agent_pos[1])
            # palce teh agent back to the start position
            new_grid[p[0]][p[1]] += AGENT
            # Check if the goal has been reached
        elif grid_item == GOAL:
            # assign the reward value set from the front end form
            reward = int(goal_reward)
            # Set the episode to done to restart another new episode
            is_done = True
            # Write the agent start postion to the agentPos text file
            f.write('%d,' % start_state.agent_pos[0])
            f.write('%d,' % start_state.agent_pos[1])
            # Reste the agent psoition to the start position in the grid
            new_grid[p[0]][p[1]] += AGENT
        # check if the gird square occupied by the agent is empty
        elif grid_item == EMPTY:
            # assign the per step cost to the reward
            # per step cost is from the front end form perameter
            reward = float(per_step_cost)
            # Set to false and keep running the current episode.
            is_done = False
            # get the last position the agent moved from
            old = state.agent_pos
            # set the last positon the agent moved from to empty
            new_grid[old[0]][old[1]] = EMPTY
            # set the new positon to the agent
            new_grid[p[0]][p[1]] = AGENT

        # check to see if the agent has returned from hitting a wall
        # back to its original position
        elif grid_item == AGENT:
            # Add the per step cost value from the front end form parameter to the reward
            reward = float(per_step_cost)
            # keep running the episode
            is_done = False

        # error exception catch
        else:
            raise ValueError('Unknown grid item {grid_item}')
            # return function parameters of the new grid state and agent position
            # return if the episode has completed or not.
        return (State(grid=new_grid, agent_pos=p), reward, is_done)
    """ 
    #########User input form parameters.############
    """
    # Selcted number of episodes
    N_EPISODES = int(episodes_form)
    # Selected maximum number of steps per episdoe
    MAX_EPISODE_STEPS = int(max_steps_form)

    # Minimum Alpha value for numpy array
    # This is the lowest possible decay value alowed
    MIN_ALPHA = 0.0001

    # Actual alpha value to be added to form on front end

    alpha = float(alpha_form)
    # selected gamma discount factor
    gamma = float(gamma_form)  # .8
    # selected epsilon vlaue
    eps = float(epsilon_form)  # .09
    # Selected aplha decay rate
    alphaDecay = float(alpha_form_decay)
    # alphas used to decay the alpha value within the nested episode loop
    # The alpha value will deacy once and episode has finshed
    alphas = np.linspace(alpha, MIN_ALPHA, N_EPISODES)

    # Epsilon deacy rate add to form on front end
    epsilon_decay = float(epsilon_form_decay)

    # print(eps)

    # Q-Table dictionary
    q_table = dict()


    # Updating the Q-Table
    # Takes the current state and action of up, down, left or right "default none"
    def q(state, action=None):
        # Add all zeros if the state is not in the dictionary
        if state not in q_table:
            # set the state to zeros within the Q-Table
            q_table[state] = np.zeros(len(ACTIONS))
        # check fro default at at start
        if action is None:
            # retrun the state
            return q_table[state]
        # return the state and action taken
        return q_table[state][action]


    # For controlling the random value.
    # Time.now can be used here
    # random.seed(145)
    # Choosing an action based on the epsilon value

    def choose_action(state):

        """
        Check if the epsilon value is greater than a randomly generated
        floating point number between 0 and 1.
        with the epsilon  value at .8  there is an 80% chance of the agent choosing a random action.
        This will force the agent to explore the environment and seek out all possible paths to teh goal.
        This values decays after each episode gradually minimising the chance of the agent choosing a random choice.
        """

        if random.uniform(0, 1) < eps:
            # choose a random action of up, down , left or right.
            return random.choice(ACTIONS)
            # If epsilon is less than the random number choosed the maximun value for the next state.
        else:
            return np.argmax(q(state))

    # Check if the Dataframe csv file exists and remove if it does.
    if os.path.exists('static/Data/Q_Table.csv'):
        os.remove('static/Data/Q_Table.csv')


    # A function to check if the goal has been reached
    # This can be used to set the decay rate for alpha and epsilon once an episode has completed
    def check_terminal_state(dn, alpha, eps):
        # check if the episode has reached a terminal state
        if dn:
            # eps = epsis[e]
            # deacy epsilon by the decay rate
            eps *= epsilon_decay
            # decay the alpha value by the decay rate
            alpha = alphas[e]
            alpha *= alphaDecay
        # return the newly decayed alpha and epsilon value
        return alpha, eps


    # Two lists for sarsa and q-learning algorithms rewards after each episode.
    # These lists will bre written out to json files for graphing on the result page.
    q_learning_list = []
    sarsa_list = []
    """
    Condition to check what algorithm has been selected from the from by the user.
    """
    if algorithm_form == "q-learning":
        # Outer loop to tru the amount of episodes chosen by the user
        # from the front end form.
        for e in range(N_EPISODES):
            # variable to hold the total reward collected after each episode has completed.
            total_reward = 0

            # the starting position when first iteration is run.
            state = start_state
            # Variable to hold the total number of steps taken by the agent for each episode
            number_of_steps = 0
            # Inner loop for executing every step of the agent within each episode.
            for _ in range(MAX_EPISODE_STEPS):
                # choose an action for each step taken
                action = choose_action(state)
                # assign the returned parameters from the act function
                (next_state, reward, done) = act(state, action)
                # assign the returned decay rate to alpha and epsilon from
                # the check_terminal_state faunction
                alpha, eps = check_terminal_state(done, alpha, eps)
                # for testing
                #print(alpha)
                """
                Q-Learning Algorithm
                
                """
                # Get the max value from the next action used for updating the
                # current states q value.
                max_next_action = np.max(q(next_state))
                # Formula fro Q Learning
                # Q(s, a) = Q(s, a) + alpha[r+ y * max_next_action - Q(s, a)]
                # The above formula has been broken into three statements
                target = reward + gamma * max_next_action
                end_eq = target - q(state)[action]
                q(state)[action] += alpha * end_eq
                # add to total reward
                total_reward += reward
                # The next new stae assigned to the current state.
                state = next_state
                # Increment the number of steps
                number_of_steps += 1
                # Check if the maximum number of steps has been exceeded
                if number_of_steps + 1 == MAX_EPISODE_STEPS:
                    # Wirte out the agent start position to agentPos.txt
                    f.write('%d,' % state.agent_pos[0])
                    f.write('%d,' % state.agent_pos[1])

                # To remove a row with all zero values in a dataframe
                # Every terminal state was adding a new row with all zero values to the Q-TAble
                # We only need to view the last actions value before the agent reaches the terminal state
                # Adapted from https://stackoverflow.com/questions/20490274/how-to-reset-index-in-a-pandas-data-frame
                # Adapted from https://stackoverflow.com/questions/22649693/drop-rows-with-all-zeros-in-pandas-data-frame

                # check for a row in the dictionary that sums to zero
                # If it does sum to zero store in empty keys
                empty_keys = {k: v for k, v in q_table.items() if sum(v) == 0}
                # iterate through empty_keys
                for k in empty_keys:
                    # delete all rows with zeros
                    del q_table[k]
                # open the Q-TAble csv file is it exits. If it doesn't exist create one.
                with open('static/Data/Q_Table.csv', 'a', newline='') as f1:
                    #Write out and append to a dataframe the q table values
                    f1.write(pd.DataFrame(list(q_table.values())).to_csv(header=None))
                    f1.flush()
                if done:
                    break
            # write the reward for each episode fdataframe out to a json file
            with open('static/Data/q_learning.json', 'w') as al:
                # add each reward to the q_learning list
                q_learning_list.append(total_reward)
                # Create a datframe from the list
                df = pd.DataFrame(q_learning_list)
                # write the dataframe out to a json file
                al.write(df.to_json())
            # Debug the episode numer to the console
            print(e)
    """
    Check for the dropdown form for the SARSA algorithm.
    """
    if algorithm_form == "sarsa":
        # Start the outer episode loop
        for e in range(N_EPISODES):
            # Get the initial start state of the agent
            state = start_state
            # Choose an action
            # This differs from the q learning algorithm
            # An action is chosen at the start of every episode
            action = choose_action(state)
            #Debug the alpha decay
            #print(alpha)
            total_reward = 0
            number_of_steps = 0
            # eps = epsis[e]
            # Inner loop for every agent time step
            for _ in range(MAX_EPISODE_STEPS):
                # assign the returned parameters from the act function
                (next_state, reward, done) = act(state, action)
                """
                The sarsa algorithm.
                """
                # the next action based on the next random or max state
                # This differs from q learning as the q table is update jus by this action
                # not the max value of all possible next actions
                next_action = choose_action(next_state)
                # For decaying alpha and epsilon
                alpha, eps = check_terminal_state(done, alpha, eps)
                # Formula for SARSA
                # Q(s,a) = Q(s,a) + alpha[r + yQ(s',a') - Q(s,a)]
                # Broken down into three statements
                target = reward + gamma * q(next_state)[next_action]
                eq_end = target - q(state)[action]
                q(state)[action] += alpha * eq_end
                # Set the current action to the next action
                action = next_action
                # set the current state to the next state
                state = next_state
                # add the current reward to the total reward
                total_reward += reward
                # increment the number of steps
                number_of_steps += 1
                # Check if the max steps has been met
                if number_of_steps + 1 == MAX_EPISODE_STEPS:
                    # Wrtie out the agent start position to the agentPos.txt file
                    f.write('%d,' % state.agent_pos[0])
                    f.write('%d,' % state.agent_pos[1])

                # To remove a row with all zero values in a dataframe
                # Every terminal state was adding a new row with all zero  values
                # Adapted from https://stackoverflow.com/questions/20490274/how-to-reset-index-in-a-pandas-data-frame
                # Adapted from https://stackoverflow.com/questions/22649693/drop-rows-with-all-zeros-in-pandas-data-frame

                # check for a row in the dictionary that sums to zero
                # If it does sum to zero store in empty keys
                empty_keys = {k: v for k, v in q_table.items() if sum(v) == 0}
                # iterate through empty_keys
                for k in empty_keys:
                    # delete all rows with zeros
                    del q_table[k]
                # open a new file of Q_Table, create one if it does not exist
                #  Keep appending to the file whilt the inner loop is alive
                with open('static/Data/Q_Table.csv', 'a', newline='') as f1:
                    # write the q table value from the q dict and convert to dataframe
                    f1.write(pd.DataFrame(list(q_table.values())).to_csv(header=None))
                    f1.flush()
                if done:
                    break
            # Open the sarsa.json file for writing the reward data
            with open('static/Data/sarsa.json', 'w') as al:
                # Append the total reward to to the sarsa array
                sarsa_list.append(total_reward)
                # Convert the array to a dataframe
                df = pd.DataFrame(sarsa_list)
                # convert the dataframe to json
                al.write(df.to_json())
            #print the episode for debugging
            print(e)
    # Close the agentPos.txt file writer
    f.close()
