document.addEventListener("DOMContentLoaded", async function() {
    loadTask();
});

const href = window.location.href.split('/');
const taskId = href[href.length-1];
const addButton = document.getElementById('add-button');
addButton.addEventListener('click', () => { window.location.replace(`http://127.0.0.1:8000/app/task/${taskId}/add-subtask`)});

const taskContainerElement = document.getElementById('task-container');
const taskNameElement = document.getElementById('task-name');
const taskStatBarElement = document.getElementById('stat-bar');
const taskDescElement = document.getElementById('task-desc');
const taskDeadlineElement = document.getElementById('task-deadline');
const taskPerformerElement = document.getElementById('performer');
const taskPerformerIconElement = document.getElementById('performer-icon');
const taskAuthorIconElement = document.getElementById('author-icon');
const taskAuthorElement = document.getElementById('author');
const taskDateUpdatedElement = document.getElementById('date-updated');
const taskDateCreatedElement = document.getElementById('date-created');

const monthsDict = {
    "01": "января",
    "02": "февраля",
    "03": "марта",
    "04": "апреля",
    "05": "мая",
    "06": "июня",
    "07": "июля",
    "08": "августа",
    "09": "сентября",
    "10": "октября",
    "11": "ноября",
    "12": "декабря",
}

async function loadTask() {
    const href = window.location.href.split('/');
    const taskId = href[href.length-1];

    const response = await fetch(`http://127.0.0.1:8000/task?task_id=${taskId}`);

    var task = await response.json()
    var category = await getCategory(task);
    var performer = await getUser(task.performer_id);
    var author = await getUser(task.author_id);

    console.log(category);

    if (response.ok)
    {
        taskNameElement.innerText = task.name;
        taskNameElement.style.fontSize = "24px";
        taskNameElement.style.fontWeight = "500";
        taskNameElement.style.textAlign = 'left';
        taskNameElement.style.marginBottom = "6px";

        const categoryContainer = document.createElement('div');
        categoryContainer.innerText = category.name;
        categoryContainer.style.backgroundColor = `${category.color}`;
        categoryContainer.style.padding = "8px";
        categoryContainer.style.borderRadius = "10px";
        categoryContainer.style.fontWeight = "500";
        
        const priorityContainer = document.createElement('div');
        const priorityImg = document.createElement('img');

        priorityImg.src = `/static/${task.priority}p.png`;
        priorityContainer.appendChild(priorityImg);

        if (task.description.length == 0) {
            taskDescElement.innerHTML = "<i>Без описания</i>";
            taskDescElement.style.color = "#A9A9A9";
        }
        else { taskDescElement.innerText = task.description; }

        taskDeadlineElement.innerText = formatDate(task.deadline);
        taskPerformerElement.innerText = performer.name;
        taskPerformerIconElement.src = `/attachments/${performer.id}/${performer.icon}`;
        taskAuthorElement.innerText = author.name;
        taskAuthorIconElement.src = `/attachments/${author.id}/${author.icon}`;
        taskDateCreatedElement.innerText = "Создано " + formatDate(task.date_created);
        taskDateUpdatedElement.innerText = "Обновлено " + formatDate(task.date_updated);
        taskStatBarElement.appendChild(categoryContainer);
        taskStatBarElement.appendChild(priorityContainer);

        const task_container = document.getElementById("subtask-container");

        const response2 = await fetch(`http://127.0.0.1:8000/subtask/all?task_id=${Number(taskId)}`);
        const subtasks = await response2.json();

        const container = document.createElement('div');
        console.log(subtasks);
        container.className = 'subtasks';
        container.style.padding = "12px";

        // 4. Для каждой категории создаем HTML-элемент
        for (const subtask of subtasks) {
        const taskElement = document.createElement('div');

        taskElement.className = 'task';
        taskElement.id = subtask.id;
        taskElement.style.padding = "12px";
        taskElement.style.backgroundColor = "#F5F5F5";
        taskElement.style.borderRadius = "10px";
        taskElement.style.marginBottom = "12px";
        taskElement.style.textAlign = "left";

        // Устанавливаем цвет фона из данных категории
        
        // Добавляем название категории
        const nameElement = document.createElement('span');
        nameElement.textContent = subtask.name;
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

        priorityElement.src = `/static/${subtask.priority}p.png`;
        priorityContainerElement.appendChild(priorityElement);
        priorityContainerElement.style.alignContent = "center";
        priorityContainerElement.style.height = "max-content";

        secondRowElement.appendChild(categoryNameElement);
        secondRowElement.appendChild(priorityContainerElement);

        const performer = await getPerformer(subtask.performer_id);
        const performerNameElement = document.createElement('div');
        
        performerNameElement.style.marginTop = "6px";
        performerNameElement.style.fontSize = "14px";
        performerNameElement.innerText = performer.name;

        taskElement.appendChild(nameElement);
        taskElement.appendChild(secondRowElement);
        taskElement.appendChild(performerNameElement);

        taskElement.onclick = () => window.location.replace(`http://127.0.0.1:8000/app/subtask/${subtask.id}`);
        container.appendChild(taskElement);

        console.log(taskElement);
        };
        
        // 5. Добавляем контейнер на страницу
        task_container.appendChild(container);
    } 
    else
    {
        console.error("ашибка что то с таском не так");
        console.error(response.statusText);
    }
}

async function getCategory(task) {
    const response = await fetch(`http://127.0.0.1:8000/project?project_id=${task.project_id}`);
    
    var project = await response.json();

    const catResponse = await fetch(`http://127.0.0.1:8000/category/${project.category_id}`);

    var category = await catResponse.json();

    return category;
}

async function getUser(user_id) {
    const response = await fetch(`http://127.0.0.1:8000/users?user_id=${user_id}`);
    var user = await response.json();

    return user;
}

function formatDate(date) {
    _ = date.split('T');
    date = _[0].split('-');
    time = _[1].split(':');

    year = date[0];
    month = date[1];
    day = date[2];

    hours = time[0];
    minutes = time[1];

    return `${day} ${monthsDict[month]} ${year}, ${hours}:${minutes}`
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