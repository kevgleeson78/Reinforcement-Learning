## Reinforcement Learning - A Browser Based Visualisation Tool
### 4th Year Final Project
### By Kevin Gleeson
### Student at: [GMIT](www.gmit.ie) Galway
## Project outline 
This project will help to explain the temporal difference reinforcement learning process by displaying an agent's behaviour, performance and Q-Table (memory) as it interacts within its environment. The application is a browser based visual tool where a user can tweak parameters within a form before running the application. Once the form is submitted, it will then make a request to run the application held on a server. Once the script has completed, the user will be presented with and animation of the agent moving through its environment. In addition, a graph of the agent performance and the q-table will presented to the user for examination. There are two different temporal difference algorithms for the user to choose being Q learning, an off policy strategy and SARSA (State Action Reward Action), an on policy strategy. The performance of these two algorithms will be presented to the user for examination within a linear chart.
This will aid the user in better understanding the concept of reinforcement learning.
## The Main objectives of this project are:
* Implement two different temporal difference algorithms SARSA and Q-learning written in python.
* Allow for user interaction via a web page form
* Using Flask server to handle request from the user
* Present the user with data generated by the main python script on the server 
* Parsing Json, text and csv files generated via Ajax
* Use the parsed data to animate the agent in HTML canvas
* Google chart for graphing the agent performance
* Generate a dynamic table that updates from the csv file
* Add a heat map to the values of the table as it updates
* Deploying the application to Google Cloud Platform

## Installation Instructions
You can access this application at the following URL: 
[https://reinforcementlearning.appspot.com/](https://reinforcementlearning.appspot.com/)

Alternatively you can clone the repository and run the application locally by following the below instructions:
### Local installation
#### Cloning the application
* To clone this repository ensure you have git installed on your machine. You can download and install it [here](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
* Open a command line tool of your choice and type the following command:
```bash
git clone https://github.com/kevgleeson78/Reinforcement-Learning.git
```
This will clone the entire repository with all of the files needed to run this application.
#### Running the application
*	Download and install anaconda python [Click here](https://www.anaconda.com/distribution/)
* Open a command line tool and change directory into the FlaskApp folder of the cloned repository.
* Type the command "python FlaskTest.py" and press enter. This will start the server at the local address http://127.0.0.1:5000/
* Copy the above address into a browser window of your choice and press enter. 
* This will now run the application within a local environment for you to interact with.
