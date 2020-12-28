import sqlite3
from db import db

class UserModel(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))

    def __init__(self, username: str, password: str) -> None:
        self.username: str = username
        self.password: str = password

    def upsert_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username: str) -> object:
        return cls.query.filter_by(username=username).first() # SELECT & FROM users WHERE username=username LIMIT 1

    @classmethod
    def find_by_id(cls, _id: int) -> dict:
        return cls.query.filter_by(id=_id).first() # SELECT & FROM users WHERE id=_id LIMIT 1