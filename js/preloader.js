/* ========================================
   PRELOADER
   ======================================== */

export function initPreloader() {
    window.addEventListener('load', () => {
        const preloader = document.getElementById('preloader');
        setTimeout(() => {
            preloader.classList.add('hidden');
            setTimeout(() => preloader.remove(), 500);
        }, 800);
    });
}
