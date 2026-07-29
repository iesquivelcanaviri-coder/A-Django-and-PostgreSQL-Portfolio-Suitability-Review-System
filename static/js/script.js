// ============================================================
// SuitabilityDesk JavaScript
// This file adds small but important frontend behaviour to the Django project.
// It supports Bootstrap validation, holding allocation warnings, and auto-closing messages.
// ============================================================

document.addEventListener("DOMContentLoaded", function () { 
    // This waits until the full HTML page has loaded before JavaScript tries to find or change any page elements.
    // This matters because Django sends the HTML template first, and JavaScript should only run after those elements exist in the browser.
    document.querySelectorAll(".needs-validation").forEach(function (form) { 
        // This finds every form on the page that has the class "needs-validation", which is the Bootstrap class pattern used for custom validation.
        // The forEach loop means the same validation behaviour can work on more than one form without repeating the code.
        form.addEventListener("submit", function (event) { 
            // This listens for the user pressing the submit button on the form.
            // In a Django project, this is important because the form usually sends data back to a Django view using POST.
            if (!form.checkValidity()) { 
                // This checks whether the form is valid according to the browser's built-in HTML rules, such as required fields and email formats.
                // The exclamation mark means "if the form is NOT valid".
                event.preventDefault(); 
                // This stops the form from being submitted to the Django backend when required fields are missing or invalid.
                // This gives the user a chance to fix mistakes before the form reaches the server.
                event.stopPropagation(); 
                // This stops the invalid submit event from continuing further through the page.
                // It helps keep the validation behaviour controlled and prevents other event handlers from acting on a bad form submission.
            }
            form.classList.add("was-validated"); 
            // This adds the Bootstrap class "was-validated" after the user tries to submit the form.
            // Bootstrap uses this class to show validation feedback, such as green valid fields or red invalid fields.
        });
    });

    const holdingForm = document.getElementById("holding-form"); 
    // This looks for a form with the id "holding-form", which is likely used for adding or editing portfolio holdings.
    // Using an id is useful because this script only applies the allocation warning to that specific holdings form.
    if (holdingForm) { 
        // This checks whether the holding form actually exists on the current page.
        // This prevents JavaScript errors on pages that do not have a holdings form.
        const currentWeightInput = holdingForm.querySelector("[name='current_weight']"); 
        // This searches inside the holding form for the input field named "current_weight".
        // In Django, this name usually matches the model/form field that stores the holding's portfolio weight.
        const warning = document.getElementById("allocation-warning"); 
        // This finds the warning message element that should appear if the user enters an invalid allocation.
        // The warning is probably hidden by default in the template using Bootstrap's "d-none" class.
        function checkAllocation() { 
            // This creates a reusable function that checks whether the holding weight is within a sensible range.
            // Keeping this in a function makes the logic cleaner and easier to call whenever the user types.
            const value = parseFloat(currentWeightInput.value || "0"); 
            // This converts the user's input into a decimal number so JavaScript can compare it mathematically.
            // The "|| 0" part means if the field is empty, treat it as zero instead of crashing or returning NaN.
            if (value < 0 || value > 100) warning.classList.remove("d-none"); 
            // This checks whether the entered portfolio weight is below 0 or above 100.
            // If it is outside the valid range, the Bootstrap "d-none" class is removed so the warning becomes visible.
            else warning.classList.add("d-none"); 
            // If the value is between 0 and 100, the warning is hidden again by adding the Bootstrap "d-none" class.
            // This gives the user real-time feedback without needing to submit the form first.
        }
        if (currentWeightInput) currentWeightInput.addEventListener("input", checkAllocation); 
        // This checks that the current weight input exists, then listens for typing or changes inside that field.
        // Every time the user changes the value, the checkAllocation function runs immediately.
    }

    window.setTimeout(function () { 
        // This starts a timer that waits before running the code inside it.
        // It is used here so success messages stay visible briefly, then disappear automatically.
        document.querySelectorAll(".alert-success").forEach(function (alert) { 
            // This finds every Bootstrap success alert on the page.
            // These alerts are often created from Django messages after actions like saving a form or creating a record.
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert); 
            // This connects the HTML alert element to Bootstrap's JavaScript alert component.
            // getOrCreateInstance means Bootstrap will use an existing alert instance or create one if needed.
            bsAlert.close(); 
            // This closes the success alert automatically.
            // It keeps the interface cleaner after the user has had time to read the message.
        });
    }, 5000); 
    // This sets the delay to 5000 milliseconds, which equals 5 seconds.
    // After 5 seconds, successful Django/Bootstrap alert messages will close automatically.
});