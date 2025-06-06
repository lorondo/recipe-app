# recipe-app
# Recipe App - Eating with Kindness

## Overview
Eating with Kindness is a simple and soothing recipe web application built with Django. It allows users to browse, view details, and search recipes by ingredients in an intuitive, calm interface.

## Features

- **Home Page:** Friendly welcome message with easy navigation links.
- **Recipe List:** View all recipes with clickable titles and images.
- **Recipe Detail:** Detailed recipe information including ingredients, cooking time, difficulty, and images.
- **Add Recipe:** Allows the user to add recipes to the recipe database.
- **Ingredient Search:** Search recipes by ingredient with a visual chart of results.
- **About Me:** Information about the developer with links to portfolio, LinkedIn, and GitHub.
- **User Authentication:** Login and logout functionality to secure pages.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/lorondo/recipe-app.git
    ```
2. Navigate to the project directory and create a virtual environment:
    ```bash
    cd recipe-app
    python -m venv venv
    ```
3. Activate the virtual environment:
    - On Windows:
      ```bash
      venv\Scripts\activate
      ```
    - On macOS/Linux:
      ```bash
      source venv/bin/activate
      ```
4. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
5. Apply database migrations:
    ```bash
    python manage.py migrate
    ```
6. Run the development server:
    ```bash
    python manage.py runserver
    ```

## Usage

- Visit `http://127.0.0.1:8000/` in your browser to open the Home page.
- Login with username "visitor" and password "test12345".
- Use the navigation menu to explore Recipes, Search, About Me, and more.
- Browse recipes, click on recipe titles to view details.
- Use the ingredient search to find recipes containing specific ingredients.
- Add more recipes into the database.
- Login/logout to manage your session.

## Technologies Used

- Python 3.x
- Django 4.x
- HTML5 & CSS3 (with a shared stylesheet for consistent styling)
- JavaScript (for navigation menu toggling)
- Pandas & Matplotlib (for generating search result charts)

## Developer

Alex Lindsay  
- Portfolio: [https://lorondo.github.io/portfolio-website/](https://lorondo.github.io/portfolio-website/)  
- LinkedIn: [https://www.linkedin.com/in/alex-lindsay-8097a755](https://www.linkedin.com/in/alex-lindsay-8097a755)  
- GitHub: [https://github.com/lorondo](https://github.com/lorondo)  

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
