
#!/usr/bin/env python
import time
from flask import Flask, Response, request, redirect, render_template
import pandas as pd
from ipython_genutils.py3compat import execfile

app = Flask(__name__)


def stream_template(template_name, **context):
    # http://flask.pocoo.org/docs/patterns/streaming/#streaming-from-templates
    app.update_template_context(context)
    t = app.jinja_env.get_template(template_name)
    rv = t.stream(context)
    # uncomment if you don't need immediate reaction
    ##rv.enable_buffering(5)
    return rv


@app.route('/')
def index():
    f = open('static/test.txt', 'r')
    lines = f.readlines()

    def g():
        for i in lines:
                conv_int_x = int(i)
               # time.sleep(.2)  # an artificial delay
                yield conv_int_x
    f.close()
    return Response(stream_template('index.html', data=g()))


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