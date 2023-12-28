from flask import request, jsonify, abort
from app import app, db
from models import Product, Supplier


# POST: Yeni ürün oluşturma
@app.route('/products', methods=['POST'])
def add_product():
    data = request.get_json()
    name = data.get('name')
    price = data.get('price')
    supplier_id = data.get('supplier_id')
    if not all([name, price, supplier_id]):
        return jsonify({'error': 'Missing data'}), 400
    new_product = Product(name=name, price=price, supplier_id=supplier_id)
    db.session.add(new_product)
    db.session.commit()
    return jsonify(new_product.to_dict()), 201

# GET: Tüm ürünleri listeleme
@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    product_list = [product.to_dict() for product in products]
    return jsonify(product_list), 200

# GET: Belirli bir ürünün detaylarını görüntüleme
@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    # product = Product.query.filter_by(id=product_id).first()
    return jsonify(product.to_dict()), 200

# PUT/PATCH: Mevcut bir ürünü güncelleme
@app.route('/products/<int:product_id>', methods=['PUT', 'PATCH'])
def update_product(product_id):
    product = Product.query.get_or_404(product_id)
    data = request.get_json()
    product.name = data.get('name', product.name)
    product.price = data.get('price', product.price)
    product.supplier_id = data.get('supplier_id', product.supplier_id)
    db.session.commit()
    return jsonify(product.to_dict()), 200

# DELETE: Ürün silme
@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product deleted'}), 200


# POST: Yeni tedarikçi oluşturma
@app.route('/suppliers', methods=['POST'])
def add_supplier():
    data = request.get_json()  # JSON data al
    name = data.get('name')
    if not name:
        return jsonify({'error': 'Name is required'}), 400
    new_supplier = Supplier(name=name)
    db.session.add(new_supplier)
    db.session.commit()
    return jsonify({'id': new_supplier.id, 'name': new_supplier.name}), 201 # 201: Created

# GET: Tüm tedarikçileri listeleme
@app.route('/suppliers', methods=['GET'])
def get_suppliers():
    suppliers = Supplier.query.all()
    supplier_list = [supplier.to_dict() for supplier in suppliers]
    return jsonify(supplier_list), 200

# Model için instance metodu
def to_dict(self):
    return {
        'id': self.id,
        'name': self.name,
        'price': self.price,
        'supplier_id': self.supplier_id
    }

# to_dict metodunu Product modeline method olarak ekliyorum.
Product.to_dict = to_dict


def supplier_to_dict(self):
    return {
        'id': self.id,
        'name': self.name
    }

Supplier.to_dict = supplier_to_dict
