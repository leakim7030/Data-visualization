import dash
from dash import html
from flask import Flask
from sunshine_asia import init_dashboard as init_sunshine_dashboard
from healthy_lifestyle import init_dashboard as init_healthy_dashboard

server = Flask(__name__)

# Assume the init_dashboard functions in sunshine_asia.py and healthy_lifestyle.py
# return a Dash 'app' object after setting up layout and callbacks.
sunshine_app = init_sunshine_dashboard(server, route='/sunshine/')
healthy_app = init_healthy_dashboard(server, route='/healthy/')

@server.route('/')
def index():
    return 'Welcome to the Dash Multi-App!'

@server.route('/sunshine')
def render_sunshine():
    return sunshine_app.index()

@server.route('/healthy')
def render_healthy():
    return healthy_app.index()

if __name__ == '__main__':
    server.run(debug=True)