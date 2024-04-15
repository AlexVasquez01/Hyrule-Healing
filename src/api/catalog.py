import sqlalchemy
from src import database as db
from fastapi import APIRouter

router = APIRouter()


@router.get("/catalog/", tags=["catalog"])
def get_catalog():
    """
    Each unique item combination must have only a single price.
    """
    sql_to_execute = """
    SELECT num_red_potions, num_green_potions, num_blue_potions
    FROM global_inventory
    LIMIT 1;
    """

    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(sql_to_execute))
        num_red_potions, num_green_potions, num_blue_potions = result.fetchone()

    # Return a list of all potions available for sale with their respective details
    catalog_items = [
        {"sku": "RED_POTION", "name": "red potion", "quantity": num_red_potions, "price": 50, "potion_type": [100, 0, 0, 0]},
        {"sku": "GREEN_POTION", "name": "green potion", "quantity": num_green_potions, "price": 50, "potion_type": [0, 100, 0, 0]},
        {"sku": "BLUE_POTION", "name": "blue potion", "quantity": num_blue_potions, "price": 50, "potion_type": [0, 0, 100, 0]}
    ]

    return catalog_items
