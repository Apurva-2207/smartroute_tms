document.addEventListener('DOMContentLoaded', function () {
    // Navbar scroll effect
    const navbar = document.querySelector('.custom-navbar');

    window.addEventListener('scroll', function () {
        if (window.scrollY > 100) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }

        // Back to top button
        const backToTop = document.getElementById('backToTop');
        if (window.scrollY > 300) {
            backToTop.classList.add('show');
        } else {
            backToTop.classList.remove('show');
        }
    });

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Back to top functionality
    document.getElementById('backToTop').addEventListener('click', function () {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });

    // Counter animation
    const animateCounter = (element, target, duration = 2000) => {
        let start = 0;
        const increment = target / (duration / 16);
        const timer = setInterval(() => {
            start += increment;
            if (start >= target) {
                element.textContent = target + (element.textContent.includes('%') ? '%' : '+');
                clearInterval(timer);
            } else {
                element.textContent = Math.floor(start) + (element.textContent.includes('%') ? '%' : '+');
            }
        }, 16);
    };

    // Intersection Observer for animations
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animated');

                // Animate counters in stats section
                if (entry.target.classList.contains('stat-box')) {
                    const counter = entry.target.querySelector('.counter');
                    if (counter) {
                        const target = parseInt(counter.getAttribute('data-target'));
                        if (!isNaN(target)) {
                            animateCounter(counter, target);
                        }
                    }
                }
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });

    // Observe all animate-on-scroll elements
    document.querySelectorAll('.animate-on-scroll').forEach(element => {
        observer.observe(element);
    });

    // Auto-advance carousel
    const myCarousel = document.getElementById('mainCarousel');
    if (myCarousel) {
        const carousel = new bootstrap.Carousel(myCarousel, {
            interval: 5000,
            wrap: true
        });
    }

    // Add loading animation
    window.addEventListener('load', function () {
        document.body.classList.add('loaded');
    });

    // Interactive feature cards
    const featureCards = document.querySelectorAll('.feature-card');
    featureCards.forEach(card => {
        card.addEventListener('mouseenter', function () {
            this.style.transform = 'translateY(-10px) scale(1.02)';
        });

        card.addEventListener('mouseleave', function () {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });

    // Add pulse animation to CTA buttons
    const ctaButtons = document.querySelectorAll('.cta-buttons .btn');
    setInterval(() => {
        ctaButtons.forEach(button => {
            button.style.transform = 'scale(1.05)';
            setTimeout(() => {
                button.style.transform = 'scale(1)';
            }, 300);
        });
    }, 3000);

    // Initialize calculator
    initializeCalculator();
});

// ==================== MODAL-BASED PRICE CALCULATOR FUNCTIONS ====================

// Update vehicle type based on weight
function updateVehicleType() {
    const weight = parseInt(document.getElementById('parcelWeight').value);
    const vehicleType = document.getElementById('vehicleType');

    if (weight >= 30 && weight <= 300) {
        vehicleType.value = 'mini';
    } else if (weight > 300 && weight <= 1000) {
        vehicleType.value = 'lcv';
    } else if (weight > 1000 && weight <= 5000) {
        vehicleType.value = 'mcv';
    } else if (weight > 5000 && weight <= 16000) {
        vehicleType.value = 'hcv';
    } else if (weight > 16000 && weight <= 35000) {
        vehicleType.value = 'trailer';
    }
}

// Main calculation function - MODIFIED FOR MODAL
function calculatePrice() {
    const fromLocation = document.getElementById('fromLocation');
    const toLocation = document.getElementById('toLocation');
    const parcelWeight = document.getElementById('parcelWeight');
    const vehicleType = document.getElementById('vehicleType');
    
    // Check if elements exist
    if (!fromLocation || !toLocation || !parcelWeight || !vehicleType) {
        showToast('Calculator not loaded properly. Please refresh the page.', 'error');
        return;
    }
    
    const from = fromLocation.value;
    const to = toLocation.value;
    const weight = parseInt(parcelWeight.value);
    const vehicle = vehicleType.value;
    
    // Validation
    if (!from || !to) {
        showToast('Please enter both pickup and delivery locations', 'error');
        return;
    }
    
    if (isNaN(weight) || weight < 30) {
        showToast('Minimum weight is 30 kg', 'error');
        return;
    }
    
    // Calculate everything
    const distance = calculateDistance(from, to);
    const priceDetails = calculateShippingPrice(weight, distance, vehicle);
    const deliveryTime = calculateDeliveryTime(distance, vehicle);
    
    // Show results in modal
    showResultsInModal(priceDetails, distance, deliveryTime);
}

