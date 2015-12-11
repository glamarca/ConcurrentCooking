__author__ = 'sarace'

from django.conf.urls import url
app_name="cooking"

from .views import cooking,recipe,ingredient

urlpatterns = [
    url(r'^$', cooking.index,name='cooking_index'),
    url(r'^recipes/$',recipe.recipes_index,name="recipes_index"),
    url(r'^recipe/(?P<recipe_id>[0-9]+)',recipe.details,name='recipe_details'),
    url(r'^recipe/delete/(?P<recipe_id>[0-9]+)',recipe.delete,name='recipe_delete'),
    url(r'^recipes/search/$',recipe.search,name='recipe_search'),
    url(r'^recipes/recipe_form/(?P<recipe_id>[0-9]*)',recipe.recipe_form,name='recipe_form'),
    url(r'^recipes/add_modif/$',recipe.add_modify,name='recipe_add_modif'),
    url(r'^ingredients/$',ingredient.ingredients_index,name='ingredients_index'),
    url(r'^ingredient/(?P<ingredient_id>[0-9]+)',ingredient.details,name="ingredient_details"),
]
