from django.db import models
from django.utils import timezone
from cooking.references.Enums import INGREDIENT_TYPES, OTHER


class Ingredient(models.Model):
    """
    Ingredient model
    """
    name = models.CharField(max_length=50, unique=True, null=False)
    type = models.CharField(max_length=5, choices=INGREDIENT_TYPES, null=False, default=OTHER)
    created = models.DateTimeField(default=models.DateTimeField(default=timezone.now))
    modified = models.DateTimeField(default=models.DateTimeField(default=timezone.now))
    user_mod = models.CharField(max_length=50, null=False)

    def __str__(self):
        return self.name