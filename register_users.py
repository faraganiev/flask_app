from werkzeug.security import generate_password_hash
from database import db, User
from app import app

def register_user(username, password, role):
    with app.app_context():
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, password=hashed_password, role=role)
        db.session.add(new_user)
        db.session.commit()
        print(f"User {username} registered successfully.")

# Примеры добавления пользователей
register_user('manager1', 'password1', 'manager')
register_user('admin', 'admin', 'admin')  # Исправлено
