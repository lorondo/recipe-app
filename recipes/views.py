from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, TemplateView
from .models import Recipe
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .forms import IngredientsSearchForm, RecipeForm
import pandas as pd
from .utils import get_chart

@login_required
def home(request):
    """
    View for the homepage. Renders a basic template for authenticated users.
    """
    return render(request, 'recipes/recipes_home.html')


@login_required
def ingredient_search(request):
    """
    View to handle ingredient search via form POST.
    Filters recipes by ingredient keyword and displays a chart of matched vs total.
    Converts matched recipes to a DataFrame for table rendering in the template.
    """
    form = IngredientsSearchForm(request.POST or None)
    ingredients_df = None  # DataFrame for displaying results in HTML table
    chart = None  # Base64 chart image (bar or pie)

    if request.method == 'POST':
        ingredient_name = request.POST.get('ingredient_name')
        chart_type = request.POST.get('chart_type')

        # Filter recipes containing the ingredient (case-insensitive match)
        qs = Recipe.objects.filter(ingredients__icontains=ingredient_name)
        total_recipes = Recipe.objects.count()
        matched_recipes = qs.count()

        # Data for chart visualization
        chart_data = pd.DataFrame({
            'category': ['Total Recipes', 'Recipes with Ingredient'],
            'count': [total_recipes, matched_recipes]
        })

        if matched_recipes > 0:
            df = pd.DataFrame(qs.values(
                'recipe_id', 'name', 'ingredients', 'cooking_time', 'difficulty'
            ))

            # Link each recipe name to its detail page
            df['name'] = df.apply(
                lambda row: f'<a href="/list/{row["recipe_id"]}">{row["name"]}</a>',
                axis=1
            )

            chart = get_chart(chart_type, chart_data)
            ingredients_df = df.to_html(escape=False, index=False)

    context = {
        'form': form,
        'ingredients_df': ingredients_df,
        'chart': chart,
    }

    return render(request, 'recipes/records.html', context)


@login_required
def add_recipe_view(request):
    """
    View to handle creation of new recipes via RecipeForm.
    Accepts both form data and uploaded image file.
    Redirects to recipe list on successful submission.
    """
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('recipe_list')
    else:
        form = RecipeForm()

    return render(request, 'recipes/add_recipe.html', {'form': form})


# ---------- Class-based views ----------

class RecipeListView(LoginRequiredMixin, ListView):
    """
    View to list all recipes for logged-in users.
    """
    model = Recipe
    template_name = 'recipes/main.html'


class RecipeDetailView(LoginRequiredMixin, DetailView):
    """
    View to show detailed information for a specific recipe.
    """
    model = Recipe
    template_name = 'recipes/detail.html'


class AboutView(LoginRequiredMixin, TemplateView):
    """
    View to render the 'About Me' page.
    """
    template_name = 'recipes/about_me.html'
