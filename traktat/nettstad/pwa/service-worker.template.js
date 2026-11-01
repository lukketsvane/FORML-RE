/* The build injects one edition hash and the exact release asset list. */
const SOURCE_HASH = '__SOURCE_HASH__';
const PRECACHE_ASSETS = __PRECACHE_ASSETS__;
const CACHE_PREFIX = 'formlaere-';
const CACHE_NAME = CACHE_PREFIX + SOURCE_HASH;
const ORIGIN = self.location.origin;

function localURL(value) {
  try {
    const url = new URL(value, ORIGIN);
    return url.origin === ORIGIN && /^https?:$/.test(url.protocol) ? url : null;
  } catch {
    return null;
  }
}

const PRECACHE_URLS = [...new Set(PRECACHE_ASSETS.map(localURL).filter(Boolean).map(url => url.href))];
const PRECACHE_PATHS = new Set(PRECACHE_URLS.map(value => new URL(value).pathname));

function cacheable(response) {
  return response.ok && ['basic', 'default'].includes(response.type) &&
    (!response.url || !!localURL(response.url));
}

async function remember(request, response) {
  if (!cacheable(response)) return;
  try {
    const cache = await caches.open(CACHE_NAME);
    await cache.put(request, response);
  } catch {
    // An exhausted cache must not prevent online reading.
  }
}

self.addEventListener('install', event => {
  event.waitUntil((async () => {
    const cache = await caches.open(CACHE_NAME);
    await Promise.all(PRECACHE_URLS.map(async url => {
      const request = new Request(url, { cache: 'reload', credentials: 'same-origin' });
      const response = await fetch(request);
      if (!cacheable(response)) throw new Error('Could not cache release asset: ' + url);
      await cache.put(url, response);
    }));
  })());
  // Updates activate after existing readers close, preserving their place.
});

self.addEventListener('activate', event => {
  event.waitUntil((async () => {
    const names = await caches.keys();
    await Promise.all(names.filter(name => name.startsWith(CACHE_PREFIX) && name !== CACHE_NAME)
      .map(name => caches.delete(name)));
  })());
});

async function cachedResponse(request, navigation = false) {
  try {
    const cache = await caches.open(CACHE_NAME);
    const exact = await cache.match(request, { ignoreSearch: true });
    if (exact) return exact;
    if (!navigation) return undefined;
    const pathname = new URL(request.url).pathname;
    const normalized = pathname === '/' ? '/' : pathname.replace(/\/$/, '');
    let paths = [normalized, normalized + '/'];
    if (/^\/(?:les\/?|traktat\/(?:index|scroll)\.html)$/.test(pathname)) paths = ['/'];
    for (const path of paths) {
      const response = await cache.match(new URL(path, ORIGIN).href, { ignoreSearch: true });
      if (response) return response;
    }
  } catch {
    // Network requests still work when storage is unavailable.
  }
  return undefined;
}

async function networkFirst(event, navigation = false) {
  let networkResponse;
  try {
    networkResponse = await fetch(event.request);
    // Navigation redirects have status 0 and ok=false. Let the browser follow
    // them instead of replacing the requested route with a cached document.
    if (networkResponse.type === 'opaqueredirect') return networkResponse;
    if (networkResponse.ok) {
      event.waitUntil(remember(event.request, networkResponse.clone()));
      return networkResponse;
    }
  } catch {
    // Offline, use the last successful copy from this edition's cache.
  }
  return await cachedResponse(event.request, navigation) || networkResponse || Response.error();
}

async function cacheFirst(event) {
  const cached = await cachedResponse(event.request);
  if (cached) return cached;
  try {
    const response = await fetch(event.request);
    if (response.ok) event.waitUntil(remember(event.request, response.clone()));
    return response;
  } catch {
    return Response.error();
  }
}

function immutableURL(url) {
  // Stable filenames, particularly the PDF, must refresh after edits.
  const hashInPath = /(?:[.-][a-f0-9]{8,}[.-]|\/[a-f0-9]{12,}\/)/i.test(url.pathname);
  const version = url.searchParams.get('v') || url.searchParams.get('version');
  return hashInPath || version === SOURCE_HASH;
}

self.addEventListener('fetch', event => {
  if (event.request.method !== 'GET') return;
  const url = localURL(event.request.url);
  if (!url) return;
  if (event.request.mode === 'navigate') {
    event.respondWith(networkFirst(event, true));
    return;
  }
  if (/\/document(?:\.[a-f0-9]+)?\.json$/i.test(url.pathname)) {
    event.respondWith(networkFirst(event));
    return;
  }
  const asset = PRECACHE_PATHS.has(url.pathname) || /\.(?:css|m?js|png|jpe?g|svg|ico|webp|avif|woff2?|ttf|otf|pdf|webmanifest)$/i.test(url.pathname);
  if (asset) event.respondWith(immutableURL(url) ? cacheFirst(event) : networkFirst(event));
});
