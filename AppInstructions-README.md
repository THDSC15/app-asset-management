# IT Asset Management Web Application

This is a Flask-based web application for managing IT assets such as laptops, monitors, and printers. It supports user authentication, role-based access control, and CRUD functionality for managing assets.

## 1. Features

- Admin and regular user roles
- User registration and login
- Create, read, update, delete (CRUD) operations for assets (admin only)
- Read and update for regular users
- Asset status tracking (Available, In Use, Maintenance, Retired)
- Relational SQLite database with tables: User, Category, Asset
- Form validation and user feedback

## 2. Setup Instructions (Local)

### Requirements

- Python 3.11+
- Flask
- Flask-SQLAlchemy
- Flask-WTF
- Flask-Login
- Werkzeug

### Installation

1. Clone or unzip the project into a local folder.
2. (Optional) Create a virtual environment and activate it:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the application:

```bash
python app.py
```

5. Open your browser and go to: [http://127.0.0.1:5000](http://127.0.0.1:5000)

## 3. Live Demo (Hosted on PythonAnywhere)

Visit the deployed app at:

🔗 https://thynes15.pythonanywhere.com/login

### Test Credentials

**Admin Users**
- `admin1` / `adminpass`
- `admin2` / `adminpass`

**Regular Users**
- `user1` / `userpass`
- `user2` / `userpass`

## 4. Screenshots

Included screenshots showing:

- Login and Register page
- Admin dashboard with asset list
- Asset creation and editing form
- Role-based UI differences (e.g. delete button visible for admins only)

## 5. Technologies Used

- Python
- Flask
- SQLite
- Jinja2 (templates)
- HTML/CSS (basic styling)