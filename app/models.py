from app import db
from flask_serialize import FlaskSerializeMixin

FlaskSerializeMixin.db = db


class Client(FlaskSerializeMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(12))
    passport = db.Column(db.String(11))
    name = db.Column(db.String(80))
    deliveries = db.relationship('Delivery', backref='client', lazy='dynamic')

    create_fields = update_fields = ['phone', 'passport', 'name', ]

    def can_delete(self):
        pass

    def __repr__(self):
        return f'<Client {self.name}>'


class Delivery(FlaskSerializeMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    items = db.relationship('Item', backref='delivery', lazy='dynamic')
    cell_deliveries = db.relationship('CellDelivery', backref='delivery', lazy='dynamic')

    create_fields = update_fields = ['client', ]

    def __repr__(self):
        return f'<Delivery {self.id}>'


class Item(FlaskSerializeMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    delivery_id = db.Column(db.Integer, db.ForeignKey('delivery.id'))
    barcode = db.Column(db.Integer)
    isReturned = db.Column(db.Boolean)
    DeliviriedDate = db.Column(db.Date)
    isInCell = db.Column(db.Boolean)
    returns = db.relationship('Return', backref='item', lazy='dynamic')

    create_fields = update_fields = ['delivery', 'barcode', 'return', ]

    def __repr__(self):
        return f'<Item {self.id}>'


class Return(FlaskSerializeMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))
    items = db.relationship('Item', backref='return', lazy='dynamic')

    create_fields = update_fields = ['return', 'item', ]

    def __repr__(self):
        return f'<Return {self.id}>'


class CellDelivery(FlaskSerializeMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    delivery_id = db.Column(db.Integer, db.ForeignKey('delivery.id'))
    cell_id = db.Column(db.Integer, db.ForeignKey('cell.id'))
    cell = db.relationship('Cell', backref='cell_delivery', lazy='dynamic')

    create_fields = update_fields = ['delivery', 'item', 'cell', ]

    def __repr__(self):
        return f'<Cell Delivery {self.id}>'


class Cell(FlaskSerializeMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    capacity = db.Column(db.Integer)
    cell_deliveries = db.relationship('CellDelivery', backref='cell', lazy='dynamic')

    create_fields = update_fields = ['cell_delivery', ]

    def __repr__(self):
        return f'<Cell Delivery {self.id}>'
