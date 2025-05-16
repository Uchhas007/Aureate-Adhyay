from flask import Flask, render_template, request, session, redirect, flash
import json
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text, create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from q import run
from datetime import datetime
import math
import os
from werkzeug.utils import secure_filename
from flask_migrate import Migrate
import pymysql
import random
import bcrypt

with open("config.json", "r") as c:
    params = json.load(c)["params"]

app = Flask(__name__)

app.secret_key = "super-secret-key"
# app.config['UPLOAD_FOLDER'] = params['upload_location']

app.config.update(
    MAIL_SERVER="smtp.gmail.com",
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME=params["store_email"],
    MAIL_PASSWORD="ksoz qsde qypk doyg",
)
mail = Mail(app)


def create_database_if_not_exists():
    connection = pymysql.connect(
        host="localhost",
        user="root",
        password="",  # your root password (IF ANY)
    )
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS bookstore")
    connection.close()


create_database_if_not_exists()

app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://root@localhost/bookstore"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

migrate = Migrate(app, db)
app.jinja_env.globals.update(getattr=getattr)

location, os_info = run()


class User(db.Model):
    __tablename__ = "user"
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(500), nullable=False)
    pw = db.Column(db.String(70), nullable=False)
    date = db.Column(db.String(100), nullable=True)

    def __repr__(self) -> str:
        return f"{self.sno} {self.name}"


class Stationary(db.Model):
    __tablename__ = "stationary"
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500), nullable=False)
    price = db.Column(db.String(1000), nullable=False)
    img_file = db.Column(db.String(500), nullable=False)
    date = db.Column(db.String(100), nullable=True)


class Author(db.Model):
    __tablename__ = "author"
    sno = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(500), nullable=False)
    dob = db.Column(db.String(100), nullable=False)
    years_active = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(1000), nullable=False)
    bio = db.Column(db.String(5000), nullable=False)
    genres = db.Column(db.String(2500), nullable=False)
    awards = db.Column(db.String(5000), nullable=False)
    date = db.Column(db.Date, nullable=True)


class Publisher(db.Model):
    __tablename__ = "publisher"
    sno = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(500), nullable=False)
    logo = db.Column(db.String(1000), nullable=False)
    type = db.Column(db.String(1000), nullable=False)
    iimprints = db.Column(db.String(1500), nullable=False)
    books = db.Column(db.String(5000), nullable=False)
    authors = db.Column(db.String(2000), nullable=False)
    link = db.Column(db.String(500), nullable=False)
    loc = db.Column(db.String(500), nullable=False)
    member_since = db.Column(db.Date, nullable=False)


class Book(db.Model):
    __tablename__ = "book"
    sno = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(1000), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    price = db.Column(db.DECIMAL(10, 2), nullable=False)

    # Foreign Key to Author
    author_id = db.Column(
        db.Integer, db.ForeignKey("author.sno"), nullable=False, index=True
    )
    author_rel = db.relationship("Author", backref=db.backref("books", lazy=True))

    total_sells = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(2500), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(300), nullable=False)
    date = db.Column(db.Date, nullable=True)


class Contact(db.Model):
    __tablename__ = "contact"
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(250), nullable=False)
    msg = db.Column(db.String(2000), nullable=False)
    date = db.Column(db.String(12), nullable=True)


class Wishlist(db.Model):
    __tablename__ = "wishlist"
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(100), nullable=False)
    product_type = db.Column(db.String(50), nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)


class Cart(db.Model):
    __tablename__ = "cart"
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(100), nullable=False)
    product_type = db.Column(db.String(50), nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)


class Payment(db.Model):
    __tablename__ = "payment"
    id = db.Column(db.Integer, primary_key=True)
    payment_method = db.Column(db.String(50), nullable=False)
    transaction_id = db.Column(db.String(100), nullable=True)
    amount = db.Column(db.DECIMAL(10, 2), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    payment_date = db.Column(db.DateTime, default=datetime.utcnow)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"), nullable=False)


class Order(db.Model):
    __tablename__ = "order"
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(100), nullable=False)
    order_date = db.Column(db.DateTime, default=datetime.utcnow)
    total_amount = db.Column(db.DECIMAL(10, 2), nullable=False)
    shipping_address = db.Column(db.String(500), nullable=False)
    status = db.Column(db.String(50), nullable=False, default="Pending")
    payment = db.relationship("Payment", backref=db.backref("order"), uselist=False)


class OrderItem(db.Model):
    __tablename__ = "order_item"
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"), nullable=False)
    product_type = db.Column(db.String(50), nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.DECIMAL(10, 2), nullable=False)
    order = db.relationship("Order", backref=db.backref("items", lazy=True))


