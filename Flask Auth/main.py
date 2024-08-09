from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a random string'
#Flask Key
WTF_CSRF_SECRET_KEY = 'a random string'

# CREATE DATABASE
class Base(DeclarativeBase):
    pass

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# Configure Flask-Login's Login Manager
login_manager = LoginManager()
login_manager.init_app(app)

# Create a user_loader callback
@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(UserDB, user_id)

# CREATE TABLE IN DB
class UserDB(UserMixin, db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(1000))


# CREATE Form
class UserForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()], render_kw={"placeholder": "Name"})
    email = EmailField('Email', validators=[DataRequired()], render_kw={"placeholder": "Email"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Password"})


with app.app_context():
    db.create_all()


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/register', methods = ["POST", "GET"])
def register():
    form = UserForm()
    if form.validate_on_submit():
        result = db.session.execute(db.select(UserDB).where(UserDB.email == email))
        # Note, email in db is unique so will only have one result.
        user = result.scalar()
        if user:
            # User already exists
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('login'))

        hash_and_salted_password = generate_password_hash(password=form.password.data, method="pbkdf2:sha256", salt_length=8)

        user = UserDB(
            name=form.name.data,
            email=form.email.data,
            password=hash_and_salted_password
        )
        db.session.add(user)
        db.session.commit()

        # Log in and authenticate user after adding details to database.
        login_user(user)

        return redirect(url_for('secrets', name=user.name))
    return render_template("register.html", form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        # Find user by email entered.
        result = db.session.execute(db.select(UserDB).where(UserDB.email == email))
        user = result.scalar()

        # Email doesn't exist or password incorrect.
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('login'))
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.')
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for('secrets'))

    return render_template("login.html")


@app.route('/secrets')
@login_required
def secrets():
    print(current_user.name)
    name = request.args.get('name')
    return render_template("secrets.html", name=name, username = current_user.name)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/download')
@login_required
def download():
    return send_from_directory('static', 'files/cheat_sheet.pdf')


if __name__ == "__main__":
    app.run(debug=True)
