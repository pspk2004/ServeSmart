document.addEventListener('DOMContentLoaded', function() {

    // --- A SINGLE, ROBUST VERIFICATION FUNCTION ---
    // This function will be used by all three methods (scanner, manual, list button)
    function verifyToken(token) {
        // We will use the main scanner's alert div for all feedback
        const resultDiv = document.getElementById('verification-status-alert');
        if (!resultDiv) {
            console.error("Verification status alert div not found!");
            return;
        }

        resultDiv.style.display = 'block';
        resultDiv.className = 'alert alert-info';
        resultDiv.textContent = `Verifying token: ${token}...`;

        const formData = new FormData();
        formData.append('token', token);

        fetch('/verify_token', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            resultDiv.className = data.success ? 'alert alert-success' : 'alert alert-danger';
            resultDiv.textContent = data.message;
            if (data.success) {
                setTimeout(() => window.location.reload(), 1500);
            }
        })
        .catch(err => {
            console.error('Verification Fetch Error:', err);
            resultDiv.className = 'alert alert-danger';
            resultDiv.textContent = 'A network error occurred.';
        });
    }

    // --- 1. QR SCANNER LOGIC ---
    if (document.getElementById('qr-reader')) {
        const html5QrCode = new Html5Qrcode("qr-reader");
        const startScanBtn = document.getElementById('start-scan-btn');
        const stopScanBtn = document.getElementById('stop-scan-btn');

        const qrCodeSuccessCallback = (decodedText, decodedResult) => {
            html5QrCode.stop().then(ignore => {
                startScanBtn.style.display = 'inline-block';
                stopScanBtn.style.display = 'none';
            }).catch(err => console.error("Failed to stop scanner.", err));
            verifyToken(decodedText);
        };
        const config = { fps: 10, qrbox: { width: 250, height: 250 } };

        startScanBtn.addEventListener('click', () => {
            document.getElementById('verification-status-alert').style.display = 'none';
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

    // --- 2. MANUAL (BACKUP) VERIFICATION LOGIC ---
    const manualVerifyForm = document.getElementById('verify-token-form');
    if (manualVerifyForm) {
        manualVerifyForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const tokenInput = document.getElementById('token-input');
            const resultDiv = document.getElementById('manual-verify-result');
            const token = tokenInput.value.trim();
            if (!token) return;
            
            // Re-route the feedback to this form's own result div
            resultDiv.style.display = 'block';
            resultDiv.className = 'alert alert-info';
            resultDiv.textContent = `Verifying token: ${token}...`;

            const formData = new FormData();
            formData.append('token', token);
            fetch('/verify_token', { method: 'POST', body: formData })
                .then(res => res.json())
                .then(data => {
                    resultDiv.className = data.success ? 'alert alert-success' : 'alert alert-danger';
                    resultDiv.textContent = data.message;
                    if (data.success) setTimeout(() => window.location.reload(), 1500);
                });
            tokenInput.value = '';
        });
    }

    // --- 3. VERIFY FROM LIST (BACKUP 2) LOGIC - NOW RESTORED ---
    document.querySelectorAll('.verify-from-list-btn').forEach(button => {
        button.addEventListener('click', function() {
            const token = this.dataset.token;
            if (confirm(`Are you sure you want to verify this registration?\nToken: ${token}`)) {
                verifyToken(token); // Use the main verification function
            }
        });
    });

    // --- STUDENT LOGIC (No changes, but included for completeness) ---
    if (document.querySelector('.register-meal-btn')) {
        const qrModal = new bootstrap.Modal(document.getElementById('qrCodeModal'));
        const qrCodeImg = document.getElementById('qr-code-img');
        const qrTokenText = document.getElementById('qr-token-text');
        
        document.querySelectorAll('.register-meal-btn').forEach(button => {
            button.addEventListener('click', function() {
                const scheduleId = this.dataset.scheduleId;
                const formData = new FormData();
                formData.append('schedule_id', scheduleId);

                fetch('/register_meal', { method: 'POST', body: formData })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        qrCodeImg.src = 'data:image/png;base64,' + data.qr_code;
                        qrTokenText.textContent = data.token;
                        qrModal.show();
                    } else {
                        alert(`Error: ${data.message}`);
                    }
                })
                .catch(error => {
                    console.error('Error during meal registration:', error);
                    alert('An unexpected error occurred.');
                });
            });
        });
    }

    const mealHistoryContainer = document.getElementById('meal-history-container');
    if (mealHistoryContainer) {
        fetch('/meal_history').then(res => res.json()).then(data => {
            let historyHtml = '<table class="table table-sm"><thead><tr><th>Date</th><th>Item</th><th>Cost</th><th>Status</th></tr></thead><tbody>';
            if (data && data.length > 0) {
                data.forEach(item => {
                    historyHtml += `<tr><td>${new Date(item.created_at).toLocaleDateString()}</td><td>${item.meal_details.item_name}</td><td>${item.meal_details.cost.toFixed(2)}</td><td><span class="badge ${item.is_used ? 'bg-success' : 'bg-info'}">${item.is_used ? 'Used' : 'Not Used'}</span></td></tr>`;
                });
            } else {
                historyHtml += '<tr><td colspan="4">No meal history found.</td></tr>';
            }
            historyHtml += '</tbody></table>';
            mealHistoryContainer.innerHTML = historyHtml;
        });
    }
});