// Show results in modal
function showResultsInModal(priceDetails, distance, deliveryTime) {
    // Format numbers with Indian Rupee symbol
    const formatter = new Intl.NumberFormat('en-IN', {
        style: 'currency',
        currency: 'INR',
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    });

    // Update modal content
    document.getElementById('modalCalculatedPrice').textContent = formatter.format(priceDetails.total);
    document.getElementById('modalBaseFare').textContent = formatter.format(priceDetails.basePrice);
    document.getElementById('modalDistanceCharge').textContent = formatter.format(priceDetails.distancePrice);
    document.getElementById('modalWeightCharge').textContent = formatter.format(priceDetails.weightPrice);
    document.getElementById('modalGstAmount').textContent = formatter.format(priceDetails.gst);
    document.getElementById('modalTotalAmount').textContent = formatter.format(priceDetails.total);
    document.getElementById('modalDistanceInfo').textContent = distance + ' km';
    document.getElementById('modalDeliveryTime').textContent = deliveryTime;

    // Show modal
    const resultsModal = new bootstrap.Modal(document.getElementById('resultsModal'));
    resultsModal.show();
}

// Calculate distance between locations
function calculateDistance(from, to) {
    const distances = {
        'delhi-mumbai': 1412,
        'mumbai-delhi': 1412,
        'delhi-bangalore': 2174,
        'bangalore-delhi': 2174,
        'mumbai-bangalore': 984,
        'bangalore-mumbai': 984,
        'delhi-chennai': 2180,
        'chennai-delhi': 2180,
        'mumbai-chennai': 1336,
        'chennai-mumbai': 1336,
        'bangalore-chennai': 347,
        'chennai-bangalore': 347,
        'delhi-kolkata': 1532,
        'kolkata-delhi': 1532,
        'mumbai-kolkata': 2048,
        'kolkata-mumbai': 2048
    };
    
    const key = from.toLowerCase() + '-' + to.toLowerCase();
    
    if (distances[key]) {
        return distances[key];
    }
    
    // For unknown routes
    let hash = 0;
    for (let i = 0; i < key.length; i++) {
        hash = ((hash << 5) - hash) + key.charCodeAt(i);
        hash = hash & hash;
    }
    
    return Math.abs(hash % 2400) + 100;
}

// Calculate shipping price with breakdown
function calculateShippingPrice(weight, distance, vehicleType) {
    const rates = {
        mini: { base: 500, perKm: 15, perKg: 8 },
        lcv: { base: 800, perKm: 20, perKg: 6 },
        mcv: { base: 1200, perKm: 25, perKg: 5 },
        hcv: { base: 2000, perKm: 30, perKg: 4 },
        trailer: { base: 3000, perKm: 35, perKg: 3 }
    };
    
    const vehicle = rates[vehicleType];
    
    const basePrice = vehicle.base;
    const distancePrice = distance * vehicle.perKm;
    const weightPrice = weight * vehicle.perKg;
    const subtotal = basePrice + distancePrice + weightPrice;
    const gst = subtotal * 0.18;
    const total = subtotal + gst;
    
    return {
        basePrice,
        distancePrice,
        weightPrice,
        gst,
        total
    };
}

// Calculate delivery time
function calculateDeliveryTime(distance, vehicleType) {
    let baseDays = Math.ceil(distance / 400);
    
    if (vehicleType === 'mini') baseDays += 0.5;
    if (vehicleType === 'trailer') baseDays += 1;
    
    const minDays = Math.max(1, Math.floor(baseDays));
    const maxDays = Math.ceil(baseDays + 1);
    
    return `${minDays}-${maxDays} days`;
}

