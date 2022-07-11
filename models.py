from app import app, db

class User(db.Model):
      id = db.Column(db.Integer, primary_key = True)
      username = db.Column(db.String(50), index = True, unique = True)

      def __repr__(self):
            return "{}".format(self.username)

class Book(db.Model):
      id = db.Column(db.Integer, primary_key = True)
      isbn = db.Column(db.Integer, index = True, unique = True)
      title = db.Column(db.String(140), index = True, unique = False)
      author = db.Column(db.String(140), index = True, unique = False)
      genre = db.Column(db.String(50), index = True, unique = False)
      year_published = db.Column(db.Integer, index = True, unique = False)

      def __repr__(self):
            return "{} by {}".format(self.title, self.author)
    
#the Item model:  
class Item(db.Model):
      id = db.Column(db.Integer, primary_key = True)
      book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
      collection_id = db.Column(db.Integer, db.ForeignKey('collection.id'))

      def __repr__(self):
            return "{}".format(Book.query.get(self.book_id))
    
#create the Collection model 
class Collection(db.Model):
      id = db.Column(db.Integer, primary_key = True)
      items = db.relationship('Item', backref='collection', lazy='dynamic')

  