from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

from app import routes, models

#cell = models.Cell(capacity=3)
# it = models.Item(barcode=21, delivery=models.Delivery.query.get(1))
# db.session.add(it)
# db.session.commit()