// Book delivery function - UPDATED FOR MODAL
function bookDelivery() {
    const fromLocation = document.getElementById('fromLocation').value;
    const toLocation = document.getElementById('toLocation').value;
    const weight = document.getElementById('parcelWeight').value;
    const vehicleType = document.getElementById('vehicleType').value;
    const price = document.getElementById('modalCalculatedPrice').textContent;
    
    // Close results modal first
    const resultsModal = bootstrap.Modal.getInstance(document.getElementById('resultsModal'));
    if (resultsModal) {
        resultsModal.hide();
    }
    
    // Check authentication
    if (!isCustomerAuthenticated()) {
        showLoginPrompt(fromLocation, toLocation, weight, vehicleType, price);
        return;
    }
    
    // If authenticated, proceed with booking confirmation
    confirmBooking(fromLocation, toLocation, weight, vehicleType, price);
}

// Check if user is authenticated as customer
function isCustomerAuthenticated() {
    // This would check your Django authentication
    // For now, return false to test login prompt
    return false;
}

// Show login prompt for unauthenticated users
function showLoginPrompt(fromLocation, toLocation, weight, vehicleType, price) {
    const promptHTML = `
        <div class="modal fade" id="loginPromptModal" tabindex="-1">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header bg-primary text-white">
                        <h5 class="modal-title">
                            <i class="fas fa-user-circle me-2"></i>Login Required
                        </h5>
                        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <div class="text-center mb-4">
                            <i class="fas fa-lock fa-3x text-primary mb-3"></i>
                            <h4>Authentication Required</h4>
                            <p class="text-muted">To book this delivery, please login or sign up as a customer.</p>
                        </div>
                        
                        <div class="booking-details-card p-3 mb-4" style="background: #f8f9fa; border-radius: 10px;">
                            <h6 class="mb-3">Delivery Summary:</h6>
                            <div class="row">
                                <div class="col-6">
                                    <small><strong>From:</strong></small><br>
                                    <span>${fromLocation}</span>
                                </div>
                                <div class="col-6">
                                    <small><strong>To:</strong></small><br>
                                    <span>${toLocation}</span>
                                </div>
                            </div>
                            <div class="row mt-2">
                                <div class="col-6">
                                    <small><strong>Weight:</strong></small><br>
                                    <span>${weight} kg</span>
                                </div>
                                <div class="col-6">
                                    <small><strong>Vehicle:</strong></small><br>
                                    <span>${vehicleType.toUpperCase()}</span>
                                </div>
                            </div>
                            <div class="row mt-2">
                                <div class="col-12">
                                    <small><strong>Total Cost:</strong></small><br>
                                    <span class="text-primary fw-bold">${price}</span>
                                </div>
                            </div>
                        </div>
                        
                        <div class="d-grid gap-2">
                            <a href="/customer/login/" class="btn btn-primary btn-lg">
                                <i class="fas fa-sign-in-alt me-2"></i>Login as Customer
                            </a>
                            <a href="/customer/register/" class="btn btn-success btn-lg">
                                <i class="fas fa-user-plus me-2"></i>Sign Up as Customer
                            </a>
                            <button class="btn btn-outline-secondary" data-bs-dismiss="modal">
                                <i class="fas fa-times me-2"></i>Cancel
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // Remove existing modal if any
    const existingModal = document.getElementById('loginPromptModal');
    if (existingModal) {
        existingModal.remove();
    }
    
    // Add modal to body
    document.body.insertAdjacentHTML('beforeend', promptHTML);
    
    // Show modal
    const modal = new bootstrap.Modal(document.getElementById('loginPromptModal'));
    modal.show();
}

// Confirm booking for authenticated customers
function confirmBooking(fromLocation, toLocation, weight, vehicleType, price) {
    const confirmHTML = `
        <div class="modal fade" id="confirmBookingModal" tabindex="-1">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header bg-success text-white">
                        <h5 class="modal-title">
                            <i class="fas fa-check-circle me-2"></i>Confirm Booking
                        </h5>
                        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <div class="text-center mb-4">
                            <i class="fas fa-shipping-fast fa-3x text-success mb-3"></i>
                            <h4>Ready to Book!</h4>
                            <p class="text-muted">Please review your delivery details below:</p>
                        </div>
                        
                        <div class="booking-summary-card p-3 mb-4" style="background: #f8f9fa; border-radius: 10px;">
                            <div class="row">
                                <div class="col-6 mb-2">
                                    <small><strong>From:</strong></small><br>
                                    <span>${fromLocation}</span>
                                </div>
                                <div class="col-6 mb-2">
                                    <small><strong>To:</strong></small><br>
                                    <span>${toLocation}</span>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-6 mb-2">
                                    <small><strong>Weight:</strong></small><br>
                                    <span>${weight} kg</span>
                                </div>
                                <div class="col-6 mb-2">
                                    <small><strong>Vehicle:</strong></small><br>
                                    <span>${vehicleType.toUpperCase()}</span>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-12">
                                    <small><strong>Total Amount:</strong></small><br>
                                    <span class="text-success fw-bold fs-5">${price}</span>
                                </div>
                            </div>
                        </div>
                        
                        <div class="d-grid gap-2">
                            <button class="btn btn-success btn-lg" onclick="proceedToCheckout()">
                                <i class="fas fa-credit-card me-2"></i>Proceed to Payment
                            </button>
                            <button class="btn btn-outline-secondary" data-bs-dismiss="modal">
                                <i class="fas fa-edit me-2"></i>Modify Details
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // Remove existing modal if any
    const existingModal = document.getElementById('confirmBookingModal');
    if (existingModal) {
        existingModal.remove();
    }
    
    // Add modal to body
    document.body.insertAdjacentHTML('beforeend', confirmHTML);
    
    // Show modal
    const modal = new bootstrap.Modal(document.getElementById('confirmBookingModal'));
    modal.show();
}

