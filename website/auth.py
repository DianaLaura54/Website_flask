from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User,Pass,Book,Location,Rents
from werkzeug.security import generate_password_hash, check_password_hash
from . import db   ##means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user
from datetime import datetime, timedelta
from sqlalchemy import text

auth = Blueprint('auth', __name__)

#this method is for logging in the user
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')
    return render_template("login.html", user=current_user)



#this method is for logging out the user
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))



#this method is for creating the pass
#the initial price is 20 ron,but if the user is less than 7 years old or is a student they receive a discount

@auth.route('/pass', methods=['GET', 'POST'])
@login_required
def pass_page():
    if request.method == 'POST':
        id_pass = User.query.count() + 1
        current_user.id_pass =id_pass
        current_user.member=True
        db.session.commit()
        initial_price = 20
        student_discount = 0.5 if current_user.student.lower() == 'yes' else 1.0
        age_discount = 0.5 if current_user.age < 7 else 1.0
        price = int(initial_price * student_discount * age_discount)
        date_today = datetime.utcnow().date()
        pass_data = Pass(
            id_pass=id_pass,
            price=price,
            status='Active',
            date=date_today
        )
        db.session.add(pass_data)
        db.session.commit()
        flash(f'Pass created! Your Membership ID is {pass_data.id_pass}. Price: {price} credits', category='success')
    return render_template("pass.html", user=current_user)


#this method is for showing the book list, and for renting
#if a user wants a specific book they have to insert the book id and the book has to be available
@auth.route('/book_list', methods=['GET', 'POST'])
@login_required
def book_list():
    genre = request.args.get('genre')
    if request.method == 'POST':
        book_id = request.form.get('reserve')
        book = Book.query.get(book_id)
        if book:
            user_pass = Pass.query.filter_by(id_pass=current_user.id_pass).first()
            if user_pass and book.status == 'Available':
                book.status = 'Reserved'
                rent = Rents(id_book=book_id, id_user=current_user.id, date=datetime.now(), return_date=datetime.now() + timedelta(days=14))
                db.session.add(rent)
                db.session.commit()
                flash(f'Status of book "{book.name}" updated to Reserved. Due in 14 days.', category='success')
            elif not user_pass:
                flash('You need a valid pass to reserve a book', category='error')
            else:
                flash(f'Book "{book.name}" is not available for reservation', category='error')
        else:
            flash('Invalid book selection', category='error')
    # filter books by genre if provided
    if genre:
        books = Book.query.filter(Book.genre.ilike(f'%{genre}%')).all()
    else:
        books = Book.query.all()
    return render_template("book_list.html", user=current_user, books=books, genre=genre)

#this method is for sign up,the user has to specify the email,name,password(once and twice for confirmation),their age and if they are a student or not
@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        age=request.form.get('age')
        student=request.form.get('student')
        id_pass=-1
        member=False
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        elif len(age)<1:
            flash("The age isn't valid")
        elif student.lower() not in ["yes", "no"]:
            flash("Please insert yes or no")
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='pbkdf2:sha256'),age=age,student=student,id_pass=id_pass,member=member,donations=0)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
    return render_template("sign_up.html", user=current_user)

#this method is for the admin to add books to the database
@auth.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form.get('name')
        author = request.form.get('author')
        location = request.form.get('location') 
        status="Available"
        genre= request.form.get('genre')
        if len(name) < 1:
            flash('Please provide a name for the book', category='error')
        elif len(author) < 1:
            flash('Please provide the author of the book', category='error')
        elif len(location) < 1:
            flash('Please provide a location for the book', category='error')
        elif len(genre) < 1:
            flash('Please provide a genre for the book', category='error')
        else:
            existing_location = Location.query.filter_by(name=location).first()
            if existing_location:
                new_book = Book(name=name, author=author, location=location,status=status,genre=genre)
                db.session.add(new_book)
                db.session.commit()
                flash('Book added!', category='success')
            else:
                flash('Location does not exist. Please choose a valid location.', category='error')
    return render_template("add.html", user=current_user)





#this method is for the admin to add new locations,without the location a new book can't be added

