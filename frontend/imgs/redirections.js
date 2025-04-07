function toProfile(href) {
    history.pushState({}, "", href); 
    window.location.replace("http://127.0.0.1:8000/app/profile"); 
}
function toCalendar(href) { 
    history.pushState({}, "", href);
    window.location.replace("http://127.0.0.1:8000/app/calendar/"); 
}
function toTasks(href) { 
    history.pushState({}, "", href);
    window.location.replace("http://127.0.0.1:8000/app/tasks/"); 
}
function toHome(href) { 
    history.pushState({}, "", href);
    window.location.replace("http://127.0.0.1:8000/app/main/"); 
}

// Categories
function toAddCategory(href) { 
    history.pushState({}, "", href);
    window.location.replace("http://127.0.0.1:8000/app/add-category"); 
}
function toEditCategory(href, category_id) {
    history.pushState({}, "", href);
    window.location.replace(`http://127.0.0.1:8000/app/category/${category_id}/edit`); 
}
function toRegister(href) { 
    history.pushState({}, "", href);
    window.location.replace("http://127.0.0.1:8000/app/register"); 
}
function toLogin(href) { 
    history.pushState({}, "", href);
    window.location.replace("http://127.0.0.1:8000/app/login"); 
}

function toCreateProject(href) { 
    const hrefs = href.split('/')
    const id = hrefs[hrefs.length-1]

    history.pushState({}, "", href);
    window.location.replace(`http://127.0.0.1:8000/app/category/${category_id}/add-project`); 
}