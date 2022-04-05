from database import db


class User(db.Model):
    __tablename__ = 't_user'
    id = db.Column(db.INTEGER(), primary_key=True, nullable=False)
    account = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    realName = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.INTEGER(), nullable=False)
    is_deleted = db.Column(db.INTEGER(), nullable=False)
    status = db.Column(db.INTEGER(), nullable=False)
    last_login = db.Column(db.DATETIME(), nullable=False)
    created_time = db.Column(db.DATETIME(), nullable=False)
    created_Id = db.Column(db.INTEGER(), nullable=False)


class Vistor(db.Model):
    __tablename__ = 'visit'
    id = db.Column(db.INTEGER(), primary_key=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    contact = db.Column(db.String(11), nullable=False)
    provinceId = db.Column(db.INTEGER(), nullable=False)
    provinceDesc = db.Column(db.String(255), nullable=False)
    cityId = db.Column(db.INTEGER(), nullable=False)
    cityDesc = db.Column(db.String(255), nullable=False)
    disctrictId = db.Column(db.INTEGER(), nullable=False)
    disctrictDesc = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    time = db.Column(db.DATETIME(), nullable=False)
    temperature = db.Column(db.FLOAT(), nullable=False)
    is_green = db.Column(db.INTEGER(), nullable=False)
    is_safe = db.Column(db.INTEGER(), nullable=False)
    is_touch = db.Column(db.INTEGER(), nullable=False)
    identityID = db.Column(db.String(255), nullable=False)
