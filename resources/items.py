from flask_restful import (
    Resource,
    reqparse
)
from flask_jwt_extended import (
    jwt_required,
    get_jwt_claims,
    get_jwt_identity
)
from models.items import ItemModel
from werkzeug.exceptions import BadRequest

_parser = reqparse.RequestParser()
_parser.add_argument(
    'title',
    type=str,
    required=True,
    help='This field is required!')

_parser.add_argument(
    'description',
    type=str,
    required=True,
    help='This field is required!')


_parser.add_argument(
    'src',
    type=str,
    required=True,
    help='This field is required!')


class ItemResource(Resource):
    @staticmethod
    def return_error(e):
        print(e)
        return {"error": "Internal Server Error!"}, 500

    @jwt_required
    def post(self):
        try:
            identity = get_jwt_identity()
            kwargs = _parser.parse_args(strict=True)
            print(kwargs)
            ItemModel(**kwargs, user_id=identity).save()
            return {"message": "Success!"}, 201

        except BadRequest as e:
            return {"error": "Bad Request"}, 400
        except BaseException as e:
            return self.return_error(e)

    @jwt_required
    def get(self):
        try:
            identity = get_jwt_identity()
            print(identity)
            items = [
                item.json() for item in ItemModel.query.filter_by(
                    user_id=identity)]
            return {"items": items}, 200
        except BaseException as e:
            print(e)
            return self.return_error(e)


class ItemIdResource(Resource):

    @staticmethod
    def return_error(e):
        print(e)
        return {"error": "Internal Server Error!"}, 500

    @jwt_required
    def put(self, id):
        try:
            kwargs = _parser.parse_args(strict=True)
            item = ItemModel.get_by_id(id)

            if item:
                item.title = kwargs["title"]
                item.description = kwargs["description"]
                item.src = kwargs["src"]
                item.save()
                return {"message": "Successfully updated resource!"}, 200
            else:
                ItemModel(**kwargs).save()
                return {"message": "Successfully created resource!"}, 201

        except BadRequest as e:
            return {"error": "Bad Request"}, 400
        except BaseException as e:
            return self.return_error(e)

    @jwt_required
    def get(self, id):
        try:
            item = ItemModel.get_by_id(id)
            if item:
                return {"item": item.json()}, 200
            else:
                return {"message": "Item not found!"}, 404
        except BaseException as e:
            return self.return_error(e)

    @jwt_required
    def delete(self, id):
        try:
            item = ItemModel.get_by_id(id)
            if item:
                item.delete()
                return {"message": "Successfully deleted item!"}, 200
            else:
                return {"message": "Item not found!"}, 404
        except BaseException as e:
            return self.return_error(e)
