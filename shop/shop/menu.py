from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'  # SQLite database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database models
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(200), nullable=False)

# Create the database and add  products
with app.app_context():
    db.create_all()
    if not Product.query.first():  # Only add products if they don't already exist
        db.session.add(Product(name='Latte', price=25, image='static/images/imgg1.jpg'))
        db.session.add(Product(name='Chocolate Mocha', price=25, image='static/images/imgg2.jpg'))
        db.session.add(Product(name='Boba', price=25, image='static/images/imgg3.jpg'))
        db.session.add(Product(name='Espresso', price=25, image='static/images/imgg4.jpg'))
        db.session.add(Product(name='Cinnamon Coffee', price=25, image='static/images/imgg5.jpg'))
        db.session.add(Product(name='Iced Latte', price=25, image='static/images/imgg6.jpg'))
        db.session.commit()

@app.route('/')
def index():
    products = Product.query.all()  # Get all products from the database
    return render_template('index.html', products=products)

@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    if 'cart' not in session:
        session['cart'] = {}
    cart = session['cart']
    
    # Check if the product exists in the database
    product = Product.query.get(product_id)
    if product:
        # Check if the product is already in the cart
        if str(product_id) in cart:
            cart[str(product_id)] += 1  # Increase quantity if item exists
        else:
            cart[str(product_id)] = 1  # Add product to cart
        session.modified = True
    else:
        # Optionally, you can handle the case when the product doesn't exist
        print(f"Product with ID {product_id} does not exist.")

    return redirect(url_for('cart'))

@app.route('/cart', methods=['GET', 'POST'])
def cart():
    if request.method == 'POST':
        product_id = request.form.get('product_id')
        
        try:
            quantity = int(request.form.get('quantity', 1))
        except ValueError:
            quantity = 1  # Default to 1 if the quantity is invalid

        if 'cart' not in session:
            session['cart'] = {}

        cart = session['cart']

        if quantity <= 0:
            cart.pop(str(product_id), None)  # Remove the product if quantity is 0 or less
        else:
            cart[str(product_id)] = quantity  # Update the quantity

        session.modified = True

    cart = session.get('cart', {})
    cart_items = []
    total_price = 0

    for product_id, quantity in cart.items():
        try:
            product = Product.query.get(int(product_id))  # Convert product_id to int here
            if product:
                cart_items.append({'product': product, 'quantity': quantity})
                total_price += product.price * quantity
        except (ValueError, TypeError):
            print(f"Invalid product ID: {product_id}")  # Handle invalid product IDs

    return render_template('cart.html', cart_items=cart_items, total_price=total_price)

@app.route('/remove_from_cart/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    cart = session.get('cart', {})
    cart.pop(str(product_id), None)  # Remove the product from cart
    session.modified = True
    return redirect(url_for('cart'))

if __name__ == '__main__':
    app.run(debug=True)



