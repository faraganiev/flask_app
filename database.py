from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # 'manager' или 'admin'

class CashierReport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cashier = db.Column(db.String(50), nullable=False)
    shift = db.Column(db.String(50), nullable=False)
    z_report = db.Column(db.Float, nullable=False)
    humo = db.Column(db.Float, nullable=False)
    uzcard = db.Column(db.Float, nullable=False)
    cash = db.Column(db.Float, nullable=False)
    click_payme = db.Column(db.Float, nullable=False)
    difference = db.Column(db.Float, nullable=False)
    comments = db.Column(db.Text)
    reason = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    z_report_doc = db.Column(db.String(255))  # Путь к документу Z-отчета
    humo_receipt = db.Column(db.String(255))  # Путь к чеку HUMO
    uzcard_receipt = db.Column(db.String(255))  # Путь к чеку UZCARD
    click_receipts = db.Column(db.Text)  # Список путей к чекам Click/Payme в виде строки
    debtor_names = db.Column(db.Text)  # Список имен должников в виде строки
    debtor_amounts = db.Column(db.Text)  # Список сумм долгов в виде строки

class Settings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    currency = db.Column(db.String(10), nullable=False, default='сум')
    language = db.Column(db.String(10), nullable=False, default='ru')
    timezone = db.Column(db.String(50), nullable=False, default='GMT+5')

class Cashier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
