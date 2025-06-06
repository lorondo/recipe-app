from django.db import models
from django.shortcuts import reverse

# Create your models here.
difficulty_choices=(
    ('easy', 'Easy'),
    ('medium', 'Medium'),
    ('intermediate', 'Intermediate'),
    ('hard', 'Hard'),
)

class Recipe(models.Model):
  recipe_id=models.AutoField(primary_key=True)
  name=models.CharField(max_length=120)
  ingredients=models.TextField(default="no ingredients")
  cooking_time=models.FloatField(help_text="in minutes")
  difficulty=models.CharField(max_length=20, choices=difficulty_choices, default='easy')
  pic = models.ImageField(upload_to='recipes', default='no_picture.jpg')

  def __str__(self):
        return str(self.name)
  
  def get_absolute_url(self):
       return reverse ('detail', kwargs={'pk': self.pk})
