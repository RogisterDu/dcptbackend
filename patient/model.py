from database import db


class Patient(db.Model):
    __tablename__ = 'patient'
    id = db.Column(db.INTEGER(), primary_key=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    contact = db.Column(db.String(255), nullable=False)
    sex = db.Column(db.INTEGER, nullable=False)
    birthday = db.Column(db.DATE(), nullable=False)
    provinceDesc = db.Column(db.String(255), nullable=False)
    cityDesc = db.Column(db.String(255), nullable=False)
    disctrictDesc = db.Column(db.String(255), nullable=True)
    pcr_json = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    is_deleted = db.Column(db.INTEGER(), nullable=False)
    tags = db.Column(db.String(255), nullable=True)
    last_visit = db.Column(db.DATETIME(), nullable=False)
    debt = db.Column(db.Integer(), nullable=False)
    identityID = db.Column(db.String(255), nullable=False)
