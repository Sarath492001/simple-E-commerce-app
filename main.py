from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Mock Database
inventory = {}
item_id = 1


class Item(BaseModel):
    name: str
    price: float


class InventoryUpdate(BaseModel):
    item_id: int
    qty: int


@app.get("/items/{item_id}")
def read_item(item_id: int):
    if item_id in inventory:
        return inventory[item_id]
    else:
        return {"error": "Item not found"}


@app.post("/items")
def create_item(item: Item):
    global item_id
    inventory[item_id] = item
    item_id += 1
    return item


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    if item_id in inventory:
        inventory[item_id] = item
        return item
    else:
        return {"error": "Item not found"}


@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    if item_id in inventory:
        del inventory[item_id]
        return {"message": "Item deleted"}
    else:
        return {"error": "Item not found"}


@app.post("/inventory/update")
def update_inventory(inventory_update: InventoryUpdate):
    item_id = inventory_update.item_id
    qty = inventory_update.qty

    if item_id in inventory:
        inventory[item_id].qty += qty
        return {"message": "Inventory updated"}
    else:
        return {"error": "Item not found"}


@app.get("/inventory")
def get_inventory():
    return inventory
