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
