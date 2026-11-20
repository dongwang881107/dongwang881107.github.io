(() => {
  const catalogue = document.querySelector('[data-papers-root]');
  if (!catalogue) return;

  const edition = catalogue.querySelector('#conference-papers-edition');
  const query = catalogue.querySelector('#conference-papers-query');
  const status = catalogue.querySelector('[data-papers-status]');
  const list = catalogue.querySelector('[data-papers-list]');
  const paginations = Array.from(catalogue.querySelectorAll('[data-papers-pagination]'), (nav) => ({
    nav,
    previous: nav.querySelector('[data-papers-previous]'),
    next: nav.querySelector('[data-papers-next]'),
    label: nav.querySelector('[data-papers-page]'),
  }));
  const retry = catalogue.querySelector('[data-papers-retry]');
  const labels = catalogue.dataset;
  const editions = new Set(Array.from(edition.options, (option) => option.value).filter(Boolean));
  const number = new Intl.NumberFormat(document.documentElement.lang);
  const pageSize = 10;
  const base = new URL(labels.papersBase, location.href);
  const normalize = (value) => value.normalize('NFKC').toLowerCase().replace(/[^\p{L}\p{M}\p{N}]+/gu, ' ').trim();
  let request;
  let papers = [];
  let matches = [];
  let searchIndex;
  let page = 1;

  function format(template, values) {
    return template.replace(/\{(\w+)\}/g, (_, key) => number.format(values[key]));
  }

  function element(tag, text) {
    const node = document.createElement(tag);
    node.textContent = text;
    return node;
  }

  function publicUrl(value) {
    if (!value) return null;
    try {
      const url = new URL(value);
      if (['https:', 'http:'].includes(url.protocol) && !url.username && !url.password) return url.href;
    } catch {
      return null;
    }
    return null;
  }

  function paperRow([title, authors, source, abstract, archivalStatus]) {
    const row = document.createElement('li');
    const titleNode = element('h3', title);
    titleNode.className = 'conference-paper-title';
    if (archivalStatus === 'retracted' || archivalStatus === 'nonresearch') {
      const badge = element('span', labels[archivalStatus]);
      badge.className = 'conference-paper-badge';
      titleNode.append(' ', badge);
    }
    row.append(titleNode);

    if (authors) {
      const authorLine = element('p', authors);
      authorLine.className = 'conference-paper-authors';
      row.append(authorLine);
    }

    const url = publicUrl(source);
    if (url) {
      const link = element('a', labels.paperLink);
      link.href = url;
      link.className = 'conference-paper-source';
      link.setAttribute('aria-label', `${labels.paperLink} · ${title}`);
      row.append(link);
    }

    if (abstract) {
      const disclosure = document.createElement('details');
      disclosure.className = 'conference-paper-abstract';
      disclosure.append(element('summary', labels.abstractLabel), element('p', abstract));
      row.append(disclosure);
    }
    return row;
  }

  function render() {
    const first = (page - 1) * pageSize;
    const last = Math.min(first + pageSize, matches.length);
    const pages = Math.ceil(matches.length / pageSize);
    list.start = first + 1;
    list.replaceChildren(...matches.slice(first, last).map(paperRow));
    const template = query.value.trim() ? labels.results : labels.resultsAll;
    if (matches.length === 0) status.textContent = labels.empty;
    else if (matches.length === 1) status.textContent = labels.oneResult;
    else status.textContent = format(template, { first: first + 1, last, total: matches.length });
    for (const { nav, previous, next, label } of paginations) {
      nav.hidden = pages <= 1;
      previous.disabled = page <= 1;
      next.disabled = page >= pages;
      label.textContent = pages ? format(labels.page, { page, pages }) : '';
    }
  }

  function search() {
    const terms = normalize(query.value).split(' ').filter(Boolean);
    if (terms.length) {
      searchIndex ??= papers.map(([title, authors, , abstract]) => normalize([title, authors, abstract].filter(Boolean).join(' ')));
      matches = papers.filter((_, index) => terms.every((term) => searchIndex[index].includes(term)));
    } else {
      matches = papers;
    }
    page = 1;
    render();
  }

  async function load(preserveQuery = false) {
    request?.abort();
    const selected = edition.value;
    papers = [];
    matches = [];
    searchIndex = undefined;
    list.replaceChildren();
    for (const { nav } of paginations) nav.hidden = true;
    retry.hidden = true;
    query.disabled = true;
    query.placeholder = labels.queryMetadata;
    if (!preserveQuery) query.value = '';

    if (!selected) {
      status.textContent = labels.noSelection;
      list.removeAttribute('aria-busy');
      return;
    }

    status.textContent = labels.loading;
    list.setAttribute('aria-busy', 'true');
    request = new AbortController();
    const { signal } = request;
    try {
      const response = await fetch(new URL(`${encodeURIComponent(selected)}.json`, base), { signal });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const data = await response.json();
      if (signal.aborted) return;
      if (data.edition !== selected || !Array.isArray(data.papers)
          || data.papers.some((paper) => !Array.isArray(paper) || typeof paper[0] !== 'string')) {
        throw new Error('Invalid proceedings data');
      }
      papers = data.papers;
      if (papers.some((paper) => paper[3])) query.placeholder = labels.queryWithAbstract;
      query.disabled = false;
      search();
    } catch {
      if (signal.aborted) return;
      query.disabled = true;
      status.textContent = labels.unavailable;
      retry.hidden = false;
    } finally {
      if (!signal.aborted) list.removeAttribute('aria-busy');
    }
  }

  function setLocation(addHistoryEntry = false) {
    const url = new URL(location.href);
    if (edition.value) url.searchParams.set('edition', edition.value);
    else url.searchParams.delete('edition');
    url.hash = 'conference-papers';
    if (url.href !== location.href) {
      if (addHistoryEntry) history.pushState(history.state, '', url);
      else history.replaceState(history.state, '', url);
    }
    catalogue.dispatchEvent(new CustomEvent('conference:view', { bubbles: true }));
  }

  function fromLocation() {
    const value = new URL(location.href).searchParams.get('edition');
    return editions.has(value) ? value : '';
  }

  function changePage(offset, controls) {
    page += offset;
    render();
    const atStart = controls === paginations[0];
    const { previous, next } = paginations[0];
    const [trigger, replacement] = offset > 0 ? [next, previous] : [previous, next];
    if (!atStart) {
      (trigger.disabled ? replacement : trigger).focus({ preventScroll: true });
      paginations[0].nav.scrollIntoView({ block: 'start' });
      return;
    }
    if (trigger.disabled && !replacement.disabled) replacement.focus();
  }

  edition.addEventListener('change', () => {
    setLocation();
    load();
  });
  query.addEventListener('input', (event) => {
    if (!event.isComposing) search();
  });
  query.addEventListener('compositionend', search);
  for (const controls of paginations) {
    controls.previous.addEventListener('click', () => changePage(-1, controls));
    controls.next.addEventListener('click', () => changePage(1, controls));
  }
  retry.addEventListener('click', () => {
    edition.focus();
    load(true);
  });
  window.addEventListener('popstate', () => {
    const selected = fromLocation();
    if (selected !== edition.value) {
      edition.value = selected;
      load();
    }
  });
  document.addEventListener('click', (event) => {
    const link = event.target.closest('[data-open-papers]');
    if (!link || event.defaultPrevented || event.button || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
    const selected = link.dataset.openPapers;
    if (!editions.has(selected)) return;
    event.preventDefault();
    edition.value = selected;
    setLocation(true);
    const heading = catalogue.querySelector('#conference-papers-heading');
    (heading?.hasAttribute('tabindex') ? heading : edition).focus({ preventScroll: true });
    catalogue.scrollIntoView({ block: 'start' });
    load();
  });

  catalogue.querySelector('[data-papers-controls]').hidden = false;
  edition.value = fromLocation();
  load();
})();
