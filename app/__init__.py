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

# c = models.Client(phone='89745612321',  passport='4568789456', name='IlyaGreen')
# c2 = models.Client(phone='89741234567',  passport='4589621234', name='KarolGreen')
# d = models.Delivery(client=c)
# d2 = models.Delivery(client=c2)
# d3 = models.Delivery(client=c2)
# cell = models.Cell(capacity=3)
# cell1 = models.Cell(capacity=3)
# cell2 = models.Cell(capacity=3)
# cell3 = models.Cell(capacity=3)
# cell4 = models.Cell(capacity=3)
# cell5 = models.Cell(capacity=3)
# cell6 = models.Cell(capacity=3)
# it_cel = models.Items_cell(cell=cell)
# i = models.Item(barcode=12, delivery=d, cell=it_cel)
# it = models.Item(barcode=14, delivery=d)
# db.session.add(c)
# db.session.add(d)
# db.session.add(cell)
# db.session.add(it_cel)
# db.session.add(i)
# db.session.add(it)
# db.session.commit()

#cell = models.Cell(capacity=3)
# it = models.Item(barcode=21, delivery=models.Delivery.query.get(1))
# db.session.add(it)
# db.session.commit()
