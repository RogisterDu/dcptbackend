from database import db


class Visitor(db.Model):
    __tablename__ = 'visit'
    id = db.Column(db.INTEGER(), primary_key=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    contact = db.Column(db.String(11), nullable=False)
    # provinceId = db.Column(db.INTEGER(), nullable=False)
    provinceDesc = db.Column(db.String(255), nullable=False)
    # cityId = db.Column(db.INTEGER(), nullable=False)
    cityDesc = db.Column(db.String(255), nullable=False)
    # disctrictId = db.Column(db.INTEGER(), nullable=False)
    disctrictDesc = db.Column(db.String(255), nullable=True)
    address = db.Column(db.String(255), nullable=False)
    time = db.Column(db.DATETIME(), nullable=False)
    temperature = db.Column(db.FLOAT(), nullable=False)
    greenCode = db.Column(db.INTEGER(), nullable=False)
    is_safe = db.Column(db.INTEGER(), nullable=False)
    is_touch = db.Column(db.INTEGER(), nullable=False)
    identityID = db.Column(db.String(255), nullable=False)
    pcr_json = db.Column(db.String(255), nullable=False)
    is_deleted = db.Column(db.INTEGER(), nullable=False)
