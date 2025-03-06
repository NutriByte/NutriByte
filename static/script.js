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
    fetch('/api/generate-meal-plan')
        .then(response => response.json())
        .then(data => {
            // Store the meal plan data in sessionStorage before redirecting
            sessionStorage.setItem('mealPlanData', JSON.stringify(data));
            window.location.href = '/meal';
        })
        .catch(error => {
            console.error('Error generating meal plan:', error);
            alert('Failed to generate meal plan. Please try again.');
        });
}

// Add this new function to display meal plan on the meal page
function displayMealPlan() {
    const mealPlanData = JSON.parse(sessionStorage.getItem('mealPlanData'));
    console.log('Meal Plan Data:', mealPlanData); // Debug log
    
    if (!mealPlanData) {
        console.log('No meal plan data found in sessionStorage');
        return;
    }

    const mealPlanContainer = document.createElement('ul');
    mealPlanContainer.classList.add('meal-list'); // Add a class for styling
    
    mealPlanData.meals.forEach(meal => {
        const listItem = document.createElement('li');
        listItem.textContent = meal;
        mealPlanContainer.appendChild(listItem);
        console.log('Added meal:', meal); // Debug log
    });

    const mealPlanSection = document.querySelector('.meal-plan-section');
    if (!mealPlanSection) {
        console.log('Could not find meal-plan-section element'); // Debug log
        return;
    }
    
    mealPlanSection.innerHTML = ''; // Clear existing content
    mealPlanSection.appendChild(mealPlanContainer);
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

// Add these functions for meal management
function loadCustomMeals() {
    if (!document.getElementById('customMealsList')) return;
    
    fetch('/api/meals')
        .then(response => response.json())
        .then(data => {
            const mealsList = document.getElementById('customMealsList');
            mealsList.innerHTML = '';
            
            data.meals.forEach(meal => {
                const mealItem = document.createElement('div');
                mealItem.className = 'meal-item';
                mealItem.innerHTML = `
                    <span>${meal.type}: ${meal.name}</span>
                    <button onclick="deleteMeal('${meal.name}')">Delete</button>
                `;
                mealsList.appendChild(mealItem);
            });
        })
        .catch(error => console.error('Error loading custom meals:', error));
}

function addMeal(event) {
    event.preventDefault();
    const form = event.target;
    const mealData = {
        type: form.type.value,
        name: form.name.value
    };

    fetch('/api/meals', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(mealData)
    })
    .then(response => response.json())
    .then(() => {
        form.reset();
        loadCustomMeals();
    })
    .catch(error => console.error('Error adding meal:', error));
}

function deleteMeal(mealName) {
    fetch('/api/meals', {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ name: mealName })
    })
    .then(response => response.json())
    .then(() => loadCustomMeals())
    .catch(error => console.error('Error deleting meal:', error));
}

// Add event listeners when the page loads
document.addEventListener('DOMContentLoaded', () => {
    const addMealForm = document.getElementById('addMealForm');
    if (addMealForm) {
        addMealForm.addEventListener('submit', addMeal);
        loadCustomMeals();
    }
});
