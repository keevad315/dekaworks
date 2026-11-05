const navToggle = document.querySelector('.nav-toggle');
const nav = document.querySelector('.site-nav');
const year = document.getElementById('year');

if (year) {
  year.textContent = new Date().getFullYear();
}

if (navToggle && nav) {
  navToggle.addEventListener('click', () => {
    const isOpen = nav.classList.toggle('open');
    navToggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
  });

  const closeNav = () => {
    nav.classList.remove('open');
    navToggle.setAttribute('aria-expanded', 'false');
  };

  // Close the menu after a link is tapped, on a tap outside it, or with Escape.
  nav.querySelectorAll('a').forEach((link) => link.addEventListener('click', closeNav));
  document.addEventListener('click', (event) => {
    if (nav.classList.contains('open') && !nav.contains(event.target) && !navToggle.contains(event.target)) {
      closeNav();
    }
  });
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') closeNav();
  });
}

let backToTopButton = document.getElementById('back-to-top');

if (!backToTopButton) {
  backToTopButton = document.createElement('button');
  backToTopButton.id = 'back-to-top';
  backToTopButton.className = 'back-to-top';
  backToTopButton.type = 'button';
  backToTopButton.setAttribute('aria-label', 'Back to top');
  backToTopButton.textContent = 'Top';
  document.body.appendChild(backToTopButton);
}

const toggleBackToTop = () => {
  const shouldShow = window.scrollY > 320;
  backToTopButton.classList.toggle('show', shouldShow);
};

window.addEventListener('scroll', toggleBackToTop, { passive: true });
toggleBackToTop();

backToTopButton.addEventListener('click', () => {
  window.scrollTo({ top: 0, behavior: 'smooth' });
});
