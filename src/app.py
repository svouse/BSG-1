import jinja2
import re
from flask import Flask, session, jsonify
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.utils import redirect
import src.models.users.errors as UserErrors
from src.common.database import Database
from src.models.projects.projects import Project
from src.models.reminder.notification import Notification
from src.models.users.users import User
from src.models.meetings.meetings import Meeting


jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(
        ['templates', 'templates/users', 'templates/meetings', 'templates/projects', 'templates/tasks',
         'templates/department'])
)

app = Flask(__name__)
app.secret_key = "123"

from src.models.users.views import user_blueprint

app.register_blueprint(user_blueprint, url_prefix="/users")


@app.context_processor
def priority_list():
    return dict(priority_list=['Low', 'Normal', 'High', 'Critical'])


@app.context_processor
def notifications():
    if session.get('email'):
        return dict(notifications=Notification.get_read_by_email(session['email']))
    else:
        return dict(notifications=[])


@app.before_first_request
def init_db():
    Database.initialize()


@app.route('/')
def home():
    if session.get('email'):
        return render_template('home.html', user=User.get_by_email(session['email']))
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            if User.is_login_valid(email, password):
                session['email'] = email
                return redirect(url_for("users.home"))
        except UserErrors.UserError as e:
            return render_template("login.html", error=e.message)
    return render_template("login.html")  # Send the user an error if their login was invalid


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        print(request.form)
        email = request.form['email']
        password = request.form['password']
        title = request.form['title']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        department = request.form['department']

        try:
            if User.register_user(email, password, title, first_name, last_name, department):
                session['email'] = email
                return redirect(url_for("users.home"))
        except UserErrors.UserError as e:
            return e.message

    return render_template("register.html")  # Send the user an error if their login was invalid


@app.route("/search")
@app.route("/search/<string:search_query>")
def search(search_query='null'):
    search_query = request.args.get("search_query", search_query)
    results = Database.search('users', search_query)
    if results.count() > 0:
        results = [{"email": dict(result)["email"],
                    "name": dict(result)["title"] + '.' + dict(result)["first_name"] + " " + dict(result)["last_name"],
                    "_id": dict(result)["_id"]}
                    for result in results]
    else:
        results = Database.find('users', {"first_name": {'$regex': '^{}'.format(search_query), '$options': 'i'}})
        results = [{"email": dict(result)["email"],
                    "name": dict(result)["title"] + '.' + dict(result)["first_name"] + " " + dict(result)["last_name"],
                    "_id": dict(result)["_id"]}
                   for result in results]

    return jsonify(results)




if __name__ == "__main__":
    app.run(debug=True, port=8000)
