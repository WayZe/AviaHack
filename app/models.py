from app import db


class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(12))
    passport = db.Column(db.String(11))
    name = db.Column(db.String(80))

    def __repr__(self):
        return '<Client {}>'.format(self.name)
