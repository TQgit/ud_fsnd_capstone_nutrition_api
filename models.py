import os
from flask_sqlalchemy import SQLAlchemy

database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


class Restaurant(db.Model):
    __tablename__ = 'restaurants'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    cuisine = db.Column(db.String(25), nullable=False)
    orders = db.relationship('Order', backref='restaurant',
                             cascade='all, delete-orphan', lazy=True)

    def __init__(self, name, cuisine):
        self.name = name
        self.cuisine = cuisine

    def insert(self):
        db.session.add(self)
        db.session.commit()
        db.session.close()

    def update(self):
        db.session.commit()
        db.session.close()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        db.session.close()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'cuisine': self.cuisine
        }


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'),
                              nullable=False)
    name = db.Column(db.String(100), nullable=False)
    calories = db.Column(db.Integer, nullable=False)
    total_fat = db.Column(db.Integer, nullable=False)
    cholesterol = db.Column(db.Integer, nullable=False)
    sodium = db.Column(db.Integer, nullable=False)
    total_carbs = db.Column(db.Integer, nullable=False)
    protein = db.Column(db.Integer, nullable=False)

    def __init__(self, restaurant_id, name, calories, total_fat, cholesterol,
                 sodium, total_carbs, protein):
        self.restaurant_id = restaurant_id
        self.name = name
        self.calories = calories
        self.total_fat = total_fat
        self.cholesterol = cholesterol
        self.sodium = sodium
        self.total_carbs = total_carbs
        self.protein = protein

    def insert(self):
        db.session.add(self)
        db.session.commit()
        db.session.close()

    def update(self):
        db.session.commit()
        db.session.close()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        db.session.close()

    def format(self):
        return {
            'id': self.id,
            'restaurant_id': self.restaurant_id,
            'name': self.name,
            'calories': self.calories,
            'total_fat': self.total_fat,
            'cholesterol': self.cholesterol,
            'sodium': self.sodium,
            'total_carbs': self.total_carbs,
            'protein': self.protein
        }
