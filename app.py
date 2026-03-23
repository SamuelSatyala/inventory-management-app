from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# ---------------- MODEL ----------------
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)


# Create DB
with app.app_context():
    db.create_all()


# ---------------- HOME / SEARCH ----------------
@app.route('/')
def index():
    query = request.args.get('q')

    if query:
        products = Product.query.filter(
            Product.name.ilike(f'%{query}%')
        ).all()
    else:
        products = Product.query.all()

    return render_template('index.html', products=products)


# ---------------- ADD ----------------
@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    quantity = request.form['quantity']
    price = request.form['price']

    if not name or int(quantity) < 0 or float(price) < 0:
        return "Invalid input"

    new_product = Product(
        name=name,
        quantity=quantity,
        price=price
    )

    db.session.add(new_product)
    db.session.commit()

    return redirect('/')


# ---------------- DELETE ----------------
@app.route('/delete/<int:id>')
def delete(id):
    product = Product.query.get(id)
    db.session.delete(product)
    db.session.commit()
    return redirect('/')


# ---------------- EDIT PAGE ----------------
@app.route('/edit/<int:id>')
def edit(id):
    product = Product.query.get(id)
    return render_template('edit.html', product=product)


# ---------------- UPDATE ----------------
@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    product = Product.query.get(id)

    product.name = request.form['name']
    product.quantity = request.form['quantity']
    product.price = request.form['price']

    db.session.commit()

    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)