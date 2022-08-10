import sqlite3
import sys
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("database_file")
parser.add_argument("--ingredients")
parser.add_argument("--meals")
args = parser.parse_args()


class Database:
    def __init__(self, name):
        self.conn = create_database(name)
        self.cursor = self.conn.cursor()
        self.enable_foreign_keys()
        self.create_tables()

    def create_tables(self):
        create_meals = """CREATE TABLE IF NOT EXISTS meals(
                meal_id INTEGER PRIMARY KEY AUTOINCREMENT,
                meal_name TEXT UNIQUE NOT NULL)
                """
        create_ingredients = """CREATE TABLE IF NOT EXISTS ingredients(
                ingredient_id INTEGER PRIMARY KEY AUTOINCREMENT,
                ingredient_name TEXT UNIQUE NOT NULL)
                """
        create_measures = """CREATE TABLE IF NOT EXISTS measures(
                measure_id INTEGER PRIMARY KEY AUTOINCREMENT,
                measure_name TEXT UNIQUE)
                """
        create_recipes = """CREATE TABLE IF NOT EXISTS recipes(
                recipe_id INTEGER PRIMARY KEY AUTOINCREMENT,
                recipe_name TEXT NOT NULL,
                recipe_description TEXT)
                """
        create_serve = """CREATE TABLE IF NOT EXISTS serve(
                serve_id INTEGER PRIMARY KEY AUTOINCREMENT,
                recipe_id INTEGER NOT NULL,
                meal_id INTEGER NOT NULL,
                FOREIGN KEY(recipe_id) REFERENCES recipes(recipe_id),
                FOREIGN KEY(meal_id) REFERENCES meals(meal_id))
                """
        create_quantity = """CREATE TABLE IF NOT EXISTS quantity(
                quantity_id INTEGER PRIMARY KEY AUTOINCREMENT,
                measure_id INTEGER NOT NULL,
                ingredient_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                recipe_id INTEGER NOT NULL,
                FOREIGN KEY(measure_id) REFERENCES measures(measure_id),
                FOREIGN KEY(ingredient_id) REFERENCES ingredients(ingredient_id),
                FOREIGN KEY(recipe_id) REFERENCES recipes(recipe_id))
                """
        self.cursor.execute(create_meals)
        self.cursor.execute(create_ingredients)
        self.cursor.execute(create_measures)
        self.cursor.execute(create_recipes)
        self.cursor.execute(create_serve)
        self.cursor.execute(create_quantity)
        self.conn.commit()

    def enable_foreign_keys(self):
        query = "PRAGMA foreign_keys = ON;"
        self.cursor.execute(query)

    #  Used to insert meals, ingredients and measures:
    def insert_value(self, table, field, value):
        query = f"INSERT INTO {table} ({field}) values ('{value}')"
        self.cursor.execute(query)
        self.conn.commit()

    def insert_recipe(self, name, description):
        query = f"""INSERT INTO recipes (recipe_name, recipe_description)
                values ('{name}', '{description}')"""
        self.cursor.execute(query)
        self.conn.commit()

    def insert_serve(self):
        options_query = "SELECT meal_id, meal_name from meals"
        recipe_id = self.cursor.lastrowid

        self.cursor.execute(options_query)
        for (meal_id, name) in self.cursor.fetchall():
            print(f"{meal_id}) {name}", end=" ")
        meal_ids = input("\nWhen the dish can be served:")
        for meal_id in meal_ids.split():
            insert_query = f"INSERT INTO serve (recipe_id, meal_id) VALUES ({recipe_id}, {meal_id})"
            self.cursor.execute(insert_query)
            self.conn.commit()

    def recipes_loop(self):
        print("Pass the empty recipe name to exit.")
        name = input("Recipe name: ")
        while name:
            description = input("Recipe description: ")
            self.insert_recipe(name, description)
            recipe_id = self.cursor.lastrowid
            self.insert_serve()
            self.insert_quantities(recipe_id)
            name = input("Recipe name: ")

    def insert_quantities(self, recipe_id):
        ingredients = input("Input quantity of ingredient <press enter to stop>:").split()
        while ingredients:
            if len(ingredients) == 2:
                ingredients.insert(1, "")
            print(ingredients)
            quantity, measure, ingredient = ingredients
            quantity = int(quantity)
            possible_measures = self.find_measure(measure)
            if len(possible_measures) != 1:
                print("The measure is not conclusive!")
            else:
                possible_ingredients = self.find_ingredient(ingredient)
                if len(possible_ingredients) != 1:
                    print("The ingredient is not conclusive!")
                else:
                    self.insert_quantity(quantity, recipe_id, possible_ingredients[0][0], possible_measures[0][0])
            ingredients = input("Input quantity of ingredient <press enter to stop>:").split()

    def find_measure(self, measure):
        if measure == "":
            query = "SELECT measure_id from measures where measure_name = ''"
        else:
            query = f"SELECT measure_id from measures WHERE measure_name LIKE '{measure}%'"
        return self.cursor.execute(query).fetchall()

    def find_ingredient(self, ingredient):
        query = f"SELECT ingredient_id FROM ingredients WHERE ingredient_name LIKE '%{ingredient}%'"
        return self.cursor.execute(query).fetchall()

    def insert_quantity(self, amount, recipe_id, ingredient_id, measure_id):
        query = f"""INSERT INTO quantity (quantity, recipe_id, measure_id, ingredient_id) VALUES(
                {amount}, {recipe_id}, {measure_id}, {ingredient_id})
                """
        try:
            self.cursor.execute(query)
        except sqlite3.IntegrityError as e:
            print(e)
        self.conn.commit()

    def filter_recipe_per_meals(self):
        allowed_meals = surround_elements_with_quotes(args.meals)
        recipes_served_in_allowed_meals = f"""
        SELECT recipes.recipe_id FROM serve JOIN recipes ON serve.recipe_id = recipes.recipe_id 
        WHERE serve.meal_id IN  (SELECT meal_id FROM meals WHERE meal_name IN ({allowed_meals}))"""
        self.cursor.execute(recipes_served_in_allowed_meals)
        return set(self.cursor.fetchall())

    def print_requested_recipes(self):
        filtered_recipe_ids = self.filter_recipe_per_meals().intersection(self.filter_recipe_per_ingredients())
        if len(filtered_recipe_ids) == 0:
            print("There are no such recipes in the database.")
        else:
            recipe_names = self.find_recipe_names_by_id(filtered_recipe_ids)
            print(f"Recipes selected for you: {recipe_names.pop()[0]}")
            while len(recipe_names):
                print(f", {recipe_names.pop()}")

    def find_recipe_names_by_id(self, recipe_ids):
        selected_recipe_ids = tuple([recipe_id[0] for recipe_id in recipe_ids])
        if len(selected_recipe_ids) == 1:
            selected_recipe_ids = f"({selected_recipe_ids[0]})"

        query = f"SELECT recipe_name FROM recipes WHERE recipe_id IN {selected_recipe_ids}"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def filter_recipe_per_ingredients(self):
        ingredient_count = len(args.ingredients.split(","))
        ingredients = surround_elements_with_quotes(args.ingredients)

        recipes_with_all_requested_ingredients = f"""
        SELECT recipe_id FROM (SELECT recipe_id, ingredient_id FROM quantity 
            WHERE ingredient_id IN (SELECT ingredient_id FROM ingredients 
                WHERE ingredient_name IN ({ingredients})))GROUP BY recipe_id HAVING COUNT(*) >= {ingredient_count} """
        self.cursor.execute(recipes_with_all_requested_ingredients)
        return self.cursor.fetchall()


def create_database(name):
    return sqlite3.connect(name)


def insert_initial_data(database):
    data = {"meals": ("breakfast", "brunch", "lunch", "supper"),
        "ingredients": ("milk", "cacao", "strawberry", "blueberry", "blackberry", "sugar"),
        "measures": ("ml", "g", "l", "cup", "tbsp", "tsp", "dsp", "")}

    for table in data:
        field = table[:-1] + "_name"
        for value in data[table]:
            try:
                database.insert_value(table, field, value)
            except sqlite3.IntegrityError:  # If it is not the first run it will violate unique constraint
                pass


# "A,X,B" => "'A','X','B'"
def surround_elements_with_quotes(comma_separated_terms):
    return "'" + comma_separated_terms.replace(',', "','") + "'"


def main():
    db = Database(sys.argv[1])
    if args.ingredients and args.meals:
        db.print_requested_recipes()
    else:
        insert_initial_data(db)
        db.recipes_loop()
    db.conn.close()


main()
