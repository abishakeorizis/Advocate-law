/* ========================================
   TESTIMONIAL CAROUSEL
   ======================================== */

export function initCarousel() {
    const track = document.getElementById('testimonialTrack');
    const dots = document.querySelectorAll('.carousel-dot');
    const prevBtn = document.getElementById('carouselPrev');
    const nextBtn = document.getElementById('carouselNext');
    let currentSlide = 0;
    const totalSlides = dots.length;
    let carouselInterval;

    function goToSlide(index) {
        currentSlide = index;
        if (currentSlide < 0) currentSlide = totalSlides - 1;
        if (currentSlide >= totalSlides) currentSlide = 0;

        track.style.transform = `translateX(-${currentSlide * 100}%)`;

        dots.forEach((dot, i) => {
            dot.classList.toggle('active', i === currentSlide);
        });
    }

    function startCarouselAutoplay() {
        carouselInterval = setInterval(() => {
            goToSlide(currentSlide + 1);
        }, 5000);
    }

    function resetCarouselAutoplay() {
        clearInterval(carouselInterval);
        startCarouselAutoplay();
    }

    prevBtn.addEventListener('click', () => {
        goToSlide(currentSlide - 1);
        resetCarouselAutoplay();
    });

    nextBtn.addEventListener('click', () => {
        goToSlide(currentSlide + 1);
        resetCarouselAutoplay();
    });

    dots.forEach(dot => {
        dot.addEventListener('click', () => {
            goToSlide(parseInt(dot.getAttribute('data-slide')));
            resetCarouselAutoplay();
        });
    });

    startCarouselAutoplay();
}
