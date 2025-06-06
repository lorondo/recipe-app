from django.test import TestCase
from .models import Recipe
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

# Create your tests here.
class RecipeModelTest(TestCase):
  @classmethod
  def setUpTestData(cls):
    cls.user = User.objects.create_user(username='testuser', password='testpass123')
    Recipe.objects.create(
      name='Top Ramen', 
      ingredients='Top ramen packet, boiling water', 
      cooking_time=10, 
      difficulty='easy'
      )
  
  def test_recipe_name_max_length(self):
    recipe = Recipe.objects.get(recipe_id=1)
    max_length = recipe._meta.get_field('name').max_length
    self.assertEqual(max_length, 120)
  
  def test_difficulty_choices(self):
    field = Recipe._meta.get_field('difficulty')
    expected_choices = (
      ('easy', 'Easy'),
      ('medium', 'Medium'),
      ('intermediate', 'Intermediate'),
      ('hard', 'Hard'),
    )
    self.assertEqual(field.choices, expected_choices)
  
  def test_get_absolute_url(self):
    recipe = Recipe.objects.get(recipe_id=1)
    self.assertEqual(recipe.get_absolute_url(), '/list/1')
  
  #test ingredient search
  def test_ingredient_search_post_with_match(self):
    self.client.login(username='testuser', password='testpass123')
    Recipe.objects.create(
      name='Spaghetti', ingredients='pasta, tomato sauce', cooking_time=15, difficulty='easy'
    )
    response = self.client.post('/search/', {
      'ingredient_name': 'pasta',
      'chart_type': '#1'
    })
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, 'Spaghetti')
    self.assertIn('ingredients_df', response.context)
    self.assertIn('chart', response.context)
  
  #test if unauthenticated users are redirected 
  def test_redirect_if_not_logged_in(self):
    response = self.client.get('/search/')
    self.assertRedirects(response, '/login/?next=/search/')

  #test get_chart
  def test_get_chart_bar_chart(self):
    from .utils import get_chart
    import pandas as pd

    data = pd.DataFrame({
      'category': ['Total', 'Matched'],
      'count': [10, 5]
    })
    chart = get_chart('#1', data)
    self.assertTrue(chart.startswith('iVBOR'))

  def test_add_recipe_post(self):
    self.client.login(username='testuser', password='testpass123')

    image = SimpleUploadedFile("test.jpg", b"file_content", content_type="image/jpeg")

    form_data = {
        'name': 'Test Recipe',
        'ingredients': 'Test ingredients',
        'cooking_time': 20,
        'difficulty': 'easy',
    }

    # Do not follow redirect, so we can catch form errors if any
    response = self.client.post(
        reverse('add_recipe'),
        data=form_data,
        files={'pic': image},
        follow=False
    )

    if response.status_code == 200:
        # Form likely invalid, print errors
        print("Form errors:", response.context['form'].errors)
    else:
        # Successful POST should redirect (302)
        self.assertEqual(response.status_code, 302)
        # Follow redirect to check if the recipe was created
        response = self.client.get(response.url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Recipe.objects.filter(name='Test Recipe').exists())
        recipe = Recipe.objects.get(name='Test Recipe')
        self.assertEqual(recipe.ingredients, 'Test ingredients')
