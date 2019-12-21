from wtforms import StringField, DateTimeField, IntegerField, SubmitField, validators, SelectField
from flask_wtf import FlaskForm
from domain import models
from wtforms.validators import DataRequired, Length, Email, NumberRange


class ProductsViewModel(FlaskForm):
    Product_name = StringField("Product_name: ", [validators.DataRequired("Please enter Product name.")])
    Product_price = IntegerField("Product_price: ", [validators.NumberRange(min=1),validators.DataRequired("Price can not be < 0.")])
    Test = SelectField("Test", validators=[validators.DataRequired()])
    CreatedOn = DateTimeField("Created On")

    Submit = SubmitField("Save")

    def domain(self):
        return models.Products(
            Product_name=self.Product_name.data,
            Product_price=self.Product_price.data,
            CreatedOn=self.CreatedOn.data,
            test_idIdFk=self.Test.data
        )
