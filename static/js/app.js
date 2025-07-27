// Modern Virtual Try-On Interface JavaScript
// Enhanced with liquid glass interactions and smooth animations

class VirtualTryOnApp {
    constructor() {
        this.personImageFile = null;
        this.garmentImageFile = null;
        this.isProcessing = false;

        this.init();
        this.createFloatingOrbs();
        this.initAnimations();
    }

    init() {
        this.bindEvents();
        this.initDragAndDrop();
        this.initParticleEffects();
        this.preloadImages();
    }

    // Create floating orbs background
    createFloatingOrbs() {
        const orbsContainer = document.createElement('div');
        orbsContainer.className = 'floating-orbs';

        for (let i = 0; i < 3; i++) {
            const orb = document.createElement('div');
            orb.className = 'orb';
            orbsContainer.appendChild(orb);
        }

        document.body.appendChild(orbsContainer);
    }

    // Initialize animations
    initAnimations() {
        // Animate elements on scroll
        this.observeElements();

        // Add mouse movement parallax
        this.initParallax();

        // Add button hover effects
        this.enhanceButtons();
    }

    // Observe elements for scroll animations
    observeElements() {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }
            });
        }, { threshold: 0.1 });

        document.querySelectorAll('.upload-card, .instructions, .process-section').forEach(el => {
            el.style.opacity = '0';
            el.style.transform = 'translateY(30px)';
            el.style.transition = 'all 0.6s ease-out';
            observer.observe(el);
        });
    }

    // Initialize parallax effect
    initParallax() {
        document.addEventListener('mousemove', (e) => {
            const { clientX, clientY } = e;
            const { innerWidth, innerHeight } = window;

            const xPercent = (clientX / innerWidth - 0.5) * 2;
            const yPercent = (clientY / innerHeight - 0.5) * 2;

            // Move floating orbs
            document.querySelectorAll('.orb').forEach((orb, index) => {
                const speed = (index + 1) * 0.5;
                orb.style.transform = `translate(${xPercent * speed * 10}px, ${yPercent * speed * 10}px)`;
            });

            // Move glass cards slightly
            document.querySelectorAll('.upload-card').forEach((card, index) => {
                const speed = 0.2;
                card.style.transform = `translate(${xPercent * speed * 2}px, ${yPercent * speed * 2}px)`;
            });
        });
    }

    // Enhance button interactions
    enhanceButtons() {
        document.querySelectorAll('.upload-button, .process-button').forEach(button => {
            button.addEventListener('mouseenter', (e) => {
                this.createRipple(e);
            });

            button.addEventListener('click', (e) => {
                this.createClickEffect(e);
            });
        });
    }

    // Create ripple effect
    createRipple(e) {
        const button = e.currentTarget;
        const rect = button.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const ripple = document.createElement('div');

        ripple.style.width = ripple.style.height = size + 'px';
        ripple.style.left = (e.clientX - rect.left - size / 2) + 'px';
        ripple.style.top = (e.clientY - rect.top - size / 2) + 'px';
        ripple.style.position = 'absolute';
        ripple.style.borderRadius = '50%';
        ripple.style.background = 'rgba(255, 255, 255, 0.3)';
        ripple.style.transform = 'scale(0)';
        ripple.style.animation = 'ripple 0.6s linear';
        ripple.style.pointerEvents = 'none';

        button.appendChild(ripple);

        setTimeout(() => {
            ripple.remove();
        }, 600);
    }

    // Create click effect
    createClickEffect(e) {
        const button = e.currentTarget;
        button.style.transform = 'scale(0.95)';
        setTimeout(() => {
            button.style.transform = '';
        }, 150);
    }

    // Initialize particle effects
    initParticleEffects() {
        // Add CSS for ripple animation
        const style = document.createElement('style');
        style.textContent = `
            @keyframes ripple {
                to {
                    transform: scale(4);
                    opacity: 0;
                }
            }

            .particle {
                position: absolute;
                width: 4px;
                height: 4px;
                background: rgba(139, 95, 191, 0.8);
                border-radius: 50%;
                pointer-events: none;
                animation: particle-float 2s ease-out forwards;
            }

            @keyframes particle-float {
                0% {
                    transform: translateY(0) scale(1);
                    opacity: 1;
                }
                100% {
                    transform: translateY(-100px) scale(0);
                    opacity: 0;
                }
            }
        `;
        document.head.appendChild(style);
    }

    // Bind event listeners
    bindEvents() {
        // Image upload handlers
        document.getElementById('personImage').addEventListener('change', (e) => {
            this.handleImageUpload(e, 'person');
        });

        document.getElementById('garmentImage').addEventListener('change', (e) => {
            this.handleImageUpload(e, 'garment');
        });

        // Process button
        document.getElementById('processButton').addEventListener('click', () => {
            this.processImages();
        });

        // Upload button clicks
        document.querySelectorAll('.upload-button').forEach(button => {
            button.addEventListener('click', (e) => {
                const card = e.target.closest('.upload-card');
                const input = card.querySelector('.upload-input');
                input.click();
            });
        });
    }

    // Handle image upload with animations
    handleImageUpload(e, type) {
        const file = e.target.files[0];
        if (!file) return;

        // Validate file size
        if (file.size > 10 * 1024 * 1024) {
            this.showError(`${type} image file is too large. Please choose a file smaller than 10MB.`);
            return;
        }

        // Store file reference
        if (type === 'person') {
            this.personImageFile = file;
        } else {
            this.garmentImageFile = file;
        }

        // Create preview with animation
        const reader = new FileReader();
        reader.onload = (e) => {
            const preview = document.getElementById(`${type}Preview`);
            const card = preview.closest('.upload-card');

            // Add loading animation
            card.style.transform = 'scale(1.02)';
            card.style.filter = 'blur(2px)';

            setTimeout(() => {
                preview.src = e.target.result;
                preview.style.display = 'block';
                preview.style.opacity = '0';
                preview.style.transform = 'scale(0.8)';

                // Animate preview appearance
                requestAnimationFrame(() => {
                    preview.style.transition = 'all 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55)';
                    preview.style.opacity = '1';
                    preview.style.transform = 'scale(1)';
                });

                // Reset card
                card.style.transform = '';
                card.style.filter = '';

                // Create success particles
                this.createSuccessParticles(card);
            }, 300);
        };

        reader.readAsDataURL(file);
        this.checkCanProcess();
    }

    // Create success particles
    createSuccessParticles(element) {
        const rect = element.getBoundingClientRect();
        const centerX = rect.left + rect.width / 2;
        const centerY = rect.top + rect.height / 2;

        for (let i = 0; i < 6; i++) {
            setTimeout(() => {
                const particle = document.createElement('div');
                particle.className = 'particle';
                particle.style.left = centerX + Math.random() * 40 - 20 + 'px';
                particle.style.top = centerY + Math.random() * 40 - 20 + 'px';
                document.body.appendChild(particle);

                setTimeout(() => particle.remove(), 2000);
            }, i * 100);
        }
    }

    // Initialize drag and drop
    initDragAndDrop() {
        ['personImage', 'garmentImage'].forEach(id => {
            const card = document.querySelector(`#${id}`).closest('.upload-card');
            const input = document.getElementById(id);

            card.addEventListener('dragover', (e) => {
                e.preventDefault();
                card.style.borderColor = 'rgba(139, 95, 191, 0.8)';
                card.style.background = 'linear-gradient(135deg, rgba(139, 95, 191, 0.2) 0%, rgba(106, 76, 147, 0.1) 100%)';
                card.style.transform = 'scale(1.02)';
            });

            card.addEventListener('dragleave', (e) => {
                e.preventDefault();
                this.resetCardStyle(card);
            });

            card.addEventListener('drop', (e) => {
                e.preventDefault();
                this.resetCardStyle(card);

                const files = e.dataTransfer.files;
                if (files.length > 0) {
                    input.files = files;
                    input.dispatchEvent(new Event('change'));
                }
            });
        });
    }

    // Reset card style
    resetCardStyle(card) {
        card.style.borderColor = '';
        card.style.background = '';
        card.style.transform = '';
    }

    // Check if processing can be enabled
    checkCanProcess() {
        const processButton = document.getElementById('processButton');
        if (this.personImageFile && this.garmentImageFile && !this.isProcessing) {
            processButton.disabled = false;
            processButton.style.animation = 'pulse 2s infinite';
        } else {
            processButton.disabled = true;
            processButton.style.animation = 'none';
        }
    }

    // Show error message with animation
    showError(message) {
        const errorElement = document.getElementById('errorMessage');
        errorElement.textContent = message;
        errorElement.style.display = 'block';
        errorElement.style.animation = 'slideInDown 0.5s ease-out';

        document.getElementById('successMessage').style.display = 'none';

        // Auto hide after 5 seconds
        setTimeout(() => {
            errorElement.style.animation = 'slideInUp 0.5s ease-out reverse';
            setTimeout(() => {
                errorElement.style.display = 'none';
            }, 500);
        }, 5000);
    }

    // Show success message with animation
    showSuccess(message) {
        const successElement = document.getElementById('successMessage');
        successElement.textContent = message;
        successElement.style.display = 'block';
        successElement.style.animation = 'slideInDown 0.5s ease-out';

        document.getElementById('errorMessage').style.display = 'none';

        // Auto hide after 3 seconds
        setTimeout(() => {
            successElement.style.animation = 'slideInUp 0.5s ease-out reverse';
            setTimeout(() => {
                successElement.style.display = 'none';
            }, 500);
        }, 3000);
    }

    // Hide messages
    hideMessages() {
        document.getElementById('errorMessage').style.display = 'none';
        document.getElementById('successMessage').style.display = 'none';
    }

    // Show loading with enhanced animation
    showLoading() {
        const loadingElement = document.getElementById('loading');
        loadingElement.style.display = 'block';
        loadingElement.style.animation = 'fadeIn 0.5s ease-out';

        // Add random loading messages
        const messages = [
            'Analyzing your style...',
            'Preparing the virtual fitting room...',
            'AI is trying on your garment...',
            'Adjusting the perfect fit...',
            'Adding finishing touches...',
            'Almost ready!'
        ];

        const messageElement = loadingElement.querySelector('p');
        let messageIndex = 0;

        const messageInterval = setInterval(() => {
            messageElement.style.opacity = '0';
            setTimeout(() => {
                messageElement.textContent = messages[messageIndex % messages.length];
                messageElement.style.opacity = '1';
                messageIndex++;
            }, 300);
        }, 3000);

        // Store interval to clear later
        this.messageInterval = messageInterval;
    }

    // Hide loading
    hideLoading() {
        const loadingElement = document.getElementById('loading');
        loadingElement.style.animation = 'fadeOut 0.5s ease-out';
        setTimeout(() => {
            loadingElement.style.display = 'none';
        }, 500);

        if (this.messageInterval) {
            clearInterval(this.messageInterval);
        }
    }

    // Show results with dramatic animation
    showResults(imageData) {
        const resultsSection = document.getElementById('results');
        const resultImage = document.getElementById('resultImage');

        resultImage.src = imageData;
        resultsSection.style.display = 'block';
        resultsSection.style.animation = 'zoomIn 0.8s cubic-bezier(0.68, -0.55, 0.265, 1.55)';

        // Add image load animation
        resultImage.onload = () => {
            resultImage.style.animation = 'imageReveal 1s ease-out';
            this.createCelebrationEffect();
        };
    }

    // Create celebration effect
    createCelebrationEffect() {
        const colors = ['#8B5FBF', '#667eea', '#f093fb', '#f5576c'];

        for (let i = 0; i < 20; i++) {
            setTimeout(() => {
                const confetti = document.createElement('div');
                confetti.style.position = 'fixed';
                confetti.style.width = '10px';
                confetti.style.height = '10px';
                confetti.style.background = colors[Math.floor(Math.random() * colors.length)];
                confetti.style.left = Math.random() * window.innerWidth + 'px';
                confetti.style.top = '-10px';
                confetti.style.borderRadius = '50%';
                confetti.style.pointerEvents = 'none';
                confetti.style.zIndex = '1000';
                confetti.style.animation = 'confetti-fall 3s ease-out forwards';

                document.body.appendChild(confetti);

                setTimeout(() => confetti.remove(), 3000);
            }, i * 100);
        }

        // Add confetti animation if not exists
        if (!document.querySelector('#confetti-style')) {
            const style = document.createElement('style');
            style.id = 'confetti-style';
            style.textContent = `
                @keyframes confetti-fall {
                    0% {
                        transform: translateY(-100vh) rotate(0deg);
                        opacity: 1;
                    }
                    100% {
                        transform: translateY(100vh) rotate(360deg);
                        opacity: 0;
                    }
                }
            `;
            document.head.appendChild(style);
        }
    }

    // Process images with enhanced UX
    async processImages() {
        if (!this.personImageFile || !this.garmentImageFile || this.isProcessing) {
            this.showError('Please upload both person and garment images.');
            return;
        }

        this.isProcessing = true;
        this.hideMessages();
        this.showLoading();

        // Disable process button with animation
        const processButton = document.getElementById('processButton');
        processButton.disabled = true;
        processButton.style.animation = 'none';
        processButton.style.transform = 'scale(0.95)';

        // Hide results section
        document.getElementById('results').style.display = 'none';

        try {
            const formData = new FormData();
            formData.append('person_image', this.personImageFile);
            formData.append('garment_image', this.garmentImageFile);

            const response = await fetch('/process', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();

            if (response.ok && result.success) {
                this.showResults(result.result_image);
                this.showSuccess('Virtual try-on completed successfully! 🎉');

                // Scroll to results smoothly
                setTimeout(() => {
                    document.getElementById('results').scrollIntoView({
                        behavior: 'smooth',
                        block: 'center'
                    });
                }, 500);
            } else {
                this.showError(result.error || 'Failed to process images. Please try again.');
            }
        } catch (error) {
            console.error('Error:', error);
            this.showError('Network error. Please check your connection and try again.');
        } finally {
            this.isProcessing = false;
            this.hideLoading();
            processButton.style.transform = '';
            this.checkCanProcess();
        }
    }

    // Preload images for better performance
    preloadImages() {
        const imageUrls = [
            // Add any placeholder images or icons here
        ];

        imageUrls.forEach(url => {
            const img = new Image();
            img.src = url;
        });
    }
}

