// LocoClic — Vérification de la session
// À inclure en première ligne du <head> de chaque page protégée
// Si pas connecté → redirection vers login.html
(function() {
  try {
    var session = localStorage.getItem('lococlic_session');
    if (!session) {
      window.location.replace(getLoginPath());
      return;
    }
    var data = JSON.parse(session);
    if (!data.expires || Date.now() >= data.expires) {
      localStorage.removeItem('lococlic_session');
      window.location.replace(getLoginPath());
      return;
    }
  } catch(e) {
    localStorage.removeItem('lococlic_session');
    window.location.replace(getLoginPath());
  }
  
  function getLoginPath() {
    // Détecter si on est dans un sous-dossier
    var path = window.location.pathname;
    if (path.includes('/fiches_pathologies/') || path.includes('/lococlic_fiches_patient/')) {
      return '../login.html';
    }
    return 'login.html';
  }
})();
