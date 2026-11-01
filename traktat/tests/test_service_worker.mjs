import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import test from 'node:test';
import { runInNewContext } from 'node:vm';

const origin = 'https://formlaere.example';
const sourceHash = 'a'.repeat(64);
const template = readFileSync(new URL('../nettstad/pwa/service-worker.template.js', import.meta.url), 'utf8');

function workerWithCachedRoot(fetchResponse) {
  const listeners = new Map();
  const calls = { fetch: 0, cacheMatch: 0, cachePut: 0 };
  const context = {
    URL, Request, Response, Set, Promise, Error,
    self: {
      location: { origin },
      addEventListener(type, listener) { listeners.set(type, listener); },
    },
    caches: {
      async open() {
        return {
          async match(request) {
            calls.cacheMatch += 1;
            const url = typeof request === 'string' ? request : request.url;
            if (new URL(url, origin).pathname === '/') return new Response('cached complete reader');
          },
          async put() { calls.cachePut += 1; },
        };
      },
    },
    async fetch(request) {
      calls.fetch += 1;
      return fetchResponse(request);
    },
  };
  const code = template.replace('__SOURCE_HASH__', sourceHash)
    .replace('__PRECACHE_ASSETS__', JSON.stringify(['/']));
  runInNewContext(code, context);

  return {
    calls,
    async navigate(path) {
      let response;
      const pending = [];
      listeners.get('fetch')({
        request: { url: new URL(path, origin).href, method: 'GET', mode: 'navigate', redirect: 'manual' },
        respondWith(value) { response = value; },
        waitUntil(value) { pending.push(value); },
      });
      const result = await response;
      await Promise.all(pending);
      return result;
    },
  };
}

test('online legacy navigation passes an opaque redirect to the browser despite a cached root', async () => {
  // A browser navigation fetch exposes redirects as filtered responses with
  // status 0 and ok=false. Node cannot construct that browser-only response.
  const redirect = Object.freeze({
    type: 'opaqueredirect', status: 0, ok: false,
    clone() { throw new Error('An opaque redirect must not be cached'); },
  });
  for (const path of ['/les', '/les/', '/traktat/index.html', '/traktat/scroll.html']) {
    const worker = workerWithCachedRoot(async () => redirect);
    assert.strictEqual(await worker.navigate(path), redirect, path);
    assert.equal(worker.calls.fetch, 1);
    assert.equal(worker.calls.cacheMatch, 0, 'A live redirect must not be replaced with an offline fallback');
    assert.equal(worker.calls.cachePut, 0, 'A filtered redirect must not enter the content cache');
  }
});

test('offline legacy navigation still falls back to the cached complete reader', async () => {
  for (const path of ['/les', '/les/', '/traktat/index.html', '/traktat/scroll.html']) {
    const worker = workerWithCachedRoot(async () => { throw new TypeError('offline'); });
    const response = await worker.navigate(path);
    assert.equal(await response.text(), 'cached complete reader', path);
    assert.equal(worker.calls.fetch, 1);
    assert.ok(worker.calls.cacheMatch > 0);
    assert.equal(worker.calls.cachePut, 0);
  }
});

test('a successful navigation returns and caches the fresh document', async () => {
  const online = new Response('fresh complete reader');
  const worker = workerWithCachedRoot(async () => online);
  assert.strictEqual(await worker.navigate('/'), online);
  assert.equal(worker.calls.cacheMatch, 0);
  assert.equal(worker.calls.cachePut, 1);
});
