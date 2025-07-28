// This is the complete and final diagnostic version of main.js

document.addEventListener('DOMContentLoaded', function() {

    // --- STUDENT: Meal Registration Logic ---
    if (document.querySelector('.register-meal-btn')) {
        document.querySelectorAll('.register-meal-btn').forEach(button => {
            button.addEventListener('click', function() {
                
                // --- THIS IS OUR TEST ---
                const scheduleId = this.dataset.scheduleId;
                console.log("Register button was clicked! Attempting to register for Meal ID:", scheduleId);

                const successModal = new bootstrap.Modal(document.getElementById('successModal'));
                const successMessageDiv = document.getElementById('success-message');
                const formData = new FormData();
                formData.append('schedule_id', scheduleId);

                fetch('/register_meal', {
                    method: 'POST',
                    body: formData
                })
                .then(response => {
                    console.log("Received a response from the server.");
                    if (!response.ok) {
                        // If response is not 200 OK, log it as an error
                        console.error("Server responded with an error status:", response.status);
                    }
                    return response.json();
                })
                .then(data => {
                    console.log("Server response data:", data);
                    if (data.success) {
                        successMessageDiv.textContent = data.message;
                        successModal.show();
                        setTimeout(() => {
                            window.location.reload();
                        }, 2000);
                    } else {
                        alert(`Error: ${data.message}`);
                    }
                })
                .catch(error => {
                    // If an error happens during the fetch, it will be printed here in red.
                    console.error('Error during meal registration fetch:', error);
                    alert('An unexpected error occurred. Please check the developer console for details.');
                });
            });
        });
    }


    // --- STUDENT: Meal History Logic ---
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
    if (document.getElementById('qr-reader')) {
        const html5QrCode = new Html5Qrcode("qr-reader");
        const startScanBtn = document.getElementById('start-scan-btn');
        const stopScanBtn = document.getElementById('stop-scan-btn');
        const tokenInput = document.getElementById('token-input');
        const verifyForm = document.getElementById('verify-token-form');

        const qrCodeSuccessCallback = (decodedText, decodedResult) => {
            html5QrCode.stop().then(ignore => {
                alert(`Scan Successful! Token: ${decodedText}`);
                tokenInput.value = decodedText;
                verifyForm.dispatchEvent(new Event('submit', { 'bubbles': true }));
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
            const resultDiv = document.getElementById('manual-verify-result') || document.getElementById('verification-status-alert');
            const token = tokenInput.value.trim();

            if (!token) {
                if (resultDiv) {
                    resultDiv.className = 'alert alert-warning';
                    resultDiv.textContent = 'Please enter or scan a token ID.';
                }
                return;
            }
            
            if (resultDiv) {
                resultDiv.className = 'alert alert-info';
                resultDiv.textContent = 'Verifying...';
                resultDiv.style.display = 'block';
            }

            const formData = new FormData();
            formData.append('token', token);
            
            fetch('/verify_token', { method: 'POST', body: formData })
                .then(res => res.json())
                .then(data => {
                    if (resultDiv) {
                        resultDiv.className = data.success ? 'alert alert-success' : 'alert alert-danger';
                        resultDiv.textContent = data.message;
                        if (data.success) {
                            setTimeout(() => window.location.reload(), 1500);
                        }
                    }
                });
        });
    }

});