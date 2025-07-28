document.addEventListener('DOMContentLoaded', function() {

    // --- STUDENT: Meal Registration Logic ---
    if (document.querySelector('.register-meal-btn')) {
        // Get a reference to the modal and its parts
        const qrModal = new bootstrap.Modal(document.getElementById('qrCodeModal'));
        const qrCodeImg = document.getElementById('qr-code-img');
        const qrTokenText = document.getElementById('qr-token-text');
        
        document.querySelectorAll('.register-meal-btn').forEach(button => {
            button.addEventListener('click', function() {
                const scheduleId = this.dataset.scheduleId;
                const formData = new FormData();
                formData.append('schedule_id', scheduleId);

                fetch('/register_meal', {
                    method: 'POST',
                    body: formData
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        // --- THIS IS THE NEW, SIMPLE LOGIC ---
                        // 1. Put the QR code image data into the image tag.
                        qrCodeImg.src = 'data:image/png;base64,' + data.qr_code;
                        // 2. Put the token text into the code tag.
                        qrTokenText.textContent = data.token;
                        // 3. Show the modal. The page does NOT reload.
                        qrModal.show();
                    } else {
                        // If it fails, just show an alert.
                        alert(`Error: ${data.message}`);
                    }
                })
                .catch(error => {
                    console.error('Error during meal registration:', error);
                    alert('An unexpected error occurred. Please try again.');
                });
            });
        });
    }


    // --- STUDENT: Meal History Logic (No changes) ---
    const mealHistoryContainer = document.getElementById('meal-history-container');
    if (mealHistoryContainer) {
        fetch('/meal_history')
            .then(response => response.json())
            .then(data => {
                let historyHtml = '<table class="table table-sm"><thead><tr><th>Date</th><th>Item</th><th>Cost</th><th>Status</th></tr></thead><tbody>';
                if (data && data.length > 0) {
                    data.forEach(item => {
                        const registrationDate = item.created_at ? new Date(item.created_at).toLocaleDateString() : 'N/A';
                        historyHtml += `
                            <tr>
                                <td>${registrationDate}</td>
                                <td>${item.meal_details.item_name}</td>
                                <td>${item.meal_details.cost.toFixed(2)}</td>
                                <td><span class="badge ${item.is_used ? 'bg-success' : 'bg-info'}">${item.is_used ? 'Used' : 'Not Used'}</span></td>
                            </tr>
                        `;
                    });
                } else {
                    historyHtml += '<tr><td colspan="4">No meal history found.</td></tr>';
                }
                historyHtml += '</tbody></table>';
                mealHistoryContainer.innerHTML = historyHtml;
            });
    }

    // --- ADMIN LOGIC (No changes) ---
    // ... (Your existing admin QR scanner and manual verification logic is fine)
    const manualVerifyForm = document.getElementById('verify-token-form');
    if (manualVerifyForm) {
        manualVerifyForm.addEventListener('submit', function(e) {
            e.preventDefault();
            // ... (rest of admin code)
        });
    }
});