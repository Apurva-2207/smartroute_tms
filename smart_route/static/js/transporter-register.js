// transporter-register.js
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('registrationForm');
    const registerButton = document.getElementById('registerButton');
    
    // Form validation
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        if (validateForm()) {
            // Show loading state
            showLoadingState();
            
            // Submit form after validation
            setTimeout(() => {
                form.submit();
            }, 1500);
        }
    });

    // Real-time validation for each field
    const fields = [
        'first_name', 'last_name', 'email', 'company_name', 
        'phone_number', 'address', 'city', 'state', 'zip_code',
        'vehicle_type', 'license_number', 'password1', 'password2'
    ];

    fields.forEach(field => {
        const element = document.getElementById(field);
        if (element) {
            element.addEventListener('blur', validateField);
            element.addEventListener('input', clearFieldError);
        }
    });

    // Password confirmation real-time check
    const password1 = document.getElementById('password1');
    const password2 = document.getElementById('password2');
    
    if (password1 && password2) {
        password1.addEventListener('input', validatePasswordMatch);
        password2.addEventListener('input', validatePasswordMatch);
        password1.addEventListener('input', showPasswordStrength);
    }

    // Terms agreement check
    const agreeTerms = document.getElementById('agree_terms');
    if (agreeTerms) {
        agreeTerms.addEventListener('change', validateTerms);
    }

    function validateForm() {
        let isValid = true;
        
        // Validate all fields
        fields.forEach(field => {
            if (!validateField({ target: document.getElementById(field) })) {
                isValid = false;
            }
        });

        // Validate terms
        if (!validateTerms()) {
            isValid = false;
        }

        return isValid;
    }

    function validateField(e) {
        const field = e.target;
        const value = field.value.trim();
        const fieldName = field.name;
        
        clearFieldError(e);
        
        let isValid = true;
        let errorMessage = '';

        switch (fieldName) {
            case 'first_name':
            case 'last_name':
            case 'company_name':
                if (!value) {
                    errorMessage = `Please enter your ${fieldName.replace('_', ' ')}.`;
                    isValid = false;
                } else if (value.length < 2) {
                    errorMessage = `${fieldName.replace('_', ' ')} must be at least 2 characters.`;
                    isValid = false;
                }
                break;

            case 'email':
                if (!value) {
                    errorMessage = 'Please enter your email address.';
                    isValid = false;
                } else if (!isValidEmail(value)) {
                    errorMessage = 'Please enter a valid email address.';
                    isValid = false;
                }
                break;

            case 'phone_number':
                if (!value) {
                    errorMessage = 'Please enter your phone number.';
                    isValid = false;
                } else if (!isValidPhone(value)) {
                    errorMessage = 'Please enter a valid phone number.';
                    isValid = false;
                }
                break;

            case 'address':
            case 'city':
            case 'state':
                if (!value) {
                    errorMessage = `Please enter your ${fieldName}.`;
                    isValid = false;
                }
                break;

            case 'zip_code':
                if (!value) {
                    errorMessage = 'Please enter your ZIP code.';
                    isValid = false;
                } else if (!isValidZipCode(value)) {
                    errorMessage = 'Please enter a valid ZIP code.';
                    isValid = false;
                }
                break;

            case 'vehicle_type':
                if (!value) {
                    errorMessage = 'Please select your vehicle type.';
                    isValid = false;
                }
                break;

            case 'license_number':
                if (!value) {
                    errorMessage = 'Please enter your license number.';
                    isValid = false;
                }
                break;

            case 'password1':
                if (!value) {
                    errorMessage = 'Please enter a password.';
                    isValid = false;
                } else if (value.length < 8) {
                    errorMessage = 'Password must be at least 8 characters long.';
                    isValid = false;
                }
                break;

            case 'password2':
                if (!value) {
                    errorMessage = 'Please confirm your password.';
                    isValid = false;
                } else if (value !== password1.value) {
                    errorMessage = 'Passwords do not match.';
                    isValid = false;
                }
                break;
        }

        if (!isValid) {
            showFieldError(field, errorMessage);
        } else {
            showFieldSuccess(field);
        }

        return isValid;
    }

    function validatePasswordMatch() {
        const password1Value = password1.value.trim();
        const password2Value = password2.value.trim();
        
        if (password2Value && password1Value !== password2Value) {
            showFieldError(password2, 'Passwords do not match.');
            return false;
        } else if (password2Value) {
            showFieldSuccess(password2);
            return true;
        }
        return true;
    }

    function validateTerms() {
        const agreeTerms = document.getElementById('agree_terms');
        const termsError = document.getElementById('termsError');
        
        if (!agreeTerms.checked) {
            agreeTerms.classList.add('is-invalid');
            termsError.style.display = 'block';
            return false;
        } else {
            agreeTerms.classList.remove('is-invalid');
            termsError.style.display = 'none';
            return true;
        }
    }

    function showPasswordStrength() {
        const password = password1.value;
        const strengthIndicator = document.getElementById('passwordStrength') || createPasswordStrengthIndicator();
        
        let strength = 'weak';
        let message = 'Weak password';
        
        if (password.length >= 12) {
            strength = 'strong';
            message = 'Strong password';
        } else if (password.length >= 10) {
            strength = 'good';
            message = 'Good password';
        } else if (password.length >= 8) {
            strength = 'fair';
            message = 'Fair password';
        }
        
        strengthIndicator.className = `password-strength strength-${strength}`;
        strengthIndicator.setAttribute('data-strength', message);
    }

    function createPasswordStrengthIndicator() {
        const strengthDiv = document.createElement('div');
        strengthDiv.id = 'passwordStrength';
        strengthDiv.className = 'password-strength';
        strengthDiv.setAttribute('data-strength', '');
        
        const passwordGroup = password1.parentElement;
        passwordGroup.appendChild(strengthDiv);
        
        return strengthDiv;
    }

    function showFieldError(field, message) {
        field.classList.add('is-invalid');
        field.classList.remove('is-valid');
        
        const errorElement = document.getElementById(field.name + 'Error');
        if (errorElement) {
            errorElement.textContent = message;
            errorElement.style.display = 'block';
        }
    }

    function showFieldSuccess(field) {
        field.classList.remove('is-invalid');
        field.classList.add('is-valid');
        
        const errorElement = document.getElementById(field.name + 'Error');
        if (errorElement) {
            errorElement.style.display = 'none';
        }
    }

    function clearFieldError(e) {
        const field = e.target;
        field.classList.remove('is-invalid');
        
        const errorElement = document.getElementById(field.name + 'Error');
        if (errorElement) {
            errorElement.style.display = 'none';
        }
    }

    function showLoadingState() {
        registerButton.disabled = true;
        registerButton.classList.add('loading');
        registerButton.innerHTML = '<i class="fas fa-spinner me-2"></i>Creating Account...';
    }

    // Utility functions
    function isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    function isValidPhone(phone) {
        const phoneRegex = /^[\+]?[1-9][\d]{0,15}$/;
        return phoneRegex.test(phone.replace(/[\s\-\(\)]/g, ''));
    }

    function isValidZipCode(zip) {
        const zipRegex = /^\d{5}(-\d{4})?$/;
        return zipRegex.test(zip);
    }

    // Add input masking for phone number
    const phoneInput = document.getElementById('phone_number');
    if (phoneInput) {
        phoneInput.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            if (value.length > 0) {
                value = '(' + value.substring(0, 3) + ') ' + value.substring(3, 6) + '-' + value.substring(6, 10);
            }
            e.target.value = value;
        });
    }

    // Add character counter for textareas
    const addressTextarea = document.getElementById('address');
    if (addressTextarea) {
        const counter = document.createElement('div');
        counter.className = 'form-text text-end';
        counter.id = 'addressCounter';
        addressTextarea.parentNode.appendChild(counter);
        
        addressTextarea.addEventListener('input', function() {
            const count = this.value.length;
            counter.textContent = `${count}/500 characters`;
            
            if (count > 500) {
                counter.style.color = 'var(--danger-color)';
            } else {
                counter.style.color = 'var(--secondary-color)';
            }
        });
        
        // Initialize counter
        addressTextarea.dispatchEvent(new Event('input'));
    }

    // Add smooth scrolling to form sections
    const formSections = document.querySelectorAll('.form-section');
    formSections.forEach(section => {
        const title = section.querySelector('.section-title');
        if (title) {
            title.style.cursor = 'pointer';
            title.addEventListener('click', function() {
                section.scrollIntoView({ 
                    behavior: 'smooth', 
                    block: 'start' 
                });
            });
        }
    });

    console.log('Transporter registration form initialized successfully.');
});