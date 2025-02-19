// Function to fetch the personalized message from the backend
function fetchMessage() {
    fetch('/api/message')
        .then(response => response.json())
        .then(data => {
            document.getElementById('message').textContent = data.message;
        })
        .catch(error => console.error('Error fetching message:', error));
}

// Function to generate a meal plan (You can modify this logic based on your needs)
function generateMealPlan() {
    // Simulating a meal plan generation process (this could be a backend request)
    const mealPlan = [
        'Breakfast: Oatmeal with berries and almonds',
        'Lunch: Grilled chicken salad with mixed greens',
        'Dinner: Quinoa with roasted vegetables and avocado',
        'Snack: Greek yogurt with honey and walnuts'
    ];

    const mealPlanContainer = document.createElement('ul');
    mealPlan.forEach(meal => {
        const listItem = document.createElement('li');
        listItem.textContent = meal;
        mealPlanContainer.appendChild(listItem);
    });

    const mealPlanSection = document.querySelector('.meal-plan-section');
    mealPlanSection.appendChild(mealPlanContainer);

    window.location.href = '/meal';
}

// Function to search for recipes based on user input
function searchRecipes() {
    const query = document.getElementById('recipe-query').value.trim();

    if (query === '') {
        alert('Please enter a recipe name or ingredient to search.');
        return;
    }

    // Simulating a recipe search (you can connect this to an API if needed)
    const recipes = [
        { name: 'Chicken Salad', ingredients: ['Chicken', 'Lettuce', 'Tomatoes'] },
        { name: 'Avocado Toast', ingredients: ['Avocado', 'Bread', 'Olive Oil'] },
        { name: 'Quinoa Bowl', ingredients: ['Quinoa', 'Vegetables', 'Avocado'] }
    ];

    const searchResults = recipes.filter(recipe =>
        recipe.name.toLowerCase().includes(query.toLowerCase()) ||
        recipe.ingredients.some(ingredient => ingredient.toLowerCase().includes(query.toLowerCase()))
    );

    const resultsContainer = document.createElement('ul');
    if (searchResults.length > 0) {
        searchResults.forEach(recipe => {
            const listItem = document.createElement('li');
            listItem.textContent = `${recipe.name}: Ingredients: ${recipe.ingredients.join(', ')}`;
            resultsContainer.appendChild(listItem);
        });
    } else {
        const noResultsItem = document.createElement('li');
        noResultsItem.textContent = 'No recipes found for your search.';
        resultsContainer.appendChild(noResultsItem);
    }

    const recipeSearchContainer = document.querySelector('.recipe-search');
    const existingResults = document.querySelector('.recipe-search ul');
    if (existingResults) existingResults.remove();
    recipeSearchContainer.appendChild(resultsContainer);
}
