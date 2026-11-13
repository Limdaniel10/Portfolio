"use strict";
const yearLabel = document.getElementById('year');
if (yearLabel) yearLabel.textContent = new Date().getFullYear();
// Both counts are derived from the deployed archive, never from speculative estimates.
fetch('data/countries.json', { cache: 'no-cache' }).then(r => {
  if (!r.ok) throw new Error('countries.json not available');
  return r.json();
}).then(data => {
  const n = Number(data.totalCountries);
  if (Number.isFinite(n)) {
    document.getElementById('country-count').textContent = `${n} countries`;
    document.getElementById('travel-tile-count').textContent = `${n} countries`;
    window.PortfolioI18n?.refreshCounts();
  }
}).catch(err => console.info('Travel count: displaying bundled fallback.', err));
fetch('reading/data/books.json', { cache: 'no-cache' }).then(r => {
  if (!r.ok) throw new Error('books.json not available');
  return r.json();
}).then(data => {
  if (Array.isArray(data.books)) {
    document.getElementById('reading-tile-count').textContent =
      `${data.books.length.toLocaleString('en-US')} books`;
    window.PortfolioI18n?.refreshCounts();
  }
}).catch(err => console.info('Reading count: displaying bundled fallback.', err));
