import re

from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt

app = Flask(__name__)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

app.config['SECRET_KEY'] = 'brutuseti'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.sqlite'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    author = db.Column(db.String(30), nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __str__(self):
        return f'Book title: {self.title}; Author: {self.author}; Price: {self.price}'


# წამოვიღოთ პირველი სტრიქონი

# b1 = Books.query.first()
# print(b1)


# all_books = Books.query.all()
# # print(all_books)
# for each in all_books:
#     print(each)

# რომ გავფილტროთ ავტორით
#
# all_books = Books.query.filter_by(author='William Shakespeare')
# for each in all_books:
#     print(each)

# b1 = Books(title='უცხო', author='ალბერ კამიუ', price=10)
# db.session.add(b1)
# db.session.commit()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

# db.create_all()


class RegisterForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Register')

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                'This username already exists. Please choose a different one.')



class LoginForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Log in')




@app.route('/')
def home():
    return render_template('index.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    # if request.method == 'POST':
    #     email = request.form['email']
    #     password = request.form['password']
    #     username = request.form['username']
    #     session['username'] = username
    #     regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    #     if email == '' or password == '' or username == '':
    #         flash('Please fill in all the required fields', 'error')
    #     elif (re.fullmatch(regex, email)) == False:
    #         flash('Enter valid email', 'error')
    #     elif len(password) < 8:
    #         flash('Password must be 8 or more characters long', 'error')
    #     else:
    #         return redirect(url_for('home'))

    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html', form=form)

@app.route('/login', methods=['POST', 'GET'])
def login():
    # if request.method == 'POST':
    #     username = request.form['username']
    #     password = request.form['username']
    #     if username == register(username) and password == register(password):
    #         return render_template('login.html')
    #     else:
    #         flash('Username or password mismatch', 'error')

    form = LoginForm()

    if form.validate_on_submit():
        #ამოწმებს db-ში არის თუ არა მომხმარებელი და თუ არის შემდეგ ამოწმებს
        #შეყვანილ პაროლს. თუ დაემთხვევა პაროლიც მაშინ შეუშვებს მომხმარებელს თავის პროფილზე
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('user'))

    return render_template('login.html', form=form)



@app.route('/user')
@login_required
def user():
    subjects = ['Python', 'Calculus', 'DB']
    return render_template('user.html',  subjects=subjects)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('register'))


@app.route('/books', methods=['GET', 'POST'])
@login_required
def books():
    if request.method == 'POST':

        t = request.form['title']
        a = request.form['author']
        p = request.form['price']

        if t == '' or a == '' or p == '':
             flash("შეიტანეთ ყველა ველი", 'error')
        elif not p.isdecimal():
            flash("შეიტანეთ რიცხვი ფასის ველში", 'error')
        else:
            b1 = Books(title=t, author=a, price=float(p))
            db.session.add(b1)
            db.session.commit()
            flash('მონაცემები დამატებულია', 'info')

    return render_template('books.html')


if __name__ == "__main__":
    app.run(debug=True)