with app.app_context():
    # creating database tables
    db.create_all()

    # checking if there's any default value in the database or not
    # Check and seed default user

    if not User.query.first():
        print("Seeding Users info...")
        default_users = [
            User(
                name="Demo", email="demo@bookstore.com", pw="demo123", date="2025-05-09"
            ),
        ]
        db.session.add_all(default_users)

    # Seed authors
    if not Author.query.first():
        print("Seeding Authors info...")
        authors = [
            Author(
                name="William Shakespeare",
                dob="1564-04-23",  # Corrected from 1564-04-27
                years_active="1585–1613",
                image="images/auth_William_Shakespeare.jpg",
                bio="William Shakespeare was an English playwright, poet, and actor, widely regarded as the greatest writer in the English language and the world's pre-eminent dramatist",
                genres="Plays (Tragedy, Comedy, History), Sonnets, Narrative Poems",  # Adjusted genres
                awards="N/A",  # Set to N/A
                date=datetime.today(),
            ),
            Author(
                name="Evelyn Reed",
                dob="1905-10-31",
                years_active="1940–1979",
                image="images/evelyn_reed.jpg",
                bio="Evelyn Reed (1905–1979) was an American communist and women’s rights activist...",
                genres="Non-fiction, Feminism, Politics",
                awards="N/A",
                date=datetime.today(),
            ),
            Author(
                name="Jian Li",
                dob="2010-01-01",  # Placeholder, retained as is
                years_active="2010–present",
                image="images/jian_li.jpg",
                bio="Dr. Jian Li is a Publishing Editor of Physics & Astronomy at Springer...",
                genres="Science, Physics, Academic Publishing",
                awards="N/A",
                date=datetime.today(),
            ),
            Author(
                name="Isabelle Moreau",
                dob="2005-01-01",  # Placeholder, retained as is
                years_active="2005–present",
                image="images/isabelle_moreau.jpg",
                bio="Isabelle Moreau is a leader, coach, and former Director of Marketing at John Wiley & Sons...",
                genres="Self-help, Personal Development",
                awards="N/A",
                date=datetime.today(),
            ),
            Author(
                name="Anya Petrova",
                dob="2018-01-01",  # Placeholder, retained as is
                years_active="2018–present",
                image="images/anya_petrova.jpg",
                bio="Anya Petrova is a Russian journalist and software reviewer with a strong focus on consumer technology...",
                genres="Technology, Journalism",
                awards="",
                date=datetime.today(),
            ),
            Author(
                name="Samuel Hayes",
                dob="2010-01-01",  # Placeholder, retained as is
                years_active="2010–present",
                image="images/samuel_hayes.jpg",
                bio="Dr. Samuel Hayes, Jr. is distinguished as a strategic designer by ministry, military...",
                genres="Leadership, Strategy, Religion",
                awards="",
                date=datetime.today(),
            ),
            Author(
                name="Rachel Hartman",
                dob="1972-07-09",
                years_active="1996–present",
                image="images/rachel_hartman.jpg",
                bio="Rachel Hartman is an American writer and comic artist, known for her young adult fantasy novels...",
                genres="Young Adult, Fantasy",
                awards="2012 Cybils Award; 2013 William C. Morris Award",
                date=datetime.today(),
            ),
            Author(
                name="Alistair Blackwood",
                dob="2015-01-01",  # Placeholder, retained as is
                years_active="2015–present",
                image="images/alistair_blackwood.jpg",
                bio="Alistair Blackwood is a technology and finance enthusiast with a background in AI development...",
                genres="Technology, Finance, AI",
                awards="",
                date=datetime.today(),
            ),
            Author(
                name="Sheena Hutchinson",
                dob="2013-01-01",  # Placeholder, retained as is
                years_active="2013–present",
                image="images/sheena_hutchinson.jpg",
                bio='Sheena Hutchinson is a New York-born author known for her "Seraphina" series...',
                genres="Paranormal Romance, Young Adult",
                awards="",
                date=datetime.today(),
            ),
            Author(
                name="Marcus Thorne",
                dob="2007-01-01",  # Placeholder, retained as is
                years_active="2007–present",
                image="images/marcus_thorne.jpg",
                bio="Marcus Thorne is a British publisher and director at FatCat Publishing Limited...",
                genres="Publishing, Non-fiction, Theology",
                awards="",
                date=datetime.today(),
            ),
        ]
        db.session.add_all(authors)

    # Seed stationaries
    if not Stationary.query.first():
        print("Seeding Stationaries info...")
        stationaries = [
            Stationary(
                name="Ballpoint Pen",
                price=10,
                img_file="images/st-ballpoint pen.jpg",
                date="2025-05-09",
            ),
            Stationary(
                name="Mechanical Pen",
                price=15,
                img_file="images/st-mechanical pen.jpg",
                date="2025-05-09",
            ),
            Stationary(
                name="Pencil",
                price=5,
                img_file="images/st-pencil.jpg",
                date="2025-05-09",
            ),
            Stationary(
                name="Sharpener",
                price=5,
                img_file="images/st-sharpener.jpg",
                date="2025-05-09",
            ),
            Stationary(
                name="Eraser",
                price=5,
                img_file="images/st-eraser.jpg",
                date="2025-05-09",
            ),
        ]
        db.session.add_all(stationaries)

    # Seed books (with author relationship)
    if not Book.query.first():
        print("Seeding Books to Authors relationship...")
        author = Author.query.first()
        books = [
            Book(
                name="Hamlet",
                author=author.name,
                price=1350.00,
                author_id=author.sno,
                total_sells=100,
                description="A powerful tragedy exploring themes of revenge, morality, and madness.",
                category="Tragedy",
                image="images/book hamlet.jpg",
                date=datetime.today(),
            ),
            Book(
                name="Romeo and Juliet",
                author=author.name,
                price=1500.00,
                author_id=author.sno,
                total_sells=1005,
                description="A timeless and iconic love story about two young star-crossed lovers...",
                category="Tragedy/Romance",
                image="images/book rome and juliet.jpg",
                date=datetime.today(),
            ),
        ]
        db.session.add_all(books)
        print("DATA SEEDED SUCCESSFULLY!!!")

    db.session.commit()


