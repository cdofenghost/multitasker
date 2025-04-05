document.addEventListener("DOMContentLoaded", async function() {
  fetchAndDisplayCategories();
});
async function loadCategories() 
{
  
    const responseDiv = document.getElementById('response2');
    try {
        const response = await fetch("http://127.0.0.1:8000/category/all", {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(),
        });
        
        if (response.ok) {
            // Успешная регистрация
            responseDiv.innerHTML = `
    
            `;
            
        } else {
            // Ошибка на сервере
            const data = await response.json();
            errorMessage.textContent = data.detail || "Ошибка при регистрации";
            errorMessage.style.display = "block";
        }

        
    } catch (error) {
        // Ошибка сети или другая ошибка
        errorMessage.textContent = "Ошибка при отправке запроса";
        errorMessage.style.display = "block";
    }
}

async function fetchAndDisplayCategories() {
  const category_container = document.getElementById("category-container");
    try {
      // 1. Делаем GET-запрос к API
      const response = await fetch('http://127.0.0.1:8000/category/all');
      
      // Проверяем, что запрос успешен
      if (!response.ok) {
        throw new Error(`Ошибка HTTP: ${response.status}`);
      }
      
      // 2. Получаем данные (список категорий)
      const categories = await response.json();
      
      // 3. Создаем контейнер для категорий
      const container = document.createElement('div');
      console.log(categories);
      container.className = 'categories-container';
      
      // 4. Для каждой категории создаем HTML-элемент
      categories["categories"].forEach(category => {
        const categoryElement = document.createElement('div');
        const colorElement = document.createElement('div');

        categoryElement.className = 'category';
        categoryElement.style.display = "flex";
        categoryElement.style.alignItems = "center";
        categoryElement.style.padding = "12px";
        categoryElement.style.marginLeft = "12px";
        categoryElement.style.marginRight = "12px";
        categoryElement.style.backgroundColor = "#F5F5F5";
        categoryElement.style.borderRadius = "10px";
        categoryElement.style.marginBottom = "12px";
        // Устанавливаем цвет фона из данных категории
        colorElement.className = 'category-color';
        
        colorElement.style.backgroundColor = category.color;
        colorElement.style.width = "24px";
        colorElement.style.height = "48px";
        colorElement.style.display = "inline-block";
        colorElement.style.borderRadius = "4px";
        
        // Добавляем название категории
        const nameElement = document.createElement('span');
        nameElement.textContent = category.name;
        nameElement.className = 'category-name';
        nameElement.style.display = "inline-block";
        nameElement.style.fontFamily = "Ubuntu";
        nameElement.style.fontWeight = "500";
        nameElement.style.fontSize = "20px";
        nameElement.style.width = "100%";
        nameElement.style.textAlign = "left";
        
        categoryElement.appendChild(nameElement);
        categoryElement.appendChild(colorElement);
        container.appendChild(categoryElement);

        console.log(categoryElement);
      });
      
      // 5. Добавляем контейнер на страницу
      category_container.appendChild(container);
      
    } catch (error) {
      console.error('Ошибка при загрузке категорий:', error);
      // Можно добавить уведомление об ошибке на страницу
      const errorElement = document.createElement('div');
      errorElement.className = 'error';
      errorElement.textContent = 'Не удалось загрузить категории';
      category_container.appendChild(errorElement);
    }
  }
  

