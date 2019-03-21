from flask import Flask, request,render_template
import environment
app = Flask(__name__)


@app.route('/')
def index():

    return render_template('index.html')


@app.route('/run', methods=['GET', 'POST'])
def test():

    if request.method == 'GET':

        environment.init()
        return 'done'
    if request.method == 'POST':
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
        return render_template('waiting.html')


@app.route('/success', methods=['GET', 'POST'])
def dealy():

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