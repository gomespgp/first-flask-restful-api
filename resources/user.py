from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    jwt_refresh_token_required,
    get_jwt_identity,
    get_raw_jwt
)
from models.user import UserModel
from blacklist import BLACKLIST

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username',
                    type=str,
                    required=True,
                    help='This field cannot be left blank!'
                    )
_user_parser.add_argument('password',
                    type=str,
                    required=True,
                    help='This field cannot be left blank!'
                    )

class UserRegister(Resource):
    def post(self) -> dict:
        data = _user_parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message': 'A user with that name already exists.'}, 400

        user = UserModel(**data)
        user.upsert_to_db()

        return {'message': 'User created successfully.'}, 201

class User(Resource):
    @classmethod
    @jwt_required
    def get(cls, user_id: int) -> dict:
        if not (user := UserModel.find_by_id(user_id)):
            return {'message': 'User not found.'}, 404
        return user.json()

    @classmethod
    @jwt_required
    def delete(cls, user_id: int) -> dict:
        if not (user := UserModel.find_by_id(user_id)):
            return {'message': 'User not found.'}, 404

        user.delete_from_db()

        return {'message': 'User deleted.'}, 200

class UserLogin(Resource):
    @classmethod
    def post(cls):
        # Get data from parser
        data = _user_parser.parse_args()
        # Find user in databas
        # Check password
        if (user := UserModel.find_by_username(data['username'])) and safe_str_cmp(user.password, data['password']):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200
        return {'message': 'Invalid credentials.'}, 401
        # Create access token
        # Create refresh token (we will look at this later)
        # Return them

class UserLogout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti'] # jti is 'JWT ID', a unique identifier for a JWT
        BLACKLIST.add(jti)
        return {'message': 'Successfully logged out.'}

class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}, 200