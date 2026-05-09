import uuid
from flask import Flask, request
from db import stores, items
from flask_smorest import abort, Api, Blueprint
app = Flask(__name__)




@app.get("/store")  # http://127.0.0.1:5000/store
def get_stores():
    return {"stores": list(stores.values())}


@app.post("/store")
def create_store():
    store_data = request.get_json()
    store_id = uuid.uuid4().hex()
    store = {**store_data, "id": store_id}
    stores[store_id] = store
    return store, 201


@app.post("/item")
def create_item():
    item_data = request.get_json()

    # 1. Validate required fields
    if (
        "store_id" not in item_data
        or "name" not in item_data
        or "price" not in item_data
    ):
        return abort(400, message="Missing required fields")

    # 2. Check store exists
    if item_data["store_id"] not in stores:
        return abort(404, message="Store not found")

    # 3. Check duplicate item
    for item in items.values():
        if (
            item_data["name"] == item["name"]
            and item_data["store_id"] == item["store_id"]
        ):
            return abort(400, message="Item already exists")

    # 4. Validate price
    if item_data["price"] <= 0:
        return abort(400, message="Price must be positive")

    # 5. Create item
    item_id = uuid.uuid4().hex
    item = {**item_data, "id": item_id}

    items[item_id] = item

    return item, 201

@app.get("/item")
def get_items():
    return {"items": list(items.values())}

@app.get("/store/<string:store_id>")
def get_store(store_id):
    try:
        return stores[store_id]
    except KeyError:
        return abort(404, message="Store not found")


@app.get("/item/<string:item_id>")
def get_item(item_id):
    try:
        return items[item_id]
    except KeyError:
        return abort(404, message="Item not found")

@app.delete("/item/<string:item_id>")
def delete_item(item_id):
    try:
        del items[item_id]
        return {"message": "Item deleted"}
    except KeyError:
        return abort(404, message="Item not found")
@app.put("/item/<string:item_id>")
def update_item(item_id):
    item_data = request.get_json()
    if "price" in item_data and item_data["price"] <= 0:
        return abort(400, message="Price must be positive")
    try:
        item = items[item_id]
        item.update(item_data)
        return item
    except KeyError:
        return abort(404, message="Item not found")
@app.delete("/store/<string:store_id>")
def delete_store(store_id):
    try:
        del stores[store_id]
        return {"message": "Store deleted"}
    except KeyError:
        return abort(404, message="Store not found")