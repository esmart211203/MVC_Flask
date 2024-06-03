from flask import Blueprint, render_template, redirect, url_for, request, flash
from models import db, Order
from datetime import datetime
from flask import session
order_bp = Blueprint('order_bp', __name__)


@order_bp.route('/management_order')
def management_order():
    orders = Order.query.all()
    return render_template('order/management_order.html', orders=orders)

@order_bp.route('/checkout', methods=['POST'])
def checkout():
    if request.method == 'POST':
        receiver_name = request.form['receiver_name']
        phone_number = request.form['phone_number']
        address = request.form['address']
        total_amount = request.form['total_amount']
        if not receiver_name or not phone_number or not address:
            flash('Please fill out all required fields.', 'error')
            return redirect(url_for('order_bp.checkout'))
        new_order = Order.create_order(receiver_name=receiver_name, phone_number=phone_number, address=address, total_amount=total_amount)
        db.session.add(new_order)
        db.session.commit()
        if 'cart' in session:
            session.pop('cart')

        flash('Order placed successfully!', 'success')
    return redirect(url_for('home'))

@order_bp.route('/delete/<int:order_id>', methods=['POST'])
def delete_order(order_id):
    if request.method == 'GET': 
        if Order.delete_order(order_id):
            flash('Order deleted successfully!', 'success')
        else:
            flash('Failed to delete order. Order not found.', 'error')
    return redirect(url_for('home'))
