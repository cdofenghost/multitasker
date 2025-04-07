document.addEventListener("DOMContentLoaded", async function() {
  fetchAndDisplayAllocatedTasks();
  fetchAndDisplayAuthoredTasks();
});
const authored_container = document.getElementById("authored-task-container");
const allocated_container = document.getElementById("allocated-task-container");

function switchToAllocated() {
  const authoredButton = document.getElementById("authored-button");
  const allocatedButton = document.getElementById("allocated-button");
  
  authoredButton.className = "free-button";
  allocatedButton.className = "chosen-button";

  authored_container.style.display = "none";
  allocated_container.style.display = "block";
}

function switchToAuthored() {
  const authoredButton = document.getElementById("authored-button");
  const allocatedButton = document.getElementById("allocated-button");

  authoredButton.className = "chosen-button";
  allocatedButton.className = "free-button";

  authored_container.style.display = "block";
  allocated_container.style.display = "none";
}

async function fetchAndDisplayAuthoredTasks() {
  const task_container = document.getElementById("authored-task-container");
    try {
      // 1. Делаем GET-запрос к API
      const response = await fetch('http://127.0.0.1:8000/task/authored');
      
      // Проверяем, что запрос успешен
      if (!response.ok) {
        throw new Error(`Ошибка HTTP: ${response.status}`);
      }
      
      // 2. Получаем данные (список категорий)
      const tasks = await response.json();
      
      // 3. Создаем контейнер для категорий
      const container = document.createElement('div');
      console.log(tasks);
      container.className = 'categories-container';
      
      // 4. Для каждой категории создаем HTML-элемент
      tasks.forEach(task => {
        const categoryElement = document.createElement('div');
        const colorElement = document.createElement('div');

        categoryElement.className = 'category';
        categoryElement.id = task.id;
        categoryElement.style.display = "flex";
        categoryElement.style.alignItems = "center";
        categoryElement.style.padding = "12px";
        categoryElement.style.marginLeft = "12px";
        categoryElement.style.marginRight = "12px";
        categoryElement.style.backgroundColor = "#F5F5F5";
        categoryElement.style.borderRadius = "10px";
        categoryElement.style.marginBottom = "12px";
        // categoryElement.onclick = () => window.location.replace(`http://127.0.0.1:8000/app/category/${task.id}`);
        // Устанавливаем цвет фона из данных категории
        
        // Добавляем название категории
        const nameElement = document.createElement('span');
        nameElement.textContent = task.name;
        nameElement.className = 'category-name';
        nameElement.style.display = "inline-block";
        nameElement.style.fontFamily = "Ubuntu";
        nameElement.style.fontWeight = "500";
        nameElement.style.fontSize = "20px";
        nameElement.style.width = "100%";
        nameElement.style.textAlign = "left";
        
        categoryElement.appendChild(nameElement);
        container.appendChild(categoryElement);

        console.log(categoryElement);
      });
      
      // 5. Добавляем контейнер на страницу
      task_container.appendChild(container);
      
    } catch (error) {
      console.error('Ошибка при загрузке категорий:', error);
      // Можно добавить уведомление об ошибке на страницу
      const errorElement = document.createElement('div');
      errorElement.className = 'error';
      errorElement.textContent = 'Не удалось загрузить категории';
      task_container.appendChild(errorElement);
    }
}

async function fetchAndDisplayAllocatedTasks() {
  const task_container = document.getElementById("allocated-task-container");
  task_container.style.display = "none";
    try {
      // 1. Делаем GET-запрос к API
      const response = await fetch('http://127.0.0.1:8000/task/allocated');
      
      // Проверяем, что запрос успешен
      if (!response.ok) {
        throw new Error(`Ошибка HTTP: ${response.status}`);
      }
      
      // 2. Получаем данные (список категорий)
      const tasks = await response.json();
      
      // 3. Создаем контейнер для категорий
      const container = document.createElement('div');
      console.log(tasks);
      container.className = 'categories-container';
      
      // 4. Для каждой категории создаем HTML-элемент
      tasks.forEach(task => {
        const categoryElement = document.createElement('div');
        const colorElement = document.createElement('div');

        categoryElement.className = 'category';
        categoryElement.id = task.id;
        categoryElement.style.display = "flex";
        categoryElement.style.alignItems = "center";
        categoryElement.style.padding = "12px";
        categoryElement.style.marginLeft = "12px";
        categoryElement.style.marginRight = "12px";
        categoryElement.style.backgroundColor = "#F5F5F5";
        categoryElement.style.borderRadius = "10px";
        categoryElement.style.marginBottom = "12px";
        // categoryElement.onclick = () => window.location.replace(`http://127.0.0.1:8000/app/category/${task.id}`);
        // Устанавливаем цвет фона из данных категории
        
        // Добавляем название категории
        const nameElement = document.createElement('span');
        nameElement.textContent = task.name;
        nameElement.className = 'category-name';
        nameElement.style.display = "inline-block";
        nameElement.style.fontFamily = "Ubuntu";
        nameElement.style.fontWeight = "500";
        nameElement.style.fontSize = "20px";
        nameElement.style.width = "100%";
        nameElement.style.textAlign = "left";
        
        categoryElement.appendChild(nameElement);
        container.appendChild(categoryElement);

        console.log(categoryElement);
      });
      
      // 5. Добавляем контейнер на страницу
      task_container.appendChild(container);
      
    } catch (error) {
      console.error('Ошибка при загрузке категорий:', error);
      // Можно добавить уведомление об ошибке на страницу
      const errorElement = document.createElement('div');
      errorElement.className = 'error';
      errorElement.textContent = 'Не удалось загрузить категории';
      task_container.appendChild(errorElement);
    }
}
  

