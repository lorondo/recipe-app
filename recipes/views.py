from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, TemplateView
from .models import Recipe
#to protect class-based view
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .forms import IngredientsSearchForm, RecipeForm
import pandas as pd
from .utils import get_chart

@login_required
def home(request):
   return render(request, 'recipes/recipes_home.html')

#define function-based view - ingredient_search()
@login_required
def ingredient_search(request):
    form = IngredientsSearchForm(request.POST or None)
    ingredients_df=None #initialize dataframe to None
    chart=None

    #check if the button is clicked
    if request.method =='POST':
        #read ingredient_name
        ingredient_name = request.POST.get('ingredient_name')
        chart_type = request.POST.get('chart_type')

        #apply filter to extract data
        qs =Recipe.objects.filter(ingredients__icontains=ingredient_name)
        total_recipes = Recipe.objects.count()
        matched_recipes = qs.count()

        chart_data = pd.DataFrame({
            'category': ['Total Recipes', 'Recipes With Ingredient'],
            'count': [total_recipes, matched_recipes]
            })

        if matched_recipes > 0: #if data found
            df = pd.DataFrame(qs.values('recipe_id', 'name', 'ingredients', 'cooking_time', 'difficulty'))
            df['name'] = df.apply(
                lambda row: f'<a href="/list/{row["recipe_id"]}">{row["name"]}</a>',
                axis=1
            )

            chart_data = pd.DataFrame({
                'category': ['Total Recipes', 'Recipes with Ingredient'],
                'count': [total_recipes, matched_recipes]
            })

            #call get_chart by passing chart_type from user input, sales dataframe and labels
            chart=get_chart(chart_type, chart_data)

            #convert the dataframe to HTML
            ingredients_df=df.to_html(escape=False, index=False)
        else:
            ingredients_df = None
        
        #display in terminal - for testing and dev only
        '''
        print (ingredient_name)

        print ('Exploring querysets:')
        print ('Case 1: Output of Recipe.objects.all()')
        qs=Recipe.objects.all()
        print (qs)

        print ('Case 2: Output of Recipe.objects.filter(ingredients__icontains=ingredient_name)')
        qs =Recipe.objects.filter(ingredients__icontains=ingredient_name)
        print (qs)

        print ('Case 3: Output of qs.values')
        print (qs.values())

        print ('Case 4: Output of qs.values_list()')
        print (qs.values_list())

        print ('Case 5: Output of Recipe.objects.get(id=1)')
        obj = Recipe.objects.get(recipe_id=1)
        print (obj)
        '''

    context={
        'form': form,
        'ingredients_df': ingredients_df,
        'chart': chart,
    }

    return render(request, 'recipes/records.html', context)

@login_required
def add_recipe_view(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('recipe_list')
    else: 
        form = RecipeForm()
        
    return render(request, 'recipes/add_recipe.html', {'form': form})

# Create your views here.

class RecipeListView(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = 'recipes/main.html'

class RecipeDetailView(LoginRequiredMixin, DetailView):
    model = Recipe
    template_name = 'recipes/detail.html'

class AboutView(LoginRequiredMixin, TemplateView):
    template_name = 'recipes/about_me.html'
