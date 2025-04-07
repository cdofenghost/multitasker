const addButton = document.getElementById("add-button");
const deleteButton = document.getElementById("delete-button");

addButton.addEventListener("click", addCategory);
deleteButton.addEventListener("click", deleteCategory);

async function addCategory() {
    const category_name = document.getElementById("category-name").value;
    const category_color = document.getElementById("category-color").value;

    const href = window.location.href.split('/')
    const id = href[href.length-2]
    
    const response = await fetch(`http://127.0.0.1:8000/category?category_id=${id}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({name: category_name, color: category_color}),
    });

    console.log({name: category_name, color: category_color});

    window.location.replace("http://127.0.0.1:8000/app/main");
}

async function deleteCategory() {
    const href = window.location.href.split('/')
    const id = href[href.length-2]

    const response = await fetch(`http://127.0.0.1:8000/category?category_id=${id}`, {
        method: "DELETE",
        headers: {
            "Content-Type": "application/json",
        },
    });

    window.location.replace("http://127.0.0.1:8000/app/main");
}