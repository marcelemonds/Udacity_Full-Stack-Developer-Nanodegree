from flask import Blueprint

bp = Blueprint('casting', __name__)

from casting import routes
