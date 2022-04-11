from database import db


class Fee(db.Model):
    __tablename__ = 'fee'
    id = db.Column(db.INTEGER(), primary_key=True)
    status = db.Column(db.String(), nullable=False)
    patient_id = db.Column(db.INTEGER(), nullable=False)
    time = db.Column(db.DateTime, nullable=False)
    is_deleted = db.Column(db.INTEGER(), nullable=False)
    should = db.Column(db.FLOAT(), nullable=False)
    paid = db.Column(db.FLOAT(), nullable=False)
    total_pay = db.Column(db.FLOAT(), nullable=False)


class FeeDetail(db.Model):
    __tablename__ = 'fee_detail'
    id = db.Column(db.INTEGER(), primary_key=True)
    fee_id = db.Column(db.INTEGER(), nullable=False)
    charge_item = db.Column(db.String(255), nullable=False)
    quantity = db.Column(db.INTEGER(), nullable=False)
    unit_price = db.Column(db.FLOAT(), nullable=False)
    unit = db.Column(db.String(255), nullable=False)
    code = db.Column(db.String(255), nullable=False)
