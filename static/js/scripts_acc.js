//hide password
document.addEventListener('DOMContentLoaded', function () {
    const togglePasswordButton = document.getElementById('togglePasswordButton');
    const togglePasswordIcon = document.getElementById('togglePasswordIcon');
    if (togglePasswordButton) {
        togglePasswordButton.addEventListener('click', function () {
            const passwordField = document.getElementById('password');
            if (passwordField.type === 'password') {
                passwordField.type = 'text';
                togglePasswordIcon.src = '../static/images/show_password_icon.png'; 
                togglePasswordIcon.alt = 'Hide Password';
            } else {
                passwordField.type = 'password';
                togglePasswordIcon.src = '../static/images/hide_password_icon.png'; 
                togglePasswordIcon.alt = 'Show Password';
            }
        });
    }
});


// Email check
document.addEventListener('DOMContentLoaded', function() {
    var emailForm = document.getElementById('emailForm');
    var emailInput = document.getElementById('email');
    var emailError = document.getElementById('emailError'); // Assuming this element exists

    emailForm.addEventListener('submit', function(event) {
        var emailValue = emailInput.value;
        if (!validateEmail(emailValue)) {
            event.preventDefault(); // Prevent form submission if email is invalid
            emailError.style.display = 'block'; // Display the error message
        } else {
            emailError.style.display = 'none'; // Hide the error message if email is valid
        }
    });

    function validateEmail(email) {
        var re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    }
});


// Delete subscriptions
// Sample items data array
//var items = [
//    { name: "Item 1" },
//    { name: "Item 2" },
//    { name: "Item 3" }
//];

// Function to populate table with item data
function populateTable() {
    var tableBody = document.querySelector("#itemsTable tbody");

    // Clear table body before populating
    tableBody.innerHTML = "";

    // Loop through items array and populate table rows
    items.forEach(function(item, index) {
        var row = "<tr><td><input type='checkbox' name='itemCheckbox' value='" + index + "'></td><td>" + item.name + "</td></tr>";
        tableBody.innerHTML += row;
    });
}

// Function to delete selected rows
function deleteSelectedRows() {
    var checkboxes = document.querySelectorAll("input[name='itemCheckbox']:checked");
    checkboxes.forEach(function(checkbox) {
        var index = checkbox.value;
        items.splice(index, 1); // Remove item from array
    });
    populateTable(); // Repopulate table to reflect changes
}

document.addEventListener('DOMContentLoaded', function() {
    populateTable();
});

// Add event listener for delete button
document.getElementById("deleteSelected").addEventListener("click", deleteSelectedRows);
