
function showLoadingModal() {
        // Show the loading modal
        $('#loadingModal').modal('show');
}
    
function validateForm(event) {
    // Prevent the default form submission behavior
    event.preventDefault();

    // Check if the required fields are filled
    if ($('#name').val() === '' || $('#gender').val() === '' || $('#country').val() === '' || $('#color').val() === '' || $('#season').val() === '' || $('#chapters').val() === '' || $('#choices').val() === '') {
        alert('Please fill in all required fields.');
        return false; // Prevent form submission
    }

    // If all required fields are filled, proceed with the form submission
    redirectToNextPage();
}

function redirectToNextPage() { 
    // After the form is submitted, hide the loading modal
    $('#loadingModal').modal('hide');

    // Redirect to the next page
    setTimeout(function() {
        window.location.href = 'prologue.html';
    }, 0);
}