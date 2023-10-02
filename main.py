from sqlalchemy import create_engine, Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import random

Base = declarative_base()

recipe_ingredient_association = Table('recipe_ingredient_association', Base.metadata,
    Column('recipe_id', Integer, ForeignKey('recipe.id')),
    Column('ingredient_id', Integer, ForeignKey('ingredient.id')),
    Column('quantity', String)
)

recipe_category_association = Table('recipe_category_association', Base.metadata,
    Column('recipe_id', Integer, ForeignKey('recipe.id')),
    Column('category_id', Integer, ForeignKey('recipe_category.id'))
)

class Recipe(Base):
    __tablename__ = 'recipe'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    instructions = Column(String)
    ingredients = relationship("Ingredient", secondary=recipe_ingredient_association, back_populates="recipes")
    categories = relationship("RecipeCategory", secondary=recipe_category_association, back_populates="recipes")

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

class Ingredient(Base):
    __tablename__ = 'ingredient'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    recipes = relationship("Recipe", secondary=recipe_ingredient_association, back_populates="ingredients")

class RecipeCategory(Base):
    __tablename__ = 'recipe_category'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    recipes = relationship("Recipe", secondary=recipe_category_association, back_populates="categories")

class RecipeBook:
    def __init__(self):
        self.engine = create_engine('sqlite:///recipe_book.db')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def add_recipe(self, recipe):
        self.session.add(recipe)
        self.session.commit()

    def remove_recipe(self, recipe):
        self.session.delete(recipe)
        self.session.commit()

    def search_recipe(self, query):
        return self.session.query(Recipe).filter(Recipe.name.ilike('%' + query + '%')).all()

    def add_to_grocery_list(self, ingredients):
        for ingredient in ingredients:
            if not self.session.query(Ingredient).filter(Ingredient.name.ilike(ingredient)).first():
                self.session.add(Ingredient(name=ingredient))
        self.session.commit()

    def remove_from_grocery_list(self, ingredient):
        ingredient_obj = self.session.query(Ingredient).filter(Ingredient.name.ilike(ingredient)).first()
        if ingredient_obj:
            self.session.delete(ingredient_obj)
            self.session.commit()

    def get_random_recipe(self):
        return random.choice(self.session.query(Recipe).all())


recipe_book = RecipeBook()

recipe1 = Recipe(name="Spaghetti Carbonara", instructions="1. Cook spaghetti until al dente, 2. Cook bacon in a large skillet until crispy. 3. In a bowl, whisk together eggs and parmesan cheese. 4. Add garlic to the bacon and cook for 1 minute. 5. Add spaghetti to the skillet and toss with bacon and garlic. 6. Pour the egg mixture over the spaghetti and toss until the eggs are cooked. Serve hot.")
recipe2 = Recipe(name="Chicken Parmesan", instructions="1. Preheat oven to 400°F. 2. Coat chicken breast in beaten eggs, then coat in breadcrumbs mixed with parmesan cheese. 3. Place chicken in a baking dish and bake for 20-25 minutes. 4. Spoon marinara sauce over chicken and top with mozzarella cheese. 5. Bake for an additional 10-15 minutes. Serve hot.")
recipe3 = Recipe(name="ugali", instructions="1. Boil water for 10mins 2. add flour when water boils.  3. stir untill ready. Serve hot.")

recipe1.ingredients.append(Ingredient(name="spaghetti"))
recipe1.ingredients.append(Ingredient(name="eggs"))
recipe1.ingredients.append(Ingredient(name="bacon"))
recipe1.ingredients.append(Ingredient(name="parmesan cheese"))
recipe1.ingredients.append(Ingredient(name="garlic"))
recipe1.ingredients.append(Ingredient(name="olive oil"))

recipe2.ingredients.append(Ingredient(name="chicken breast"))
recipe2.ingredients.append(Ingredient(name="breadcrumbs"))
recipe2.ingredients.append(Ingredient(name="parmesan cheese"))
recipe2.ingredients.append(Ingredient(name="eggs"))
recipe2.ingredients.append(Ingredient(name="marinara sauce"))
recipe2.ingredients.append(Ingredient(name="mozzarella cheese"))

recipe3.ingredients.append(Ingredient(name="chicken breast"))
recipe3.ingredients.append(Ingredient(name="breadcrumbs"))
recipe3.ingredients.append(Ingredient(name="parmesan cheese"))
recipe3.ingredients.append(Ingredient(name="eggs"))
recipe3.ingredients.append(Ingredient(name="marinara sauce"))
recipe3.ingredients.append(Ingredient(name="mozzarella cheese"))

recipe_book.add_recipe(recipe1)
recipe_book.add_recipe(recipe2)
recipe_book.add_recipe(recipe3)


# Searching for a recipe
query = "spaghetti"
search_results = recipe_book.search_recipe(query)
print("Search results for '{}':".format(query))
for recipe in search_results:
    print(recipe)

# Adding ingredients
recipe = recipe_book.get_random_recipe()
print("Adding ingredients for '{}' to grocery list...".format(recipe))
recipe_book.add_to_grocery_list([ingredient.name for ingredient in recipe.ingredients])

# Removing ingredient 
ingredient = recipe.ingredients[0].name
print("Removing '{}' from grocery list...".format(ingredient))
recipe_book.remove_from_grocery_list(ingredient)
