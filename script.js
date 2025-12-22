// Dashboard Navigation and Interactivity
document.addEventListener('DOMContentLoaded', function() {
    // Navigation functionality
    const navButtons = document.querySelectorAll('.nav-btn');
    const sections = document.querySelectorAll('.dashboard-section');

    navButtons.forEach(button => {
        button.addEventListener('click', function() {
            const targetSection = this.getAttribute('data-section');
            
            // Remove active class from all buttons and sections
            navButtons.forEach(btn => btn.classList.remove('active'));
            sections.forEach(section => section.classList.remove('active'));
            
            // Add active class to clicked button and corresponding section
            this.classList.add('active');
            document.getElementById(targetSection).classList.add('active');
            
            // Smooth scroll to top of main content
            document.querySelector('.dashboard-main').scrollIntoView({ 
                behavior: 'smooth' 
            });
        });
    });

    // Add hover effects to metric cards
    const metricCards = document.querySelectorAll('.metric-card');
    metricCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-8px) scale(1.02)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });

    // Add click effects to champion cards
    const championCards = document.querySelectorAll('.champion-card');
    championCards.forEach(card => {
        card.addEventListener('click', function() {
            // Add a pulse effect
            this.style.animation = 'pulse 0.6s ease';
            setTimeout(() => {
                this.style.animation = '';
            }, 600);
        });
    });

    // Add interactive timeline effects
    const timelineItems = document.querySelectorAll('.timeline-item');
    
    // Intersection Observer for timeline animations
    const observerOptions = {
        threshold: 0.3,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateX(0)';
            }
        });
    }, observerOptions);

    timelineItems.forEach((item, index) => {
        // Initial state for animation
        item.style.opacity = '0';
        item.style.transition = 'all 0.6s ease';
        
        // Alternate slide directions
        if (index % 2 === 0) {
            item.style.transform = 'translateX(-50px)';
        } else {
            item.style.transform = 'translateX(50px)';
        }
        
        observer.observe(item);
    });

    // Add sector card interactions
    const sectorCards = document.querySelectorAll('.sector-card');
    sectorCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            const icon = this.querySelector('.sector-icon');
            icon.style.transform = 'scale(1.2) rotate(10deg)';
            icon.style.transition = 'transform 0.3s ease';
        });
        
        card.addEventListener('mouseleave', function() {
            const icon = this.querySelector('.sector-icon');
            icon.style.transform = 'scale(1) rotate(0deg)';
        });
    });

    // Add chart image lazy loading and zoom effect
    const chartImages = document.querySelectorAll('.chart-image');
    chartImages.forEach(img => {
        img.addEventListener('click', function() {
            // Create modal overlay for image zoom
            const modal = document.createElement('div');
            modal.style.cssText = `
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0, 0, 0, 0.9);
                display: flex;
                justify-content: center;
                align-items: center;
                z-index: 1000;
                cursor: pointer;
            `;
            
            const modalImg = document.createElement('img');
            modalImg.src = this.src;
            modalImg.style.cssText = `
                max-width: 95%;
                max-height: 95%;
                border-radius: 8px;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
            `;
            
            modal.appendChild(modalImg);
            document.body.appendChild(modal);
            
            // Close modal on click
            modal.addEventListener('click', function() {
                document.body.removeChild(modal);
            });
            
            // Close modal on escape key
            document.addEventListener('keydown', function(e) {
                if (e.key === 'Escape' && document.body.contains(modal)) {
                    document.body.removeChild(modal);
                }
            });
        });
        
        // Add hover effect to indicate clickability
        img.addEventListener('mouseenter', function() {
            this.style.cursor = 'pointer';
            this.style.transform = 'scale(1.02)';
            this.style.transition = 'transform 0.3s ease';
        });
        
        img.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
        });
    });

    // Add smooth scrolling for internal navigation
    function smoothScroll(target) {
        const element = document.querySelector(target);
        if (element) {
            element.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    }

    // Add keyboard navigation
    document.addEventListener('keydown', function(e) {
        const activeSection = document.querySelector('.dashboard-section.active');
        const currentIndex = Array.from(sections).indexOf(activeSection);
        
        if (e.key === 'ArrowRight' && currentIndex < sections.length - 1) {
            navButtons[currentIndex + 1].click();
        } else if (e.key === 'ArrowLeft' && currentIndex > 0) {
            navButtons[currentIndex - 1].click();
        }
    });

    // Add progress indicator
    function createProgressIndicator() {
        const progressBar = document.createElement('div');
        progressBar.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 0%;
            height: 3px;
            background: linear-gradient(90deg, #2E4A6B, #2ECC71);
            z-index: 1001;
            transition: width 0.3s ease;
        `;
        document.body.appendChild(progressBar);
        
        window.addEventListener('scroll', function() {
            const scrolled = (window.scrollY / (document.documentElement.scrollHeight - window.innerHeight)) * 100;
            progressBar.style.width = scrolled + '%';
        });
    }
    
    createProgressIndicator();

    // Add loading animation for images
    chartImages.forEach(img => {
        img.addEventListener('load', function() {
            this.style.opacity = '0';
            this.style.transform = 'translateY(20px)';
            this.style.transition = 'all 0.6s ease';
            
            setTimeout(() => {
                this.style.opacity = '1';
                this.style.transform = 'translateY(0)';
            }, 100);
        });
    });

    // Add tooltip functionality for metrics
    const metricValues = document.querySelectorAll('.metric-value');
    metricValues.forEach(metric => {
        metric.addEventListener('mouseenter', function() {
            const tooltip = document.createElement('div');
            tooltip.className = 'tooltip';
            tooltip.textContent = 'Click to learn more about this metric';
            tooltip.style.cssText = `
                position: absolute;
                background: #2c3e50;
                color: white;
                padding: 8px 12px;
                border-radius: 4px;
                font-size: 12px;
                white-space: nowrap;
                z-index: 1000;
                pointer-events: none;
                transform: translateX(-50%);
                margin-top: -40px;
                left: 50%;
            `;
            
            this.style.position = 'relative';
            this.appendChild(tooltip);
        });
        
        metric.addEventListener('mouseleave', function() {
            const tooltip = this.querySelector('.tooltip');
            if (tooltip) {
                this.removeChild(tooltip);
            }
        });
    });

    // Add section transition effects
    function addSectionTransitions() {
        const style = document.createElement('style');
        style.textContent = `
            @keyframes pulse {
                0% { transform: scale(1); }
                50% { transform: scale(1.05); }
                100% { transform: scale(1); }
            }
            
            .dashboard-section {
                opacity: 0;
                transform: translateY(30px);
                transition: all 0.5s ease;
            }
            
            .dashboard-section.active {
                opacity: 1;
                transform: translateY(0);
            }
        `;
        document.head.appendChild(style);
    }
    
    addSectionTransitions();

    console.log('EU Tourism Recovery Dashboard loaded successfully! 🚀');
    console.log('Navigate with arrow keys or click the navigation buttons');
});