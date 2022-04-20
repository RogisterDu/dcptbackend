from database import db


class Dicom(db.Model):
    __tablename__ = 'dicom'
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DATETIME, nullable=False)
    dicom_url = db.Column(db.String(255), nullable=False)
    patient_id = db.Column(db.String(255), nullable=False)
    is_deleted = db.Column(db.Integer, nullable=False)
