from flask import Blueprint
from flask import render_template
from flask import request
from flask import url_for,session
from src.models.reminder.notification import Notification
from werkzeug.utils import redirect
import src.models.users.decorators as user_decorators
from src.models.users.users import User


user_blueprint = Blueprint('users', __name__)

@user_blueprint.context_processor
def user():
    return dict(user=User.get_by_email(session['email']))

@user_blueprint.context_processor
def notifications():
    return dict(notifications=Notification.get_by_email(session['email']))

@user_blueprint.route('/<string:user_id>')
def view(user_id):
    return render_template('users/profile.html', user=User.get_by_id(user_id))



@user_blueprint.route('/')
@user_decorators.requires_login
def home():
    #user = User.get_by_email(session['email'])
    return render_template('') # front end template for the dashboard


@user_blueprint.route('/profile')
@user_decorators.requires_login
def view_profile():
    return render_template('', user=User.get_by_email(session['email'])) #front end code for the profile page


@user_blueprint.route('/profile/edit',methods=['GET','POST'])
@user_decorators.requires_login
def edit_profile():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        user_name = request.form['user_name']

        try:
            if User.register_user(email, password, title, first_name, last_name, department):
                session['email'] = email
                return redirect(url_for("users.home"))
        except UserErrors.UserError as e:
            return e.message

    return render_template("register.html")  # Send the user an error if their login was invalid





@user_blueprint.route('/logout')
def logout():
    session['email'] = None
    return redirect(url_for('login'))
