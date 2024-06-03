from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FloatField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class ProductForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    image = StringField('Image URL')
    desc = TextAreaField('Description', validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Add Product')
