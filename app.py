from flask import Flask, request, render_template, redirect, url_for
from domain.models import db, Clients, Tests, Products, Shops
from domain.credentials import *
from views.clients import ClientsViewModel
from views.tests import TestsViewModel
from views.products import ProductsViewModel
from views.shops import ShopsViewModel
from views.dashboard import DashboardViewModel
from services.visualization import client_distribution_pie, product_shops_population_bar



from sqlalchemy import desc
import os

app = Flask(__name__)
app.secret_key = 'development key'

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL",
                                                  f"postgresql://{username}:{password}@{hostname}:{port}/{database}")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db.init_app(app)


@app.route("/")
def index():
    db.create_all()
    return render_template("layout.html")


@app.route("/clients")
def clients():
    all_clients = Clients.query.all()
    return render_template("clients/index.html", clients=all_clients)


@app.route("/clients/new", methods=["GET", "POST"])
def new_client():
    form = ClientsViewModel()

    if request.method == "POST":
        if not form.validate():
            return render_template("clients/create.html", form=form)
        else:
            client = form.domain()
            db.session.add(client)
            db.session.commit()
            return redirect(url_for("clients"))

    return render_template("clients/create.html", form=form)


@app.route("/clients/delete/<uuid>", methods=["POST"])
def delete_client(uuid):
    client = Clients.query.filter(Clients.client_id == uuid).first()
    if client:
        db.session.delete(client)
        db.session.commit()

    return redirect(url_for("clients"))


@app.route("/clients/<uuid>", methods=["GET", "POST"])
def update_client(uuid):
    client = Clients.query.filter(Clients.client_id == uuid).first()
    form = client.wtf()

    if request.method == "POST":
        if not form.validate():
            return render_template("clients/update.html", form=form)

        client.map_from(form)
        db.session.commit()
        return redirect(url_for("clients"))

    return render_template("clients/update.html", form=form)

@app.route("/tests")
def tests():
    all_tests = Tests.query.join(Clients).order_by(desc(Tests.CreatedOn)).all()
    return render_template("tests/index.html", tests=all_tests)


@app.route("/tests/new", methods=["GET", "POST"])
def new_test():
    form = TestsViewModel()
    form.Client.choices = [(str(client.client_id), client.Client_name) for client in Clients.query.all()]

    if request.method == "POST":
        if not form.validate():
            return render_template("tests/create.html", form=form)
        else:
            client = form.domain()
            db.session.add(client)
            db.session.commit()
            return redirect(url_for("tests"))

    return render_template("tests/create.html", form=form)


@app.route("/tests/delete/<uuid>", methods=["POST"])
def delete_test(uuid):
    test = Tests.query.filter(Tests.test_id == uuid).first()
    if test:
        db.session.delete(test)
        db.session.commit()

    return redirect(url_for("tests"))


@app.route("/tests/<uuid>", methods=["GET", "POST"])
def update_test(uuid):
    test = Tests.query.filter(Tests.test_id == uuid).first()
    form = test.wtf()
    form.Client.choices = [(str(client.client_id), client.Client_name) for client in Clients.query.all()]

    if request.method == "POST":
        if not form.validate():
            return render_template("tests/update.html", form=form)
        test.map_from(form)
        db.session.commit()
        return redirect(url_for("tests"))

    return render_template("tests/update.html", form=form)

@app.route("/products")
def products():
    all_products = Products.query.join(Tests).order_by(desc(Products.CreatedOn)).all()
    return render_template("products/index.html", products=all_products)


@app.route("/products/new", methods=["GET", "POST"])
def new_product():
    form = ProductsViewModel()
    form.Test.choices = [(str(test.test_id), test.Price) for test
                         in Tests.query.join(Clients, Tests.client_idIdFk == Clients.client_id).all()]

    if request.method == "POST":
        if not form.validate():
            return render_template("products/create.html", form=form)
        else:
            client = form.domain()
            db.session.add(client)
            db.session.commit()
            return redirect(url_for("products"))

    return render_template("products/create.html", form=form)


@app.route("/products/<uuid>", methods=["GET", "POST"])
def update_product(uuid):
    product = Products.query.filter(Products.product_id == uuid).first()
    form = product.wtf()
    form.Test.choices = [(str(test.test_id), test.Price) for test
                         in Tests.query.join(Clients, Tests.client_idIdFk == Clients.client_id).all()]

    if request.method == "POST":
        if not form.validate():
            return render_template("products/update.html", form=form)
        product.map_from(form)
        db.session.commit()
        return redirect(url_for("products"))

    return render_template("products/update.html", form=form)


@app.route("/products/delete/<uuid>", methods=["POST"])
def delete_product(uuid):
    product = Products.query.filter(Products.product_id == uuid).first()
    if product:
        db.session.delete(product)
        db.session.commit()

    return redirect(url_for("products"))

@app.route("/shops")
def shops():
    all_shops = Shops.query.join(Products).all()
    return render_template("shops/index.html", shops=all_shops)


@app.route("/shops/new", methods=["GET", "POST"])
def new_shop():
    form = ShopsViewModel()
    form.Product.choices = [(str(product.product_id), product.Product_name) for product
                           in Products.query.join(Tests, Products.test_idIdFk == Tests.test_id).all()]

    if request.method == "POST":
        if not form.validate():
            return render_template("shops/create.html", form=form)
        else:
            test = form.domain()
            db.session.add(test)
            db.session.commit()
            return redirect(url_for("shops"))

    return render_template("shops/create.html", form=form)


@app.route("/shops/<uuid>", methods=["GET", "POST"])
def update_shop(uuid):
    shop = Shops.query.filter(Shops.shop_id == uuid).first()
    form = shop.wtf()
    form.Product.choices = [(str(product.product_id), product.Product_name) for product
                           in Products.query.join(Tests, Products.test_idIdFk == Tests.test_id).all()]

    if request.method == "POST":
        if not form.validate():
            return render_template("shops/update.html", form=form)
        shop.map_from(form)
        db.session.commit()
        return redirect(url_for("shops"))

    return render_template("shops/update.html", form=form)


@app.route("/shops/delete/<uuid>", methods=["POST"])
def delete_shop(uuid):
    shop = Shops.query.filter(Shops.shop_id == uuid).first()
    if shop:
        db.session.delete(shop)
        db.session.commit()

    return redirect(url_for("shops"))

@app.route("/dashboard")
def dashboard():
    all_clients = db.session.query(Clients.client_id, Clients.Client_name).all()
    distinct_products = db.session.query(Products.Product_name).distinct().all()
    dashboardViewModel = DashboardViewModel()
    if len(all_clients):
        dashboardViewModel.Clients = [(str(client.client_id), client.Client_name) for client in all_clients]
        dashboardViewModel.Clients_distribution_data = client_distribution_pie(all_clients[0][0])

    if len(distinct_products):
        dashboardViewModel.Products = distinct_products
        dashboardViewModel.Products_shops_population_data = product_shops_population_bar(
            distinct_products[0][0])

    return render_template("dashboard/index.html", model=dashboardViewModel)


@app.route("/client_distribution/<uuid>")
def client_distribution(uuid):
    return client_distribution_pie(uuid)


@app.route("/product_shops_population/<name>")
def product_shops_population(name):
    return product_shops_population_bar(name)



if __name__ == "__main__":
    app.run(debug=True)



