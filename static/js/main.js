// Main JavaScript file for GST Billing Software
// Handles common functionality across the application

// Initialize application when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

/**
 * Initialize the application
 */
function initializeApp() {
    // Initialize tooltips
    initializeTooltips();
    
    // Initialize form validations
    initializeFormValidations();
    
    // Initialize auto-save functionality
    initializeAutoSave();
    
    // Initialize number formatting
    initializeNumberFormatting();
    
    // Initialize keyboard shortcuts
    initializeKeyboardShortcuts();
    
    // Initialize search functionality
    initializeSearch();
    
    // Add loading states to forms
    initializeLoadingStates();
    
    console.log('GST Billing Software initialized successfully');
}

/**
 * Initialize Bootstrap tooltips
 */
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * Initialize form validations
 */
function initializeFormValidations() {
    // Add validation for GST numbers
    const gstInputs = document.querySelectorAll('input[name*="gst_number"]');
    gstInputs.forEach(input => {
        input.addEventListener('input', validateGSTNumber);
        input.addEventListener('blur', validateGSTNumber);
    });
    
    // Add validation for email fields
    const emailInputs = document.querySelectorAll('input[type="email"]');
    emailInputs.forEach(input => {
        input.addEventListener('blur', validateEmail);
    });
    
    // Add validation for phone fields
    const phoneInputs = document.querySelectorAll('input[name*="phone"]');
    phoneInputs.forEach(input => {
        input.addEventListener('input', formatPhoneNumber);
        input.addEventListener('blur', validatePhoneNumber);
    });
    
    // Add currency formatting to price fields
    const priceInputs = document.querySelectorAll('input[name*="price"], input[name*="rate"], input[name*="amount"]');
    priceInputs.forEach(input => {
        input.addEventListener('blur', formatCurrency);
    });
}

/**
 * Initialize auto-save functionality for forms
 */
function initializeAutoSave() {
    const forms = document.querySelectorAll('form[data-autosave="true"]');
    forms.forEach(form => {
        const formInputs = form.querySelectorAll('input, textarea, select');
        formInputs.forEach(input => {
            input.addEventListener('input', debounce(function() {
                autoSaveForm(form);
            }, 2000));
        });
    });
}

/**
 * Initialize number formatting
 */
function initializeNumberFormatting() {
    // Format all existing currency displays
    const currencyElements = document.querySelectorAll('.currency');
    currencyElements.forEach(element => {
        const value = parseFloat(element.textContent.replace(/[^0-9.-]+/g, ''));
        if (!isNaN(value)) {
            element.textContent = formatCurrencyDisplay(value);
        }
    });
}

/**
 * Initialize keyboard shortcuts
 */
function initializeKeyboardShortcuts() {
    document.addEventListener('keydown', function(event) {
        // Ctrl+N or Cmd+N: New bill
        if ((event.ctrlKey || event.metaKey) && event.key === 'n') {
            event.preventDefault();
            const newBillLink = document.querySelector('a[href*="create_bill"]');
            if (newBillLink) {
                window.location.href = newBillLink.href;
            }
        }
        
        // Ctrl+S or Cmd+S: Save form
        if ((event.ctrlKey || event.metaKey) && event.key === 's') {
            event.preventDefault();
            const submitButton = document.querySelector('button[type="submit"]');
            if (submitButton && !submitButton.disabled) {
                submitButton.click();
            }
        }
        
        // Escape: Close modals
        if (event.key === 'Escape') {
            const openModals = document.querySelectorAll('.modal.show');
            openModals.forEach(modal => {
                const modalInstance = bootstrap.Modal.getInstance(modal);
                if (modalInstance) {
                    modalInstance.hide();
                }
            });
        }
    });
}

/**
 * Initialize search functionality
 */
function initializeSearch() {
    const searchInputs = document.querySelectorAll('input[type="search"], input[placeholder*="Search"]');
    searchInputs.forEach(input => {
        input.addEventListener('input', debounce(function() {
            if (input.value.length >= 2 || input.value.length === 0) {
                // Auto-submit search forms
                const form = input.closest('form');
                if (form) {
                    form.submit();
                }
            }
        }, 500));
    });
}

/**
 * Initialize loading states for forms
 */
function initializeLoadingStates() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            const submitButton = form.querySelector('button[type="submit"]');
            if (submitButton) {
                submitButton.disabled = true;
                submitButton.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Processing...';
                
                // Add loading class to form
                form.classList.add('loading');
            }
        });
    });
}

/**
 * Validate GST number format
 */
