from app import app, db, User, Category, Asset
import random

with app.app_context():
    db.drop_all()
    db.create_all()

    # Plain-text passwords for testing
    admin_password = 'adminpass'
    user_password = 'userpass'

    # Admin users
    admin_users = [
        User(username='admin1', password=admin_password, role='admin'),
        User(username='admin2', password=admin_password, role='admin'),
        User(username='admin3', password=admin_password, role='admin'),
        User(username='admin4', password=admin_password, role='admin'),
        User(username='admin5', password=admin_password, role='admin'),
    ]

    # Regular users
    regular_users = [
        User(username='user1', password=user_password, role='regular'),
        User(username='user2', password=user_password, role='regular'),
        User(username='user3', password=user_password, role='regular'),
        User(username='user4', password=user_password, role='regular'),
        User(username='user5', password=user_password, role='regular'),
    ]

    users = admin_users + regular_users
    for u in users:
        db.session.add(u)

    # Categories
    category_names = [
        'Laptop', 'Desktop', 'Monitor', 'Printer', 'Router',
        'Switch', 'Projector', 'Server', 'Tablet', 'Phone'
    ]
    categories = []
    for name in category_names:
        cat = Category(name=name)
        db.session.add(cat)
        categories.append(cat)

    db.session.commit()

    # Assets
    asset_data = [
        ('Dell XPS 13', 'Laptop for mobile employees'),
        ('HP EliteDesk 800', 'High-performance desktop'),
        ('BenQ PD2700U', '27-inch 4K Monitor'),
        ('HP LaserJet Pro M404', 'Office printer'),
        ('Cisco RV340', 'Small business router'),
        ('Netgear GS308', '8-port gigabit switch'),
        ('Epson EX3280', 'Meeting room projector'),
        ('Dell PowerEdge T40', 'Entry-level server'),
        ('iPad Air', 'Used by sales team'),
        ('iPhone 13', 'Company mobile phone'),
    ]

    for i, (name, description) in enumerate(asset_data):
        asset = Asset(
            name=name,
            description=description,
            category_id=categories[i].id,
            assigned_to=random.choice(users).username
        )
        db.session.add(asset)

    db.session.commit()

    print("✅ Database seeded. Passwords stored as plain text for viewing.")
