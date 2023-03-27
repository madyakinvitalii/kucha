import sqlite3

with sqlite3.connect("animal.db") as connection:
    cursor = connection.cursor()

    query_animal_types = """            
            CREATE TABLE animal_types (
            id integer PRIMARY KEY AUTOINCREMENT,
            type_name varchar(40)      
            )            
    """

    query_breeds = """
            CREATE TABLE breeds (
            id integer PRIMARY KEY AUTOINCREMENT,
            breeds_name varchar(40)
            )
    """

    query_birth_dates = """
            CREATE TABLE birth_dates (
            id integer PRIMARY KEY AUTOINCREMENT,
            "date" varchar(40)
            )
    """

    query_outcome_year = """
            CREATE TABLE outcome_year (
            id integer PRIMARY KEY AUTOINCREMENT,
            "year" varchar(40)
            )
    """

    query_outcome_month = """
            CREATE TABLE outcome_month (
            id integer PRIMARY KEY AUTOINCREMENT,
            "month" varchar(40)
            )
    """

    query_animal_new = """
            CREATE TABLE animal_new (
            id integer PRIMARY KEY AUTOINCREMENT,
            "index" integer,
            age_upon_outcome varchar(40),
            animal_id varchar(10),
            type_id integer,
            breeds_id integer,
            birth_dates_id integer,
            outcome_year_id integer,
            outcome_month_id integer,
            FOREIGN KEY (type_id) REFERENCES animal_types(id),
            FOREIGN KEY (breeds_id) REFERENCES breeds(id),
            FOREIGN KEY (birth_dates_id) REFERENCES birth_dates(id),
            FOREIGN KEY (outcome_year_id) REFERENCES outcome_year(id),
            FOREIGN KEY (outcome_month_id) REFERENCES outcome_month(id)
            )
    """

    query_colors = """
            CREATE TABLE colors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            color VARCHAR(40) NOT NULL 
            )
    """

    query_names = """
            CREATE TABLE animals_names (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            animal_name VARCHAR(40) NOT NULL 
            )
    """

    query_outcome_type = """
            CREATE TABLE outcome_type (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type_name VARCHAR(40) NOT NULL 
            )
    """

    query_outcome_subtype = """
            CREATE TABLE outcome_subtype (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subtype_name VARCHAR(40) NOT NULL 
            )
    """

    query_animals_colors = """
            CREATE TABLE animals_colors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            animals_id INTEGER NOT NULL,
            colors_id INTEGER NOT NULL, 
            FOREIGN KEY (animals_id) REFERENCES animal_new(id),
            FOREIGN KEY (colors_id) REFERENCES colors(id)
            )
    """

    query_animals_and_names = """
            CREATE TABLE animals_and_names (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            animals_id INTEGER,
            name_id INTEGER, 
            FOREIGN KEY (animals_id) REFERENCES animal_new(id),
            FOREIGN KEY (name_id) REFERENCES animals_names(id)
            )
    """

    query_animals_outcome_types = """
            CREATE TABLE animals_outcome_types (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            animals_id INTEGER,
            type_name_id INTEGER, 
            FOREIGN KEY (animals_id) REFERENCES animal_new(id),
            FOREIGN KEY (type_name_id) REFERENCES outcome_type(id)
            )
    """

    query_animals_outcome_subtypes = """
            CREATE TABLE animals_outcome_subtypes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            animals_id INTEGER,
            subtype_name_id INTEGER, 
            FOREIGN KEY (animals_id) REFERENCES animal_new(id),
            FOREIGN KEY (subtype_name_id) REFERENCES outcome_subtype(id)
            )
    """

    # cursor.execute(query_animal_types)
    # cursor.execute(query_breeds)
    # cursor.execute(query_birth_dates)
    # cursor.execute(query_outcome_year)
    # cursor.execute(query_outcome_month)
    # cursor.execute(query_animal_new)
    # cursor.execute(query_colors)
    # cursor.execute(query_names)
    # cursor.execute(query_outcome_type)
    # cursor.execute(query_outcome_subtype)
    # cursor.execute(query_animals_colors)
    # cursor.execute(query_animals_and_names)
    # cursor.execute(query_animals_outcome_types)
    # cursor.execute(query_animals_outcome_subtypes)
