from django.db import models
from django.core.validators import MaxValueValidator,MinValueValidator
from django.utils import timezone


class Recipe(models.Model):

    name = models.CharField(default='name',max_length=100,unique=True,null=False)
    global_time=models.IntegerField(null=True,validators=[MinValueValidator(1),MaxValueValidator(500)])
    preparation_time=models.IntegerField(null=True,validators=[MinValueValidator(1),MaxValueValidator(500)])
    waiting_time=models.IntegerField(null=True,validators=[MinValueValidator(1),MaxValueValidator(500)])
    difficulty=models.IntegerField(default=3,validators=[MinValueValidator(1),MaxValueValidator(5)])
    costs=models.IntegerField(default=3,validators=[MinValueValidator(1),MaxValueValidator(5)])
    num_people=models.IntegerField(default=4,validators=[MinValueValidator(1),MaxValueValidator(50)])
    created = models.DateTimeField(null=False)
    modified = models.DateTimeField(default=models.DateTimeField(default=timezone.now))
    user_mod = models.CharField(max_length=50,null=False)
    description = models.CharField(max_length=200,null=False)
    process = models.TextField(null=False)


    def  __str__(self):
        return self.name