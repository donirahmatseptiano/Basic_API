from flask import Flask, json, request, flash, url_for, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy


DB_URI = "postgresql+psycopg2://username:password@hostname:port/db_name"
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

class Users(db.Model):
   __table_args__ = {"schema": "public"}
   id = db.Column('user_id', db.Integer, primary_key = True)
   first_name = db.Column(db.String(30))
   last_name = db.Column(db.String(30))
   address = db.Column(db.String())
   phone = db.Column(db.String(14))
   email = db.Column(db.String(50))

   
class Product(db.Model):
   __table_args__ = {"schema": "public"}
   productID = db.Column(db.Integer, primary_key = True)
   productName = db.Column(db.String(100))
   productPrice = db.Column(db.Integer)   

class Order(db.Model):
   __table_args__ = {"schema": "public"}
   orderID = db.Column(db.Integer, primary_key = True)
   orderDate = db.Column(db.Date)   
   orderTotal = db.Column(db.Integer)


@app.route('/user', methods=['GET', 'POST'])
def user():

   if request.method == 'GET':
      users = Users.query.all()
      results = [{"id": u.id, "first_name": u.first_name, 
                  "last_name": u.last_name, "address": u.address, 
                  "phone": u.phone, "email": u.email} for u in users]
      return jsonify(results)
   
   elif request.method == 'POST':
      user = Users(
         first_name=request.form['first_name'],
         last_name=request.form['last_name'],
         address=request.form['address'],
         phone=request.form['phone'],
         email=request.form['email']
      )
      db.session.add(user)
      db.session.commit()
      return jsonify({'status': 'ok'})
   
   else:
      return 'Method not allowed'

@app.route('/product', methods=['GET', 'POST'])
def product():

   if request.method == 'GET':
      product = Product.query.all()
      results = [{"id": p.productID, "product_name": p.productName, 
                  "price": p.productPrice} for p in product]

      return jsonify(results)
   
   elif request.method == 'POST':
      product = Product(         
         productName=request.form['product_name'],
         productPrice=request.form['price']
      )
      db.session.add(product)
      db.session.commit()
      return jsonify({'status': 'ok'})
   
   else:
      return 'Method not allowed'

@app.route('/order', methods=['GET', 'POST'])
def order():

   if request.method == 'GET':
      order = Order.query.all()
      results = [{"id": o.orderID, "date": o.orderDate, 
                  "total": o.orderTotal} for o in order]

      return jsonify(results)
   
   elif request.method == 'POST':
      order = Order(         
         orderDate=request.form['date'],
         orderTotal=request.form['total']
      )
      db.session.add(order)
      db.session.commit()
      return jsonify({'status': 'ok'})
   
   else:
      return 'Method not allowed'
   
@app.route("/user/<id>", methods=['GET'])
def user_by_id(id):
   users = Users.query.filter_by(id=id)
   results = [{"id": u.id, "first_name": u.first_name, 
               "last_name": u.last_name, "address": u.address, 
               "phone": u.phone, "email": u.email} for u in users]
   return jsonify(results)

@app.route("/product/<id>", methods=['GET'])
def product_by_id(id):
   product = Product.query.filter_by(productID=id)
   results = [{"id": p.productID, "product_name": p.productName, 
               "price": p.productPrice} for p in product]
   return jsonify(results)

@app.route("/order/<id>", methods=['GET'])
def order_by_id(id):
   order = Order.query.filter_by(orderID=id)
   results = [{"id": o.orderID, "date": o.orderDate, 
               "total": o.orderTotal} for o in order]
   return jsonify(results)

if __name__ == '__main__':
   app.run(debug = True)
db.create_all()
