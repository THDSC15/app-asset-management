# app.py
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import DataRequired, Length
from myforms import RegisterForm, LoginForm, AssetForm
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///it_assets.db'
csrf = CSRFProtect(app)
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Models
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)  # stores hashed passwords
    role = db.Column(db.String(10), nullable=False)  # 'admin' or 'regular'

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

class Asset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    assigned_to = db.Column(db.String(100))
    status = db.Column(db.String(50), default='Available')
    category = db.relationship('Category')


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

# Forms
# class RegisterForm(FlaskForm):
#     username = StringField('Username', validators=[DataRequired(), Length(min=3)])
#     password = PasswordField('Password', validators=[DataRequired()])
#     role = SelectField('Role', choices=[('admin', 'Admin'), ('regular', 'Regular')])

# class LoginForm(FlaskForm):
#     username = StringField('Username', validators=[DataRequired()])
#     password = PasswordField('Password', validators=[DataRequired()])

# Routes
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_pw = generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_pw, role=form.role.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Login successful.', 'success')
            return redirect(url_for('index'))

        flash('Invalid username or password.', 'danger')

    return render_template('login.html', form=form)


@app.route('/')
@login_required
def index():
    assets = Asset.query.all()
    return render_template('index.html', assets=assets)

@app.route('/asset/create', methods=['GET', 'POST'])
@login_required
def create_asset():
    if current_user.role not in ['admin', 'regular']:
        flash('You do not have permission.', 'danger')
        return redirect(url_for('index'))

    form = AssetForm()

    form.category_id.choices = [(c.id, c.name) for c in Category.query.all()]

    form.assigned_to.choices = [('', 'Unassigned')] + [
        (user.username, user.username) for user in User.query.all()
    ]

    if form.validate_on_submit():
        new_asset = Asset(
            name=form.name.data,
            description=form.description.data,
            category_id=form.category_id.data,
            assigned_to=form.assigned_to.data,
            status=form.status.data
        )

        db.session.add(new_asset)
        db.session.commit()

        flash('Asset created!', 'success')
        return redirect(url_for('index'))
    
    print(form.errors)

    return render_template('create_asset.html', form=form)


@app.route('/asset/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_asset(id):
    asset = Asset.query.get_or_404(id)

    if current_user.role not in ['admin', 'regular']:
        flash('You do not have permission.', 'danger')
        return redirect(url_for('index'))

    form = AssetForm(obj=asset)
    form.category_id.choices = [(c.id, c.name) for c in Category.query.all()]

    form.assigned_to.choices = [('', 'Unassigned')] + [
        (user.username, user.username) for user in User.query.all()
    ]
    
    # Pre-fill status dropdown (needed if not using obj=asset for this field)
    if request.method == 'GET':
        form.status.data = asset.status
        form.assigned_to.data = asset.assigned_to

    if form.validate_on_submit():
        asset.name = form.name.data
        asset.description = form.description.data
        asset.category_id = form.category_id.data
        asset.assigned_to = form.assigned_to.data
        asset.status = form.status.data

        db.session.commit()
        flash('Asset updated successfully!', 'success')
        return redirect(url_for('index'))

    return render_template('edit_asset.html', form=form)




@app.route('/asset/delete/<int:id>', methods=['POST'])
@login_required
def delete_asset(id):
    if current_user.role != 'admin':
        flash('Only admins can delete assets.', 'danger')
        return redirect(url_for('index'))

    asset = Asset.query.get_or_404(id)

    db.session.delete(asset)
    db.session.commit()

    flash('Asset deleted.', 'info')
    return redirect(url_for('index'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