@auth.route('/locations', methods=['GET', 'POST'])
@login_required
def locations():
    if request.method == 'POST':
        name = request.form.get('location')
        if len(name) < 1:
            flash('Please give a name', category='error')
        else:
            existing_location = Location.query.filter_by(name=name).first()
            if existing_location:
                flash('Location already exists', category='error')
            else:
                new_location = Location(name=name)
                db.session.add(new_location)
                db.session.commit()
                flash('Location added!', category='success')
    locations = Location.query.all()
    return render_template("locations.html", user=current_user, locations=locations)



#this method is for showing the user rents,and returning the book if the user specifies a id
@auth.route('/rents', methods=['GET', 'POST'])
@login_required
def user_rents():
    if request.method == 'POST':
        rent_id_to_delete = request.form.get('rent')
        if rent_id_to_delete:
            rent_query = text(f"SELECT * FROM Rents WHERE id = {rent_id_to_delete} AND id_user = {current_user.id}")
            rent_to_delete = db.session.execute(rent_query).fetchone()
            if rent_to_delete:
                # delete the rent with the specified ID
                delete_query = text(f"DELETE FROM Rents WHERE id = {rent_id_to_delete} AND id_user = {current_user.id}")
                db.session.execute(delete_query)
                db.session.commit()
                # update the book status to 'Available'
                update_book_query = text(f"UPDATE Book SET status = 'Available' WHERE id = {rent_to_delete.id_book}")
                db.session.execute(update_book_query)
                db.session.commit()
                flash(f'Rent with ID {rent_id_to_delete} deleted successfully, and book status updated', category='success')
            else:
                flash(f'Invalid Rent ID or Rent does not belong to the current user', category='error')
    # fetch the rents for the current user using a raw SQL query
    query = text(f"SELECT * FROM Rents WHERE id_user = {current_user.id}")
    user_rents = db.session.execute(query).fetchall()
    # fetch the book details for each rent
    books = []
    for rent in user_rents:
        book_id = rent.id_book
        book_query = text(f"SELECT * FROM Book WHERE id = {book_id}")
        book = db.session.execute(book_query).fetchone()
        books.append(book)
    return render_template("rents.html", user=current_user, user_rents=user_rents, books=books)


#this method is for the admin to delete existing books from the database
@auth.route('/delete', methods=['GET', 'POST'])
@login_required
def delete_book():
    if request.method == 'POST':
        book_id = request.form.get('delete')
        if book_id is not None and book_id.isdigit():
            book = Book.query.get(book_id)
            if book and book.status == 'Available':
                db.session.delete(book)
                db.session.commit()
                flash(f'Book with ID {book_id} deleted successfully', category='success')
            elif book and book.status != 'Available':
                flash(f'Book with ID {book_id} is not available for deletion', category='error')
            else:
                flash(f'Book with ID {book_id} not found', category='error')
        else:
            flash('Invalid book ID', category='error')
    books = Book.query.all()
    return render_template("delete.html", books=books, user=current_user)



#this method is for users to donate books,if they want to
@auth.route('/donate', methods=['GET', 'POST'])
@login_required
def donate():
    if request.method == 'POST':
        name = request.form.get('name')
        author = request.form.get('author')
        location = request.form.get('location') 
        status = "Available"
        genre= request.form.get('genre')
        if len(name) < 1:
            flash('Please provide a name for the book', category='error')
        elif len(author) < 1:
            flash('Please provide the author of the book', category='error')
        elif len(location) < 1:
            flash('Please provide a location for the book', category='error')
        elif len(genre) < 1:
            flash('Please provide a genre for the book', category='error')
        else:
            existing_location = Location.query.filter_by(name=location).first()
            if existing_location:
                new_book = Book(name=name, author=author, location=location, status=status,genre=genre)
                db.session.add(new_book)
                db.session.commit()
                # Increase the current user's donations
                current_user.donations=current_user.donations+1
                db.session.commit()
                flash('Book added! Thank you for your donation.', category='success')
                return redirect(url_for('views.home'))
            else:
                flash('Location does not exist. Please choose a valid location.', category='error')
    return render_template("donate.html", user=current_user)

# route for admin to view users
@auth.route('/users')
@login_required
def view_users():
    users = User.query.all()
    return render_template("users.html", users=users, user=current_user)




