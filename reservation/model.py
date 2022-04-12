from database import db


class Reserve(db.Model):
    __tablename__ = 'appointment'
    id = db.Column(db.INTEGER(), primary_key=True, nullable=False)
    patient_id = db.Column(db.INTEGER(), nullable=False)
    doctor_id = db.Column(db.INTEGER(), nullable=False)
    operator_id = db.Column(db.INTEGER(), nullable=False)
    operator_time = db.Column(db.DATETIME(), nullable=True)
    title = db.Column(db.VARCHAR(255), nullable=False)
    rank = db.Column(db.INTEGER(), nullable=False)
    description = db.Column(db.VARCHAR(255), nullable=False)
    reserve_time = db.Column(db.DATETIME(), nullable=False)
