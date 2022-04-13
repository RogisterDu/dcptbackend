from database import db


class Charge(db.Model):
    __tablename__ = 'charge_item'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    item_group = db.Column(db.String(255), nullable=True)
    is_deleted = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer, nullable=False)
    unit = db.Column(db.String(255), nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    abbreviation = db.Column(db.String(255), nullable=False)
    code = db.Column(db.String(255), nullable=False)
    item_type = db.Column(db.Integer, nullable=False)
