from db import db

class ItemModel(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    price = db.Column(db.Float(precision=2))

    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    store = db.relationship('StoreModel')

    def __init__(self, name: str, price: float, store_id: int) -> None:
        self.name: str = name
        self.price: float = price
        self.store_id: int = store_id

    def json(self) -> dict:
        return {'name': self.name, 'price': self.price}

    @classmethod
    def find_by_name(cls, name: str) -> object:
        return cls.query.filter_by(name=name).first() # SELECT * FROM items WHERE name=name LIMIT 1

    def upsert_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()