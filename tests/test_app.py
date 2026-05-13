import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app
from app import db, User, Category, Asset
from werkzeug.security import generate_password_hash

app.config['TESTING'] = True
app.config['WTF_CSRF_ENABLED'] = False


def test_home_redirect():
    tester = app.test_client()

    response = tester.get('/', follow_redirects=True)

    assert response.status_code == 200

def test_invalid_login_rejected():
    tester = app.test_client()

    response = tester.post('/login', data={
        'username': 'fakeuser',
        'password': 'wrongpassword'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Invalid username or password' in response.data

def test_regular_user_cannot_delete_asset():

    with app.app_context():

        # Create test category
        category = Category(name='Test Category')
        db.session.add(category)
        db.session.commit()

        # Create regular user
        user = User(
            username='regularuser',
            password=generate_password_hash('password123'),
            role='regular'
        )

        db.session.add(user)
        db.session.commit()

        # Create asset
        asset = Asset(
            name='Test Asset',
            description='Testing',
            category_id=category.id,
            assigned_to='regularuser',
            status='Available'
        )

        db.session.add(asset)
        db.session.commit()

        asset_id = asset.id

    tester = app.test_client()

    # Login as regular user
    tester.post('/login', data={
        'username': 'regularuser',
        'password': 'password123'
    }, follow_redirects=True)

    # Attempt delete
    response = tester.post(f'/asset/delete/{asset_id}', follow_redirects=True)

    assert b'Only admins can delete assets' in response.data