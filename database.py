import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json
from datetime import datetime
from flask_migrate import Migrate

from dataclasses import dataclass
import os

from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash





database_name = "magazzino19"

database_path = 'postgres://zohgdhzmyigqbu:02b85783284bff4eb876aaf8bd173026386b08c3a9bd75e106786cff8e42bd7c@ec2-54-205-232-84.compute-1.amazonaws.com:5432/d1ubrhld30748t'

db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()




class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(12), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    user_stock = db.relationship('StockItems', backref='user', lazy='select')
    user_product_codes = db.relationship('ProductCodes', backref='user', lazy='select')
    sales_data = db.relationship('Sales', backref='user', lazy='select')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def __repr__(self):
        return '<User {}>'.format(self.username)




class StockItems(db.Model):
    __tablename__ = 'stock_items'

    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String)
    quantity = db.Column(db.Integer)
    expiration_date = db.Column(db.Date, nullable=False)
    product_code = db.Column(db.Integer, db.ForeignKey('product_codes.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


    def __init__(self, product_name, quantity, expiration_date, product_code, user_id):
        self.product_name = product_name
        self.quantity = quantity
        self.expiration_date = expiration_date

        self.product_code = product_code
        self.user_id = user_id

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()



class ProductCodes(db.Model):
    __tablename__ = 'product_codes'

    id = db.Column(db.Integer, primary_key=True)
    product_code = db.Column(db.String)
    description = db.Column(db.String)
    unit = db.Column(db.String)
    stock_items = db.relationship('StockItems', backref='product_codes', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, product_code, description, unit, user_id):
        self.product_code = product_code
        self.description = description
        self.unit = unit
        self.user_id = user_id


    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()





class Sales(db.Model):
    __tablename__ = 'sales'

    id = db.Column(db.Integer, primary_key=True)
    sold_product = db.Column(db.String)
    sale_date = db.Column(db.Date)
    sold_quantity = db.Column(db.Integer)
    restock_quantity = db.Column(db.Integer)

    product_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


    def __init__(self, sold_product, sale_date, sold_quantity, restock_quantity, product_id, user_id):
        self.sold_product = sold_product
        self.sale_date = sale_date
        self.sold_quantity = sold_quantity
        self.restock_quantity = restock_quantity
        self.user_id = user_id
        self.product_id = product_id


    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()







