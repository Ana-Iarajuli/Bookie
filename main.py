import requests
from bs4 import BeautifulSoup
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
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


#წიგნები user.html-ზე გამოსატანად
page = 1
bookPhoto = {}
bookAuthor = {}
bookRating = {}
while page < 15:
    url1 = 'https://www.goodreads.com/review/list/57424153-ana?ref=nav_mybooks&shelf=read&page=' + str(page)
    r1 = requests.get(url1)
    soup1 = BeautifulSoup(r1.text, 'html.parser')
    sub_soup1 = soup1.find('tbody', id='booksBody')
    all_books1 = sub_soup1.find_all('tr', class_='bookalike review')

    for each in all_books1:
        photo = each.img.attrs.get('src')
        book_title = each.find('td', class_='field title').a.text.strip()
        book_title1 = book_title.replace
        book_author = each.find('td', class_='field author').a.text
        rating = each.find('td', class_='field avg_rating').div.text.strip()
        bookPhoto[book_title] = photo
        bookAuthor[book_title] = book_author
        bookRating[book_title] = rating

    page += 1

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    review = db.Column(db.String(30), nullable=False)


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
            flash('This username already exists. Please choose a different one.')



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

    return render_template('user.html', bookPhoto=bookPhoto,bookRating=bookRating,
                           bookAuthor=bookAuthor)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('register'))

# @app.route('/fantasy')
# def fantasy():
#     return render_template('index.html')

@app.route('/books', methods=['GET', 'POST'])
@login_required
def books():
    return render_template('books.html')


@app.route('/review', methods=['POST', 'GET'])
@login_required
def review():
    if request.method == "POST":
        title = request.form['title']
        review = request.form['review']
        if title == '' or review == '':
            flash('Fill every field')
        #შეყვანილი შეფასებების ბაზაში დამატება
        else:
            r1 = Review(title=title, review=review)
            db.session.add(r1)
            db.session.commit()
            # return 'Your review was added successfully!'
            flash('Your review was added successfully!')

    return render_template('review.html')


if __name__ == "__main__":
    app.run(debug=True)