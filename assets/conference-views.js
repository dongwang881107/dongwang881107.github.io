(() => {
  const tracker = document.querySelector('[data-conference-tracker]');
  if (!tracker) return;

  const views = [...tracker.querySelectorAll('[data-conference-view]')];
  if (!views.length) return;

  const schedule = tracker.querySelector('#conference-schedule');
  const papers = tracker.querySelector('#conference-papers');
  const categories = [...tracker.querySelectorAll('[data-conference-category]')];
  const viewLinks = tracker.querySelectorAll('[data-conference-view-link]');
  const categoryLinks = tracker.querySelectorAll('[data-conference-category-link]');
  const top = document.getElementById('conference-top');
  const floatingTop = tracker.querySelector('[data-conference-floating-top]');
  const languageLink = document.querySelector('.site-preferences [data-set-language]');
  const alternateUrl = languageLink ? new URL(languageLink.href) : null;
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const targetFor = (hash) => document.getElementById(hash.slice(1));
  let lastCategory = categories[0];

  function updateCurrent(links, current) {
    for (const link of links) {
      if (targetFor(link.hash) === current) link.setAttribute('aria-current', 'location');
      else link.removeAttribute('aria-current');
    }
  }

  function updateFloatingTop() {
    if (floatingTop) floatingTop.hidden = window.scrollY < 480;
  }

  function render() {
    const target = targetFor(location.hash);
    const anchoredView = target?.closest('[data-conference-view]');
    const hasEdition = new URLSearchParams(location.search).get('edition');
    const active = anchoredView || (hasEdition && papers) || schedule || views[0];
    const category = target?.closest('[data-conference-category]') || categories[0];

    for (const view of views) view.hidden = view !== active;
    for (const panel of categories) panel.hidden = panel !== category;
    if (active === schedule) lastCategory = category;

    updateCurrent(viewLinks, active);
    updateCurrent(categoryLinks, category);
    if (alternateUrl) {
      alternateUrl.search = location.search;
      alternateUrl.hash = location.hash;
      languageLink.href = alternateUrl.href;
    }

    updateFloatingTop();
  }

  tracker.addEventListener('click', (event) => {
    const link = event.target.closest('a');
    if (!link || event.defaultPrevented || event.button || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;

    if (link.hasAttribute('data-conference-top-link')) {
      event.preventDefault();
      top?.focus({ preventScroll: true });
      window.scrollTo({ top: 0, behavior: reducedMotion.matches ? 'instant' : 'smooth' });
      return;
    }

    const isCategory = link.hasAttribute('data-conference-category-link');
    if (!isCategory && !link.hasAttribute('data-conference-view-link')) return;
    let target = targetFor(link.hash);
    if (!target) return;

    event.preventDefault();
    if (target === schedule && lastCategory && lastCategory !== categories[0]) target = lastCategory;
    const hash = `#${target.id}`;
    if (hash !== location.hash) history.pushState(history.state, '', hash);
    render();

    const view = target.closest('[data-conference-view]');
    if (!isCategory) {
      const heading = view?.querySelector('h2[tabindex="-1"], h3[tabindex="-1"]');
      heading?.focus({ preventScroll: true });
    }
    view?.scrollIntoView({ block: 'start' });
  });

  tracker.addEventListener('conference:view', render);
  window.addEventListener('popstate', render);
  window.addEventListener('hashchange', render);
  window.addEventListener('scroll', updateFloatingTop, { passive: true });

  render();
  const initialTarget = targetFor(location.hash);
  if (initialTarget?.closest('[data-conference-view]')) {
    requestAnimationFrame(() => initialTarget.scrollIntoView({ block: 'start' }));
  }
})();
