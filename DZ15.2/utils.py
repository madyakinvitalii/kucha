import sqlite3
import json


def get_animal_by_id(itemid):
    with sqlite3.connect("animal.db") as connection:
        cursor = connection.cursor()

        query = f"""
        SELECT animal_new.age_upon_outcome, animal_new.animal_id, animal_types.type_name, animals_names.animal_name
        FROM animal_new 
        INNER JOIN animal_types ON animal_new.type_id = animal_types.id
        INNER JOIN animals_and_names ON animal_new.id = animals_and_names.id
        INNER JOIN animals_names ON animals_and_names.name_id = animals_names.id
        WHERE animal_new.id = {itemid}
        """

    cursor.execute(query)
    result = cursor.fetchall()
    return result

