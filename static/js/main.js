/* ==============================================
   MALAIKA SHOP - MAIN JAVASCRIPT
   Sidebar Drawer & Interactive Features
   ============================================== */

document.addEventListener('DOMContentLoaded', function() {
    
    // ==============================================
    // SIDEBAR DRAWER FUNCTIONALITY
    // ==============================================
    const menuToggle = document.getElementById('menuToggle');
    const sidebarOverlay = document.getElementById('sidebarOverlay');
    const sidebarDrawer = document.getElementById('sidebarDrawer');
    const sidebarClose = document.getElementById('sidebarClose');

    // Open sidebar
    if (menuToggle) {
        menuToggle.addEventListener('click', function() {
            sidebarOverlay.classList.add('active');
            sidebarDrawer.classList.add('active');
            document.body.style.overflow = 'hidden'; // Prevent background scroll
        });
    }

    // Close sidebar - via close button
    if (sidebarClose) {
        sidebarClose.addEventListener('click', closeSidebar);
    }

    // Close sidebar - via overlay click
    if (sidebarOverlay) {
        sidebarOverlay.addEventListener('click', closeSidebar);
    }

    // Close sidebar function
    function closeSidebar() {
        sidebarOverlay.classList.remove('active');
        sidebarDrawer.classList.remove('active');
        document.body.style.overflow = ''; // Restore scroll
    }

    // Close sidebar on escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && sidebarDrawer.classList.contains('active')) {
            closeSidebar();
        }
    });

    // ==============================================
    // SEARCH FUNCTIONALITY
    // ==============================================
    const searchForm = document.getElementById('searchForm');
    const searchInput = document.getElementById('searchInput');

    if (searchForm) {
        searchForm.addEventListener('submit', function(e) {
            if (searchInput.value.trim() === '') {
                e.preventDefault();
                searchInput.focus();
            }
        });
    }

    // ==============================================
    // ADD TO CART ANIMATION
    // ==============================================
    const addToCartButtons = document.querySelectorAll('.add-to-cart-btn');
    
    addToCartButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            // Add loading state
            const originalText = this.innerHTML;
            this.innerHTML = '<i class="bi bi-arrow-repeat"></i> Adding...';
            this.disabled = true;
            
            // Simulate animation (actual form submission will happen)
            setTimeout(() => {
                this.innerHTML = '<i class="bi bi-check-circle"></i> Added!';
                
                setTimeout(() => {
                    this.innerHTML = originalText;
                    this.disabled = false;
                }, 1000);
            }, 300);
        });
    });

    // ==============================================
    // SMOOTH SCROLL FOR ANCHOR LINKS
    // ==============================================
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href !== '#' && document.querySelector(href)) {
                e.preventDefault();
                document.querySelector(href).scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // ==============================================
    // AUTO-HIDE ALERTS/MESSAGES
    // ==============================================
    const alerts = document.querySelectorAll('.alert');
    
    alerts.forEach(alert => {
        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            alert.style.transition = 'opacity 0.5s ease';
            alert.style.opacity = '0';
            setTimeout(() => {
                alert.remove();
            }, 500);
        }, 5000);
    });

    // ==============================================
    // STICKY HEADER ON SCROLL
    // ==============================================
    const mainHeader = document.querySelector('.main-header');
    let lastScroll = 0;

    window.addEventListener('scroll', () => {
        const currentScroll = window.pageYOffset;
        
        if (currentScroll > 100) {
            mainHeader.style.boxShadow = '0 2px 8px rgba(0, 0, 0, 0.15)';
        } else {
            mainHeader.style.boxShadow = '0 2px 4px rgba(0, 0, 0, 0.08)';
        }
        
        lastScroll = currentScroll;
    });

    // ==============================================
    // IMAGE LAZY LOADING FALLBACK
    // ==============================================
    const images = document.querySelectorAll('img[data-src]');
    
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.add('loaded');
                observer.unobserve(img);
            }
        });
    });

    images.forEach(img => imageObserver.observe(img));

    // ==============================================
    // PRODUCT CARD HOVER EFFECT
    // ==============================================
    const productCards = document.querySelectorAll('.product-card');
    
    productCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.borderColor = '#0066cc';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.borderColor = '#e0e0e0';
        });
    });

    // ==============================================
    // RESPONSIVE SEARCH BAR
    // ==============================================
    function handleResponsiveSearch() {
        const searchBar = document.querySelector('.search-bar');
        
        if (window.innerWidth <= 768) {
            // On mobile, search bar moves to full width
            searchBar.style.order = '3';
        } else {
            searchBar.style.order = '1';
        }
    }

    // Run on load and resize
    handleResponsiveSearch();
    window.addEventListener('resize', handleResponsiveSearch);

    // ==============================================
    // CART BADGE UPDATE (if using AJAX)
    // ==============================================
    function updateCartBadge(count) {
        const cartBadge = document.querySelector('.cart-badge');
        if (cartBadge) {
            cartBadge.textContent = count;
            
            // Add animation
            cartBadge.style.transform = 'scale(1.3)';
            setTimeout(() => {
                cartBadge.style.transform = 'scale(1)';
            }, 200);
        }
    }

    // ==============================================
    // CONSOLE INFO
    // ==============================================
    console.log('%cMalaika Shop', 'color: #0066cc; font-size: 24px; font-weight: bold;');
    console.log('%cProfessional E-commerce Platform', 'color: #666; font-size: 14px;');
});