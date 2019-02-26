from flask import Flask, request,render_template
import loopTest
app = Flask(__name__)

@app.route('/')
def index():

    return render_template('index.html')


@app.route('/run', methods=['GET', 'POST'])

def test():




    if request.method == 'GET':

        loopTest.init()
        return 'done'
    if request.method == 'POST':
        loopTest.algorithm_form = request.form.get('algorithm')
        loopTest.episodes_form = request.form.get('episode')
        loopTest.max_steps_form = request.form.get('max_steps')
        loopTest.per_step_cost = request.form.get('per_step_cost')
        loopTest.goal_reward = request.form.get('goal_reward')
        loopTest.gamma_form = request.form.get('gamma')
        loopTest.epsilon_form = request.form.get('epsilon')
        loopTest.epsilon_form_decay = request.form.get('epsilon_decay')
        loopTest.alpha_form = request.form.get('alpha')
        loopTest.alpha_form_decay = request.form.get('alpha_decay')
        return render_template('waiting.html')




@app.route('/success', methods=['GET', 'POST'])
def dealy():
    var1 = loopTest.algorithm_form
    var2 = loopTest.epsilon_form
    var3 = loopTest.epsilon_form_decay
    var4 = loopTest.gamma_form
    var5 = loopTest.alpha_form

    var6 = loopTest.alpha_form_decay
    var7 = loopTest.episodes_form
    var8 = loopTest.max_steps_form
    var9 = loopTest.per_step_cost
    var10 = loopTest.goal_reward



    return render_template("result.html",var1=var1,var2=var2,var3=var3,var4=var4,var5=var5,var6=var6,var7=var7,var8=var8,var9=var9,var10=var10)


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