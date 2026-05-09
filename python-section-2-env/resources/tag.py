from flask import abort

from db import db
from models import TagModel, StoreModel
from schemas import TagSchema, StoreSchema
from flask_restful import Resource

bip = Blueprint('resources.tags', __name__, url_prefix='/api/tags') 
@bip.route('/store/<string:store_id>/tags')
class TagInStore(MethodView):
    @blp.response(200, TagSchema(many=True))
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store.tags.all()
    
    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    def post(self, tag_data, store_id):
        if Tagmodel.query.filter(TagModel.name == tag_data['name'], TagModel.store_id == store_id).first():
            abort(400, message='A tag with that name already exists in that store.')
        tag = TagModel(**tag_data, store_id=store_id)
        db.session.add(tag)
        db.session.commit()
        return tag
    
@bip.route('/<string:tag_id>')
class Tag(MethodView):
    @blp.response(200, TagSchema)
    def get(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        return tag
    
    @blp.response(200, TagSchema)
    def delete(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        db.session.delete(tag)
        db.session.commit()
        return tag    