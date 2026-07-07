// ============================================================
// SuitabilityDesk JavaScript
// Adds assignment-relevant interactivity: Bootstrap validation,
// holding allocation warnings and auto-dismiss notifications.
// ============================================================

document.addEventListener("DOMContentLoaded", function () {
    // Bootstrap-style validation: stop forms with invalid required fields.
    document.querySelectorAll(".needs-validation").forEach(function (form) {
        form.addEventListener("submit", function (event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add("was-validated");
        });
    });

    // Real-time allocation check used on the holding form.
    const holdingForm = document.getElementById("holding-form");
    if (holdingForm) {
        const currentWeightInput = holdingForm.querySelector("[name='current_weight']");
        const warning = document.getElementById("allocation-warning");
        function checkAllocation() {
            const value = parseFloat(currentWeightInput.value || "0");
            if (value < 0 || value > 100) warning.classList.remove("d-none");
            else warning.classList.add("d-none");
        }
        if (currentWeightInput) currentWeightInput.addEventListener("input", checkAllocation);
    }

    // Auto-close success messages after a short delay to keep the UI clean.
    window.setTimeout(function () {
        document.querySelectorAll(".alert-success").forEach(function (alert) {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            bsAlert.close();
        });
    }, 5000);
});
