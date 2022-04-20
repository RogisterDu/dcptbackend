from database import db


class Task(db.Model):
    __tablename__ = 'export_task'
    id = db.Column(db.INTEGER(), primary_key=True)
    # 100 准备中 200待下载 300 已下载 400失败
    status = db.Column(db.INTEGER(), nullable=False)
    statusDesc = db.Column(db.String(255), nullable=False)
    file_url = db.Column(db.String(255), nullable=False)
    finish_time = db.Column(db.DateTime(), nullable=True)
    creator_id = db.Column(db.INTEGER(), nullable=False)
    taskName = db.Column(db.String(255), nullable=False)
