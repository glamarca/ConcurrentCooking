# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-10 19:08
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('type', models.CharField(choices=[('VG', 'VEGETABLE'), ('MT', 'Meat'), ('FT', 'Fruit'), ('CL', 'Cereal'), ('SP', 'Spice'), ('MK', 'Milky'), ('SG', 'Sugar'), ('OL', 'Oil'), ('OT', 'Other')], default='OT', max_length=5)),
                ('created', models.DateTimeField()),
                ('modified', models.DateTimeField(default=models.DateTimeField(default=django.utils.timezone.now))),
                ('user_mod', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='IngredientRecipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(decimal_places=2, default=1, max_digits=6)),
                ('measurement', models.CharField(choices=[('KG', 'Kilo'), ('GR', 'Gram'), ('LT', 'Liter'), ('ML', 'Mililiter'), ('TS', 'Tea spoon'), ('SS', 'Soup spoon'), ('GL', 'Glas'), ('PC', 'Piece'), ('GT', 'Goute'), ('PI', 'Pinch')], default='GR', max_length=2)),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cooking.Ingredient')),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='name', max_length=100, unique=True)),
                ('global_time', models.TimeField(null=True)),
                ('preparation_time', models.TimeField(null=True)),
                ('waiting_time', models.TimeField(null=True)),
                ('difficulty', models.IntegerField(default=3, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('costs', models.IntegerField(default=3, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('num_people', models.IntegerField(default=4, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(50)])),
                ('created', models.DateTimeField()),
                ('modified', models.DateTimeField(default=models.DateTimeField(default=django.utils.timezone.now))),
                ('user_mod', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=200)),
                ('process', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='ingredientrecipe',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cooking.Recipe'),
        ),
    ]
