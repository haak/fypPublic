# flake8: noqa
from flask import Blueprint

app = Blueprint('recommender', __name__)

from app.recommender import routes
