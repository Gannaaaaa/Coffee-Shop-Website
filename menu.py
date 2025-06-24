from flask import Blueprint, render_template, request, redirect, url_for, session
from extensions import db

menu_bp = Blueprint("menu", __name__, static_folder="static", template_folder="templates")

# Database models
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<Product {self.name}>'


# Routes
@menu_bp.route('/index', methods=['GET', 'POST'])
def index():
    products = Product.query.all()  # Get all products from the database
    return render_template('menu.html', products=products)

@menu_bp.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    product = Product.query.get(product_id)
    
    if not product:
        print(f"Product with ID {product_id} does not exist.")
        return redirect(url_for('menu.index'))  # Redirect to menu if product not found

    # Initialize the cart if not present
    if 'cart' not in session:
        session['cart'] = {}

    cart = session['cart']
    
    # Add or update product quantity in cart
    if str(product_id) in cart:
        cart[str(product_id)] += 1  # Increase quantity if already in the cart
    else:
        cart[str(product_id)] = 1  # Add the product to the cart with quantity 1

    session.modified = True
    print(f"Current cart contents: {session.get('cart')}")
    
    return redirect(url_for('menu.cart'))





@menu_bp.route('/cart', methods=['GET', 'POST'])
def cart():
    if request.method == 'POST':
        product_id = request.form.get('product_id')
        try:
            quantity = int(request.form.get('quantity', 1))
        except ValueError:
            quantity = 1  # Default to 1 if quantity is invalid

        cart = session.get('cart', {})
        if quantity <= 0:
            cart.pop(str(product_id), None)  # Remove the product if quantity is 0 or less
        else:
            cart[str(product_id)] = quantity  # Update the quantity
        session.modified = True  # Mark session as modified

    cart = session.get('cart', {})
    print("Current cart contents:", cart)  # Debug print
    cart_items = []
    total_price = 0

    for product_id, quantity in cart.items():
        try:
            product = Product.query.get(int(product_id))  # Convert product_id to int here
            if product:
                cart_items.append({'product': product, 'quantity': quantity})
                total_price += product.price * quantity
        except (ValueError, TypeError):
            print(f"Invalid product ID: {product_id}")

    return render_template('cart.html', cart_items=cart_items, total_price=total_price)


@menu_bp.route('/remove_from_cart/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    cart = session.get('cart', {})
    if str(product_id) in cart:
        cart.pop(str(product_id), None)  # Remove the product from cart
        session.modified = True  # Mark session as modified
    print("Cart after removal:", cart)  # Debug print
    return redirect(url_for('menu.cart'))  # Redirect to cart page


