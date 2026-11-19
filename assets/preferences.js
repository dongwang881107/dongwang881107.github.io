(() => {
  const root = document.documentElement;
  const themeKey = 'research-site-theme';
  const languageKey = 'research-site-language';
  const systemTheme = window.matchMedia('(prefers-color-scheme: dark)');

  function saved(key) {
    try {
      return localStorage.getItem(key);
    } catch {
      return null;
    }
  }

  function save(key, value) {
    try {
      localStorage.setItem(key, value);
    } catch {
      // Navigation and theme changes still work when storage is disabled.
    }
  }

  const theme = saved(themeKey);
  if (theme === 'light' || theme === 'dark') root.dataset.theme = theme;

  if (root.dataset.englishHome && saved(languageKey) === 'en' && !location.hash && !location.search) {
    location.replace(root.dataset.englishHome);
  }

  document.addEventListener('click', (event) => {
    const link = event.target.closest('[data-set-language]');
    if (link) save(languageKey, link.dataset.setLanguage);
  });

  document.addEventListener('DOMContentLoaded', () => {
    const toggle = document.querySelector('.theme-toggle');
    const label = toggle.querySelector('.theme-label');
    const currentTheme = () => root.dataset.theme || (systemTheme.matches ? 'dark' : 'light');
    const nextTheme = () => currentTheme() === 'dark' ? 'light' : 'dark';
    function updateLabel() {
      const next = nextTheme();
      toggle.dataset.nextTheme = next;
      label.textContent = next === 'light' ? toggle.dataset.lightLabel : toggle.dataset.darkLabel;
    }
    toggle.addEventListener('click', () => {
      root.dataset.theme = nextTheme();
      save(themeKey, root.dataset.theme);
      updateLabel();
    });
    systemTheme.addEventListener('change', updateLabel);
    updateLabel();
    toggle.hidden = false;
  });
})();
