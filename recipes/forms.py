from django import forms
from .models import Recipe

CHART__CHOICES = (          #specify choices as a tuple
   ('#1', 'Bar chart'),    # when user selects "Bar chart", it is stored as "#1"
   ('#2', 'Pie chart'),
   ('#3', 'Line chart')
   )

class IngredientsSearchForm(forms.Form):
  ingredient_name= forms.CharField(label='Ingredient', max_length=120)
  chart_type = forms.ChoiceField(choices=CHART__CHOICES)

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'ingredients', 'cooking_time', 'difficulty', 'pic']