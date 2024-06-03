import os
from flask import Blueprint, render_template, request, redirect, url_for, current_app
from werkzeug.utils import secure_filename
from models import db, Product, User
from flask import flash


product_bp = Blueprint('product_bp', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@product_bp.route('/management_product', methods=['GET', 'POST'])
def management_product():
    title = "Product Management"
    products = Product.query.all()
    users = User.query.all()
    return render_template('product/management_product.html', title=title, products=products, users=users)

@product_bp.route('/add_product', methods=['POST'])
def add_product():
    name = request.form['name']
    image = request.files['image']
    desc = request.form['desc']
    price = request.form['price']

    if image and allowed_file(image.filename):
        filename = secure_filename(image.filename)
        # Save the filename only
        image_path = filename
        # Move the file to the uploads folder
        image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
    else:
        image_path = None

    new_product = Product.create_product(name=name, image=image_path, desc=desc, price=price)

    return redirect(url_for('product_bp.management_product'))



@product_bp.route('/delete_product/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    if Product.delete_product(product_id):
        return redirect(url_for('product_bp.management_product'))
    else:
        flash("Product not found", "error")
        return redirect(url_for('product_bp.management_product'))

@product_bp.route('/edit_product/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    current_image = product.image
    if request.method == 'POST':
        name = request.form['name']
        desc = request.form['desc']
        price = request.form['price']

        if 'image' in request.files:
            image = request.files['image']
            if image and allowed_file(image.filename):
                filename = secure_filename(image.filename)
                image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                image.save(image_path)
                product.image = filename
            else:
                product.image = current_image

        product.name = name
        product.desc = desc
        product.price = price
        db.session.commit()
        return redirect(url_for('product_bp.management_product'))

    return render_template('product/edit_product.html', product=product)


@product_bp.route('/search')
def searc_product():
    keyword = request.args.get('keyword', '')
    products = Product.search_products(keyword)
    return render_template('search.html', products=products)