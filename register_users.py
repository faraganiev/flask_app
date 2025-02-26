from werkzeug.security import generate_password_hash
from database import db, User
from app import app

def register_user(username, password, role):
    """Создает нового пользователя с хешированным паролем."""
    with app.app_context():
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, password=hashed_password, role=role)
        db.session.add(new_user)
        db.session.commit()
        print(f"✅ Пользователь {username} зарегистрирован.")

def change_password(username, new_password):
    """Меняет пароль пользователя в базе данных."""
    with app.app_context():
        user = User.query.filter_by(username=username).first()
        if not user:
            print(f"⚠ Пользователь {username} не найден!")
            return

        hashed_password = generate_password_hash(new_password, method='pbkdf2:sha256')
        user.password = hashed_password
        db.session.commit()
        print(f"🔑 Пароль для {username} успешно изменен.")

# ✅ Примеры добавления пользователей
# register_user('manager1', 'password1', 'manager')
# register_user('admin', 'admin', 'admin')

# Меняем пароли пользователей
change_password('admin', '4320005')  # Новый пароль для admin
change_password('manager1', '5586878')  # Новый пароль для manager1

