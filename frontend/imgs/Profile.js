var username = document.getElementById('user-name');
var email = document.getElementById('email');

// username.addEventListener('keypress', function(event) {
//     if (event.key == )
// });

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