// Enhanced CSS additions
const enhancedCSS = `
    @keyframes fadeOut {
        from { opacity: 1; }
        to { opacity: 0; }
    }

    .upload-card.dragover {
        transform: scale(1.05) !important;
        box-shadow: 0 25px 70px rgba(139, 95, 191, 0.4) !important;
    }

    .image-preview {
        transition: all 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
    }

    .process-button:not(:disabled):hover {
        animation: pulse 1s infinite !important;
    }
`;

// Add enhanced CSS to document
const styleSheet = document.createElement('style');
styleSheet.textContent = enhancedCSS;
document.head.appendChild(styleSheet);

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.virtualTryOnApp = new VirtualTryOnApp();
});

// Add smooth scrolling and page transitions
window.addEventListener('beforeunload', () => {
    document.body.style.opacity = '0';
    document.body.style.transform = 'scale(0.95)';
});

// Performance monitoring
if ('performance' in window) {
    window.addEventListener('load', () => {
        const perfData = performance.timing;
        const pageLoadTime = perfData.loadEventEnd - perfData.navigationStart;
        console.log(`Page loaded in ${pageLoadTime}ms`);
    });
}

// Add keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // Press 'R' to reset uploads
    if (e.key === 'r' || e.key === 'R') {
        if (e.ctrlKey || e.metaKey) {
            e.preventDefault();
            location.reload();
        }
    }

    // Press Space to process (if ready)
    if (e.code === 'Space' && e.target === document.body) {
        e.preventDefault();
        const processButton = document.getElementById('processButton');
        if (!processButton.disabled) {
            processButton.click();
        }
    }
});

// Export for potential module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = VirtualTryOnApp;
}
