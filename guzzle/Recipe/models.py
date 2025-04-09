from django.db import models
from django.contrib.auth.models import User

class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    instructions = models.TextField()
    duration = models.IntegerField()
    servings = models.IntegerField()
    calories = models.IntegerField()
    createdAt = models.DateTimeField(auto_now_add=True)

class Ingredient(models.Model):
    name = models.CharField(max_length=20)

class Tag(models.Model):
    name = models.CharField(max_length=20)

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.FloatField()
    unit = models.CharField(max_length=10)

class RecipeTag(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

