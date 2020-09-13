from flask_restful import (
    Resource,
    reqparse
)

from flask_jwt_extended import (
    create_access_token,
)
from .utils.valid_email import valid_email
from models.users import UserModel
from werkzeug.exceptions import BadRequest

_parser = reqparse.RequestParser()
_parser.add_argument(
    "email",
    type=valid_email,
    required=True,
    help='This field is required!')

_parser.add_argument(
    "password",
    type=str,
    required=True,
    help='This field is required!')


class UserSignup(Resource):
    def post(self):

        try:
            args = _parser.parse_args(strict=True)
            user = UserModel.get_by_email(args["email"])

            print(args)
            if user:
                return {"message":
                        "Conflict: User already exists!!"}, 409

            UserModel(**args).save_to_db()
            return {"message": "Success!"}, 200

        except BadRequest as e:
            return {"error": "Bad Request"}, 400
        except BaseException as e:
            print(e)
            return {"error": "Internal Server Error"}, 500


class UserLogin(Resource):
    def post(self):
        try:
            args = _parser.parse_args(strict=True)
            user = UserModel.get_by_email(args["email"])

            if user:
                is_password_valid = user.password == args.password
                if is_password_valid:
                    claims = {"email": user.email}
                    access_token = create_access_token(
                        identity=user.id, user_claims=claims)
                    return {"access_token": access_token}, 200
            return {"error": "Unauthorized!"}, 401

        except BadRequest as e:
            return {"error": "Bad Request"}, 400
        except BaseException as e:
            print(e)
            return {"error": "Internal Server Error"}, 500
