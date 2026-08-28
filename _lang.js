(function(){
  // Progressive enhancement only. The English content is already in the HTML
  // and already visible; this script swaps it, it does not reveal it. If the
  // CSP hash stops matching, the page degrades to readable English rather
  // than to a blank page.
  var buttons = document.querySelectorAll('.langs button');
  var blocks = document.querySelectorAll('[data-lang-block]');
  var attrs = document.querySelectorAll('[data-en],[data-fr]');
  function setLang(lang){
    document.documentElement.lang = lang;
    blocks.forEach(function(b){ b.classList.toggle('on', b.dataset.langBlock === lang); });
    attrs.forEach(function(n){
      var v = n.getAttribute('data-' + lang);
      if (v !== null) n.innerHTML = v;
    });
    buttons.forEach(function(b){ b.setAttribute('aria-pressed', String(b.dataset.lang === lang)); });
    try { localStorage.setItem('yu-lang', lang); } catch(e){}
  }
  buttons.forEach(function(b){ b.addEventListener('click', function(){ setLang(b.dataset.lang); }); });
  var saved = null;
  try { saved = localStorage.getItem('yu-lang'); } catch(e){}
  if (saved === 'fr' || (!saved && (navigator.language||'en').toLowerCase().indexOf('fr') === 0)) setLang('fr');
})();