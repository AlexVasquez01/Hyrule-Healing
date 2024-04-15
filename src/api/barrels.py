import sqlalchemy
from src import database as db
from fastapi import APIRouter, Depends, HTTPException
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
    try:
        sql_to_execute = "SELECT num_red_potions, num_green_potions, num_blue_potions, gold FROM global_inventory LIMIT 1"
        with db.engine.begin() as connection:
            inventory_info = connection.execute(sqlalchemy.text(sql_to_execute)).fetchone()
            if not inventory_info:
                raise HTTPException(status_code=404, detail="Inventory information not found")

            num_red_potions, num_green_potions, num_blue_potions, current_gold = inventory_info

        purchase_plan = []
        for barrel in wholesale_catalog:
            if current_gold >= barrel.price:
                needed = False
                if "RED" in barrel.sku and num_red_potions < 10:
                    needed = True
                elif "GREEN" in barrel.sku and num_green_potions < 10:
                    needed = True
                elif "BLUE" in barrel.sku and num_blue_potions < 10:
                    needed = True

                if needed:
                    purchase_plan.append({"sku": barrel.sku, "quantity": 1})
                    current_gold -= barrel.price

                    update_gold_sql = "UPDATE global_inventory SET gold = :new_gold"
                    connection.execute(sqlalchemy.text(update_gold_sql), {'new_gold': current_gold})
        return purchase_plan
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

