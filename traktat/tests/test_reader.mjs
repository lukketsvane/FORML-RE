import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import test from 'node:test';
import { runInNewContext } from 'node:vm';

const script = readFileSync(new URL('../nettstad/reader.js', import.meta.url), 'utf8');

// A small DOM facade runs the actual reader without a browser dependency.
// Native anchor navigation is represented by an uncancelled click and href.
class Element {
  constructor(tag) {
    this.tagName = tag.toUpperCase(); this.children = []; this.dataset = {};
    this.attributes = new Map(); this.listeners = new Map(); this.style = {};
    this.className = ''; this.ownText = ''; this.hidden = false; this.scrolls = 0;
    this.classList = {
      contains: name => this.className.split(/\s+/).includes(name),
      add: name => { if (!this.classList.contains(name)) this.className += ' ' + name; },
      remove: name => { this.className = this.className.split(/\s+/).filter(item => item !== name).join(' '); },
      toggle: (name, enabled) => enabled ? this.classList.add(name) : this.classList.remove(name),
    };
  }
  set textContent(text) { this.ownText = String(text); this.children = []; }
  get textContent() { return this.ownText + this.children.map(child => child.textContent).join(''); }
  set innerHTML(text) { this.textContent = text; }
  get lastElementChild() { return this.children.filter(child => child.tagName !== '#TEXT').at(-1); }
  appendChild(child) { child.parentNode = this; this.children.push(child); return child; }
  append(...children) { children.forEach(child => this.appendChild(child)); }
  replaceChildren(...children) { this.ownText = ''; this.children = []; this.append(...children); }
  setAttribute(name, value) { this.attributes.set(name, String(value)); if (name === 'class') this.className = String(value); }
  getAttribute(name) { return this.attributes.get(name) ?? null; }
  removeAttribute(name) { this.attributes.delete(name); }
  addEventListener(type, handler) {
    if (!this.listeners.has(type)) this.listeners.set(type, []);
    this.listeners.get(type).push(handler);
  }
  dispatch(type, properties = {}) {
    const event = { target: this, detail: 1, button: 0, defaultPrevented: false,
      preventDefault() { this.defaultPrevented = true; }, stopPropagation() {}, ...properties };
    for (const handler of this.listeners.get(type) || []) handler(event);
    return event;
  }
  matches(selector) { return selector === ':focus-visible' && !!this.focusVisible; }
  contains(target) { return this === target || this.children.some(child => child.contains(target)); }
  getBoundingClientRect() { return { left: 40, top: 220, right: 100, bottom: 240, width: 60, height: 20 }; }
  setPointerCapture(pointerId) { this.capturedPointer = pointerId; }
  scrollIntoView() { this.scrolls += 1; }
}

function descendants(element) { return [element, ...element.children.flatMap(descendants)]; }

