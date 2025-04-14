const addButton = document.getElementById("add-button");
addButton.addEventListener("click", addProject);

async function addProject() {
    const project_name = document.getElementById("project-name").value;
    const project_desc = document.getElementById("project-desc").value;

    const href = window.location.href.split('/')
    const id = href[href.length - 2]

    const response = await fetch(`http://127.0.0.1:8000/project/${id}`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            name: project_name, 
            description: project_desc, 
            category_id: id,
        }),
    });
    if (!response.ok)
    {
        console.error("Ашибка заполнения папробуй снвоа");
        return;
    }
    else {
        window.location.replace(`http://127.0.0.1:8000/app/category/${id}`);
    }

}