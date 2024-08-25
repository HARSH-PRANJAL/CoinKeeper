function getUserInput() {
    const selectElement = document.getElementById("category");
    const selectedValue = selectElement.value;

    if (selectedValue === "other") {
        // Reset the select element to the default value (if necessary)
        selectElement.value = ""; // or "category1" or any other default value

        const userInput = prompt("Please enter your data:");
        if (userInput !== null) {
            sendDataToBackend(userInput);
        }
    }
}

function sendDataToBackend(data) {
    fetch('/addCategory', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken') // Ensure CSRF token is included
        },
        body: JSON.stringify({ userInput: data })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            location.reload(true);
            alert("New category updated!");
        } else {
            alert("Failed to send data: " + data.error);
        }
    })
    .catch((error) => {
        console.error('Error:', error);
        alert("An error occurred.");
    });
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
