// This is the complete, correct, and final main.js file.
// It contains all the logic for both students and admins.

document.addEventListener('DOMContentLoaded', function() {

    // --- STUDENT: Meal Registration Logic ---
    // Check if we are on the student page by looking for the register buttons
    if (document.querySelector('.register-meal-btn')) {
        document.querySelectorAll('.register-meal-btn').forEach(button => {
            button.addEventListener('click', function() {
                // Use the simpler modal from our previous working version
                const successModal = new bootstrap.Modal(document.getElementById('successModal'));
                const successMessageDiv = document.getElementById('success-message');

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
                        // On success, show the success message in the modal
                        successMessageDiv.textContent = data.message;
                        successModal.show();
                        
                        // Reload the page after a short delay to display the new active token
                        setTimeout(() => {
                            window.location.reload();
                        }, 2000);

                    } else {
                        // If it fails (e.g., not enough points), just show a simple alert
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


    // --- STUDENT: Meal History Logic ---
    // Check if we are on the student page by looking for this container
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


    // --- ADMIN: QR Scanner and Verification Logic ---
    // Check if we are on the admin page by looking for the qr-reader element
    if (document.getElementById('qr-reader')) {
        const html5QrCode = new Html5Qrcode("qr-reader");
        const startScanBtn = document.getElementById('start-scan-btn');
        const stopScanBtn = document.getElementById('stop-scan-btn');
        const tokenInput = document.getElementById('token-input');
        const verifyForm = document.getElementById('verify-token-form');

        // This is the function that gets called when a QR code is successfully scanned.
        const qrCodeSuccessCallback = (decodedText, decodedResult) => {
            html5QrCode.stop().then(ignore => {
                // Stop the camera feed
                alert(`Scan Successful! Token: ${decodedText}`);
                // Put the scanned token into the manual input field
                tokenInput.value = decodedText;
                // Automatically submit the manual form for verification
                verifyForm.dispatchEvent(new Event('submit', { 'bubbles': true }));
                
                // Reset button visibility
                startScanBtn.style.display = 'inline-block';
                stopScanBtn.style.display = 'none';

            }).catch(err => console.error("Failed to stop scanner.", err));
        };

        const config = { fps: 10, qrbox: { width: 250, height: 250 } };

        startScanBtn.addEventListener('click', () => {
            html5QrCode.start({ facingMode: "environment" }, config, qrCodeSuccessCallback)
                .catch(err => alert("Could not start scanner. Please grant camera permissions."));
            startScanBtn.style.display = 'none';
            stopScanBtn.style.display = 'inline-block';
        });

        stopScanBtn.addEventListener('click', () => {
            html5QrCode.stop().then(ignore => {
                startScanBtn.style.display = 'inline-block';
                stopScanBtn.style.display = 'none';
            }).catch(err => console.error("Failed to stop scanner.", err));
        });
    }

    // --- ADMIN: Manual (Backup) Verification Logic ---
    const manualVerifyForm = document.getElementById('verify-token-form');
    if (manualVerifyForm) {
        manualVerifyForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const tokenInput = document.getElementById('token-input');
            const resultDiv = document.getElementById('manual-verify-result') || document.getElementById('verification-status-alert'); // Support both divs
            const token = tokenInput.value.trim();

            if (!token) {
                resultDiv.className = 'alert alert-warning';
                resultDiv.textContent = 'Please enter or scan a token ID.';
                return;
            }
            
            resultDiv.className = 'alert alert-info';
            resultDiv.textContent = 'Verifying...';
            resultDiv.style.display = 'block';

            const formData = new FormData();
            formData.append('token', token);
            
            fetch('/verify_token', { method: 'POST', body: formData })
                .then(res => res.json())
                .then(data => {
                    resultDiv.className = data.success ? 'alert alert-success' : 'alert alert-danger';
                    resultDiv.textContent = data.message;
                    if (data.success) {
                        setTimeout(() => window.location.reload(), 1500);
                    }
                });
        });
    }

});