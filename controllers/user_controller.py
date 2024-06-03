from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import db, User, Product

user_bp = Blueprint('user_bp', __name__)
def format_currency(amount):
    return "{:,.0f} VND".format(amount).replace(',', '.')


@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['user_id'] = user.id
            flash('Login successful', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password', 'error')
    return render_template('auth/login.html')

@user_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Logout successful', 'success')
    return redirect(url_for('home'))


@user_bp.route('/cart', methods=['GET'])
def cart():
    cart_items = []
    product_details = []
    total_amount = 0
    if 'cart' in session:
        cart_items = session['cart']
        product_details = Product.query.filter(Product.id.in_(cart_items)).all()
        for product in product_details:
            total_amount += product.price
    total_amout_value = total_amount
    total_amount = format_currency(total_amount)
    return render_template('cart.html', products=product_details, cart_items=cart_items, total_amount=total_amount,total_amout_value=total_amout_value)

@user_bp.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    if 'cart' not in session:
        session['cart'] = []
    session['cart'].append(product_id)
    session.modified = True
    return redirect(url_for('user_bp.cart'))


@user_bp.route('/remove_from_cart/<int:product_id>')
def remove_from_cart(product_id):
    if 'cart' in session:
        try:
            session['cart'].remove(product_id)
            session.modified = True
        except ValueError:
            pass 
    return redirect(url_for('user_bp.cart'))