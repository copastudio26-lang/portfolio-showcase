// Ajay Portfolio — main.js

// Auto-remove flash messages after 4s
document.querySelectorAll('.flash-msg').forEach(el => {
  setTimeout(() => el.remove(), 4000);
});

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(a => {
  a.addEventListener('click', e => {
    const target = document.querySelector(a.getAttribute('href'));
    if (target) {
      e.preventDefault();
      target.scrollIntoView({ behavior: 'smooth' });
    }
  });
});
