const addButton = document.getElementById("add-button");
addButton.addEventListener("click", addTask);

async function addTask() {
    const project_name = document.getElementById("task-name").value;
    const project_desc = document.getElementById("task-desc").value;
    const project_performer_email = document.getElementById("task-performer-email").value;
    const project_date = document.getElementById("task-date").value;
    const project_priority = document.getElementById("task-priority").value;

    const response_performer = await fetch(`http://127.0.0.1:8000/users/by-email?email=${project_performer_email}&send_notification=True`);
    const performer = await response_performer.json();
    var perfId = Number(performer.id);

    if (isNaN(perfId))
    {
        perfId = -1;
    }
    const href = window.location.href.split('/')
    const id = href[href.length - 2]
    const rbody = {
        performer_id: perfId,
        name: project_name, 
        description: project_desc, 
        deadline: project_date,
        priority: Number(project_priority),
    };
    console.log(rbody);
    const response = await fetch(`http://127.0.0.1:8000/task?project_id=${id}`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(rbody),
    });

    if (response.ok) {
        window.location.replace(`http://127.0.0.1:8000/app/project/${id}`);
    }
}