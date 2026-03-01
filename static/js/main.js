document.addEventListener('DOMContentLoaded', () => {
    // -----------------------------------------
    // 1. Theme Toggle Logic (Light / Dark Mode)
    // -----------------------------------------
    const themeToggleBtn = document.getElementById('themeToggle');
    const themeIcon = themeToggleBtn ? themeToggleBtn.querySelector('i') : null;

    function setTheme(themeName) {
        document.documentElement.setAttribute('data-theme', themeName);
        localStorage.setItem('theme', themeName);

        // Update Icon
        if (themeIcon) {
            if (themeName === 'dark') {
                themeIcon.classList.remove('fa-moon');
                themeIcon.classList.add('fa-sun');
            } else {
                themeIcon.classList.remove('fa-sun');
                themeIcon.classList.add('fa-moon');
            }
        }
    }

    // Set Initial Theme based on script in layout.html
    const currentTheme = localStorage.getItem('theme') || 'light';
    setTheme(currentTheme);

    // Toggle listener
    if (themeToggleBtn) {
        themeToggleBtn.addEventListener('click', () => {
            const current = document.documentElement.getAttribute('data-theme');
            if (current === 'light') {
                setTheme('dark');
            } else {
                setTheme('light');
            }
        });
    }

    // -----------------------------------------
    // 2. Scroll Reveal Animations
    // -----------------------------------------
    const observerOptions = {
        threshold: 0.1,
        rootMargin: "0px 0px -50px 0px"
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Only apply observer to manually defined cards if they don't have .animate-up
    document.querySelectorAll('.card:not(.animate-up)').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'all 0.5s cubic-bezier(0.4, 0, 0.2, 1)';
        observer.observe(el);
    });

    // -----------------------------------------
    // 3. Form Interactions & Loaders
    // -----------------------------------------
    const predictForm = document.querySelector('form');
    if (predictForm) {
        predictForm.addEventListener('submit', (e) => {
            const btn = predictForm.querySelector('button[type="submit"]');

            // Create a small loading state
            const originalContent = btn.innerHTML;
            btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Processing...';
            btn.style.opacity = '0.8';
            btn.style.pointerEvents = 'none';
        });

        // Add focus hover lift to inputs
        const inputs = document.querySelectorAll('.form-control, .form-select');
        inputs.forEach(input => {
            input.addEventListener('focus', () => {
                const parentGroup = input.closest('.form-group');
                if (parentGroup) {
                    parentGroup.style.transform = 'translateY(-2px)';
                    parentGroup.style.transition = 'all 0.3s ease';
                }
            });
            input.addEventListener('blur', () => {
                const parentGroup = input.closest('.form-group');
                if (parentGroup) {
                    parentGroup.style.transform = 'translateY(0)';
                }
            });
        });
    }

    // -----------------------------------------
    // 4. Number Counter Animation for Metrics
    // -----------------------------------------
    const counters = document.querySelectorAll('.m-val');
    if (counters.length > 0) {
        counters.forEach(counter => {
            const targetStr = counter.innerText.replace(/,/g, '');
            const target = parseInt(targetStr);
            if (isNaN(target)) return;

            const increment = Math.ceil(target / 50);
            let current = 0;

            const updateCounter = () => {
                current += increment;
                if (current < target) {
                    counter.innerText = Math.ceil(current).toLocaleString();
                    setTimeout(updateCounter, 20);
                } else {
                    counter.innerText = target.toLocaleString();
                }
            };

            // trigger
            updateCounter();
        });
    }

    // -----------------------------------------
    // 5. Disclaimer Modal Logic
    // -----------------------------------------
    const disclaimerModal = document.getElementById('disclaimerModal');
    const acceptDisclaimerBtn = document.getElementById('acceptDisclaimerBtn');

    if (disclaimerModal && acceptDisclaimerBtn) {
        // Check if user has already accepted
        if (!localStorage.getItem('disclaimer_accepted')) {
            // Add a small delay for better UX
            setTimeout(() => {
                disclaimerModal.classList.add('show');
            }, 500);
        }

        acceptDisclaimerBtn.addEventListener('click', () => {
            localStorage.setItem('disclaimer_accepted', 'true');
            disclaimerModal.classList.remove('show');
        });
    }
});
