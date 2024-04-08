import sqlalchemy
from src import database as db
from fastapi import APIRouter

router = APIRouter()


@router.get("/catalog/", tags=["catalog"])
def get_catalog():
    """
    Each unique item combination must have only a single price.
    """
    sql_to_execute = "SELECT num_green_potions FROM global_inventory LIMIT 1"

    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(sql_to_execute))
        num_green_potions = result.scalar()

    return [{"sku": "GREEN_POTION", "name": "green potion", "quantity": num_green_potions, "price": 50, "potion_type": [0, 100, 0, 0]}]
