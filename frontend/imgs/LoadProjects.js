document.addEventListener("DOMContentLoaded", async function() {
  getCategory();
  fetchAndDisplayProjects();
});

const addButton = document.getElementById("add-button");
const href = window.location.href.split('/')
const id = href[href.length-1]

addButton.addEventListener("click", function() { window.location.replace(`http://127.0.0.1:8000/app/category/${id}/add-project`); } )

async function getCategory() {
  const category_name = document.getElementById("category-name");

  try {
    const response = await fetch(`http://127.0.0.1:8000/category/${Number(id)}`);
      
    // Проверяем, что запрос успешен
    if (!response.ok) {
      throw new Error(`Ошибка HTTP: ${response.status}`);
    }
    
    // 2. Получаем данные (список категорий)
    const category = await response.json();

    category_name.innerText = category.name;

    return category;
  } catch (error) {
    console.error('Ошибка при загрузке категорий:', error);
  }
}

async function fetchAndDisplayProjects() {
  const project_container = document.getElementById("project-container");
  
    try {
      const response = await fetch(`http://127.0.0.1:8000/project/all/${Number(id)}`);
      
      const category = await getCategory();

      // Проверяем, что запрос успешен
      if (!response.ok) {
        throw new Error(`Ошибка HTTP: ${response.status}`);
      }
      
      // 2. Получаем данные (список категорий)
      const projects = await response.json();
      
      // 3. Создаем контейнер для категорий
      const container = document.createElement('div');
      console.log(projects);
      container.className = 'projects-container';
      container.style.padding = "12px";
      
      // 4. Для каждой категории создаем HTML-элемент
      projects.forEach(project => {
        const projectElement = document.createElement('div');

        projectElement.className = 'project';
        projectElement.id = project.id;
        projectElement.style.padding = "12px";
        projectElement.style.backgroundColor = "#F5F5F5";
        projectElement.style.borderRadius = "10px";
        projectElement.style.marginBottom = "12px";
        projectElement.style.textAlign = "left";

        projectElement.onclick = () => window.location.replace("http://127.0.0.1:8000/app/category");
        // Устанавливаем цвет фона из данных категории
        
        // Добавляем название категории
        const nameElement = document.createElement('span');
        nameElement.textContent = project.name;
        nameElement.className = 'project-name';
        nameElement.style.fontFamily = "Ubuntu";
        nameElement.style.fontWeight = "500";
        nameElement.style.fontSize = "20px";
        nameElement.style.width = "100%";
        nameElement.style.textAlign = "left";

        const categoryNameElement = document.createElement('div');
        categoryNameElement.innerText = category.name;
        categoryNameElement.style.backgroundColor = category.color;
        categoryNameElement.style.borderRadius = "10px";
        categoryNameElement.style.padding = "6px";
        categoryNameElement.style.width = "max-content";
        categoryNameElement.style.marginTop = "12px";
        
        projectElement.appendChild(nameElement);
        projectElement.appendChild(categoryNameElement);
        container.appendChild(projectElement);

        console.log(projectElement);
      });
      
      // 5. Добавляем контейнер на страницу
      project_container.appendChild(container);
      
    } catch (error) {
      console.error('Ошибка при загрузке категорий:', error);
      // // Можно добавить уведомление об ошибке на страницу
      // const errorElement = document.createElement('div');
      // errorElement.className = 'error';
      // errorElement.textContent = 'Не удалось загрузить категории';
      // projects_container.appendChild(errorElement);
    }
  }
  

