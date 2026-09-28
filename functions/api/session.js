// LocoClic — dépôt et retrait du « badge » de session (cookie) sur lococlic.com.
//
// Après une connexion réussie, la page de connexion envoie ici le jeton de session.
// On le fait vérifier par le serveur LocoClic, puis on le dépose dans un cookie que
// JavaScript ne peut pas lire (HttpOnly) et que le navigateur renverra à chaque page.

const WORKER_PAR_DEFAUT = 'https://lococlic-worker.simon-albiach.workers.dev';
const NOM_COOKIE = 'lococlic_session';
const DUREE_SECONDES = 2 * 60 * 60; // identique à la durée de vie d'un jeton côté serveur
const FORME_JETON = /^[A-Za-z0-9+/=_-]{10,1500}\.[a-f0-9]{64}$/;

function reponse(statut, corps, extra) {
  return new Response(JSON.stringify(corps), {
    status: statut,
    headers: Object.assign({ 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store' }, extra || {})
  });
}

function cookie(valeur, maxAge) {
  return NOM_COOKIE + '=' + encodeURIComponent(valeur) + '; Path=/; Max-Age=' + maxAge + '; HttpOnly; Secure; SameSite=Lax';
}

async function sessionValide(env, jeton) {
  const base = (env && env.WORKER_URL) || WORKER_PAR_DEFAUT;
  const r = await fetch(base + '/verifier-session?limite=1', {
    headers: { Authorization: 'Bearer ' + jeton },
    signal: AbortSignal.timeout(4000)
  });
  if (r.status >= 500) throw new Error('serveur indisponible');
  let d = {};
  try { d = await r.json(); } catch (e) { d = {}; }
  return d.valide === true;
}

export async function onRequest(context) {
  const { request, env } = context;
  const url = new URL(request.url);

  if (request.method !== 'POST' && request.method !== 'DELETE') {
    return reponse(405, { error: 'Méthode non autorisée' }, { Allow: 'POST, DELETE' });
  }
  // Protection contre les appels venant d'un autre site : seule la page LocoClic elle-même peut déposer ou retirer le badge.
  if (request.headers.get('Origin') !== url.origin) {
    return reponse(403, { error: 'Origine refusée' });
  }
  if (request.method === 'DELETE') {
    return reponse(200, { ok: true }, { 'Set-Cookie': cookie('', 0) });
  }

  let corps;
  try { corps = await request.json(); } catch (e) { return reponse(400, { error: 'Requête invalide' }); }
  const jeton = corps && typeof corps.jeton === 'string' ? corps.jeton : '';
  if (!FORME_JETON.test(jeton)) return reponse(400, { error: 'Jeton invalide' });

  let ok;
  try { ok = await sessionValide(env, jeton); } catch (e) { return reponse(503, { error: 'Service momentanément indisponible' }); }
  if (!ok) return reponse(401, { error: 'Session invalide' });
  return reponse(200, { ok: true }, { 'Set-Cookie': cookie(jeton, DUREE_SECONDES) });
}
