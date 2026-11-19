(() => {
  const followLegacyLink = () => {
    const target = document.getElementById(window.location.hash.slice(1));
    if (target?.classList.contains('legacy-link')) {
      window.location.replace(target.href);
    }
  };

  followLegacyLink();
  window.addEventListener('hashchange', followLegacyLink);
})();
