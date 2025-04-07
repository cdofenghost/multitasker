const addButton = document.getElementById("add-button");
addButton.addEventListener("click", addCategory);

async function addCategory() {
    const category_name = document.getElementById("category-name").value;
    const category_color = document.getElementById("category-color").value;

    const response = await fetch("http://127.0.0.1:8000/category", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({name: category_name, color: category_color}),
    });

    console.log({name: category_name, color: category_color});

    window.location.replace("http://127.0.0.1:8000/app/main");
}