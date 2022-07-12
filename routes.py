from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired
from app import app, db
from models import User, Book, Collection, Item
from flask import render_template, request, url_for, redirect, flash

#A form for inputing new books via Dashboard
class AddBookForm(FlaskForm):
  isbn = IntegerField(label = 'ISBN:', validators=[DataRequired()])
  title = StringField(label = 'Book Title:', validators=[DataRequired()])
  author = StringField(label = 'Author Name:', validators=[DataRequired()])
  genre = StringField(label = 'Genre:', validators=[DataRequired()])
  year_published = IntegerField(label = 'Year Published:', validators=[DataRequired()] )
  submit = SubmitField('Add Book')
  
#function to check if an item to be added is already in the collection
def exists(item, collection):
  """Return a boolean
    True if collection contains item. False otherwise.
    """
  for i in collection: #for each item in collection
    if i.book_id == item.book_id: #check if the primary key is equal
       return True
  return False

#The home page of Gambiana.
#Lists all the users currently in the database
#renders the home.html template providing the list of current users
@app.route('/profiles')
def profiles():
  current_users = User.query.all()
  return render_template('users.html', current_users = current_users)

#Displays profile pages for a user with the user_id primary key
#renders the profile.html template for a specific user, book library and 
#the user's collection 
@app.route('/profile/<int:user_id>')
def profile(user_id):
  user = User.query.filter_by(id = user_id).first_or_404(description = "No such user found.")
  books = Book.query.all()
  my_collection = Collection.query.get(user.collection_id)
  return render_template('profile.html', user = user, books = books, my_collection = my_collection)

#Adds new books to a user's collection from the book library
#redirects back to the profile that issued the addition
@app.route('/add_item/<int:user_id>/<int:book_id>/<int:collection_id>')
def add_item(user_id, book_id, collection_id):
  new_item = Item(book_id = book_id, collection_id = collection_id)
  user = User.query.filter_by(id = user_id).first_or_404(description = "No such user found.")
  my_collection = Collection.query.filter_by(id = user.collection_id).first()
  if not exists(new_item, my_collection.items):
    book = Book.query.get(book_id)
      #using db session add the new item
    db.session.add(new_item)
      #increase the counter for the book here
    book.n += 1
      #commit the database changes here
    db.session.commit()
  return redirect(url_for('profile', user_id = user_id))

#Remove an item from a user's collection
#Redirects back to the profile that issues the removal
@app.route('/remove_item/<int:user_id>/<int:item_id>')
def remove_item(user_id, item_id):
   #from the Item model, fetch the item with primary key item_id to be deleted
  db.session.delete(Item.query.get(item_id))
   #using db.session delete the item
   #commit the deletion
  db.session.commit()
  return redirect(url_for('profile', user_id = user_id))

#Retrieve Book by id
@app.route('/<int:book_id>/')
def show_book(book_id):
  book = Book.query.get_or_404(book_id)
  return render_template('book.html', book=book)


#Show all books
@app.route('/library')
def library():
    books = Book.query.all()
    return render_template('library.html', books=books)

#Delete a book from the library
@app.route('/delete_book/<int:book_id>')
def delete_book(book_id):
  db.session.delete(Book.query.get(book_id))
  db.session.commit()
  return redirect(url_for('dashboard')) 

# #Update/edit a Book   
# @app.route('/update_book/<int:book_id>')
# def update_book(book_id):
      

#Display the Dashboard page with a form for adding books
#Renders the dashboard template
@app.route('/dashboard', methods=["GET", "POST"])
def dashboard():
  form = AddBookForm()
  title = request.form.get("title")
  author = request.form.get("author")
  genre = request.form.get("genre")
  isbn = request.form.get("isbn")
  year = request.form.get("year_published")
  if request.method == 'POST':
      book = Book(title=title, author=author, genre=genre, isbn=isbn, year_published=year)
      db.session.add(book)
      db.session.commit()
      return redirect(url_for('dashboard')) 
  books = Book.query.all()  
  return render_template('dashboard.html', books = books, form = form)