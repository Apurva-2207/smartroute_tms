// static/js/transporter-login.js
// Transporter Login Page Functionality

document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    const loginButton = document.getElementById('loginButton');
    const usernameInput = document.getElementById('username');
    const passwordInput = document.getElementById('password');
    
    // Initialize form validation
    initFormValidation();
    
    // Auto-hide alerts after 5 seconds
    initAutoHideAlerts();
    
    // Add form submission handler
    if (loginForm) {
        loginForm.addEventListener('submit', handleFormSubmission);
    }
    
    // Add real-time validation
    if (usernameInput) {
        usernameInput.addEventListener('blur', validateEmail);
        usernameInput.addEventListener('input', clearValidation);
    }
    
    if (passwordInput) {
        passwordInput.addEventListener('blur', validatePassword);
        passwordInput.addEventListener('input', clearValidation);
    }
    
    // Add keyboard shortcuts
    document.addEventListener('keydown', handleKeyboardShortcuts);
});

/**
 * Initialize form validation
 */
function initFormValidation() {
    // Clear any existing validation styles
    const inputs = document.querySelectorAll('.form-control');
    inputs.forEach(input => {
        input.classList.remove('is-invalid', 'is-valid');
    });
}

/**
 * Initialize auto-hide functionality for alerts
 */
function initAutoHideAlerts() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
}

/**
 * Handle form submission
 */
function handleFormSubmission(e) {
    e.preventDefault();
    
    // Validate form before submission
    const isEmailValid = validateEmail();
    const isPasswordValid = validatePassword();
    
    if (isEmailValid && isPasswordValid) {
        showLoadingState();
        // Form is valid, proceed with submission
        this.submit();
    } else {
        showValidationErrors();
    }
}

/**
 * Validate email format
 */
function validateEmail() {
    const email = usernameInput.value.trim();
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    const isValid = emailRegex.test(email);
    
    if (usernameInput) {
        if (email && !isValid) {
            usernameInput.classList.add('is-invalid');
            usernameInput.classList.remove('is-valid');
            return false;
        } else if (email && isValid) {
            usernameInput.classList.add('is-valid');
            usernameInput.classList.remove('is-invalid');
            return true;
        }
    }
    return false;
}

/**
 * Validate password (basic validation)
 */
function validatePassword() {
    const password = passwordInput.value.trim();
    const isValid = password.length >= 6; // Minimum 6 characters
    
    if (passwordInput) {
        if (password && !isValid) {
            passwordInput.classList.add('is-invalid');
            passwordInput.classList.remove('is-valid');
            return false;
        } else if (password && isValid) {
            passwordInput.classList.add('is-valid');
            passwordInput.classList.remove('is-invalid');
            return true;
        }
    }
    return false;
}

/**
 * Clear validation styles on input
 */
function clearValidation(e) {
    e.target.classList.remove('is-invalid', 'is-valid');
}

/**
 * Show loading state on login button
 */
function showLoadingState() {
    if (loginButton) {
        const originalText = loginButton.innerHTML;
        loginButton.innerHTML = '<span class="loading-spinner me-2"></span>Logging in...';
        loginButton.disabled = true;
        
        // Store original content for potential reset
        loginButton.dataset.originalContent = originalText;
    }
}

/**
 * Reset loading state (useful if submission fails)
 */
function resetLoadingState() {
    if (loginButton && loginButton.dataset.originalContent) {
        loginButton.innerHTML = loginButton.dataset.originalContent;
        loginButton.disabled = false;
    }
}

/**
 * Show validation errors summary
 */
function showValidationErrors() {
    const errors = [];
    
    if (!validateEmail()) {
        errors.push('Please enter a valid email address.');
    }
    
    if (!validatePassword()) {
        errors.push('Password must be at least 6 characters long.');
    }
    
    if (errors.length > 0) {
        showToast('Please fix the following errors:', errors.join('\n'));
    }
}

/**
 * Show toast notification
 */
function showToast(title, message) {
    // Create toast element
    const toastContainer = document.createElement('div');
    toastContainer.className = 'toast-container position-fixed top-0 end-0 p-3';
    toastContainer.style.zIndex = '9999';
    
    const toastHtml = `
        <div class="toast align-items-center text-bg-danger border-0" role="alert">
            <div class="d-flex">
                <div class="toast-body">
                    <strong>${title}</strong><br>${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        </div>
    `;
    
    toastContainer.innerHTML = toastHtml;
    document.body.appendChild(toastContainer);
    
    // Show toast
    const toastElement = toastContainer.querySelector('.toast');
    const toast = new bootstrap.Toast(toastElement);
    toast.show();
    
    // Remove toast from DOM after it's hidden
    toastElement.addEventListener('hidden.bs.toast', () => {
        toastContainer.remove();
    });
}

/**
 * Handle keyboard shortcuts
 */
function handleKeyboardShortcuts(e) {
    // Ctrl + Enter to submit form
    if (e.ctrlKey && e.key === 'Enter') {
        if (loginForm) {
            loginForm.dispatchEvent(new Event('submit'));
        }
    }
    
    // Escape key to clear form
    if (e.key === 'Escape') {
        if (loginForm) {
            loginForm.reset();
            initFormValidation();
        }
    }
}

/**
 * Demo function for development (remove in production)
 */
function demoLogin() {
    if (usernameInput) usernameInput.value = 'transporter@demo.com';
    if (passwordInput) passwordInput.value = 'demo123';
    
    // Trigger validation
    validateEmail();
    validatePassword();
    
    console.log('Demo credentials filled. Remove this function in production.');
}

// Export functions for potential module use (if needed)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        validateEmail,
        validatePassword,
        showLoadingState,
        resetLoadingState
    };
}