async function reader() {
  const props = [
    { n: '1', status: 'd', paragraphs: ['Form med kjelde.[[kjelde:7]] Sjå (1.1).'], notes: ['note-one'] },
    { n: '1.1', status: 't', paragraphs: ['Ein utfyllande proposisjon.'], notes: [] },
    { n: '1.11', status: 't', paragraphs: ['Ei nærare utgreiing.'], notes: [] },
    { n: '1.111', status: 'i', paragraphs: ['Eit døme.'], notes: [] },
    { n: '1.1111', status: 'o', paragraphs: ['Den siste i greina.'], notes: [] },
  ];
  const data = { schemaVersion: 1, sourceHash: 'edition', props,
    tokens: [{ kind: 'heading', text: 'Føreord' }, { kind: 'paragraph', text: 'Eit føreord.' },
      { kind: 'heading', text: 'Lesekode' }, ...props.map(prop => ({ kind: 'prop', ...prop }))],
    notes: [{ id: 'note-one', number: 1, proposition: '1', relation: 'grunnlag', note: 'Dette er notatet.', sources: ['7'] }],
    sources: [{ id: '7', citation: 'Ei fullstendig bibliografisk kjelde.', doi: '10.1234/example' }],
    figures: [], glossary: [{ id: 'form', term: 'Form', symbol: 'F', fields: ['Biologi', 'Dynamiske system'],
      definition: 'Ei ordning av skilnader.', connection: 'Omgrepet knyter saman faglege perspektiv.', propositions: ['1'], sources: ['7'] }],
  };
  const document = new Element('document'); document.body = new Element('body');
  const read = new Element('main'); read.id = 'read'; read.scrollTop = 0;
  const stream = new Element('div'); stream.id = 'stream'; read.append(stream);
  const tree = new Element('svg'); tree.id = 'tree'; document.body.append(tree, read);
  document.createElement = tag => new Element(tag);
  document.createElementNS = (_, tag) => new Element(tag);
  document.createTextNode = text => { const node = new Element('#text'); node.textContent = text; return node; };
  document.getElementById = id => descendants(document.body).find(node => node.id === id);
  document.querySelector = () => ({ content: 'edition' });
  const window = new Element('window'); window.parent = window;
  window.location = { hash: '', hostname: 'formlaere.example' };
  window.history = { replaceState() {} }; window.innerWidth = 390; window.innerHeight = 844;
  window.matchMedia = () => ({ matches: false }); window.getSelection = () => null;
  const errors = [];
  const frames = [];
  runInNewContext(script, { document, window, navigator: {}, URL, Map, Set, Promise,
    fetch: async () => ({ ok: true, json: async () => data }),
    setTimeout: () => 1, clearTimeout() {}, requestAnimationFrame: callback => { frames.push(callback); return frames.length; },
    performance: { now: () => 0 }, console: { error: error => errors.push(error) } });
  await new Promise(resolve => setImmediate(resolve));
  assert.deepEqual(errors, [], 'The reader fixture must initialize successfully');
  const nodes = descendants(document.body);
  return { document, window, stream, nodes, byId: id => document.getElementById(id),
    flushFrames() { while (frames.length) frames.shift()(); },
    preview: document.getElementById('prop-preview'),
    source: nodes.find(node => node.href === '#referanse-7'),
    note: nodes.find(node => node.href === '#notat-note-one'),
    proposition: nodes.find(node => node.tagName === 'BUTTON' && node.dataset.ref === '1.1'),
  };
}

test('notes, sources and propositions share the same hover and focus preview', async () => {
  const app = await reader();
  for (const [link, title, text] of [[app.proposition, '1.1 · teorem', 'Ein utfyllande proposisjon.'],
    [app.note, 'Notat 1 · 1 · grunnlag', 'Referansar: 7'],
    [app.source, 'Referanse 7', 'DOI: 10.1234/example']]) {
    link.dispatch('pointerenter', { pointerType: 'mouse' });
    assert.equal(app.preview.hidden, false);
    assert.equal(app.preview.children[0].textContent, title);
    assert.ok(app.preview.children[1].textContent.includes(text));
    assert.equal(link.getAttribute('aria-describedby'), 'prop-preview');
    link.dispatch('pointerleave', { pointerType: 'mouse' });
    assert.equal(app.preview.hidden, true);
    link.focusVisible = true; link.dispatch('focus');
    assert.equal(app.preview.hidden, false);
    link.dispatch('blur'); assert.equal(app.preview.hidden, true);
    assert.equal(link.getAttribute('aria-describedby'), null);
  }
});

test('native note and source anchors preview on first touch and navigate on second', async () => {
  const app = await reader();
  for (const [link, href] of [[app.note, '#notat-note-one'], [app.source, '#referanse-7']]) {
    assert.equal(link.tagName, 'A'); assert.equal(link.href, href);
    link.dispatch('pointerdown', { pointerType: 'touch' });
    assert.equal(link.dispatch('click').defaultPrevented, true);
    assert.equal(app.preview.hidden, false);
    link.dispatch('pointerdown', { pointerType: 'touch' });
    assert.equal(link.dispatch('click').defaultPrevented, false);
    assert.equal(app.preview.hidden, true);
    link.dispatch('pointerenter', { pointerType: 'mouse' });
    assert.equal(link.dispatch('click').defaultPrevented, false, 'Mouse navigation takes one click');
  }
});

test('keyboard activation after touch navigates and shared previews dismiss consistently', async () => {
  const app = await reader();
  app.note.dispatch('pointerdown', { pointerType: 'touch' });
  assert.equal(app.note.dispatch('click', { detail: 0 }).defaultPrevented, false);
  for (const dismiss of [() => app.document.dispatch('keydown', { key: 'Escape' }),
    () => app.byId('read').dispatch('scroll'),
    () => app.document.dispatch('pointerdown', { target: app.byId('read') })]) {
    app.source.dispatch('pointerenter', { pointerType: 'pen' });
    assert.equal(app.preview.hidden, false); dismiss(); assert.equal(app.preview.hidden, true);
  }
  app.proposition.dispatch('click', { detail: 0 });
  assert.equal(app.byId('1.1').scrolls, 1, 'Existing proposition navigation still scrolls to the proposition');
});

