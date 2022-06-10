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


# def book_genre(genre):
#     url = f'https://www.goodreads.com/shelf/show/{genre}'
#     r = requests.get(url)
#     soup = BeautifulSoup(r.text, 'html.parser')
#     sub_soup = soup.find('div', class_='leftContainer')
#     all_items = sub_soup.find_all('div', class_='elementList')
#     for each in all_items:
#         img_url = each.img.attrs['src']
#         t = each.find('div', class_='left')
#         title = t.find('a', class_='bookTitle').text
#         author = each.find('div', class_='authorName__container').span.text
#         avg = each.find('div', class_='left')
#         avgRating = avg.find('span', class_='greyText smallText').text
#
#         if genre == 'fantasy':
#             fantasy[title] = img_url
#             fant[title] = avgRating
#             fantas[title] = author
#         elif genre == 'crime':
#             crime[title] = img_url
#             cr[title] = avgRating
#             crim[title] = author
#         else:
#             scienceFiction[title] = img_url
#             sf[title] = avgRating
#             sciencef[title] = author

# fantasyBooks = book_genre('fantasy')
# crimeBooks = book_genre('crime')
# sci_fiBooks = book_genre('science-fiction')
# fantasy = {}
# fant = {}
# fantas = {}

# url = 'https://www.goodreads.com/shelf/show/fantasy'
# r = requests.get(url)
# soup = BeautifulSoup(r.text, 'html.parser')
# sub_soup = soup.find('div', class_='leftContainer')
# all_items = sub_soup.find_all('div', class_='elementList')
# for each in all_items:
#
#     img_url = each.img.attrs['src']
#     t = each.find('div', class_='left')
#     title = t.find('a', class_='bookTitle').text
#     author = each.find('div', class_='authorName__container').span.text
#     avg = each.find('div', class_='left')
#     avgRating = avg.find('span', class_='greyText smallText').text
#     fantasy[title] = img_url
#     fant[title] = avgRating
#     fantas[title] = author



# crime = {}
# cr = {}
# crim = {}

# url1 = 'https://www.goodreads.com/shelf/show/crime'
# r1 = requests.get(url1)
# soup1 = BeautifulSoup(r.text, 'html.parser')
# sub_soup1 = soup1.find('div', class_='leftContainer')
# all_items1 = sub_soup1.find_all('div', class_='elementList')
# for each in all_items1:
#
#     img_url1 = each.img.attrs['src']
#     t1 = each.find('div', class_='left')
#     title1 = t1.find('a', class_='bookTitle').text
#     author1 = each.find('div', class_='authorName__container').span.text
#     avg1 = each.find('div', class_='left')
#     avgRating1 = avg1.find('span', class_='greyText smallText').text
#     crime[title1] = img_url1
#     cr[title1] = avgRating1
#     crim[title1] = author1

# scienceFiction = {}
# sf = {}
# sciencef = {}
# url2 = 'https://www.goodreads.com/shelf/show/science-fiction'
# r2 = requests.get(url2)
# soup2 = BeautifulSoup(r.text, 'html.parser')
# sub_soup2 = soup2.find('div', class_='leftContainer')
# all_items2 = sub_soup2.find_all('div', class_='elementList')
# for each in all_items2:
#
#     img_url2 = each.img.attrs['src']
#     # s_img_url.append(img_url2)
#     t2 = each.find('div', class_='left')
#     title2 = t2.find('a', class_='bookTitle').text
#     # s_title.append(title2)
#     author2 = each.find('div', class_='authorName__container').span.text
#     # s_author.append(author2)
#     avg2 = each.find('div', class_='left')
#     avgRating2 = avg2.find('span', class_='greyText smallText').text
#     # s_avg.append(avgRating2)
#     scienceFiction[title2] = img_url2
#     sf[title2] = avgRating2
#     sciencef[title] = author2


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
    return render_template('user.html', bookPhoto=bookPhoto,bookRating=bookRating,
                           bookAuthor=bookAuthor, subjects=subjects)


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

@app.route('/fantasy')
def fantasy():
    return redirect('fantasy.html')

def recommendations():
    return render_template('fantasy.html','crime.html','science_fiction.html',
                           fantasy=fantasy, crime=crime,
                           scienceFiction=scienceFiction,
                           fant=fant, cr=cr, sf=sf, fantas=fantas,
                           crim=crim, sciencef=sciencef)

if __name__ == "__main__":
    app.run(debug=True)