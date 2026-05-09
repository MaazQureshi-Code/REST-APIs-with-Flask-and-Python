import uuid
from flask import Flask, request
from db import stores, items
from flask.views  import MethodView
from flask_smorest import abort, Api, Blueprint
import db
from db import db
from models import StoreModel
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from schemas import Storeschema

bip = Blueprint("stores", __name__, description="Operations on stores")
@bip.route("/store/<string:store_id>")
class Store(MethodView):
    @blp.response(200,Storeschema)
    def get(self, store_id):
       return  StoreModel.query.all()

    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        try:
            db.session.delete(store)
            db.session.commit()
            return {"message": "Store deleted"}
        except SQLAlchemyError:
            db.session.rollback()
            return abort(500, message="An error occurred while deleting the store")

@bip.route("/store")
class StoreList(MethodView):
    @blp.response(200, Storeschema(many=True))
    def get(self):
        return list(stores.values())
    @blp.arguments(Storeschema)
    @blp.response(201, Storeschema)
    def post(self , store_data):
        store = StoreModel(**store_data)
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return abort(400, message="A store with that name already exists.")
        except SQLAlchemyError:
            db.session.rollback()
            return abort(500, message="An error occurred while creating the store.")
        return store, 201