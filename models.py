from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(200), nullable=True)
    desc = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    def format_price(self):
        return '{:,.0f} VND'.format(self.price)
    
    def search_products(query):
        search_pattern = f"%{query}%"
        return Product.query.filter(Product.name.ilike(search_pattern)).all()
    @classmethod
    def create_product(cls, name, image, desc, price):
        """
        Create a new product.
        """
        new_product = cls(name=name, image=image, desc=desc, price=price)
        db.session.add(new_product)
        db.session.commit()
        return new_product

    def edit_product(self, name, image, desc, price):
        """
        Edit an existing product.
        """
        self.name = name
        self.image = image
        self.desc = desc
        self.price = price
        db.session.commit()

    @classmethod
    def delete_product(cls, product_id):
        """
        Delete a product by its ID.
        """
        product = cls.query.get(product_id)
        if product:
            db.session.delete(product)
            db.session.commit()
            return True
        return False

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    receiver_name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    total_amount = db.Column(db.Integer)
    order_date = db.Column(db.DateTime, nullable=False, default=datetime.now)

    @classmethod
    def create_order(cls, receiver_name, phone_number, address, total_amount):
        """
        Create a new order.
        """
        new_order = cls(receiver_name=receiver_name, phone_number=phone_number, address=address, total_amount=total_amount)
        db.session.add(new_order)
        db.session.commit()
        return new_order
    
    @classmethod
    def delete_order(cls, order_id):
        """
        Delete an order by its ID.
        """
        order = cls.query.get(order_id)
        if order:
            db.session.delete(order)
            db.session.commit()
            return True
        return False
