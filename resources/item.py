from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help='This field cannot be left blank!'
    )
    parser.add_argument('store_id',
        type=int,
        required=True,
        help='Every item needs a store id.'
    )

    @jwt_required()
    def get(self, name: str) -> dict:
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found.'}, 404

    def post(self, name: str) -> dict:
        if ItemModel.find_by_name(name):
            return {'message': f'An item with name {name} already exists.'}, 400

        data = Item.parser.parse_args()

        item = ItemModel(name, **data)

        try:
            item.upsert_to_db()
        except Exception as err:
            print(err)
            return {'message': 'An error occurred inserting the item.'}, 500

        return item.json(), 201

    def delete(self, name: str) -> dict:
        if item := ItemModel.find_by_name(name):
            item.delete_from_db()
        else:
            return {'message': 'Item not found.'}, 404
        return {'message': 'Item deleted.'}, 200


    def put(self, name: str) -> dict:
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            try:
                item = ItemModel(name, **data)
            except Exception as err:
                print(err)
                return {'message': 'An error occurred inserting the item.'}, 500
        else:
            try:
                item.price = data['price']
            except Exception as err:
                print(err)
                return {'message': 'An error occurred updating the item.'}, 500

        item.upsert_to_db()

        return item.json()

class ItemList(Resource):
    def get(self) -> dict:
        return {'items': [item.json() for item in ItemModel.query.all()]} # Before: {'items': [item for item in [{'name': item[1], 'price': item[2]} for item in list(result)]]}