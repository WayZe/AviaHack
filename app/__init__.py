from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models

# c = models.Client(phone='12',  passport='12345', name='Ilya')
# d = models.Delivery(client=c)
# cell = models.Cell(capacity=3)
# it_cel = models.ItemsCell(cell=cell)
# i = models.Item(barcode=12, delivery=d, cell=it_cel)
# it = models.Item(barcode=13, delivery=d, cell=it_cel)
# db.session.add(c)
# db.session.add(d)
# db.session.add(cell)
# db.session.add(it_cel)
# db.session.add(i)
# db.session.add(it)
# db.session.commit()

