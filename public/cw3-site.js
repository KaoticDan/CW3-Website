const removeWebflowBadge = () => {
  document.querySelectorAll('.w-webflow-badge').forEach((badge) => badge.remove());
};
removeWebflowBadge();
new MutationObserver(removeWebflowBadge).observe(document.body, { childList: true, subtree: true });

document.addEventListener('DOMContentLoaded', () => {
  const menuToggle = document.querySelector('.navbar .hamburger');
  const menu = document.querySelector('.menu');
  if (menuToggle && menu) {
    menu.id = menu.id || 'site-menu';
    menuToggle.setAttribute('role', 'button');
    menuToggle.setAttribute('tabindex', '0');
    menuToggle.setAttribute('aria-controls', menu.id);
    const syncMenuState = () => {
      const open = getComputedStyle(menu).display !== 'none';
      menuToggle.setAttribute('aria-expanded', String(open));
      menuToggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    };
    new MutationObserver(syncMenuState).observe(menu, { attributes: true, attributeFilter: ['style', 'class'] });
    menuToggle.addEventListener('keydown', (event) => {
      if (event.key === 'Enter' || event.key === ' ') {
        event.preventDefault();
        menuToggle.click();
      }
    });
    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape' && menuToggle.getAttribute('aria-expanded') === 'true') {
        menuToggle.click();
        menuToggle.focus();
      }
    });
    syncMenuState();
  }
  document.querySelectorAll('.navbar .brand-logo, .footer .brand-logo').forEach((link) => {
    link.setAttribute('aria-label', 'Careers in Web3 home');
  });

  const form = document.querySelector('form[data-name="Email Form"]');
  if (!form || location.pathname !== '/work') return;

  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    event.stopImmediatePropagation();

    const submit = form.querySelector('[type="submit"]');
    const wrapper = form.closest('.w-form');
    const success = wrapper?.querySelector('.w-form-done');
    const failure = wrapper?.querySelector('.w-form-fail');
    const data = new FormData(form);
    const name = String(data.get('name') || '').trim();
    const email = String(data.get('Email') || '').trim();
    const phone = String(data.get('Phone-Number') || '').trim();

    if (!name || !email || !phone || !form.reportValidity()) return;
    if (submit) submit.disabled = true;
    if (failure) failure.style.display = 'none';

    try {
      const response = await fetch('/api/work-submission', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, email, phone }),
      });
      if (!response.ok) throw new Error(`Submission failed (${response.status})`);
      form.style.display = 'none';
      if (success) success.style.display = 'block';
    } catch {
      if (failure) failure.style.display = 'block';
    } finally {
      if (submit) submit.disabled = false;
    }
  }, true);
});
