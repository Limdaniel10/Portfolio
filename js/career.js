// Career page: optional progressive enhancement only.
// Content is edited directly in career/index.html.
document.querySelectorAll('.logo-card img').forEach((img) => {
  const showFallback = () => {
    img.hidden = true;
    const fallback = img.nextElementSibling;
    if (fallback && fallback.classList.contains('fallback-logo')) {
      fallback.style.display = 'block';
    }
  };
  img.addEventListener('error', showFallback);
  if (img.complete && img.naturalWidth === 0) showFallback();
});
