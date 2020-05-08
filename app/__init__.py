from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models
c = models.Client(phone='1', passport='1234', name='Andrey')
d = models.Delivery(client=c)
db.session.add(c)
db.session.add(d)
db.session.commit()