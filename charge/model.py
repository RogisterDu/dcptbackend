from database import db


class Charge(db.Model):
    __tablename__ = 'charge_item'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    group = db.Column(db.String(255), nullable=True)
    is_deleted = db.Column(db.Boolean, default=False)
    status = db.Column(db.Integer, default=0)
    unit = db.Column(db.String(255), nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    abbreviation = db.Column(db.String(255), nullable=False)
    code = db.Column(db.String(255), nullable=False)
