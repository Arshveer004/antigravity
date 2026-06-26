document.addEventListener('DOMContentLoaded', () => {
    // Mobile Menu Toggle
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');

    if (hamburger && navLinks) {
        hamburger.addEventListener('click', () => {
            navLinks.classList.toggle('active');
        });
    }

    // Countdown Timer logic targeting Nov 12, 2026
    const countdownDate = new Date("November 12, 2026 09:00:00").getTime();

    const updateCountdown = () => {
        const now = new Date().getTime();
        const distance = countdownDate - now;

        if (distance < 0) {
            // Event has started
            const container = document.querySelector('.countdown-container');
            if (container) {
                container.innerHTML = "<h3>The Event Has Started!</h3>";
            }
            return;
        }

        // Time calculations
        const days = Math.floor(distance / (1000 * 60 * 60 * 24));
        const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((distance % (1000 * 60)) / 1000);

        // Update DOM
        const dElem = document.getElementById('cd-days');
        const hElem = document.getElementById('cd-hours');
        const mElem = document.getElementById('cd-minutes');
        const sElem = document.getElementById('cd-seconds');

        if (dElem) dElem.textContent = days.toString().padStart(2, '0');
        if (hElem) hElem.textContent = hours.toString().padStart(2, '0');
        if (mElem) mElem.textContent = minutes.toString().padStart(2, '0');
        if (sElem) sElem.textContent = seconds.toString().padStart(2, '0');
    };

    // Initial call
    updateCountdown();
    // Update every second
    setInterval(updateCountdown, 1000);
});
