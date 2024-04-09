import sqlalchemy
from src import database as db
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth

router = APIRouter(
    prefix="/barrels",
    tags=["barrels"],
    dependencies=[Depends(auth.get_api_key)],
)

class Barrel(BaseModel):
    sku: str

    ml_per_barrel: int
    potion_type: list[int]
    price: int

    quantity: int

@router.post("/deliver/{order_id}")
def post_deliver_barrels(barrels_delivered: list[Barrel], order_id: int):
    """ """
    print(f"barrels delievered: {barrels_delivered} order_id: {order_id}")

    return "OK"

# Gets called once a day
@router.post("/plan")
def get_wholesale_purchase_plan(wholesale_catalog: list[Barrel]):
    sql_to_execute = "SELECT num_green_potions, gold FROM global_inventory LIMIT 1"
    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(sql_to_execute))
        inventory_info = result.fetchone()
        num_green_potions, current_gold = inventory_info if inventory_info else (0, 0)

    purchase_plan = []
    for barrel in wholesale_catalog:
        if barrel["sku"] == "SMALL_GREEN_BARREL" and num_green_potions < 10:
            if current_gold >= barrel["price"]:
                purchase_plan.append({"sku": barrel["sku"], "quantity": 1})
                current_gold -= barrel["price"]  
                update_gold_sql = "UPDATE global_inventory SET gold = :new_gold"
                connection.execute(sqlalchemy.text(update_gold_sql), {'new_gold': current_gold})
            break

    return purchase_plan

