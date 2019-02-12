
from flask import Flask, request,render_template

app = Flask(__name__)

@app.route('/')
def index():

    return render_template('index.html')


@app.route('/test', methods=['GET', 'POST'])

def test():
    from FlaskApp import loopTest
    loopTest.episodes_form = request.form.get("episode")
    loopTest.max_steps_form = request.form.get("max_steps")
    loopTest.per_step_cost = request.form.get("per_step_cost")
    loopTest.goal_reward = request.form.get("goal_reward")
    loopTest.gamma_form = request.form.get("gamma")
    loopTest.epsilon_form = request.form.get("epsilon")
    loopTest.init()

    return render_template('index.html')



if __name__ == "__main__":

    app.run(host='localhost', port=23423)
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