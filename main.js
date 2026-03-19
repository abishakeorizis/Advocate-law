/* ========================================
   ADVOCATE PORTFOLIO — MAIN JAVASCRIPT
   All modules are organized into separate files by feature.
   ======================================== */

import { initPreloader } from './js/preloader.js';
import { initNavbar } from './js/navbar.js';
import { initScrollReveal, initCounterAnimation } from './js/animations.js';
import { initCarousel } from './js/carousel.js';
import { initContactForm } from './js/contact-form.js';
import { initBackToTop } from './js/utils.js';

// Prevent any possible forced "snap" scrolling behavior and keep wheel scroll continuous.
// Some browsers or CSS can impose scroll snapping (e.g., snap-to-section behavior).
// We disable it globally to keep scrolling like a normal document or chat app.
function disableScrollSnap() {
  if (!document || !document.documentElement) return;

  document.documentElement.style.scrollBehavior = 'auto';
  document.documentElement.style.scrollSnapType = 'none';
  document.body.style.scrollSnapType = 'none';

  // Force-disable snap on all elements in case a stylesheet adds it.
  document.querySelectorAll('*').forEach(el => {
    el.style.scrollSnapType = 'none';
    el.style.scrollSnapAlign = 'none';
  });
}

if (typeof window !== 'undefined') {
  window.addEventListener('DOMContentLoaded', disableScrollSnap);
  // Also run once immediately (in case script runs after DOM loaded)
  disableScrollSnap();
}

// Initialize all modules
initPreloader();
initNavbar();
initScrollReveal();
initCounterAnimation();
initCarousel();
initContactForm();
initBackToTop();
