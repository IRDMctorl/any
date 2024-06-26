from flask import Flask

app = Flask(__name__)

# Define a route for the subdomain
@app.route('/', subdomain='sub')
def subdomain_home():
    return 'Hello from the subdomain!'

# Define a route for the main domain
@app.route('/')
def main_home():
    return 'Hello from the main domain!'
