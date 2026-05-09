from marshmallow import Schema, fields


class PlainItemschema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str()
    price = fields.Float(required=True)
class ItemUpdateSchema(Schema):
    name = fields.Str()
    description = fields.Str()
    price = fields.Float()
    store_id = fields.Int()
    
class PlainStoreSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    
class ItemSchema(PlainItemschema):
    store_id = fields.Int(required=True, load_only=True)
    store = fields.Nested('PlainStoreSchema', dump_only=True)
    
class StoreSchema(PlainStoreSchema):
    items = fields.List(fields.Nested(PlainItemschema), dump_only=True)