from sqlalchemy import text
from database import db
from app import app

def add_store_column():
    with app.app_context():
        # Проверяем существование колонки store
        result = db.session.execute(text("PRAGMA table_info(cashier);")).fetchall()
        column_names = [row[1] for row in result]

        if "store" not in column_names:
            db.session.execute(text("ALTER TABLE cashier ADD COLUMN store TEXT DEFAULT 'kanimex';"))
            db.session.commit()
            print("✅ Поле 'store' добавлено в таблицу 'cashier'!")
        else:
            print("⚠️ Поле 'store' уже существует!")

if __name__ == "__main__":
    add_store_column()
