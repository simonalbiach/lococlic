// LocoClic — contrôle d'accès CÔTÉ SERVEUR (Cloudflare Pages Functions).
//
// Ce petit programme s'exécute AVANT l'envoi de chaque page. Les modules, les fiches
// et l'accueil ne sont envoyés que si le « badge » de session (cookie) est valide :
// c'est le serveur LocoClic (le Worker) qui décide, pas le navigateur.
// Sans badge valide, le contenu n'est JAMAIS envoyé : seulement une redirection.

const WORKER_PAR_DEFAUT = 'https://lococlic-worker.simon-albiach.workers.dev';
const NOM_COOKIE = 'lococlic_session';
const FORME_JETON = /^[A-Za-z0-9+/=_-]{10,1500}\.[a-f0-9]{64}$/;

// PRINCIPE : TOUT est protégé par défaut. Seules les pages ci-dessous (qui ne contiennent aucun contenu
// payant) et les images sont publiques. Une adresse inconnue, mal formée ou déguisée est donc protégée :
// impossible de contourner le contrôle en inventant une variante d'adresse.
// ➜ Si vous ajoutez un jour une page publique (ex. « tarifs.html »), ajoutez-la ICI, sinon elle sera protégée.
const PAGES_PUBLIQUES = new Set([
  '/login', '/inscription', '/licence-msp', '/cgu', '/confidentialite', '/mentions-legales',
  '/mot-de-passe-oublie', '/reinitialiser-mot-de-passe', '/compte', '/references',
  '/auth-check.js', '/api/session', '/favicon.ico', '/robots.txt'
]);
const DOSSIERS_PUBLICS = ['/images/', '/images_pathologies/'];

// Classe une adresse : 'contenu' (abonnement actif requis), 'accueil' (session valide, même abonnement
// terminé), 'public', 'introuvable' ou 'refuser'.
export function classer(pathname) {
  let p;
  try { p = decodeURIComponent(pathname); } catch (e) { return 'refuser'; }
  // Un « % » encore présent après décodage = double encodage (%256c pour « l ») : aucune adresse légitime
  // n'en contient, et un hébergeur qui décoderait une 2e fois pourrait servir un fichier protégé. On refuse.
  // Idem pour les caractères de contrôle et les « ; » (paramètres de chemin) qu'aucune adresse du site n'utilise.
  if (/%[0-9a-f]{2}/i.test(p) || /[\u0000-\u001f\u007f;]/.test(p)) return 'refuser';
  p = p.replace(/\\/g, '/').replace(/\/{2,}/g, '/').toLowerCase();
  if (p.includes('/../') || p.endsWith('/..') || p.includes('/./') || p.endsWith('/.')) return 'refuser';
  if (p.startsWith('/functions') || p.startsWith('/_')) return 'introuvable';
  if (p === '/' || p.startsWith('/index')) return 'accueil';
  const sansExtension = p.endsWith('.html') ? p.slice(0, -5) : p;
  if (PAGES_PUBLIQUES.has(sansExtension) || PAGES_PUBLIQUES.has(p)) return 'public';
  if (DOSSIERS_PUBLICS.some(d => p.startsWith(d))) return 'public';
  return 'contenu';
}

function lireJeton(request) {
  const cookies = request.headers.get('Cookie') || '';
  for (const morceau of cookies.split(';')) {
    const i = morceau.indexOf('=');
    if (i < 0) continue;
    if (morceau.slice(0, i).trim() === NOM_COOKIE) {
      try { return decodeURIComponent(morceau.slice(i + 1).trim()); } catch (e) { return ''; }
    }
  }
  return '';
}

// Demande au serveur LocoClic si la session est valide. Lève une erreur si le serveur est injoignable.
async function verifierAupresDuServeur(env, jeton) {
  const base = (env && env.WORKER_URL) || WORKER_PAR_DEFAUT;
  const reponse = await fetch(base + '/verifier-session?limite=1', {
    headers: { Authorization: 'Bearer ' + jeton },
    signal: AbortSignal.timeout(4000)
  });
  if (reponse.status >= 500) throw new Error('serveur indisponible');
  let d = {};
  try { d = await reponse.json(); } catch (e) { d = {}; }
  return { valide: d.valide === true, termine: d.abonnement_termine === true };
}

function redirection(chemin) {
  return new Response(null, { status: 302, headers: { Location: chemin, 'Cache-Control': 'no-store' } });
}

export async function onRequest(context) {
  const { request, env, next } = context;
  const url = new URL(request.url);
  const type = classer(url.pathname);

  if (type === 'introuvable') return new Response('Introuvable', { status: 404, headers: { 'Cache-Control': 'no-store' } });
  if (type === 'refuser') return new Response('Requête invalide', { status: 400, headers: { 'Cache-Control': 'no-store' } });
  if (type === 'public') return next();

  // Zone protégée : pas de badge (ou badge mal formé) → on n'envoie rien, on renvoie vers la connexion.
  const jeton = lireJeton(request);
  if (!jeton || !FORME_JETON.test(jeton)) return redirection('/login.html');

  let etat;
  try {
    etat = await verifierAupresDuServeur(env, jeton);
  } catch (e) {
    return new Response('Service momentanément indisponible. Réessayez dans un instant.', {
      status: 503,
      headers: { 'Content-Type': 'text/plain; charset=utf-8', 'Cache-Control': 'no-store', 'Retry-After': '30' }
    });
  }
  if (!etat.valide) return redirection('/login.html');
  if (type === 'contenu' && etat.termine) return redirection('/compte.html');

  const reponse = await next();
  const entetes = new Headers(reponse.headers);
  entetes.set('Cache-Control', 'private, no-store');
  entetes.append('Vary', 'Cookie');
  return new Response(reponse.body, { status: reponse.status, statusText: reponse.statusText, headers: entetes });
}
