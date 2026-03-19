/* ========================================
   UTILITIES — Back to Top
   ======================================== */

export function initBackToTop() {
    const backToTop = document.getElementById('backToTop');

    window.addEventListener('scroll', () => {
        if (window.scrollY > 500) {
            backToTop.classList.add('visible');
        } else {
            backToTop.classList.remove('visible');
        }
    });

    backToTop.addEventListener('click', () => {
        // Smooth scroll back to top
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
}
