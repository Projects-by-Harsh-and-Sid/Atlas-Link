// Function to get transaction ID from URL
function getTransactionId() {
    const pathParts = window.location.pathname.split('/');
    return pathParts[pathParts.length - 1];
}

// Function to update the displayed transaction parameters
function updateTransactionDisplay(data) {
    for (const [key, value] of Object.entries(data.transaction_parameters)) {
        const element = document.getElementById(key);
        if (element) {
            element.textContent = value;
        }
    }
    for (const [key, value] of Object.entries(data.item_information)) {
        const element = document.getElementById(`item-${key}`);
        if (element) {
            element.textContent = value;
        }
    }
}

// Function to send POST request
function sendPostRequest(formData) {
    const transactionId = getTransactionId();
    console.log('Transaction ID:', transactionId);
    console.log('Form data:', formData);
    fetch(`/review_create_order/${transactionId}`, {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => {
        if (response.redirected) {
            window.location.href = response.url;
        } else {
            return response.json();
        }
    })
    .then(data => {
        if (data && data.error) {
            alert(`Error: ${data.error}`);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while processing your request.');
    });
}

// Event listener for form submission
document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('update-form');
    form.addEventListener('submit', (e) => {
        e.preventDefault();
        const formData = new FormData(form);
        sendPostRequest(formData);
    });

});