import sqlite3

with sqlite3.connect("animal.db") as connection:
    cursor = connection.cursor()

    query_animal_types = """
                 INSERT INTO animal_types (type_name)
                 SELECT DISTINCT animal_type FROM animals
                 """

    query_breeds = """
                 INSERT INTO breeds (breeds_name)
                 SELECT DISTINCT breed FROM animals
                 """

    query_birth_dates = """
                 INSERT INTO birth_dates ('date')
                 SELECT DISTINCT date_of_birth FROM animals
                 """

    query_outcome_year = """
                 INSERT INTO outcome_year ('year')
                 SELECT DISTINCT outcome_year FROM animals
                 """

    query_outcome_month = """
                 INSERT INTO outcome_month ('month')
                 SELECT DISTINCT outcome_month FROM animals
                 """

    update_animals_breeds_id = """
                update animal_new
                set breeds_id = breeds.id
                from  breeds 
                where animal_new.breeds_id = breeds.breeds_name
                """

    update_animals_birth_dates_id = """
                update animal_new
                set birth_dates_id = birth_dates.id
                from  birth_dates 
                where animal_new.birth_dates_id = birth_dates.date
                """

    update_animals_outcome_year_id = """
                update animal_new
                set outcome_year_id = outcome_year.id
                from  outcome_year 
                where animal_new.outcome_year_id = outcome_year.year
                """

    update_animals_outcome_month_id = """
                update animal_new
                set outcome_month_id = outcome_month.id
                from  outcome_month
                where animal_new.outcome_month_id = outcome_month.month
                """

    query_colors1 = """
                 INSERT INTO colors (color)
                 SELECT DISTINCT (color1) FROM animals
                 WHERE color1 IS NOT NULL
                 """

    query_colors2 = """
                 INSERT INTO colors (color)
                 SELECT DISTINCT (color2) FROM animals
                 WHERE color2 IS NOT NULL AND color2 NOT IN (SELECT color1 FROM animals)
                 """

    query_names = """
                 INSERT INTO animals_names (animal_name)
                 SELECT DISTINCT "name" FROM animals
                 WHERE "name" IS NOT NULL
                 """

    query_outcome_type = """
                 INSERT INTO outcome_type (type_name)
                 SELECT DISTINCT outcome_type FROM animals
                 WHERE outcome_type IS NOT NULL
                 """

    query_outcome_subtype = """
                 INSERT INTO outcome_subtype (subtype_name)
                 SELECT DISTINCT outcome_subtype FROM animals\
                 WHERE outcome_subtype IS NOT NULL
                 """

    query_animals_and_names = """
                     INSERT INTO animals_and_names (animals_id, name_id)
                     SELECT DISTINCT animal_id, "name" FROM animals
                     WHERE "name" IS NOT NULL
                     """

    update_animals_and_names_id_1 = """
                UPDATE animals_and_names
                SET animals_id = animal_new.id
                FROM  animal_new 
                WHERE animals_and_names.animals_id = animal_new.animal_id
                """

    update_animals_and_names_id_2 = """
                UPDATE animals_and_names
                SET name_id = animals_names.id
                FROM  animals_names 
                WHERE animals_and_names.name_id = animals_names.animal_name
                """

    query_animals_outcome_types = """
                     INSERT INTO animals_outcome_types (animals_id, type_name_id)
                     SELECT DISTINCT animal_id, outcome_type FROM animals
                     WHERE outcome_type IS NOT NULL
                     """

    update_animals_outcome_types_id_1 = """
                UPDATE animals_outcome_types
                SET animals_id = animal_new.id
                FROM  animal_new 
                WHERE animals_outcome_types.animals_id = animal_new.animal_id
                """

    update_animals_outcome_types_id_2 = """
                UPDATE animals_outcome_types
                SET type_name_id = outcome_type.id
                FROM  outcome_type 
                WHERE animals_outcome_types.type_name_id = outcome_type.type_name
                """

    query_animals_outcome_subtypes = """
                     INSERT INTO animals_outcome_subtypes (animals_id, subtype_name_id)
                     SELECT DISTINCT animal_id, outcome_subtype FROM animals
                     WHERE outcome_subtype IS NOT NULL
                     """

    update_animals_outcome_subtypes_id_1 = """
                UPDATE animals_outcome_subtypes
                SET animals_id = animal_new.id
                FROM  animal_new 
                WHERE animals_outcome_subtypes.animals_id = animal_new.animal_id
                """

    update_animals_outcome_subtypes_id_2 = """
                UPDATE animals_outcome_subtypes
                SET subtype_name_id = outcome_subtype.id
                FROM  outcome_subtype 
                WHERE animals_outcome_subtypes.subtype_name_id = outcome_subtype.subtype_name
                """

    query_animals_colors_1 = """
                     INSERT INTO animals_colors (animals_id, colors_id)
                     SELECT DISTINCT animal_id, color1 FROM animals
                     WHERE color1 IS NOT NULL
                     """

    query_animals_colors_2 = """
                     INSERT INTO animals_colors (animals_id, colors_id)
                     SELECT DISTINCT animal_id, color2 FROM animals
                     WHERE color2 IS NOT NULL
                     """

    update_animals_colors_1 = """
                UPDATE animals_colors
                SET animals_id = animal_new.id
                FROM  animal_new 
                WHERE animals_colors.animals_id = animal_new.animal_id
                """

    update_animals_colors_2 = """
                UPDATE animals_colors
                SET colors_id = colors.id
                FROM  colors 
                WHERE animals_colors.colors_id = colors.color
                """

    cursor.execute(update_animals_colors_2)
