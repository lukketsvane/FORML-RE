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
    this.attributes = new Map(); this.listeners = new Map();
    this.style = { values: new Map(), setProperty(name,value){ this.values.set(name,value); } };
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
  appendChild(child) {
    if(child.parentNode)child.parentNode.children=child.parentNode.children.filter(node=>node!==child);
    child.parentNode = this; this.children.push(child); return child;
  }
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

async function reader({ mathText, mathematics = {}, extraSource = false } = {}) {
  const props = [
    { n: '1', status: 'd', paragraphs: ['Form med kjelde.[[kjelde:7]] Sjå (1.1).'], notes: ['note-one'] },
    { n: '1.1', status: 't', paragraphs: ['Ein utfyllande proposisjon.'], notes: [] },
    { n: '1.11', status: 't', paragraphs: ['Ei nærare utgreiing.'], notes: [] },
    { n: '1.111', status: 'i', paragraphs: ['Eit døme.'], notes: [] },
    { n: '1.1111', status: 'o', paragraphs: ['Den siste i greina.'], notes: [] },
  ];
  if (mathText) props[1].paragraphs = [mathText];
  const data = { schemaVersion: 1, sourceHash: 'edition', props, mathematics,
    tokens: [{ kind: 'heading', text: 'Føreord' }, { kind: 'paragraph', text: 'Eit føreord.' },
      { kind: 'heading', text: 'Lesekode' }, ...props.map(prop => ({ kind: 'prop', ...prop }))],
    notes: [{ id: 'note-one', number: 1, proposition: '1', relation: 'grunnlag', note: 'Dette er notatet.', sources: ['7'] }],
    sources: [{ id: '7', number: 1, citation: 'Ei fullstendig bibliografisk kjelde.', doi: '10.1234/example' }],
    figures: [], glossary: [{ id: 'form', term: 'Form', symbol: 'F', fields: ['Biologi', 'Dynamiske system'],
      definition: 'Ei ordning av skilnader.', connection: 'Omgrepet knyter saman faglege perspektiv.', propositions: ['1'], sources: ['7'] }],
  };
  if(extraSource){
    data.sources.push({id:'110',number:2,citation:'Ei anna kjelde.'});
    data.sourceAliases={'63':'7'};
    data.props[0].paragraphs[0]+='[[kjelde:110]]';
    data.notes[0].sources.push('110');
    data.glossary[0].sources.push('110');
  }
  const document = new Element('document'); document.body = new Element('body');
  const read = new Element('main'); read.id = 'read'; read.scrollTop = 0;
  const stream = new Element('div'); stream.id = 'stream'; read.append(stream);
  const tree = new Element('svg'); tree.id = 'tree';
  const strip = new Element('div'); strip.className = 'strip'; strip.offsetHeight = 72; strip.append(tree);
  document.body.append(strip, read);
  document.createElement = tag => new Element(tag);
  document.createElementNS = (_, tag) => new Element(tag);
  document.createTextNode = text => { const node = new Element('#text'); node.textContent = text; return node; };
  document.getElementById = id => descendants(document.body).find(node => node.id === id);
  document.querySelector = selector => selector === '.strip' ? strip : { content: 'edition' };
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
    [app.note, 'Notat 1 · 1 · grunnlag', 'Referansar: 1'],
    [app.source, 'Referanse 1', 'DOI: 10.1234/example']]) {
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

test('inline scripts stay legible in the reader and the shared proposition preview', async () => {
  const text = 'I_Γ(A) og τ^Γ_k(A): e^β. ∑_{k∈I_Γ(A_i)} ω_k. Sjå (1.1). År 2026 og 6.65.';
  const app = await reader({ mathText: text });
  const paragraph = descendants(app.byId('1.1')).find(node => node.classList.contains('prop-paragraph'));
  const runs = descendants(paragraph).filter(node => node.classList.contains('math-inline'));
  const power = runs.find(node => node.getAttribute('data-source') === 'e^β');
  assert.ok(power, 'An explicit exponent becomes a mathematical run');
  assert.equal(power.children[0].textContent, 'e');
  assert.equal(power.children[1].children[0].tagName, 'SUP');
  assert.equal(power.children[1].children[0].textContent, 'β');
  const horizon = runs.find(node => node.getAttribute('data-source') === 'τ^Γ_k');
  assert.deepEqual(horizon.children[1].children.map(node => [node.tagName, node.textContent]), [['SUP', 'Γ'], ['SUB', 'k']]);
  const sum = runs.find(node => node.getAttribute('data-source') === '∑_{k∈I_Γ(A_i)}');
  assert.ok(sum, 'Balanced, nested script groups are retained');
  assert.ok(descendants(sum).some(node => node.getAttribute('data-source') === 'I_Γ'));
  assert.ok(descendants(sum).some(node => node.getAttribute('data-source') === 'A_i'));
  assert.ok(paragraph.textContent.includes('År 2026 og 6.65.'));
  assert.equal(descendants(paragraph).filter(node => node.tagName === 'BUTTON').length, 1, 'Only the explicit proposition reference becomes a link');
  app.proposition.dispatch('pointerenter', { pointerType: 'mouse' });
  assert.ok(descendants(app.preview).some(node => node.getAttribute('data-source') === 'e^β'), 'The existing tooltip uses the same mathematical typography');
});

function cloneElement(element) {
  const clone = new Element(element.tagName);
  clone.className = element.className; clone.ownText = element.ownText;
  for (const [name, value] of element.attributes) clone.setAttribute(name, value);
  element.children.forEach(child => clone.appendChild(cloneElement(child)));
  return clone;
}

test('copying a formula retains its canonical scripts while ordinary copy is untouched', async () => {
  const text = 'τ^Γ_k(A), I_Γ(A_i), ∑_{k∈I_Γ(A_i)} ω_k og e^β; 2026 (1.1).';
  const app = await reader({ mathText: text });
  const paragraph = descendants(app.byId('1.1')).find(node => node.classList.contains('prop-paragraph'));
  const fragment = new Element('fragment'); fragment.append(cloneElement(paragraph));
  app.window.getSelection = () => ({ isCollapsed: false, rangeCount: 1,
    anchorNode: paragraph.children[0], focusNode: paragraph.children.at(-1),
    containsNode: node => paragraph.contains(node), getRangeAt: () => ({ cloneContents: () => fragment }) });
  const clipboard = new Map();
  const event = app.document.dispatch('copy', { clipboardData: { setData: (type, value) => clipboard.set(type, value) } });
  assert.equal(event.defaultPrevented, true);
  assert.equal(clipboard.get('text/plain'), text, 'Whole equations copy as the original source, including nested braces');

  const plain = descendants(app.byId('1')).find(node => node.classList.contains('prop-paragraph'));
  app.window.getSelection = () => ({ isCollapsed: false, rangeCount: 1,
    anchorNode: plain.children[0], focusNode: plain.children.at(-1),
    containsNode: node => plain.contains(node), getRangeAt: () => ({ cloneContents: () => cloneElement(plain) }) });
  const untouched = app.document.dispatch('copy', { clipboardData: { setData() { assert.fail('Ordinary copy must use the browser default'); } } });
  assert.equal(untouched.defaultPrevented, false);
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
  assert.deepEqual(sections.filter(node=>node.classList.contains('endmatter')).map(node => node.id), ['ordliste', 'notat', 'referansar']);
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
  assert.equal(refs.textContent, '1 · Kjelder: 1');
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
  assert.equal(app.preview.children[0].textContent, 'Referanse 1');
  assert.ok(app.preview.children[1].textContent.includes('Ei fullstendig bibliografisk kjelde.'));
});

test('continuous source numbers share labels across citations, glossary, notes and reference entries while IDs remain stable', async () => {
  const app=await reader({extraSource:true});
  const inline=descendants(app.byId('1')).find(node=>node.href==='#referanse-110');
  assert.equal(inline.textContent,'2');
  assert.equal(inline.getAttribute('aria-label'),'Til referanse 2');
  assert.equal(descendants(app.byId('ord-form')).find(node=>node.classList.contains('glossary-links')).textContent,'1 · Kjelder: 1, 2');
  assert.equal(app.byId('referanse-7').children[0].textContent,'1');
  assert.equal(app.byId('referanse-110').children[0].textContent,'2');
  app.note.dispatch('pointerenter',{pointerType:'mouse'});
  assert.ok(app.preview.textContent.includes('Referansar: 1, 2'));
  inline.dispatch('pointerenter',{pointerType:'mouse'});
  assert.equal(app.preview.children[0].textContent,'Referanse 2');
  app.window.location.hash='#referanse-63';
  app.window.dispatch('hashchange');
  assert.equal(app.byId('referanse-7').scrolls,1,'A historical alias still reaches its canonical reference');
  assert.equal(app.byId('referanse-63'),undefined,'An alias does not add a numbered bibliography entry');
});

test('the proposition tree begins after Lesekode and is bounded before endnotes', async () => {
  const app = await reader();
  const blocks = app.stream.children;
  const section = blocks.find(node => node.classList.contains('proposition-section'));
  assert.ok(section, 'The numbered propositions have a dedicated container');
  assert.equal(section.children[0].className, 'strip', 'Tree is the first item of the proposition section');
  assert.equal(section.children[0].children[0].id, 'tree');
  assert.equal(section.children[1].id, '1');
  assert.equal(section.children.at(-1).id, '1.1111', 'The last subproposition closes the sticky section');
  const readingCode = blocks.findIndex(node => node.id === 'del-lesekode');
  const start = blocks.indexOf(section);
  const glossary = blocks.findIndex(node => node.id === 'ordliste');
  assert.ok(readingCode < start && start < glossary,
    'Foreword and reading code precede the tree, while endnotes follow its containing section');
  assert.equal(app.byId('read').style.values.get('--tree-height'), '72px');
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


test('native LaTeX math is rendered from the shared MathML and copied once as TeX', async () => {
  const key='a'.repeat(24),tex=String.raw`\frac{a}{b}`;
  const app=await reader({mathText:`Verdien er ⟦math:${key}⟧.`,mathematics:{[key]:{tex,display:false,
    mathml:'<math xmlns="http://www.w3.org/1998/Math/MathML"><mfrac><mi>a</mi><mi>b</mi></mfrac></math>'}}});
  const paragraph=descendants(app.byId('1.1')).find(node=>node.classList.contains('prop-paragraph'));
  const native=descendants(paragraph).find(node=>node.classList.contains('native-math'));
  assert.equal(native.getAttribute('data-source'),tex);
  assert.ok(native.textContent.includes('<mfrac>'));
  const fragment=new Element('fragment');fragment.append(cloneElement(paragraph));
  app.window.getSelection=()=>({isCollapsed:false,rangeCount:1,anchorNode:paragraph.children[0],focusNode:paragraph.children.at(-1),
    containsNode:node=>paragraph.contains(node),getRangeAt:()=>({cloneContents:()=>fragment})});
  const clipboard=new Map();app.document.dispatch('copy',{clipboardData:{setData:(type,value)=>clipboard.set(type,value)}});
  assert.equal(clipboard.get('text/plain'),String.raw`Verdien er \(\frac{a}{b}\).`);
});


test('whole display math copies as TeX when Chromium containsNode reports only partial containment', async () => {
  const key='b'.repeat(24),tex=String.raw`\frac{a}{b}`;
  const app=await reader({mathText:`⟦math:${key}⟧`,mathematics:{[key]:{tex,display:true,
    mathml:'<math xmlns="http://www.w3.org/1998/Math/MathML"><mfrac><mi>a</mi><mi>b</mi></mfrac></math>'}}});
  const paragraph=descendants(app.byId('1.1')).find(node=>node.classList.contains('prop-paragraph'));
  const native=descendants(paragraph).find(node=>node.classList.contains('native-math'));
  assert.equal(native.getAttribute('tabindex'),'0');
  assert.equal(native.getAttribute('role'),'region');
  assert.ok(native.getAttribute('aria-label'));
  const fragment=new Element('fragment');fragment.append(cloneElement(native));
  app.document.createRange=()=>({selectNodeContents(node){assert.equal(node,native);}});
  app.window.getSelection=()=>({isCollapsed:false,rangeCount:1,anchorNode:paragraph,focusNode:paragraph,
    containsNode:()=>false,getRangeAt:()=>({cloneContents:()=>fragment,compareBoundaryPoints:point=>point===0?-1:1})});
  const clipboard=new Map();app.document.dispatch('copy',{clipboardData:{setData:(type,value)=>clipboard.set(type,value)}});
  assert.equal(clipboard.get('text/plain'),String.raw`\[\frac{a}{b}\]`);
});