// Proceed to checkout (for authenticated customers)
function proceedToCheckout() {
    // Close the confirmation modal
    const modal = bootstrap.Modal.getInstance(document.getElementById('confirmBookingModal'));
    if (modal) {
        modal.hide();
    }

    // Show success message
    showToast('Redirecting to checkout page...', 'success');

    // In a real application, you would redirect to the checkout page
    // window.location.href = '/checkout/';

    // For demo purposes, show a success message after a delay
    setTimeout(() => {
        showToast('Booking confirmed! Your delivery has been scheduled.', 'success');
    }, 1000);
}

// Reset calculator
function resetCalculator() {
    document.getElementById('fromLocation').value = 'Delhi';
    document.getElementById('toLocation').value = 'Mumbai';
    document.getElementById('parcelWeight').value = 30;
    document.getElementById('vehicleType').value = 'mini';
}

// Toast notification function
function showToast(message, type = 'info') {
    // Remove existing toasts
    const existingToasts = document.querySelectorAll('.custom-toast');
    existingToasts.forEach(toast => toast.remove());

    const toast = document.createElement('div');
    toast.className = `custom-toast toast-${type}`;
    toast.innerHTML = `
        <div class="toast-content">
            <i class="fas ${type === 'error' ? 'fa-exclamation-circle' : type === 'success' ? 'fa-check-circle' : 'fa-info-circle'} me-2"></i>
            ${message}
        </div>
    `;

    // Add styles
    toast.style.cssText = `
        position: fixed;
        top: 100px;
        right: 20px;
        background: ${type === 'error' ? '#dc3545' : type === 'success' ? '#198754' : '#0dcaf0'};
        color: white;
        padding: 15px 20px;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        z-index: 9999;
        max-width: 400px;
        animation: slideInRight 0.3s ease;
    `;

    document.body.appendChild(toast);

    // Remove toast after 5 seconds
    setTimeout(() => {
        toast.style.animation = 'slideOutRight 0.3s ease';
        setTimeout(() => toast.remove(), 300);
    }, 5000);
}

// Initialize calculator
function initializeCalculator() {
    // Set default values
    resetCalculator();
    
    // Update vehicle type when weight changes
    const weightInput = document.getElementById('parcelWeight');
    if (weightInput) {
        weightInput.addEventListener('input', updateVehicleType);
    }
}

// Add some interactive console message
console.log('🚀 SmartRoute - Transforming Transportation Logistics');
console.log('📍 Calculator system initialized with modal approach');