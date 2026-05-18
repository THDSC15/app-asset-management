import sys
import os
import uuid

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app
from app import db, User, Category, Asset
from werkzeug.security import generate_password_hash

app.config['TESTING'] = True
app.config['WTF_CSRF_ENABLED'] = False

def test_home_redirect():
    client = app.test_client()

    response = client.get('/', follow_redirects=True)

    assert response.status_code == 200

def test_invalid_login_rejected():
    client = app.test_client()

    response = client.post('/login', data={
        'username': 'fakeuser',
        'password': 'wrongpassword'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Invalid username or password' in response.data

def test_regular_user_cannot_delete_asset():
    client = app.test_client()

    with app.app_context():

        # Create test category
        category = Category(name='Test Category')
        db.session.add(category)
        db.session.commit()

        # Create unique username
        username = f"regularuser_{uuid.uuid4().hex[:8]}"

        # Create regular user
        user = User(
            username=username,
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
            assigned_to=username,
            status='Available'
        )

        db.session.add(asset)
        db.session.commit()

        asset_id = asset.id


    # Login as regular user
    client.post('/login', data={
        'username': username,
        'password': 'password123'
    }, follow_redirects=True)

    # Attempt delete
    response = client.post(f'/asset/delete/{asset_id}', follow_redirects=True)

    assert b'Only admins can delete assets' in response.data


def test_admin_user_can_delete_asset():
    client = app.test_client()

    with app.app_context():

        category = Category(name='Admin Test Category')
        db.session.add(category)
        db.session.commit()

        username = f"adminuser_{uuid.uuid4().hex[:8]}"

        admin = User(
            username=username,
            password=generate_password_hash('password123'),
            role='admin'
        )

        db.session.add(admin)
        db.session.commit()

        asset = Asset(
            name='Admin Delete Test Asset',
            description='Testing admin delete',
            category_id=category.id,
            assigned_to=username,
            status='Available'
        )

        db.session.add(asset)
        db.session.commit()

        asset_id = asset.id


    client.post('/login', data={
        'username': username,
        'password': 'password123'
    }, follow_redirects=True)

    response = client.post(f'/asset/delete/{asset_id}', follow_redirects=True)

    assert response.status_code == 200
    assert b'Asset deleted' in response.data

    with app.app_context():
        deleted_asset = db.session.get(Asset, asset_id)
        assert deleted_asset is None

def test_asset_name_validation_rejects_short_name():
    client = app.test_client()

    with app.app_context():

        category = Category(name='Validation Test Category')
        db.session.add(category)
        db.session.commit()

        username = f"validationuser_{uuid.uuid4().hex[:8]}"

        user = User(
            username=username,
            password=generate_password_hash('password123'),
            role='regular'
        )

        db.session.add(user)
        db.session.commit()

        category_id = category.id


    client.post('/login', data={
        'username': username,
        'password': 'password123'
    }, follow_redirects=True)

    response = client.post('/asset/create', data={
        'name': 'A',
        'description': 'Valid description',
        'category_id': category_id,
        'assigned_to': username,
        'status': 'Available'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Field must be between 2 and 100 characters long' in response.data