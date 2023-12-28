from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

# ortam değişkenleri
load_dotenv()

app = Flask(__name__)

# SQLALCHEMY_DATABASE_URI ve diğer konfigürasyon ayarları
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# SQLAlchemy instance
db = SQLAlchemy(app)

# Modeller ve route'ları
from models import Supplier, Product
from routes import *

with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run()

