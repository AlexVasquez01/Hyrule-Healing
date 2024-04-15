import sqlalchemy
from src import database as db
from fastapi import APIRouter, Depends, HTTPException
from enum import Enum
from pydantic import BaseModel
from src.api import auth

router = APIRouter(
    prefix="/bottler",
    tags=["bottler"],
    dependencies=[Depends(auth.get_api_key)],
)

class PotionInventory(BaseModel):
    potion_type: list[int]
    quantity: int

@router.post("/deliver/{order_id}")
def post_deliver_bottles(potions_delivered: list[PotionInventory], order_id: int):
    """ """
    print(f"potions delievered: {potions_delivered} order_id: {order_id}")

    return "OK"

@router.post("/plan")
def get_bottle_plan():
    """
    Go from barrel to bottle.
    """

    # Each bottle has a quantity of what proportion of red, blue, and
    # green potion to add.
    # Expressed in integers from 1 to 100 that must sum up to 100.

    # Initial logic: bottle all barrels into red potions.
    try:
        sql_to_execute = "SELECT num_red_ml, num_green_ml, num_blue_ml FROM global_inventory LIMIT 1"
        with db.engine.begin() as connection:
            ml_inventory = connection.execute(sqlalchemy.text(sql_to_execute)).fetchone()
            num_red_ml, num_green_ml, num_blue_ml = ml_inventory if ml_inventory else (0, 0, 0)

        potion_plans = []
        for color, ml in zip(["red", "green", "blue"], [num_red_ml, num_green_ml, num_blue_ml]):
            num_potions_to_bottle = ml // 100
            if num_potions_to_bottle > 0:
                update_inventory_sql = f"""
                    UPDATE global_inventory
                    SET num_{color}_potions = num_{color}_potions + :num_new_potions,
                        num_{color}_ml = num_{color}_ml - (:num_new_potions * 100)
                """
                connection.execute(sqlalchemy.text(update_inventory_sql), {'num_new_potions': num_potions_to_bottle})
                potion_plans.append({"potion_type": color, "quantity": num_potions_to_bottle})

        return potion_plans
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    print(get_bottle_plan())