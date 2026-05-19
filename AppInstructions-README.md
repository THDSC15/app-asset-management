# IT Asset Management Web Application

A Flask-based web application for managing IT assets such as laptops, monitors, printers, and other equipment. The application supports user authentication, role-based access control, asset tracking, and secure CRUD operations.

---

# Features

- User registration and login
- Password hashing using Werkzeug security utilities
- Admin and regular user roles
- Role-based access control
- Create, read, update, and delete (CRUD) asset management
- Asset assignment to registered users
- Asset status tracking:
  - Available
  - In Use
  - Maintenance
  - Retired
- SQLite relational database
- CSRF protection using Flask-WTF
- Server-side form validation
- Automated tests using Pytest

---

# Technologies Used

- Python
- Flask
- Flask-SQLAlchemy
- Flask-Login
- Flask-WTF
- SQLite
- Jinja2
- HTML/CSS
- Pytest
- Git/GitHub

---

# Database Structure

The application uses a relational SQLite database with the following main tables:

- User
- Category
- Asset

Relationships are implemented using foreign keys and SQLAlchemy ORM relationships.

---

# Running The Application Locally

## 1. Create and activate virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

## 2. Install dependencies

```bash
python3 -m pip install -r requirements.txt
```

## 3. Seed sample data

```bash
python3 seed_data.py
```

## 4. Run the Flask application

```bash
python3 app.py
```

## 5. Open in browser

```text
http://127.0.0.1:5000
```

---

# Testing

Automated tests are included using Pytest.

Run tests with:

```bash
python3 -m pytest
```

The tests currently cover:
- authentication validation
- role-based access control
- asset deletion permissions
- form validation behaviour

---

# Security Features

The application includes several security-focused features aligned to OWASP secure development practices:

- Password hashing
- Login-protected routes
- Role-based access control
- CSRF protection
- Server-side validation
- Controlled dropdown-based user assignment

---

# Development Approach

The project was developed using an iterative Agile-style approach. Features were implemented incrementally and tracked using Git version control.

Example development phases included:
- Authentication system
- Asset CRUD functionality
- Role-based permissions
- Security improvements
- Automated testing
- Deployment preparation

---

# Live Deployment

The application can be deployed using platforms such as PythonAnywhere.

---

# Author

Created by Ted Hynes