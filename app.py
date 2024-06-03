import os
from flask import Flask, render_template,url_for
from models import db, Product, User
from controllers.product_controller import product_bp
from controllers.user_controller import user_bp
from controllers.order_controller import order_bp
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['UPLOAD_FOLDER'] = os.path.join(app.static_folder, 'uploads')

db.init_app(app)

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


# Function to create tables
def create_tables():
    with app.app_context():
        db.create_all()

        if not User.query.first():
            # Tạo một người dùng mặc định
            default_user = User(username='admin', email='admin@gmail.com', password='admin')
            db.session.add(default_user)
            db.session.commit()


@app.route('/')
def home():
    title = "Home"
    products = Product.query.all()
    return render_template('home.html', title=title, products=products)

app.register_blueprint(product_bp)
app.register_blueprint(user_bp)
app.register_blueprint(order_bp)
if __name__ == '__main__':
    create_tables()
    app.run(debug=True)
