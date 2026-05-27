from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Optional

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3)])
    password = PasswordField('Password', validators=[DataRequired()])
    role = SelectField('Role', choices=[('admin', 'Admin'), ('regular', 'Regular')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

    
class AssetForm(FlaskForm):
    name = StringField('Asset Name', validators=[
        DataRequired(),
        Length(min=2, max=100)
    ])

    description = StringField('Description', validators=[
        Optional(),
        Length(max=200, message='Description must not exceed 200 characters.'),
    ])

    category_id = SelectField('Category', coerce=int, validators=[
        DataRequired()
    ])

    assigned_to = SelectField('Assigned To', validators=[
        Optional()
    ])

    status = SelectField('Status', choices=[
        ('Available', 'Available'),
        ('In Use', 'In Use'),
        ('Maintenance', 'Maintenance'),
        ('Retired', 'Retired')
    ], validators=[
        DataRequired()
    ])

    submit = SubmitField('Save')

