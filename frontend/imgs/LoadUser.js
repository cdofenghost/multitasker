document.addEventListener("DOMContentLoaded", async function() {
    fetchAndDisplayCategories();
  });
  
async function fetchAndDisplayCategories() {
    const userNameElement = document.getElementById("user-name");
    const userIconElement = document.getElementById("user-icon");
    const userEmailElement = document.getElementById("user-email");

    try {
        const response = await fetch('http://127.0.0.1:8000/users/get/');
    
        if (!response.ok) {
            throw new Error(`Ошибка HTTP: ${response.status}`);
        }
        
        const user = await response.json()

        userNameElement.innerText = user["name"]
        userEmailElement.innerText = user["email"]
        
        } catch (error) {
        console.error('Ошибка при загрузке категорий:', error);
    }
}
    
async function logout() {
    try {
        // 1. Делаем GET-запрос к API
            const response = await fetch('http://127.0.0.1:8000/profile/logout/', {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(),
            });
        
            // Проверяем, что запрос успешен
            if (!response.ok) {
                throw new Error(`Ошибка HTTP: ${response.status}`);
            }

            window.location.replace("http://127.0.0.1:8000/app/login");
            
            } catch (error) {
            console.error('Ошибка при загрузке категорий:', error);
            // // Можно добавить уведомление об ошибке на страницу
            // const errorElement = document.createElement('div');
            // errorElement.className = 'error';
            // errorElement.textContent = 'Не удалось загрузить категории';
            // category_container.appendChild(errorElement);
        }
}
  
  