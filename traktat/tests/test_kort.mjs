import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import test from 'node:test';
import { runInNewContext } from 'node:vm';

const html = readFileSync(new URL('../nettstad/kort.html', import.meta.url), 'utf8');
const script = html.match(/<script>([\s\S]*?)<\/script>/)[1];
const groups = JSON.parse(script.match(/const groups = (.*);/)[1]);
const inlineKey = 'a'.repeat(24), displayKey = 'b'.repeat(24);
const inlineTex = String.raw`\mathbb{M}`, displayTex = String.raw`\frac{a}{b}`;

// Exercise the real inline page script, including rendering and clipboard events.
class Element {
  constructor(tag) {
    this.tagName = tag.toUpperCase(); this.children = []; this.attributes = new Map();
    this.className = ''; this.ownText = ''; this.listeners = new Map();
    this.classList = { contains: name => this.className.split(/\s+/).includes(name) };
  }
  set textContent(value) { this.ownText = String(value); this.children = []; }
  get textContent() { return this.ownText + this.children.map(child => child.textContent).join(''); }
  set innerHTML(value) { this.textContent = value; }
  appendChild(child) { child.parentNode = this; this.children.push(child); return child; }
  append(...children) { children.forEach(child => this.appendChild(child)); }
  replaceChildren(...children) { this.ownText = ''; this.children = []; this.append(...children); }
  setAttribute(key, value) { this.attributes.set(key, String(value)); }
  getAttribute(key) { return this.attributes.get(key) ?? null; }
  addEventListener(type, listener) { this.listeners.set(type, listener); }
  contains(node) { return node === this || this.children.some(child => child.contains(node)); }
  dispatch(type, extra) {
    const event = { defaultPrevented: false, preventDefault() { this.defaultPrevented = true; }, ...extra };
    this.listeners.get(type)?.(event); return event;
  }
}
const descendants = node => [node, ...node.children.flatMap(descendants)];
function clone(node) {
  const result = new Element(node.tagName); result.className = node.className; result.ownText = node.ownText;
  result.attributes = new Map(node.attributes); node.children.forEach(child => result.appendChild(clone(child)));
  return result;
}

async function overview({ missingMath = false } = {}) {
  const data = {
    sourceHash: 'edition',
    props: groups.flatMap(([, numbers]) => numbers.map(n => ({ n, status: 'd', paragraphs: ['Ei vanleg utsegn.'] }))),
    mathematics: {
      [inlineKey]: { tex: inlineTex, display: false, mathml: '<math><mi>𝕄</mi></math>' },
      [displayKey]: { tex: displayTex, display: true, mathml: '<math display="block"><mfrac><mi>a</mi><mi>b</mi></mfrac></math>' },
    },
  };
  data.props.find(prop => prop.n === '1.31').paragraphs = [`Formrommet er *⟦math:${inlineKey}⟧*.[[kjelde:2]]`];
  data.props.find(prop => prop.n === '5.7').paragraphs = [`⟦math:${displayKey}⟧`];
  if (missingMath) delete data.mathematics[inlineKey];
  const host = new Element('div'), document = new Element('document');
  document.getElementById = id => id === 'chapters' ? host : null;
  document.querySelector = () => ({ content: 'edition' });
  document.createElement = tag => new Element(tag);
  document.createDocumentFragment = () => new Element('fragment');
  document.createTextNode = text => { const node = new Element('#text'); node.textContent = text; return node; };
  const window = { getSelection: () => null }, errors = [];
  runInNewContext(script, { document, window, Map, Promise,
    fetch: async () => ({ ok: true, json: async () => data }), console: { error: error => errors.push(error) } });
  await new Promise(resolve => setImmediate(resolve));
  const nodes = descendants(host), math = nodes.filter(node => node.classList.contains('native-math'));
  return { host, document, window, nodes, math, errors };
}

test('the proposition overview renders shared inline and display MathML without exposing source markers', async () => {
  const app = await overview();
  assert.deepEqual(app.errors, []);
  assert.equal(app.math.length, 2);
  assert.ok(app.math[0].textContent.includes('<mi>𝕄</mi>'));
  assert.equal(app.math[0].parentNode.tagName, 'EM', 'Inline maths retains its surrounding emphasis');
  assert.ok(app.math[1].textContent.includes('<mfrac>'));
  assert.ok(app.math[1].classList.contains('math-display'));
  assert.equal(app.math[1].getAttribute('tabindex'), '0');
  assert.equal(app.math[1].getAttribute('role'), 'region');
  assert.ok(app.math[1].getAttribute('aria-label'));
  assert.ok(!app.host.textContent.includes('⟦math:'));
  assert.ok(!app.host.textContent.includes('[[kjelde:'));
  assert.ok(app.nodes.some(node => node.href === '/#1.31'), 'The original proposition remains linked to full text');
  assert.match(html, /\.math-display\{[^}]*overflow-x:auto/);
});

test('copying whole overview formulas returns canonical inline or display LaTeX once', async () => {
  const app = await overview();
  for (const [index, expected] of [[0, String.raw`\(\mathbb{M}\)`], [1, String.raw`\[\frac{a}{b}\]`]]) {
    const native = app.math[index], fragment = clone(native);
    app.window.getSelection = () => ({ isCollapsed: false, rangeCount: 1, anchorNode: native, focusNode: native,
      containsNode: node => node === native, getRangeAt: () => ({ cloneContents: () => fragment }) });
    const clipboard = new Map();
    const event = app.document.dispatch('copy', { clipboardData: { setData: (type, value) => clipboard.set(type, value) } });
    assert.equal(clipboard.get('text/plain'), expected);
    assert.equal(event.defaultPrevented, true);
  }
});

test('whole display copying supports Chromium range boundaries and leaves plain text to the browser', async () => {
  const app = await overview(), native = app.math[1];
  app.document.createRange = () => ({ selectNodeContents(node) { assert.equal(node, native); } });
  app.window.getSelection = () => ({ isCollapsed: false, rangeCount: 1, anchorNode: native, focusNode: native,
    containsNode: () => false,
    getRangeAt: () => ({ cloneContents: () => clone(native), compareBoundaryPoints: point => point === 0 ? -1 : 1 }) });
  const clipboard = new Map();
  app.document.dispatch('copy', { clipboardData: { setData: (type, value) => clipboard.set(type, value) } });
  assert.equal(clipboard.get('text/plain'), String.raw`\[\frac{a}{b}\]`);
  const plain = app.nodes.find(node => node.tagName === 'P' && node.textContent === 'Ei vanleg utsegn.');
  app.window.getSelection = () => ({ isCollapsed: false, rangeCount: 1, anchorNode: plain, focusNode: plain,
    containsNode: () => true, getRangeAt: () => ({ cloneContents: () => clone(plain) }) });
  const plainEvent = app.document.dispatch('copy', { clipboardData: { setData() { assert.fail('Plain copy must remain native'); } } });
  assert.equal(plainEvent.defaultPrevented, false);
});

test('missing mathematics fails visibly instead of publishing internal markers to readers', async () => {
  const app = await overview({ missingMath: true });
  assert.equal(app.errors.length, 1);
  assert.ok(app.host.textContent.includes('Kortversjonen kunne ikkje lastast.'));
  assert.ok(!app.host.textContent.includes('⟦math:'));
});
