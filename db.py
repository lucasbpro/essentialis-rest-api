from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# materials_by_recipe = db.Table('materials_by_recipe',
#         db.Column('material_id', db.Integer, db.ForeignKey('raw_materials.material_id')),
#         db.Column('recipe_id', db.Integer, db.ForeignKey('recipes.recipe_id'))
#         )
