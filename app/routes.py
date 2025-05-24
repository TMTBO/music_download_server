from flask import Blueprint, url_for

# Create a Blueprint for the app
main = Blueprint('main', __name__)

@main.route('/')
def home():
    return "Hello, World!"