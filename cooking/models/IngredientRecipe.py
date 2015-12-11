from django.db import models
from django.utils import timezone
from cooking.models.Ingredient import Ingredient
from cooking.models.Recipe import Recipe
from cooking.references.Enums import MEASUREMENT,GRAM

class IngredientRecipe(models.Model):

    recipe = models.ForeignKey(Recipe,on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient,on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=6,decimal_places=2,null=False,default=1)
    measurement = models.CharField(max_length=2,choices=MEASUREMENT,null=False,default=GRAM)
