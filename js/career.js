// Try an alternate institutional image before showing an accessible text fallback.
document.querySelectorAll('.logo-card img').forEach((img) => {
  const fallback = img.nextElementSibling;
  const onError = () => {
    if (img.dataset.alternative && !img.dataset.alternativeTried) {
      img.dataset.alternativeTried = 'true';
      img.src = img.dataset.alternative;
      return;
    }
    img.hidden = true;
    if (fallback?.classList.contains('fallback-logo')) fallback.style.display = 'block';
  };
  img.addEventListener('error', onError);
  if (img.complete && img.naturalWidth === 0) onError();
});