function validateGSTNumber(event) {
    const input = event.target;
    const value = input.value.toUpperCase();
    const gstPattern = /^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}[Z]{1}[0-9A-Z]{1}$/;
    
    // Auto-format to uppercase
    input.value = value;
    
    if (value && !gstPattern.test(value)) {
        showValidationError(input, 'Invalid GST number format');
    } else {
        clearValidationError(input);
    }
}

/**
 * Validate email format
 */
function validateEmail(event) {
    const input = event.target;
    const value = input.value;
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    
    if (value && !emailPattern.test(value)) {
        showValidationError(input, 'Invalid email format');
    } else {
        clearValidationError(input);
    }
}

/**
 * Format phone number
 */
function formatPhoneNumber(event) {
    const input = event.target;
    let value = input.value.replace(/\D/g, '');
    
    if (value.length > 10) {
        value = value.slice(0, 10);
    }
    
    input.value = value;
}

/**
 * Validate phone number
 */
function validatePhoneNumber(event) {
    const input = event.target;
    const value = input.value;
    
    if (value && (value.length < 10 || value.length > 10)) {
        showValidationError(input, 'Phone number must be 10 digits');
    } else {
        clearValidationError(input);
    }
}

/**
 * Format currency input
 */
function formatCurrency(event) {
    const input = event.target;
    const value = parseFloat(input.value);
    
    if (!isNaN(value)) {
        input.value = value.toFixed(2);
    }
}

/**
 * Format currency for display
 */
function formatCurrencyDisplay(amount) {
    return new Intl.NumberFormat('en-IN', {
        style: 'currency',
        currency: 'INR',
        minimumFractionDigits: 2
    }).format(amount);
}

/**
 * Show validation error
 */
function showValidationError(input, message) {
    input.classList.add('is-invalid');
    
    // Remove existing error message
    const existingError = input.parentNode.querySelector('.invalid-feedback');
    if (existingError) {
        existingError.remove();
    }
    
    // Add new error message
    const errorDiv = document.createElement('div');
    errorDiv.className = 'invalid-feedback';
    errorDiv.textContent = message;
    input.parentNode.appendChild(errorDiv);
}

/**
 * Clear validation error
 */
function clearValidationError(input) {
    input.classList.remove('is-invalid');
    const errorMessage = input.parentNode.querySelector('.invalid-feedback');
    if (errorMessage) {
        errorMessage.remove();
    }
}

/**
 * Auto-save form data
 */
function autoSaveForm(form) {
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());
    
    // Save to localStorage
    const formId = form.id || 'autosave_form';
    localStorage.setItem(`autosave_${formId}`, JSON.stringify(data));
    
    // Show auto-save indicator
    showAutoSaveIndicator();
}

/**
 * Show auto-save indicator
 */
function showAutoSaveIndicator() {
    let indicator = document.querySelector('.autosave-indicator');
    if (!indicator) {
        indicator = document.createElement('div');
        indicator.className = 'autosave-indicator';
        indicator.innerHTML = '<i class="fas fa-check-circle text-success"></i> Auto-saved';
        indicator.style.cssText = `
            position: fixed;
            top: 70px;
            right: 20px;
            background: white;
            padding: 8px 16px;
            border-radius: 4px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.15);
            z-index: 1050;
            opacity: 0;
            transition: opacity 0.3s;
        `;
        document.body.appendChild(indicator);
    }
    
    indicator.style.opacity = '1';
    setTimeout(() => {
        indicator.style.opacity = '0';
    }, 2000);
}

/**
 * Debounce function to limit function calls
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Show loading spinner
 */
function showLoading(element) {
    element.classList.add('loading');
    element.style.position = 'relative';
}

/**
 * Hide loading spinner
 */
function hideLoading(element) {
    element.classList.remove('loading');
}

/**
 * Show toast notification
 */
function showToast(message, type = 'success') {
    const toast = document.createElement('div');
    toast.className = `toast-notification toast-${type}`;
    toast.innerHTML = `
        <div class="d-flex align-items-center">
            <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'} me-2"></i>
            <span>${message}</span>
        </div>
    `;
    toast.style.cssText = `
        position: fixed;
        top: 80px;
        right: 20px;
        background: var(--bs-${type === 'error' ? 'danger' : type});
        color: white;
        padding: 12px 20px;
        border-radius: 4px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        z-index: 1051;
        opacity: 0;
        transform: translateX(100%);
        transition: all 0.3s ease;
        max-width: 400px;
    `;
    
    document.body.appendChild(toast);
    
    // Animate in
    setTimeout(() => {
        toast.style.opacity = '1';
        toast.style.transform = 'translateX(0)';
    }, 100);
    
    // Animate out
    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(100%)';
        setTimeout(() => {
            if (toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
        }, 300);
    }, 3000);
}

