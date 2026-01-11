/* ==========================================
   ANIMATIONS & INTERACTIONS - אנימציות ותגובות
   ========================================== */

document.addEventListener('DOMContentLoaded', function () {
    initializeAnimations();
    initializeLoaders();
    initializeScrollEffects();
    initializeInteractions();
});

/* ==========================================
   Initialize Animations
   ========================================== */

function initializeAnimations() {
    // Observe elements for intersection
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -100px 0px'
    };

    const observer = new IntersectionObserver(function (entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-fade-in');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observe all cards and feature elements
    document.querySelectorAll('.feature-card, .card').forEach(el => {
        observer.observe(el);
    });

    // Stagger animation delays
    document.querySelectorAll('[data-animate]').forEach((el, index) => {
        el.style.animationDelay = (index * 0.1) + 's';
    });
}

/* ==========================================
   Loading Effects
   ========================================== */

function initializeLoaders() {
    const loader = document.getElementById('site-loader');

    // Don't auto-show loader on page load
    // Page navigation loaders are disabled to prevent animation issues
}

/* ==========================================
   Scroll Effects
   ========================================== */

function initializeScrollEffects() {
    const navbar = document.querySelector('.navbar');
    let lastScrollTop = 0;

    window.addEventListener('scroll', function () {
        let scrollTop = window.pageYOffset || document.documentElement.scrollTop;

        if (navbar) {
            if (scrollTop > 50) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        }

        lastScrollTop = scrollTop <= 0 ? 0 : scrollTop;
    }, false);

    // Parallax effect for hero elements
    const heroSection = document.querySelector('.welcome-section');
    if (heroSection) {
        window.addEventListener('scroll', function () {
            const scrollPercent = window.scrollY / (heroSection.offsetHeight / 2);
            const bubbles = document.querySelectorAll('.accent-bubble');
            bubbles.forEach((bubble, index) => {
                bubble.style.transform = `translateY(${scrollPercent * 50 * (index + 1)}px)`;
            });
        });
    }
}

/* ==========================================
   Interactions & Hover Effects
   ========================================== */

function initializeInteractions() {
    // Button ripple effect
    document.querySelectorAll('.btn').forEach(button => {
        button.addEventListener('click', function (e) {
            createRipple(e, this);
        });
    });

    // Card hover effects
    document.querySelectorAll('.feature-card').forEach(card => {
        card.addEventListener('mouseenter', function () {
            this.style.transform = 'translateY(-10px)';
        });
        card.addEventListener('mouseleave', function () {
            this.style.transform = 'translateY(0)';
        });
    });

    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(link => {
        link.addEventListener('click', function (e) {
            if (this.getAttribute('href') !== '#') {
                e.preventDefault();
                const targetId = this.getAttribute('href');
                const targetElement = document.querySelector(targetId);
                if (targetElement) {
                    targetElement.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });
}

/* ==========================================
   Create Ripple Effect
   ========================================== */

function createRipple(event, element) {
    const ripple = document.createElement('span');
    const rect = element.getBoundingClientRect();
    const size = Math.max(rect.width, rect.height);
    const x = event.clientX - rect.left - size / 2;
    const y = event.clientY - rect.top - size / 2;

    ripple.style.width = ripple.style.height = size + 'px';
    ripple.style.left = x + 'px';
    ripple.style.top = y + 'px';
    ripple.classList.add('ripple');

    // Add styles for ripple
    const style = document.createElement('style');
    if (!document.getElementById('ripple-styles')) {
        style.id = 'ripple-styles';
        style.textContent = `
            .btn {
                position: relative;
                overflow: hidden;
            }
            .ripple {
                position: absolute;
                border-radius: 50%;
                background: rgba(255, 255, 255, 0.6);
                transform: scale(0);
                animation: ripple-animation 0.6s ease-out;
                pointer-events: none;
            }
            @keyframes ripple-animation {
                to {
                    transform: scale(4);
                    opacity: 0;
                }
            }
        `;
        document.head.appendChild(style);
    }

    element.appendChild(ripple);
    setTimeout(() => ripple.remove(), 600);
}

/* ==========================================
   Form Validation & Interactions
   ========================================== */

function validateForm(formElement) {
    const inputs = formElement.querySelectorAll('input, textarea, select');
    let isValid = true;

    inputs.forEach(input => {
        if (!input.value.trim()) {
            input.classList.add('is-invalid');
            isValid = false;
        } else {
            input.classList.remove('is-invalid');
            input.classList.add('is-valid');
        }
    });

    return isValid;
}

/* ==========================================
   Counter Animation
   ========================================== */

function animateCounter(element, targetNumber, duration = 2000) {
    let currentNumber = 0;
    const increment = targetNumber / (duration / 16);
    const counter = setInterval(() => {
        currentNumber += increment;
        if (currentNumber >= targetNumber) {
            element.textContent = targetNumber;
            clearInterval(counter);
        } else {
            element.textContent = Math.floor(currentNumber);
        }
    }, 16);
}

/* ==========================================
   Tooltip Initialization
   ========================================== */

function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/* ==========================================
   Toast Notification
   ========================================== */

function showToast(message, type = 'info', duration = 3000) {
    const toastContainer = document.getElementById('toast-container') || createToastContainer();
    const toast = document.createElement('div');
    toast.className = `alert alert-${type} alert-dismissible fade show`;
    toast.setAttribute('role', 'alert');
    toast.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;

    toastContainer.appendChild(toast);

    setTimeout(() => {
        toast.remove();
    }, duration);
}

function createToastContainer() {
    const container = document.createElement('div');
    container.id = 'toast-container';
    container.style.cssText = `
        position: fixed;
        top: 100px;
        right: 20px;
        z-index: 9999;
        max-width: 400px;
    `;
    document.body.appendChild(container);
    return container;
}

/* ==========================================
   Lazy Loading Images
   ========================================== */

function initializeLazyLoading() {
    const images = document.querySelectorAll('img[data-src]');
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.removeAttribute('data-src');
                observer.unobserve(img);
            }
        });
    });

    images.forEach(img => imageObserver.observe(img));
}

/* ==========================================
   Dark Mode Toggle (Optional)
   ========================================== */

function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
    localStorage.setItem('darkMode', document.body.classList.contains('dark-mode'));
}

// Initialize dark mode on load
if (localStorage.getItem('darkMode') === 'true') {
    document.body.classList.add('dark-mode');
}

/* ==========================================
   Keyboard Shortcuts (Optional)
   ========================================== */

document.addEventListener('keydown', function (e) {
    // Ctrl+M or Cmd+M to toggle mobile menu
    if ((e.ctrlKey || e.metaKey) && e.key === 'm') {
        e.preventDefault();
        const navbarToggler = document.querySelector('.navbar-toggler');
        if (navbarToggler) navbarToggler.click();
    }

    // Esc to close modals
    if (e.key === 'Escape') {
        const modals = document.querySelectorAll('.modal.show');
        modals.forEach(modal => {
            const bootstrapModal = bootstrap.Modal.getInstance(modal);
            if (bootstrapModal) bootstrapModal.hide();
        });
    }
});

/* ==========================================
   Export functions for external use
   ========================================== */

window.AppUtils = {
    validateForm,
    animateCounter,
    showToast,
    initializeTooltips,
    initializeLazyLoading,
    toggleDarkMode
};
