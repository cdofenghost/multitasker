document.addEventListener("DOMContentLoaded", async function() {
  getProject();
  fetchAndDisplayTasks();
});

const addButton = document.getElementById("add-button");
const href = window.location.href.split('/')
const id = href[href.length-1]

addButton.addEventListener("click", function() { window.location.replace(`http://127.0.0.1:8000/app/project/${id}/add-task`); } )

async function getPerformer(performer_id) {
  try {
    const response = await fetch(`http://127.0.0.1:8000/users?user_id=${performer_id}`);
      
    // Проверяем, что запрос успешен
    if (!response.ok) {
      throw new Error(`Ошибка HTTP: ${response.status}`);
    }
    
    // 2. Получаем данные (список категорий)
    const performer = await response.json();

    return performer;
  } catch (error) {
    console.error('Ошибка при загрузке категорий:', error);
  }
}

async function getCategory(category_id) {
  try {
    const response = await fetch(`http://127.0.0.1:8000/category/${category_id}`);
      
    // Проверяем, что запрос успешен
    if (!response.ok) {
      throw new Error(`Ошибка HTTP: ${response.status}`);
    }
    
    // 2. Получаем данные (список категорий)
    const category = await response.json();

    return category;
  } catch (error) {
    console.error('Ошибка при загрузке категорий:', error);
  }
}

async function getProject() {
  const project_name = document.getElementById("project-name");

  try {
    const response = await fetch(`http://127.0.0.1:8000/project?project_id=${id}`);
      
    // Проверяем, что запрос успешен
    if (!response.ok) {
      throw new Error(`Ошибка HTTP: ${response.status}`);
    }
    
    // 2. Получаем данные (список категорий)
    const project = await response.json();

    project_name.innerText = project.name;

    return project;
  } catch (error) {
    console.error('Ошибка при загрузке категорий:', error);
  }
}

async function fetchAndDisplayTasks() {
  const task_container = document.getElementById("task-container");
  
    try {
      const response = await fetch(`http://127.0.0.1:8000/task/all?project_id=${Number(id)}`);
      
      const project = await getProject();
      const category = await getCategory(project.category_id);

      // Проверяем, что запрос успешен
      if (!response.ok) {
        throw new Error(`Ошибка HTTP: ${response.status}`);
      }
      
      // 2. Получаем данные (список категорий)
      const tasks = await response.json();
      
      // 3. Создаем контейнер для категорий
      const container = document.createElement('div');
      console.log(tasks);
      container.className = 'tasks-container';
      container.style.padding = "12px";
      
      // 4. Для каждой категории создаем HTML-элемент
      for (const task of tasks) {
        const taskElement = document.createElement('div');

        taskElement.className = 'task';
        taskElement.id = task.id;
        taskElement.style.padding = "12px";
        taskElement.style.backgroundColor = "#F5F5F5";
        taskElement.style.borderRadius = "10px";
        taskElement.style.marginBottom = "12px";
        taskElement.style.textAlign = "left";

        // Устанавливаем цвет фона из данных категории
        
        // Добавляем название категории
        const nameElement = document.createElement('span');
        nameElement.textContent = task.name;
        nameElement.className = 'task-name';
        nameElement.style.fontFamily = "Ubuntu";
        nameElement.style.fontWeight = "500";
        nameElement.style.fontSize = "20px";
        nameElement.style.width = "100%";
        nameElement.style.textAlign = "left";

        const categoryNameElement = document.createElement('div');
        const priorityElement = document.createElement('img');
        const priorityContainerElement = document.createElement('div');
        const secondRowElement = document.createElement('div');

        secondRowElement.style.textAlign = "left";
        secondRowElement.style.display = "flex";
        secondRowElement.style.verticalAlign = "top";
        secondRowElement.style.marginTop = "12px";

        categoryNameElement.innerText = category.name;
        categoryNameElement.style.backgroundColor = category.color;
        categoryNameElement.style.borderRadius = "10px";

        if (findColorWithMaxBrightness(category.color) < 150) { categoryNameElement.style.color = "white"; }

        categoryNameElement.style.borderRadius = "10px";
        categoryNameElement.style.padding = "6px";
        categoryNameElement.style.width = "max-content";

        priorityElement.src = `/static/${task.priority}p.png`;
        priorityContainerElement.appendChild(priorityElement);
        priorityContainerElement.style.alignContent = "center";
        priorityContainerElement.style.height = "max-content";

        secondRowElement.appendChild(categoryNameElement);
        secondRowElement.appendChild(priorityContainerElement);

        const performer = await getPerformer(task.performer_id);
        const performerNameElement = document.createElement('div');
        
        performerNameElement.style.marginTop = "6px";
        performerNameElement.style.fontSize = "14px";
        performerNameElement.innerText = performer.name;

        taskElement.appendChild(nameElement);
        taskElement.appendChild(secondRowElement);
        taskElement.appendChild(performerNameElement);

        taskElement.onclick = () => window.location.replace(`http://127.0.0.1:8000/app/task/${task.id}`);
        container.appendChild(taskElement);

        console.log(taskElement);
      };
      
      // 5. Добавляем контейнер на страницу
      task_container.appendChild(container);
      
    } catch (error) {
      console.error('Ошибка при загрузке категорий:', error);
      // // Можно добавить уведомление об ошибке на страницу
      // const errorElement = document.createElement('div');
      // errorElement.className = 'error';
      // errorElement.textContent = 'Не удалось загрузить категории';
      // projects_container.appendChild(errorElement);
    }
  }

  function findColorWithMaxBrightness(color) {
    console.log(color, color.length);
    var r, g, b;
    if (color.length == 7)
    {
      r = color[1] + color[2];
      g = color[3] + color[4];
      b = color[5] + color[6];
    }

    else if (color.length == 4)
    {
      r = color[1];
      g = color[2];
      b = color[3];
    }

    else { return 255; }

    console.log("number: " + Math.max(Number("0x"+r), Number("0x"+g), Number("0x"+b)));
    return Math.max(Number("0x"+r), Number("0x"+g), Number("0x"+b));

  }
  