/**
 * Confirm dialog
 */
function confirmDialog(message, callback) {
    const modal = document.createElement('div');
    modal.className = 'modal fade';
    modal.innerHTML = `
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Confirm Action</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    <p>${message}</p>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                    <button type="button" class="btn btn-danger confirm-action">Confirm</button>
                </div>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    
    const modalInstance = new bootstrap.Modal(modal);
    modalInstance.show();
    
    modal.querySelector('.confirm-action').addEventListener('click', function() {
        modalInstance.hide();
        callback();
    });
    
    modal.addEventListener('hidden.bs.modal', function() {
        document.body.removeChild(modal);
    });
}

/**
 * AJAX helper function
 */
function ajaxRequest(url, options = {}) {
    const defaults = {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        }
    };
    
    const config = Object.assign(defaults, options);
    
    return fetch(url, config)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .catch(error => {
            console.error('AJAX request failed:', error);
            showToast('Request failed. Please try again.', 'error');
            throw error;
        });
}

/**
 * Form serialization helper
 */
function serializeForm(form) {
    const formData = new FormData(form);
    const data = {};
    
    for (let [key, value] of formData.entries()) {
        if (data[key]) {
            if (Array.isArray(data[key])) {
                data[key].push(value);
            } else {
                data[key] = [data[key], value];
            }
        } else {
            data[key] = value;
        }
    }
    
    return data;
}

/**
 * Local storage helpers
 */
const LocalStorage = {
    set: function(key, value) {
        try {
            localStorage.setItem(key, JSON.stringify(value));
        } catch (e) {
            console.warn('LocalStorage not available:', e);
        }
    },
    
    get: function(key) {
        try {
            const item = localStorage.getItem(key);
            return item ? JSON.parse(item) : null;
        } catch (e) {
            console.warn('LocalStorage not available:', e);
            return null;
        }
    },
    
    remove: function(key) {
        try {
            localStorage.removeItem(key);
        } catch (e) {
            console.warn('LocalStorage not available:', e);
        }
    }
};

/**
 * Number to words converter (Indian format)
 */
function numberToWords(num) {
    if (num === 0) return "Zero";
    
    const ones = ["", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", 
                  "Ten", "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen", 
                  "Seventeen", "Eighteen", "Nineteen"];
    
    const tens = ["", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"];
    
    function convertHundreds(n) {
        let result = "";
        if (n >= 100) {
            result += ones[Math.floor(n / 100)] + " Hundred ";
            n %= 100;
        }
        if (n >= 20) {
            result += tens[Math.floor(n / 10)] + " ";
            n %= 10;
        }
        if (n > 0) {
            result += ones[n] + " ";
        }
        return result;
    }
    
    let result = "";
    num = Math.floor(num); // Convert to integer
    
    // Crores
    if (num >= 10000000) {
        result += convertHundreds(Math.floor(num / 10000000)) + "Crore ";
        num %= 10000000;
    }
    
    // Lakhs
    if (num >= 100000) {
        result += convertHundreds(Math.floor(num / 100000)) + "Lakh ";
        num %= 100000;
    }
    
    // Thousands
    if (num >= 1000) {
        result += convertHundreds(Math.floor(num / 1000)) + "Thousand ";
        num %= 1000;
    }
    
    // Hundreds
    if (num > 0) {
        result += convertHundreds(num);
    }
    
    return result.trim();
}

/**
 * Export functions to global scope for template usage
 */
window.GST = {
    showToast,
    confirmDialog,
    ajaxRequest,
    formatCurrencyDisplay,
    numberToWords,
    LocalStorage,
    showLoading,
    hideLoading
};

/**
 * Analytics and performance monitoring
 */
function trackEvent(eventName, eventData = {}) {
    // Placeholder for analytics tracking
    console.log('Event tracked:', eventName, eventData);
}

/**
 * Error handling
 */
window.addEventListener('error', function(event) {
    console.error('JavaScript error:', event.error);
    // In production, you might want to send this to an error tracking service
});

window.addEventListener('unhandledrejection', function(event) {
    console.error('Unhandled promise rejection:', event.reason);
    // In production, you might want to send this to an error tracking service
});

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        formatCurrencyDisplay,
        numberToWords,
        validateGSTNumber,
        validateEmail
    };
}
