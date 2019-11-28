from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
from datetime import datetime
from views.clients import ClientsViewModel
from views.tests import TestsViewModel
from views.products import ProductsViewModel
from views.shops import ShopsViewModel

db = SQLAlchemy()

class Clients(db.Model):
	__tablename__ = 'clients'

	client_id = db.Column("client_id", db.Integer, primary_key=True)
	Client_name = db.Column("client_name", db.String)
	Age = db.Column("age", db.Integer)
	Money = db.Column("money", db.Integer)
	Contact = db.Column("contact", db.Integer)
	CreatedOn = db.Column("created", db.TIMESTAMP, default=datetime.now)

	def wtf(self):
		return ClientsViewModel(
			Client_name=self.Client_name,
			Age=self.Age,
			Money=self.Money,
			Contact=self.Contact,
			CreatedOn=self.CreatedOn
		)

	def map_from(self, form):
		self.Client_name = form.Client_name.data,
		self.Age = form.Age.data,
		self.Money = form.Money.data,
		self.Contact = form.Contact.data

class Tests(db.Model):
	__tablename__ = 'tests'

	test_id = db.Column("test_id", db.Integer, primary_key=True)
	Price = db.Column("price", db.Integer, nullable=False)
	Productor = db.Column("productor", db.String, nullable=False)
	CreatedOn = db.Column("created", db.TIMESTAMP, default=datetime.now)

	client_idIdFk = db.Column("client_ididfk", db.Integer, db.ForeignKey("clients.client_id"))
	Client = db.relationship("Clients", backref=backref('Tests', cascade='all,delete'), passive_deletes=True)

	def wtf(self):
		return TestsViewModel(
			Price=self.Price,
			Productor=self.Productor,
			CreatedOn=self.CreatedOn,
			Client=self.client_idIdFk
		)

	def map_from(self, form):
		self.Price = form.Price.data,
		self.Productor = form.Productor.data,
		self.client_idIdFk = form.Client.data

class Products(db.Model):
	__tablename__ = 'products'

	product_id = db.Column("product_id", db.Integer, primary_key=True)
	Product_name = db.Column("product_name", db.String, nullable=False)
	Product_price = db.Column("product_price", db.Integer, nullable=False)
	CreatedOn = db.Column("created", db.TIMESTAMP, default=datetime.now)

	test_idIdFk = db.Column("test_ididfk", db.Integer, db.ForeignKey("tests.test_id"))
	Test = db.relationship("Tests", backref=backref('Products', cascade='all,delete'), passive_deletes=True)

	def wtf(self):
		return ProductsViewModel(
			Product_name=self.Product_name,
			Product_price=self.Product_price,
			CreatedOn=self.CreatedOn,
			Test=self.test_idIdFk
		)

	def map_from(self, form):
		self.Product_name = form.Product_name.data,
		self.Product_price = form.Product_price.data,
		self.test_idIdFk = form.Test.data
		
class Shops(db.Model):
	__tablename__ = "shops"

	shop_id = db.Column("shop_id", db.Integer, primary_key=True)
	Shop_name = db.Column("shop_name", db.String, nullable=False)
	Locale = db.Column("locale", db.String, nullable=False)
	Shop_contact = db.Column("shop_contact", db.Integer, nullable=False)
	CreatedOn = db.Column("created", db.TIMESTAMP, default=datetime.now)

	product_idIdFk = db.Column("product_ididfk", db.Integer, db.ForeignKey("products.product_id"))
	Product = db.relationship("Products", backref=backref('Shops', cascade='all,delete'), passive_deletes=True)

	def wtf(self):
		return ShopsViewModel(
			Shop_name=self.Shop_name,
			Locale=self.Locale,
			Shop_contact=self.Shop_contact,
			CreatedOn=self.CreatedOn,
			Product=self.product_idIdFk
		)

	def map_from(self, form):
		self.Shop_name = form.Shop_name.data,
		self.Locale = form.Locale.data,
		self.Shop_contact = form.Shop_contact.data,
		self.product_idIdFk = form.Product.data
