document.addEventListener("DOMContentLoaded", function(){
    // Attach event listeners for each meal section
    const mealSections = document.querySelectorAll('.meal-section');
    
    mealSections.forEach(section => {
        const searchBtn = section.querySelector('.food-search-btn');
        const searchInput = section.querySelector('.food-search-input');
        const resultsDiv = section.querySelector('.search-results');
        const mealList = section.querySelector('.meal-list');
        
        searchBtn.addEventListener('click', function(){
            const query = searchInput.value.trim();
            if(query === '') return;
            // Add an "active" class to show the dropdown
            section.querySelector('.meal-search').classList.add('active');
            // Fetch search results from our API endpoint
            fetch(`/api/food_search?query=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(data => {
                // Clear any previous results
                resultsDiv.innerHTML = "";
                if(data.products && data.products.length > 0) {
                    // Create a dropdown list (ul) for results
                    const ul = document.createElement('ul');
                    data.products.forEach(product => {
                        const li = document.createElement('li');
                        li.textContent = (product.brands ? product.brands + " - " : "") + (product.product_name || "Unknown Product");
                        li.addEventListener('click', function(){
                            // When a product is selected, create a meal item element
                            const itemDiv = document.createElement('div');
                            itemDiv.className = 'meal-item';
                            
                            // Extract nutritional info (fallback to 0 if missing)
                            const nutriments = product.nutriments || {};
                            const cal = parseFloat(nutriments["energy-kcal_100g"]) || 0;
                            const fat = parseFloat(nutriments["fat_100g"]) || 0;
                            const carbs = parseFloat(nutriments["carbohydrates_100g"]) || 0;
                            const protein = parseFloat(nutriments["proteins_100g"]) || 0;
                            const sodium = parseFloat(nutriments["sodium_100g"]) || 0;
                            
                            // Set data attributes so we can remove and update macros later
                            itemDiv.setAttribute('data-calories', cal);
                            itemDiv.setAttribute('data-fat', fat);
                            itemDiv.setAttribute('data-carbs', carbs);
                            itemDiv.setAttribute('data-protein', protein);
                            itemDiv.setAttribute('data-sodium', sodium);
                            
                            // Display detailed product info
                            itemDiv.innerHTML = `<span>Brand: ${product.brands || "Unknown Brand"}, Item: ${product.product_name || "Unknown Product"}, Calories: ${cal} kcal, Fat: ${fat}g, Carbs: ${carbs}g, Protein: ${protein}g, Sodium: ${sodium}g</span>`;
                            
                            const removeBtn = document.createElement('span');
                            removeBtn.className = 'remove-btn';
                            removeBtn.textContent = '×';
                            removeBtn.addEventListener('click', function(e){
                                e.stopPropagation();
                                itemDiv.remove();
                                updateMealSectionSummary(section);
                                updateDailySummary();
                            });
                            itemDiv.appendChild(removeBtn);
                            
                            mealList.appendChild(itemDiv);
                            
                            // Update summary for this meal section
                            updateMealSectionSummary(section);
                            // Update overall daily summary
                            updateDailySummary();
                            
                            // Clear search results and input field, remove "active" class
                            resultsDiv.innerHTML = "";
                            searchInput.value = "";
                            section.querySelector('.meal-search').classList.remove('active');
                        });
                        ul.appendChild(li);
                    });
                    resultsDiv.appendChild(ul);
                } else {
                    resultsDiv.textContent = "No results found.";
                }
            })
            .catch(err => {
                console.error(err);
                resultsDiv.textContent = "Error fetching results.";
            });
        });
    });
    
    // Function to update a meal section summary by iterating over its meal items
    function updateMealSectionSummary(section) {
        const mealList = section.querySelector('.meal-list');
        let macros = { calories: 0, fat: 0, carbs: 0, protein: 0, sodium: 0 };
        const items = mealList.querySelectorAll('.meal-item');
        items.forEach(item => {
            macros.calories += parseFloat(item.getAttribute('data-calories'));
            macros.fat += parseFloat(item.getAttribute('data-fat'));
            macros.carbs += parseFloat(item.getAttribute('data-carbs'));
            macros.protein += parseFloat(item.getAttribute('data-protein'));
            macros.sodium += parseFloat(item.getAttribute('data-sodium'));
        });
        const summaryDiv = section.querySelector('.meal-summary');
        summaryDiv.textContent = `Total: Calories: ${macros.calories.toFixed(1)} kcal, Fat: ${macros.fat.toFixed(1)}g, Carbs: ${macros.carbs.toFixed(1)}g, Protein: ${macros.protein.toFixed(1)}g, Sodium: ${macros.sodium.toFixed(1)}g`;
    }
    
    // Function to update the overall daily summary by summing each meal section's summary
    function updateDailySummary() {
        let overall = { calories: 0, fat: 0, carbs: 0, protein: 0, sodium: 0 };
        const mealSections = document.querySelectorAll('.meal-section');
        mealSections.forEach(section => {
            const mealList = section.querySelector('.meal-list');
            const items = mealList.querySelectorAll('.meal-item');
            items.forEach(item => {
                overall.calories += parseFloat(item.getAttribute('data-calories'));
                overall.fat += parseFloat(item.getAttribute('data-fat'));
                overall.carbs += parseFloat(item.getAttribute('data-carbs'));
                overall.protein += parseFloat(item.getAttribute('data-protein'));
                overall.sodium += parseFloat(item.getAttribute('data-sodium'));
            });
        });
        const dailySummary = document.getElementById('daily-summary');
        dailySummary.innerHTML = `<h2>Daily Summary</h2>
            <p>Total: Calories: ${overall.calories.toFixed(1)} kcal, Fat: ${overall.fat.toFixed(1)}g, Carbs: ${overall.carbs.toFixed(1)}g, Protein: ${overall.protein.toFixed(1)}g, Sodium: ${overall.sodium.toFixed(1)}g</p>`;
    }
  });
  