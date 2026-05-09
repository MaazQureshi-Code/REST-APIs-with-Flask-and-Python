import uuid
from flask import Flask, request
from db import stores, items
from flask.views  import MethodView
from flask_smorest import abort, Api, Blueprint
from schemas import Itemschema , ItemUpdateSchema
from models import ItemModel
from db import db
from sqlalchemy.exc import SQLAlchemyError
bip = Blueprint("items", __name__, description="Operations on items")
@bip.route("/item/<string:item_id>")
class Item(MethodView):
    @blp.response(200, Itemschema)
    def get(self):
        return  ItemModel.query.all()

    def delete(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        try:
            db.session.delete(item)
            db.session.commit()
            return {"message": "Item deleted"}
        except SQLAlchemyError:
            db.session.rollback()
            return abort(500, message="An error occurred while deleting the item")
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, Itemschema)
    def put(self, item_data, item_id):
        try:
            item = ItemModel.query.get_or_404(item_id)
            if item:
              item.name = item_data["name"]
              item.price = item_data["price"]
            else:
                item = ItemModel(id=item_id, **item_data)
                db.session.add(item)
            db.session.commit()
            return item
        except KeyError:
            return abort(404, message="Item not found")
@bip.route("/item")
class ItemList(MethodView):
    @blp.response(200, Itemschema(many=True)    )
    def get(self):
        return {"items": list(items.values())}
    @blp.arguments(Itemschema)
    @blp.response(201, Itemschema)
    def post(self,item_data):
        item = ItemModel(**item_data)
        items[item.id] = item
        try:
            db.session.add(item)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return abort(500, message="An error occurred while adding the item")
        return item, 201