test('the semantic glossary precedes notes and references and reuses proposition previews', async () => {
  const app = await reader();
  const sections = app.stream.children.filter(node => node.tagName === 'SECTION');
  assert.deepEqual(sections.map(node => node.id), ['ordliste', 'notat', 'referansar']);
  const glossary = app.byId('ordliste');
  assert.equal(glossary.children[1].tagName, 'DL');
  const entry = app.byId('ord-form');
  assert.equal(entry.children[0].tagName, 'DT');
  assert.equal(entry.children[1].tagName, 'DD');
  const link = descendants(entry).find(node => node.href === '#1');
  link.dispatch('pointerenter', { pointerType: 'mouse' });
  assert.equal(app.preview.children[0].textContent, '1 · definisjon');
  assert.ok(app.byId('notat-note-one').textContent.includes('Dette er notatet.'));
  assert.ok(app.byId('referanse-7').textContent.includes('Ei fullstendig bibliografisk kjelde.'));
});

test('glossary bibliography links share the existing source tooltip and native anchor behavior', async () => {
  const app = await reader();
  const entry = app.byId('ord-form');
  const refs = descendants(entry).find(node => node.classList.contains('glossary-links'));
  assert.equal(refs.textContent, '1 · Kjelder: 7');
  const source = descendants(refs).find(node => node.href === '#referanse-7');
  assert.equal(source.tagName, 'A');
  app.source.dispatch('pointerenter', { pointerType: 'mouse' });
  const inlineContent = app.preview.textContent;
  source.dispatch('pointerenter', { pointerType: 'mouse' });
  assert.strictEqual(app.byId('prop-preview'), app.preview, 'The same tooltip element is reused');
  assert.equal(app.preview.textContent, inlineContent);
  assert.equal(source.getAttribute('aria-describedby'), 'prop-preview');
  assert.equal(source.dispatch('click').defaultPrevented, false);
  assert.equal(app.preview.hidden, true);
});

test('glossary fields and scoped connections render without changing linked previews', async () => {
  const app = await reader();
  const definition = app.byId('ord-form').children.find(node => node.tagName === 'DD');
  assert.equal(definition.children[0].className, 'endnote-meta');
  assert.equal(definition.children[0].textContent, 'Biologi · Dynamiske system');
  assert.equal(definition.children[1].textContent, 'Ei ordning av skilnader.');
  assert.equal(definition.children[2].textContent, 'I teksten: Omgrepet knyter saman faglege perspektiv.');
  const proposition = descendants(definition).find(node => node.href === '#1');
  proposition.dispatch('pointerenter', { pointerType: 'mouse' });
  assert.equal(app.preview.children[0].textContent, '1 · definisjon');
  assert.ok(!app.preview.textContent.includes('I teksten:'));
  const source = descendants(definition).find(node => node.href === '#referanse-7');
  source.dispatch('pointerenter', { pointerType: 'mouse' });
  assert.equal(app.preview.children[0].textContent, 'Referanse 7');
  assert.ok(app.preview.children[1].textContent.includes('Ei fullstendig bibliografisk kjelde.'));
});

test('the tree viewBox ends just below its longest visible branch', async () => {
  const app = await reader();
  const tree = app.byId('tree');
  const [, , width, height] = tree.getAttribute('viewBox').split(' ').map(Number);
  const stems = descendants(tree).filter(node => node.classList.contains('stem'));
  const bottom = Math.max(...stems.map(node => Number(node.getAttribute('d').split(' V')[1])));
  assert.equal(width, 358, 'The horizontal geometry stays unchanged');
  assert.equal(height - bottom, 5, 'Only the small drawing margin remains below the stems');
});

test('scrubbing the visible bottom of a short branch reaches its last proposition', async () => {
  const app = await reader();
  const tree = app.byId('tree');
  const [, , width, height] = tree.getAttribute('viewBox').split(' ').map(Number);
  tree.getBoundingClientRect = () => ({ left: 0, top: 0, width, height });
  const stem = descendants(tree).find(node => node.classList.contains('stem'));
  const [, x, , bottom] = stem.getAttribute('d').match(/^M([\d.]+) ([\d.]+) V([\d.]+)$/).map(Number);
  tree.dispatch('pointerdown', { pointerId: 1, clientX: x, clientY: bottom });
  app.flushFrames();
  assert.equal(app.byId('1.1111').scrolls, 1, 'The full member range fits the actual drawn stem');
  assert.ok(app.byId('1.1111').classList.contains('active'));
});
