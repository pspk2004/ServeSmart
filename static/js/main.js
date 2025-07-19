// This is the complete, corrected main.js file.

document.addEventListener('DOMContentLoaded', function() {

    // --- SHARED VERIFICATION LOGIC ---
    // A single, reliable function to verify a token, whether from scanner or manual input.
    function verifyToken(token) {
        const statusAlert = document.getElementById('verification-status-alert');
        
        // 1. Show immediate feedback
        statusAlert.style.display = 'block';
        statusAlert.className = 'alert alert-info'; // Blue 'info' style
        statusAlert.textContent = 'Verifying token...';

        const formData = new FormData();
        formData.append('token', token);

        fetch('/verify_token', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            // 2. Show the final result from the server
            if (data.success) {
                statusAlert.className = 'alert alert-success'; // Green 'success' style
                statusAlert.textContent = data.message;
                // Reload the page after a success to update the registration list
                setTimeout(() => window.location.reload(), 1500);
            } else {
                statusAlert.className = 'alert alert-danger'; // Red 'danger' style
                statusAlert.textContent = `Failed: ${data.message}`;
            }
        })
        .catch(err => {
            console.error('Verification Fetch Error:', err);
            statusAlert.className = 'alert alert-danger';
            statusAlert.textContent = 'A network error occurred. Please check your connection and try again.';
        });
    }


    // --- QR SCANNER SETUP ---
    // Check if we are on the admin page by looking for the qr-reader element
    if (document.getElementById('qr-reader')) {
        const html5QrCode = new Html5Qrcode("qr-reader");
        const startScanBtn = document.getElementById('start-scan-btn');
        const stopScanBtn = document.getElementById('stop-scan-btn');
        const statusAlert = document.getElementById('verification-status-alert');

        const qrCodeSuccessCallback = (decodedText, decodedResult) => {
            // This function is called when a QR code is successfully scanned.
            
            // Immediately stop the camera
            html5QrCode.stop().then(ignore => {
                startScanBtn.style.display = 'inline-block';
                stopScanBtn.style.display = 'none';
            }).catch(err => console.error("Failed to stop scanner cleanly.", err));
            
            // Directly call our verification logic
            verifyToken(decodedText);
        };

        const config = { fps: 10, qrbox: { width: 250, height: 250 } };

        startScanBtn.addEventListener('click', () => {
            statusAlert.style.display = 'none'; // Hide old alerts
            html5QrCode.start({ facingMode: "environment" }, config, qrCodeSuccessCallback)
                .catch(err => {
                    alert("Unable to start scanner. Please grant camera permissions and use a secure (HTTPS) connection.");
                    console.error("Scanner Start Error:", err);
                });
            startScanBtn.style.display = 'none';
            stopScanBtn.style.display = 'inline-block';
        });

        stopScanBtn.addEventListener('click', () => {
            html5QrCode.stop().then(ignore => {
                startScanBtn.style.display = 'inline-block';
                stopScanBtn.style.display = 'none';
            }).catch(err => console.error("Failed to stop scanner cleanly.", err));
        });
    }


    // --- MANUAL (BACKUP) VERIFICATION LOGIC ---
    const manualVerifyForm = document.getElementById('verify-token-form');
    if (manualVerifyForm) {
        manualVerifyForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const tokenInput = document.getElementById('token-input');
            const resultDiv = document.getElementById('manual-verify-result');

            // This logic is now just for the manual form's result div
            const token = tokenInput.value.trim();
            if (!token) {
                resultDiv.className = 'alert alert-warning';
                resultDiv.textContent = 'Please enter a token ID.';
                return;
            }
            
            // We can reuse our robust verifyToken function, but we need to update a different div
            const formData = new FormData();
            formData.append('token', token);
            fetch('/verify_token', { method: 'POST', body: formData })
                .then(res => res.json())
                .then(data => {
                    resultDiv.className = data.success ? 'alert alert-success' : 'alert alert-danger';
                    resultDiv.textContent = data.message;
                    if (data.success) setTimeout(() => window.location.reload(), 1500);
                });
        });
    }


    // --- STUDENT MEAL HISTORY LOGIC ---
    // Check if we are on the student page by looking for this container
    const mealHistoryContainer = document.getElementById('meal-history-container');
    if (mealHistoryContainer) {
        fetch('/meal_history')
            .then(response => response.json())
            .then(data => {
                let historyHtml = '<table class="table table-sm"><thead><tr><th>Date</th><th>Item</th><th>Cost</th><th>Status</th></tr></thead><tbody>';
                if (data && data.length > 0) {
                    data.forEach(item => {
                        const registrationDate = item.created_at ? new Date(item.created_at.$date).toLocaleDateString() : 'N/A';
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

});