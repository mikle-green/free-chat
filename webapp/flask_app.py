# A Flask application to run Free Chat

from datetime import datetime
from flask import Flask, flash, g, render_template, redirect, request, url_for
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from os import urandom

from database import Message, User, db_uri, db
from forms import ChatForm, LoginForm, RegistrationForm


MAX_SHOWN_MESSAGES = 50

app = Flask(__name__)

# Application configuration
app.config["DEBUG"] = True
app.config["SECRET_KEY"] = urandom(20)
app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(name=user_id).first()


@app.before_first_request
def init_before_first_request():
    #db.drop_all()
    #db.create_all()
    pass


@app.before_request
def before_request():
    g.user = current_user


def get_chat_messages():
    max = Message.query.count()
    min = (max - MAX_SHOWN_MESSAGES) if (max - MAX_SHOWN_MESSAGES) > 0 else 0
    return Message.query.slice(min, max).all()


# Routing
@app.route("/", methods=["get", "post"])
def index():
    return render_template("index.html")


@app.route("/chat")
@login_required
def chat():
    msg_count = request.args.get("msg_count", type=int)
    messages = get_chat_messages()
    if len(messages) < 1 or messages[-1].id == msg_count:
        return "", 204

    last_msg_id = 0 if len(messages) < 1 else messages[-1].id
    return render_template("chat.html", messages=messages, count=last_msg_id)


@app.route("/login", methods=["get", "post"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("session"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password", "warning")
            return redirect(url_for("login"))

        login_user(user)
        user.last_login = datetime.utcnow()
        db.session.commit()
        return redirect(url_for("session"))

    return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/register", methods=["get", "post"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("session"))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(name=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Congratulations, you are now a registered user!", "info")
        return redirect(url_for("login"))

    return render_template("register.html", form=form)


@app.route("/session", methods=["get", "post"])
@login_required
def session():
    form = ChatForm()
    if form.validate_on_submit():
        message = Message(user=current_user)
        message.content = form.message.data.strip()
        db.session.add(message)
        db.session.commit()
        return "", 204

    messages = get_chat_messages()
    last_msg_id = 0 if len(messages) < 1 else messages[-1].id
    return render_template("session.html", form=form, messages=messages, count=last_msg_id)