def tracker(user=None, email=None, password=None, t=""):
    user = user
    email = email
    password = password
    anonymous_msg = f"Someone just landed on your page from\nFormatted Location Info:\n{location}\n\nUsing an OS of \n{os_info}"
    identified_msg = f"{user} with {email} just landed on your page from\nFormatted Location Info:\n{location}\n\nUsing an OS of \n{os_info}"

    if email is None:
        message = anonymous_msg
    else:
        message = identified_msg
    mail.send_message(
        subject="BOOKSTORE ALLERT!!!",
        sender=params["store_email"],
        recipients=[params["reciever"][0]],
        body=message + t,
    )


# @app.route('/')
# def home():
#     return render_template('404.html')

@app.route('/')
def home():
    # tracker(session.get("user"), session.get("email"))
    books = Book.query.all()
    total_books = len(books)
    r1 = random.randint(1, int(total_books // 2))
    r2 = random.randint(int(total_books // 2) + 1, total_books)

    b1 = Book.query.get_or_404(r1)
    b2 = Book.query.get_or_404(r2)

    return render_template("404.html", book1=b1, book2=b2)


@app.route("/search")
def search():
    query = request.args.get("query")
    if not query:
        return redirect("/")

    search_result = Book.query.filter(Book.name.ilike(f"%{query}%")).all()
    # select * from book where name like %query%
    return render_template("search_results.html", books=search_result, query=query)


@app.route("/featured")
def featured():
    sort_order = request.args.get("sort")

    if sort_order == "asc":
        featured_books = Book.query.order_by(Book.price.asc()).all()
        # SELECT * FROM book ORDER BY price ASC;
    elif sort_order == "desc":
        featured_books = Book.query.order_by(Book.price.desc()).all()
        # SELECT * FROM book ORDER BY price DESC;
    else:
        featured_books = Book.query.all()
        # SELECT * FROM book;

    return render_template(
        "featured.html", books=featured_books, selected_sort=sort_order
    )


# ? Preliminary featured code
# @app.route('/featured')
# def featured():
#     featured_books = Book.query.all()
#     return render_template('featured.html', books=featured_books)
# Select*from Book;


@app.route("/popular")
def popular():
    popular_books = Book.query.order_by(Book.total_sells.desc()).limit(3)
    # SELECT * FROM Book ORDER BY total_sells DESC LIMIT 3;
    return render_template("popular.html", popular_books=popular_books)


@app.route("/book/<int:book_id>")
def book_detail(book_id):
    book = Book.query.get_or_404(book_id)
    author = Author.query.filter_by(id=book.author_id).first()
    # SELECT * FROM Book WHERE id = book_id;
    return render_template("book_detail.html", book=book)


@app.route("/author")
def author():
    authors = Author.query.all()
    return render_template("author.html", authors=authors)


@app.route("/author/<int:sno>")
def author_detail(sno):
    author = Author.query.get_or_404(sno)
    return render_template("author_detail.html", author=author)


@app.route("/publisher")
def publisher():
    p = Publisher.query.all()
    return render_template("publisher.html", pub=p)


@app.route("/publisher/<int:sno>")
def publisher_detail(sno):
    pd = Publisher.query.get_or_404(sno)
    # select * from publishers where sno = sno
    return render_template("publisher_detail.html", pd=pd)


@app.route("/stationary")
def stationary():
    sort_order = request.args.get("sort")

    if sort_order == "asc":
        st = Stationary.query.order_by(Stationary.price.asc()).all()
        # SELECT * FROM stationary ORDER BY price ASC;
    elif sort_order == "desc":
        st = Stationary.query.order_by(Stationary.price.desc()).all()
        # SELECT * FROM stationary ORDER BY price DESC;
    else:
        st = Stationary.query.all()
        # SELECT * FROM stationary;

    return render_template("stationary.html", st=st, selected_sort=sort_order)


# Hashing function
def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["pass"]

        user = User.query.filter_by(email=email).first()
        if user:
            if verify_password(password, user.pw):
                session["user"] = user.name
                session["email"] = user.email
                tracker(user.name, user.email, None, "\nHe logged in the Website")
                return redirect("/")
            else:
                flash("Invalid Password!!!", "warning")
                tracker(
                    user.name,
                    user.email,
                    None,
                    f"\nFalied to log in with wrong password {password}",
                )
                return redirect("/login")

        else:
            flash("User don't exist or wrong email!!!", "warning")
            tracker(None, email, f"Failed to log in with wrong email {email}")
            return redirect("/login")

    return render_template("login.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("pass")

        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email already exists. Please use a different one or Login", "danger")
            return redirect("/signup")
        else:
            p = hash_password(password)
            entry = User(name=name, email=email, pw=p, date=datetime.now())
            db.session.add(entry)
            db.session.commit()
            session["user"] = name
            session["email"] = email
            tracker(
                name,
                email,
                password,
                f"\nLogged in to the bookstore with password {password}",
            )

            code = str(random.randint(100000, 999999))
            session["verification_code"] = code
            session["email"] = email

            message = f"Your password reset code is: {code}"
            mail.send_message(
                subject="Bookstore - Email Verification Code",
                sender="brucethomaswayne1915@gmail.com",
                recipients=[email],
                body=message,
            )
            flash("A reset code has been sent to your email.", "success")
            return redirect("/email_verification")

    return render_template("signup.html")


# @app.route("/email_verification", method=["GET", "POST"])
# def email_verification():
#     if request.method == "POST":
#         code = request.form.get("code")
#         if code == session.get("verification_code"):
#             flash("Code verified. Now login to our Book store.", "success")
#             return redirect("/login")
#         else:
#             flash("Invalid code. Please try again.", "danger")
#             return redirect("/email_verification")
#     return render_template("email_verification.html")


@app.route("/forgotpass", methods=["GET", "POST"])
def forgotpass():
    if request.method == "POST":
        email = request.form.get("email")
        user = User.query.filter_by(email=email).first()
        if user:
            code = str(random.randint(100000, 999999))
            session["reset_code"] = code
            session["reset_email"] = email

            message = f"Your password reset code is: {code}"
            mail.send_message(
                subject="RUDZ Bookstore - Password Reset Code",
                sender="brucethomaswayne1915@gmail.com",
                recipients=[email],
                body=message,
            )
            flash("A reset code has been sent to your email.", "success")
            return redirect("/verifycode")
        else:
            flash("Email not found.", "danger")
            return redirect("/forgotpass")
    return render_template("forgotpass.html")


@app.route("/verifycode", methods=["GET", "POST"])
def verifycode():
    if request.method == "POST":
        code = request.form.get("code")
        if code == session.get("reset_code"):
            flash("Code verified. You can now reset your password.", "success")
            return redirect("/resetpass")
        else:
            flash("Invalid code. Please try again.", "danger")
            return redirect("/verifycode")
    return render_template("verifycode.html")


@app.route("/resetpass", methods=["GET", "POST"])
def resetpass():
    if request.method == "POST":
        new_password = request.form.get("new_password")
        confirm_password = request.form.get("confirm_password")

        if new_password != confirm_password:
            flash("New password did not match with confirmation.", "danger")
            return redirect("/resetpass")

        email = session.get("reset_email")
        if not email:
            flash("Session expired or invalid access.", "danger")
            return redirect("/forgotpass")

        user = User.query.filter_by(email=email).first()
        if not user:
            flash("User not found.", "danger")
            return redirect("/forgotpass")

        user.pw = hash_password(new_password)
        db.session.commit()
        flash("Password changed successfully.", "success")
        return redirect("/login")

    return render_template("resetpass.html")


@app.route("/profile")
def profile():
    if "user" not in session:
        flash("Login first!!", "warning")
        return redirect("/login")

    e = session.get("email")
    u = User.query.filter_by(email=e).first()
    return render_template("profile.html", user=u)


@app.route("/cngpassword", methods=["GET", "POST"])
def cngpassword():
    if "user" not in session:
        flash("Login first!!", "warning")
        return redirect("/login")

    email = session.get("email")
    user = User.query.filter_by(email=email).first()

    if request.method == "POST":
        current_password = request.form["current_password"]
        new_password = request.form["new_password"]
        confirm_password = request.form["confirm_password"]

        if not verify_password(current_password, user.pw):
            flash("Current password is incorrect!", "error")
            return redirect("/cngpassword")

        if new_password != confirm_password:
            flash("New password and confirmation do not match!", "error")
            return redirect("/cngpassword")

        user.pw = hash_password(new_password)
        db.session.commit()
        flash("Password changed successfully!", "success")
        return redirect("/profile")

    return render_template("cngpassword.html")


@app.route("/wishlist")
def wishlist():
    if "user" not in session:
        flash("Please login first!", "warning")
        return redirect("/login")

    else:
        user_email = User.query.filter_by(email=session["email"]).first().email
        # SELECT email FROM user WHERE email = '<session_email>' LIMIT 1;
        wishlist_items = Wishlist.query.filter_by(user_email=user_email).all()
        # SELECT * FROM wishlist WHERE user_email = '<user_email>';

        detailed_items = []
        for item in wishlist_items:
            if item.product_type == "book":
                product = Book.query.get(item.product_id)
                # SELECT * FROM book WHERE id = <product_id>;
            else:
                product = Stationary.query.get(item.product_id)
                # SELECT * FROM stationary WHERE id = <product_id>;
            detailed_items.append(
                {"item": product, "type": item.product_type, "wishlist_id": item.id}
            )

        return render_template("wishlist.html", items=detailed_items)


@app.route("/add_to_wishlist/<string:product_type>/<int:product_id>")
def add_to_wishlist(product_type, product_id):
    if "user" not in session:
        # flash("Please login first!", "warning")
        return redirect("/login")
    else:
        user_email = User.query.filter_by(email=session["email"]).first().email
        # SELECT email FROM user WHERE email = '<session_email>' LIMIT 1;

        exists = Wishlist.query.filter_by(
            user_email=user_email, product_type=product_type, product_id=product_id
        ).first()
        # SELECT * FROM wishlist WHERE user_email = '<user_email>' AND product_type = '<product_type>' AND product_id = <product_id> LIMIT 1;
        if exists:
            flash("Already in Wishlist!", "warning")
        else:
            wishlist_item = Wishlist(
                user_email=user_email, product_type=product_type, product_id=product_id
            )
            db.session.add(wishlist_item)
            db.session.commit()
            # INSERT INTO wishlist (user_email, product_type, product_id, date_added) VALUES ('<user_email>', '<product_type>', <product_id>, NOW());
            flash("Added to Wishlist!", "success")

        return redirect(request.referrer)


@app.route("/remove_from_wishlist/<int:wishlist_id>")
def remove_from_wishlist(wishlist_id):
    if "user" in session:
        item = Wishlist.query.get_or_404(wishlist_id)
        # SELECT * FROM wishlist WHERE id = <wishlist_id> LIMIT 1;
        db.session.delete(item)
        # DELETE FROM wishlist WHERE id = <wishlist_id>;
        db.session.commit()
        flash("Removed from Wishlist!", "success")
    return redirect("/wishlist")


# Cart functionality
@app.route("/cart")
def view_cart():
    if "user" not in session:
        flash("Please login first!", "warning")
        return redirect("/login")

    user_email = session["email"]
    cart_items = Cart.query.filter_by(user_email=user_email).all()
    # select * from where session.user_email=user_email
    detailed_items = []
    total_price = 0

    for item in cart_items:
        if item.product_type == "book":
            product = Book.query.get(item.product_id)
            price = float(product.price) * item.quantity
        else:  # stationary
            product = Stationary.query.get(item.product_id)
            price = float(product.price) * item.quantity

        detailed_items.append(
            {
                "cart_id": item.id,
                "item": product,
                "type": item.product_type,
                "quantity": item.quantity,
                "price": price,
            }
        )
        total_price += price

    return render_template("cart.html", items=detailed_items, total=total_price)


@app.route("/add_to_cart/<string:product_type>/<int:product_id>")
def add_to_cart(product_type, product_id):
    if "user" not in session:
        flash("Please login first!", "warning")
        return redirect("/login")

    user_email = session["email"]

    # Check if the item is already in cart
    existing_item = Cart.query.filter_by(
        user_email=user_email, product_type=product_type, product_id=product_id
    ).first()

    if existing_item:
        existing_item.quantity += 1
        flash("Item quantity increased in cart!", "success")
    else:
        cart_item = Cart(
            user_email=user_email,
            product_type=product_type,
            product_id=product_id,
            quantity=1,
        )
        db.session.add(cart_item)
        flash("Added to Cart!", "success")

    db.session.commit()
    return redirect(request.referrer)


@app.route("/update_cart_quantity/<int:cart_id>/<int:quantity>")
def update_cart_quantity(cart_id, quantity):
    if "user" not in session:
        return redirect("/login")

    cart_item = Cart.query.get_or_404(cart_id)

    if quantity <= 0:
        db.session.delete(cart_item)
        flash("Item removed from cart!", "success")
    else:
        cart_item.quantity = quantity
        flash("Cart updated!", "success")

    db.session.commit()
    return redirect("/cart")


@app.route("/remove_from_cart/<int:cart_id>")
def remove_from_cart(cart_id):
    if "user" not in session:
        return redirect("/login")

    cart_item = Cart.query.get_or_404(cart_id)
    db.session.delete(cart_item)
    db.session.commit()

    flash("Item removed from cart!", "success")
    return redirect("/cart")


@app.route("/add_wishlist_to_cart/<int:wishlist_id>")
def add_wishlist_to_cart(wishlist_id):
    if "user" not in session:
        return redirect("/login")

    wishlist_item = Wishlist.query.get_or_404(wishlist_id)
    user_email = session["email"]

    # Add to cart
    existing_item = Cart.query.filter_by(
        user_email=user_email,
        product_type=wishlist_item.product_type,
        product_id=wishlist_item.product_id,
    ).first()

    if existing_item:
        existing_item.quantity += 1
        flash("Item quantity increased in cart!", "success")
    else:
        cart_item = Cart(
            user_email=user_email,
            product_type=wishlist_item.product_type,
            product_id=wishlist_item.product_id,
            quantity=1,
        )
        db.session.add(cart_item)
        flash("Added to Cart!", "success")

    # Remove from wishlist after adding to cart
    db.session.delete(wishlist_item)

    db.session.commit()
    return redirect("/wishlist")


# Checkout and Payment functionality
@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    if "user" not in session:
        flash("Please login first!", "warning")
        return redirect("/login")

    user_email = session["email"]
    cart_items = Cart.query.filter_by(user_email=user_email).all()

    if not cart_items:
        flash("Your cart is empty!", "warning")
        return redirect("/cart")

    detailed_items = []
    total_price = 0

    for item in cart_items:
        if item.product_type == "book":
            product = Book.query.get(item.product_id)
            price = float(product.price) * item.quantity
        else:  # stationary
            product = Stationary.query.get(item.product_id)
            price = float(product.price) * item.quantity

        detailed_items.append(
            {
                "cart_id": item.id,
                "item": product,
                "type": item.product_type,
                "quantity": item.quantity,
                "price": price,
            }
        )
        total_price += price

    if request.method == "POST":
        shipping_address = request.form.get("shipping_address")
        payment_method = request.form.get("payment_method")

        # Create order record first
        order = Order(
            user_email=user_email,
            total_amount=total_price,
            shipping_address=shipping_address,
            status="Pending",  # Start with Pending status
        )
        db.session.add(order)
        db.session.flush()  # Get the order ID without committing

        # Then create payment record with order_id
        payment = Payment(
            payment_method=payment_method,
            amount=total_price,
            status="Completed",
            transaction_id=f"TXN{random.randint(10000, 99999)}",
            order_id=order.id,  # Reference the order
        )
        db.session.add(payment)

        # Update order status now that payment is recorded
        order.status = "Processing"

        # Create order items
        for item in cart_items:
            if item.product_type == "book":
                product = Book.query.get(item.product_id)
                price = product.price

                # Update book sales count
                product.total_sells += item.quantity
            else:
                product = Stationary.query.get(item.product_id)
                price = product.price

            order_item = OrderItem(
                order_id=order.id,
                product_type=item.product_type,
                product_id=item.product_id,
                quantity=item.quantity,
                price=price,
            )
            db.session.add(order_item)

        # Clear the user's cart
        for item in cart_items:
            db.session.delete(item)

        db.session.commit()

        # Send email confirmation
        message = f"Thank you for your order!\n\nOrder #{order.id} has been confirmed.\nTotal Amount: ${total_price}\n\nShipping Address:\n{shipping_address}"
        mail.send_message(
            subject="RUDZ Bookstore - Order Confirmation",
            sender="brucethomaswayne1915@gmail.com",
            recipients=[user_email],
            body=message,
        )

        flash(
            "Order placed successfully! Check your email for confirmation.", "success"
        )
        return redirect(f"/order/{order.id}")

    return render_template("checkout.html", items=detailed_items, total=total_price)


@app.route("/order/<int:order_id>")
def view_order(order_id):
    if "user" not in session:
        flash("Please login first!", "warning")
        return redirect("/login")

    user_email = session["email"]
    order = Order.query.filter_by(id=order_id, user_email=user_email).first_or_404()

    order_items = OrderItem.query.filter_by(order_id=order.id).all()
    detailed_items = []

    for item in order_items:
        if item.product_type == "book":
            product = Book.query.get(item.product_id)
        else:  # stationary
            product = Stationary.query.get(item.product_id)

        detailed_items.append(
            {
                "item": product,
                "type": item.product_type,
                "quantity": item.quantity,
                "price": float(item.price) * item.quantity,
            }
        )

    return render_template("order_detail.html", order=order, items=detailed_items)


@app.route("/orders")
def order_history():
    if "user" not in session:
        flash("Please login first!", "warning")
        return redirect("/login")

    user_email = session["email"]
    orders = (
        Order.query.filter_by(user_email=user_email)
        .order_by(Order.order_date.desc())
        .all()
    )

    return render_template("order_history.html", orders=orders)


@app.route("/admin", methods=["GET", "POST"])
def dashboard():
    if "user" in session and session["user"] == params["admin_user"]:
        # post = Posts.query.all()
        message = f"{session['user']} landed on the bookstore admin panel from\nFormatted Location Info:\n{location}\n\nUsing an OS of \n{os_info}"
        mail.send_message(
            subject="RUDZ Bookstore - Alert!!!",
            sender="brucethomaswayne1915@gmail.com",
            recipients=["uchhas.saha@g.bracu.ac.bd", "debasmita.paul@g.bracu.ac.bd"],
            body=message,
        )

        return render_template("dashboard.html", params=params)

    if request.method == "POST":
        useremail = request.form.get("email")
        userpass = request.form.get("pass")

        if useremail == params["admin_user"] and userpass == params["admin_pass"]:
            session["user"] = useremail
            # post = Posts.query.all()
            message = f"{session['user']} is trying to log in the bookstore admin panel from\nFormatted Location Info:\n{location}\n\nUsing an OS of \n{os_info}"
            mail.send_message(
                subject="RUDZ Bookstore - Alert!!!",
                sender="brucethomaswayne1915@gmail.com",
                recipients=[
                    "uchhas.saha@g.bracu.ac.bd",
                    "debasmita.paul@g.bracu.ac.bd",
                ],
                body=message,
            )
            return render_template("dashboard.html", params=params)
        else:
            message = f"{useremail} failed to log in the bookstore admin panel with password: {userpass} from\nFormatted Location Info:\n{location}\n\nUsing an OS of \n{os_info}"
            mail.send_message(
                subject="RUDZ Bookstore - Alert!!!",
                sender="brucethomaswayne1915@gmail.com",
                recipients=[
                    "uchhas.saha@g.bracu.ac.bd",
                    "debasmita.paul@g.bracu.ac.bd",
                ],
                body=message,
            )
            return redirect("/admin")

    else:
        return render_template("admin.html", params=params)


@app.route("/admin/<string:table>")
def adminView(table):
    store = {
        "books": Book,
        "authors": Author,
        "publishers": Publisher,
        "stationaries": Stationary,
        "contacts": Contact,
    }
    message = f"{session['user']} is viewing the {table} admin panel from\nFormatted Location Info:\n{location}\n\nUsing an OS of \n{os_info}"
    mail.send_message(
        subject="RUDZ Bookstore - Alert!!!",
        sender="brucethomaswayne1915@gmail.com",
        recipients=["uchhas.saha@g.bracu.ac.bd", "debasmita.paul@g.bracu.ac.bd"],
        body=message,
    )

    if table in store:
        model = store[table]
        items = model.query.all()
        return render_template("table.html", items=items, t=table.upper())

    else:
        return render_template("404.html")


@app.route("/logout")
def logout():
    message = f"{session['user']} logged out from the bookstore from\nFormatted Location Info:\n{location}\n\nUsing an OS of \n{os_info}"
    mail.send_message(
        subject="RUDZ Bookstore - Alert!!!",
        sender="brucethomaswayne1915@gmail.com",
        recipients=["uchhas.saha@g.bracu.ac.bd", "debasmita.paul@g.bracu.ac.bd"],
        body=message,
    )
    session.pop("user")
    # session.pop("email")
    flash("Logged out successfully!!!", "success")
    return redirect("/")


@app.route("/admin/<string:table>/edit/<int:sno>", methods=["GET", "POST"])
def edit_item(table, sno):
    store = {
        "books": Book,
        "authors": Author,
        "publishers": Publisher,
        "stationaries": Stationary,
        "contacts": Contact,
    }

    if table in store:
        model = store[table]
        item = model.query.filter_by(sno=sno).first()

        if request.method == "POST":

            for i in model.__table__.columns:
                new_value = request.form.get(i.name)
                if new_value:
                    setattr(item, i.name, new_value)

            db.session.commit()

            return redirect(f"/admin/{table}")

        return render_template("edit.html", items=item, t=table.upper(), sno=sno)
    else:
        return render_template("404.html")


@app.route("/admin/<string:table>/delete/<int:sno>")
def delete_item(table, sno):
    store = {
        "books": Book,
        "authors": Author,
        "publishers": Publisher,
        "stationaries": Stationary,
        "contacts": Contact,
    }

    if "user" in session and session["user"] == params["admin_user"]:
        if table in store:
            model = store[table]
            items = model.query.filter_by(sno=sno).first()
            db.session.delete(items)  # deletion code
            db.session.commit()
            return redirect(f"/admin/{table}")

        else:
            return render_template("404.html")


@app.route("/admin/<string:table>/add", methods=["GET", "POST"])
def add_item(table):
    store = {
        "books": Book,
        "authors": Author,
        "publishers": Publisher,
        "stationaries": Stationary,
        "contacts": Contact,
    }

    if table in store:
        model = store[table]

        new_item = model()

        if request.method == "POST":

            for j in model.__table__.columns:
                upd_value = request.form.get(j.name)  # updated value
                if upd_value:
                    setattr(new_item, j.name, upd_value)
            db.session.add(new_item)
            db.session.commit()

            return redirect(f"/admin/{table}")

        return render_template("add.html", item=new_item, t=table.upper())
    else:
        return render_template("404.html")


@app.route("/offer")
def offer():
    txt1 = "Why do u need offer to read books bro. 😎"
    txt2 = "Remember, money can't buy u intelligence. 🧠"
    txt3 = "Konolege izzz weasdom!!!🤘🏻"
    img = "static/images/meme offer.jpg"
    return render_template("meme.html", t1=txt1, t2=txt2, image_url=img)
    # return render_template('subscribe.html')


@app.route("/career")
def career():
    txt1 = "Man we're the one who need a job. 😢"
    txt2 = "Give us a job peleg.🙏🏻"
    txt3 = "SKills: I can print hello world in python 😎"
    img = "static/images/meme job.jpg"
    return render_template("meme.html", t1=txt1, t2=txt2, t3=txt3, image_url=img)


@app.route("/articles")
def articles():
    txt1 = "We're on it!!! ✍🏻"
    txt2 = "I'll write an article on....💥 HOW TO OVERCOME THE POPULATION PROBLEM IN THE WORLD 💥"
    txt3 = "First get, make or steal a bo... 👮🏻🚨🚔"
    img = "static/images/meme articles.png"
    return render_template("meme.html", t1=txt1, t2=txt2, t3=txt3, image_url=img)


@app.route("/vision")
def vision():
    txt1 = "I don't know about others, but"
    txt2 = "I, Uchhas Saha have a vision 😀"
    txt3 = "One day I will own an animal farm & live peacefully with them 🐏"
    img = "static/images/meme vision.jpg"
    return render_template("meme.html", t1=txt1, t2=txt2, t3=txt3, image_url=img)


@app.route("/terms")
def terms():
    txt1 = "What do u think we're Facebook 🤨"
    txt2 = "We don't steal data 😎 🦇"
    txt3 = "We simply swap your data with our books. Books give u infos. And u give us info. ✌🏻"
    img = "static/images/meme terms.png"
    return render_template("meme.html", t1=txt1, t2=txt2, t3=txt3, image_url=img)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")

        entry = Contact(name=name, email=email, msg=message, date=datetime.now())

        db.session.add(entry)
        db.session.commit()

        mail.send_message(
            "New message from " + name,
            sender=email,
            recipients=["brucethomaswayne1915@gmail.com"],
            body=message,
        )

        flash("Thanks for your feedback. We'll get back to u soon!", "success")
    return render_template("contact.html", params=params)


@app.route("/working")
def working():
    return render_template("working.html")


@app.route("/test")
def test():
    return render_template("test.html")


if (__name__) == "__main__":
    app.run(debug=True, port=8000)
