from flask import Flask, request,render_template
import environment
app = Flask(__name__)


@app.route('/')
def index():
    # Return the main home page when the route resource is requested
    return render_template('index.html')

# The first request made once teh form has been submitted
@app.route('/run', methods=['GET', 'POST'])
def test():

    if request.method == 'GET':
        # Call the init function from the environment.py script
        environment.init()
        # Return done as the response text for the ajax request
        # Originally for a work around of the Heroku time request limit
        # Leaving in place as a loading page
        return 'done'

    if request.method == 'POST':
        # Assign all form parameters to the environment variables from the form data
        # Adapted from : https://stackoverflow.com/questions/42154602/how-to-get-form-data-in-flask
        environment.environment_form = request.form.get('grid_type')
        environment.algorithm_form = request.form.get('algorithm')
        environment.episodes_form = request.form.get('episode')
        environment.max_steps_form = request.form.get('max_steps')
        environment.per_step_cost = request.form.get('per_step_cost')
        environment.goal_reward = request.form.get('goal_reward')
        environment.gamma_form = request.form.get('gamma')
        environment.epsilon_form = request.form.get('epsilon')
        environment.epsilon_form_decay = request.form.get('epsilon_decay')
        environment.alpha_form = request.form.get('alpha')
        environment.alpha_form_decay = request.form.get('alpha_decay')
        environment.trap_reward = request.form.get('trap_reward')
        # Show the waiting "loading page"
        return render_template('waiting.html')
        # The loading page will make a post request to the success resource once it has received the done message

@app.route('/success', methods=['GET', 'POST'])
def dealy():
    # Theese variables are used as templates within the result page for keeping the chosen parameters the user has
    # chosen from the previous form submit.
    # Adapted from : https://stackoverflow.com/questions/42154602/how-to-get-form-data-in-flask
    var0 = environment.environment_form
    var1 = environment.algorithm_form
    var2 = environment.epsilon_form
    var3 = environment.epsilon_form_decay
    var4 = environment.gamma_form
    var5 = environment.alpha_form
    var6 = environment.alpha_form_decay
    var7 = environment.episodes_form
    var8 = environment.max_steps_form
    var9 = environment.per_step_cost
    var10 = environment.goal_reward
    var11 = environment.trap_reward
    # Databinding the varables to be on the result.html page
    return render_template("result.html",var0=var0,var1=var1,var2=var2,var3=var3,var4=var4,var5=var5,var6=var6,var7=var7,var8=var8,var9=var9,var10=var10,var11=var11)


if __name__ == "__main__":

    app.run()
# Adapted from https://stackoverflow.com/questions/31948285/display-data-streamed-from-a-flask-view-as-it-updates

"""
from time import sleep

from flask import Flask, render_template


app = Flask(__name__)


@app.route('/')
def index():
    # render the template (below) that will use JavaScript to read the stream
    return render_template('index.html')


@app.route('/stream_sqrt')
def stream():
    def generate():
        for i in range(5000):
            yield '{}n'.format(i)
            sleep(.01)

    return app.response_class(generate(), mimetype='text/plain')

app.run()
"""