
function showLoadingModal() {
        // Show the loading modal
        $('#loadingModal').modal('show');
}
    
function validateForm(event) {
    // Prevent the default form submission behavior
    event.preventDefault();

    // Show the loading modal if all fields are filled
    showLoadingModal();

    // If all required fields are filled, proceed with the form submission
    redirectToNextPage();
}

function redirectToNextPage() { 
    // After the form is submitted and all fields are filled, hide the loading modal
    $('#loadingModal').modal('hide');

    // Redirect to the next page
    setTimeout(function() {
        window.location.href = 'prologue.html';
    }, 0);
}

function validateNumericInput(inputFieldId, errorMessageId, minVal, maxVal) {
    var inputField = document.getElementById(inputFieldId);
    var value = inputField.value;
    var errorMessage = document.getElementById(errorMessageId);

    // Check if the input is empty or out of range
    if (value < minVal || value > maxVal) {
        errorMessage.textContent = `Please enter a number between ${minVal} and ${maxVal}.`;
        inputField.value = ''; // Clear the input field
    } else {
        errorMessage.textContent = ''; // Clear the message when the input is valid
    }
}

document.addEventListener('DOMContentLoaded', function() {
    // Validate 'chapters' input
    document.getElementById('chapters').addEventListener('change', function() {
        validateNumericInput('chapters', 'error-message', 3, 15);
    });

    // Validate 'choices' input
    document.getElementById('choices').addEventListener('change', function() {
        validateNumericInput('choices', 'choices-error-message', 2, 5);
    });

    // Load country options
    fetch('assets/country-codes.html')
        .then(response => response.text())
        .then(html => {
            document.getElementById('country-container').innerHTML = html;
        })
        .catch(error => console.error('Error loading country data:', error));
});
