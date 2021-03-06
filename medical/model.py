from database import db


class Medical(db.Model):
    __tablename__ = 'record'
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DATETIME, nullable=False)
    is_First = db.Column(db.Integer, nullable=True)
    allergic = db.Column(db.String(255), nullable=True)
    main = db.Column(db.String(255), nullable=True)
    now = db.Column(db.String(255), nullable=True)
    cure = db.Column(db.String(255), nullable=True)
    epidemic = db.Column(db.String(255), nullable=True)
    doctor_id = db.Column(db.String(255), nullable=True)
    advice = db.Column(db.String(255), nullable=True)
    hasInfo = db.Column(db.Integer, nullable=False)
    patient_id = db.Column(db.Integer, nullable=False)
    check_json = db.Column(db.String(255), nullable=True)
    history = db.Column(db.String(255), nullable=True)


class Templet(db.Model):
    __tablename__ = 'record_template'
    id = db.Column(db.Integer, primary_key=True)
    allergic = db.Column(db.String(255), nullable=False)
    main = db.Column(db.String(255), nullable=False)
    now = db.Column(db.String(255), nullable=False)
    cure = db.Column(db.String(255), nullable=False)
    epidemic = db.Column(db.String(255), nullable=False)
    advice = db.Column(db.String(255), nullable=False)
    history = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=True)
