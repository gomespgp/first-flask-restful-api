from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from models.store import StoreModel

class Store(Resource):
    @jwt_required
    def get(self, name: str) -> dict:
        if store := StoreModel.find_by_name(name):
            return store.json(), 200
        return {'message': 'Store not found.'}, 404

    @jwt_required
    def post(self, name: str) -> dict:
        if StoreModel.find_by_name(name):
            return {'message': f'A store with name {name} already exists.'}, 400

        store = StoreModel(name)
        try:
            store.upsert_to_db()
        except Exception as err:
            print(err)
            return {'message': 'An error occurred while creating the store.'}, 500
        return store.json(), 201

    @jwt_required
    def delete(self, name: str) -> dict:
        if store := StoreModel.find_by_name(name):
            store.delete_from_db()
            return {'message': 'Store deleted.'}, 200
        return {'message': 'Store not found.'}, 404

class StoreList(Resource):
    @jwt_required
    def get(self):
        return {'stores': [store.json() for store in StoreModel.find_all()]}