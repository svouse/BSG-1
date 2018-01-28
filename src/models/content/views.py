from flask import Blueprint
from flask import render_template
from flask import request
from flask import url_for,session

from werkzeug.utils import redirect
import src.models.users.decorators as user_decorators
from src.models.users.users import User


content_blueprint = Blueprint('content', __name__)

@content_blueprint.route("/new",methods=['POST'])
def new_content():
    if request.method == 'POST': # actually not sure what to do here until we talk
