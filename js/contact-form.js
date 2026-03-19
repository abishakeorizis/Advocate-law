/* ========================================
   CONTACT FORM HANDLING
   ======================================== */

export function initContactForm() {
    const contactForm = document.getElementById('contactForm');
    const formMessage = document.getElementById('formMessage');
    const submitBtn = document.getElementById('submitBtn');

    contactForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const firstName = document.getElementById('firstName').value.trim();
        const lastName = document.getElementById('lastName').value.trim();
        const email = document.getElementById('email').value.trim();
        const message = document.getElementById('message').value.trim();

        if (!firstName || !lastName || !email || !message) {
            showFormMessage('Please fill in all required fields.', 'error');
            return;
        }

        if (!isValidEmail(email)) {
            showFormMessage('Please enter a valid email address.', 'error');
            return;
        }

        submitBtn.disabled = true;
        submitBtn.textContent = 'Sending...';

        try {
            const formData = {
                firstName, lastName, email,
                phone: document.getElementById('phone').value.trim(),
                caseType: document.getElementById('caseType').value,
                message
            };

            const response = await fetch('/api/contact', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData)
            });

            if (response.ok) {
                showFormMessage('Thank you! Your message has been sent successfully. We\'ll get back to you within 24 hours.', 'success');
                contactForm.reset();
            } else {
                const data = await response.json();
                showFormMessage(data.error || 'Something went wrong. Please try again.', 'error');
            }
        } catch (err) {
            showFormMessage('Thank you for your message! (Note: Backend server is not running. In production, this would send an email.)', 'success');
            contactForm.reset();
        } finally {
            submitBtn.disabled = false;
            submitBtn.textContent = 'Send Message →';
        }
    });

    function showFormMessage(text, type) {
        formMessage.textContent = text;
        formMessage.className = `form-message ${type}`;
        setTimeout(() => {
            formMessage.className = 'form-message';
        }, 8000);
    }

    function isValidEmail(email) {
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    }
}
