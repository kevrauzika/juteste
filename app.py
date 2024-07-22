from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

def load_products():
    try:
        with open('products.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_products(products):
    with open('products.json', 'w') as file:
        json.dump(products, file, indent=4)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        try:
            name = request.form['name']
            price = float(request.form['price'])
            products = load_products()
            products.append({"name": name, "price": price})
            save_products(products)
            return redirect(url_for('index'))
        except ValueError as e:
            return f"Erro: {str(e)}", 400
    return render_template('add_product.html')

@app.route('/calculate_price', methods=['GET', 'POST'])
def calculate_price():
    products = load_products()
    total_cost = 0
    selected_products = []
    if request.method == 'POST':
        for product in products:
            try:
                quantity_str = request.form.get(f'quantity_{product["name"]}', '0')
                quantity = float(quantity_str)
                if quantity > 0:
                    total_cost += product['price'] * quantity
                    selected_products.append({"name": product["name"], "quantity": quantity, "price": product['price']})
            except ValueError as e:
                return f"Erro: {str(e)}", 400

        try:
            hours_str = request.form['hours']
            hours = float(hours_str)
            total_cost += hours * 10
        except ValueError as e:
            return f"Erro: {str(e)}", 400

    return render_template('calculate_price.html', products=products, total_cost=total_cost, selected_products=selected_products)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
