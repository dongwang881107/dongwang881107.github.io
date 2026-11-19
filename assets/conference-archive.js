(() => {
  const archive = document.querySelector('#conference-archive');
  const filters = archive.querySelector('[data-archive-filters]');
  const search = filters.querySelector('input');
  const year = filters.querySelector('select');
  const clear = filters.querySelector('[data-archive-clear]');
  const status = archive.querySelector('[data-archive-status]');
  const number = new Intl.NumberFormat(document.documentElement.lang);
  const normalize = (value) => value.normalize('NFKC').toLowerCase().replace(/[^\p{L}\p{N}]/gu, '');
  const groups = Array.from(archive.querySelectorAll('[data-archive-year]'), (group) => ({
    group,
    count: group.querySelector('[data-year-count]'),
    entries: Array.from(group.querySelectorAll('[data-archive-entry]'), (entry) => ({
      entry,
      text: normalize(entry.dataset.search),
    })),
    wasOpen: group.open,
  }));
  let wasFiltering = false;

  function update() {
    const terms = search.value.trim().split(/\s+/u).map(normalize).filter(Boolean);
    const filtering = Boolean(terms.length || year.value);
    let total = 0;

    for (const data of groups) {
      const { group, count, entries } = data;
      if (filtering && !wasFiltering) data.wasOpen = group.open;

      const inYear = !year.value || year.value === group.dataset.archiveYear;
      let matches = 0;
      for (const { entry, text } of entries) {
        const visible = inYear && terms.every((term) => text.includes(term));
        entry.hidden = !visible;
        if (visible) matches++;
      }

      count.textContent = number.format(matches);
      group.hidden = matches === 0;
      if (filtering) group.open = matches > 0;
      else if (wasFiltering) group.open = data.wasOpen;
      total += matches;
    }

    if (total === 0) status.textContent = status.dataset.noResults;
    else if (total === 1) status.textContent = status.dataset.oneResult;
    else status.textContent = status.dataset.results.replace('{count}', number.format(total));
    clear.disabled = !search.value && !year.value;
    wasFiltering = filtering;
  }

  search.addEventListener('input', update);
  year.addEventListener('change', update);
  clear.addEventListener('click', () => {
    search.value = '';
    year.value = '';
    update();
    search.focus();
  });
  update();
  filters.hidden = false;
  status.hidden = false;
})();
