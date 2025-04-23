const username = document.getElementById('user-name');
const email = document.getElementById('user-email');
const icon = document.getElementById('user-icon');


var nameButton = document.getElementById('change-name-button');
var emailButton = document.getElementById('change-email-button');
var iconButton = document.getElementById('change-icon-button');

nameButton.addEventListener('click',async () => {
    if (username.isContentEditable)
    {
        username.contentEditable = false;
        changeData();
    }

    else {
        username.contentEditable = true;
    }
});

async function changeData() {
    console.log(email);
    const response = await fetch(`http://127.0.0.1:8000/profile/update`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            email: email.innerText,
            name: username.textContent,
            icon: icon.src,
        }),
    });
}

async function changePassword() {
    const password = document.getElementById("new-password").value;
    const response = await fetch(`http://127.0.0.1:8000/profile/update-password?new_password=${password}`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(),
    });

    if (response.ok)
    {
        console.log("password changed successfully");
        return;
    }

    else {
        console.error("ашибка пассворд");
        console.error(response.statusText);   
    }
}

function on() {
    document.getElementById("overlay").style.display = "block";
}
  
function off() {
    document.getElementById("overlay").style.display = "none";
}
