// Citation marks are explicit. Never infer sources from ordinary numbers or powers.
export function splitCitations(text) {
  const parts = [];
  const pattern = /\[\[kjelde:(\d+(?:,\d+)*)\]\]/g;
  let start = 0;
  for (const match of text.matchAll(pattern)) {
    if (match.index > start) parts.push({kind: 'text', text: text.slice(start, match.index)});
    parts.push({kind: 'citation', ids: match[1].split(',')});
    start = match.index + match[0].length;
  }
  if (start < text.length) parts.push({kind: 'text', text: text.slice(start)});
  return parts;
}

export function plainText(text) {
  return text.replace(/\[\[kjelde:\d+(?:,\d+)*\]\]/g, '').replace(/\*{1,2}/g, '');
}

export function parseSource(src) {
  const tokens = [], props = [];
  let active = null, buf = [];
  const flush = () => {
    const text = buf.join('\n').trim();
    buf = [];
    if (!text) return;
    if (active) active.paragraphs.push(text);
    else tokens.push({kind: 'paragraph', text});
  };
  for (const line of src.replace(/\r\n?/g, '\n').split('\n')) {
    if (line.startsWith('## ')) { flush(); active = null; tokens.push({kind:'heading',text:line.slice(3).trim()}); continue; }
    if (line.startsWith('# ')) { flush(); active = null; tokens.push({kind:'title',text:line.slice(2).trim()}); continue; }
    const match = line.match(/^\*\*(\d+(?:\.\d+)*)([datio])\*\*\s+(.*)$/);
    if (match) {
      flush();
      active = {kind: 'prop', n: match[1], status: match[2], paragraphs: []};
      tokens.push(active); props.push(active);
      if (match[3]) buf.push(match[3]);
      continue;
    }
    if (!line.trim()) { flush(); continue; }
    buf.push(line);
  }
  flush();
  return {tokens, props};
}

export function validateEdition(src, catalog) {
  const parsed = parseSource(src);
  if (parsed.props.length !== 375 || parsed.props[0]?.n !== '1' || parsed.props.at(-1)?.n !== '7.4') {
    throw new Error('Ufullstendig eller feil utgåve av FORMLÆRE');
  }
  const numbers = new Set(parsed.props.map(prop => prop.n));
  if (numbers.size !== parsed.props.length) throw new Error('Dupliserte proposisjonsnummer');
  if (!Array.isArray(catalog.sources) || !catalog.sources.length) throw new Error('Kjeldelista manglar');
  const ids = new Set();
  for (const source of catalog.sources) {
    if (!/^\d+$/.test(source.id) || !source.citation?.trim() || ids.has(source.id)) throw new Error('Ugyldig kjeldepost');
    ids.add(source.id);
  }
  for (const part of splitCitations(src)) {
    if (part.kind === 'citation' && part.ids.some(id => !ids.has(id))) throw new Error('Ukjend kjeldetilvising');
  }
  if (/\[\[kjelde:/.test(src.replace(/\[\[kjelde:\d+(?:,\d+)*\]\]/g,''))) throw new Error('Feilforma kjeldemarkør');
  for (const note of catalog.annotations || []) {
    const prop = parsed.props.find(item => item.n === note.proposition);
    if (!prop || !plainText(prop.paragraphs.join('\n\n')).includes(note.anchor)) throw new Error('Kjeldenotat utan tekstanker: '+note.proposition);
    if (!note.sources?.length || note.sources.some(id => !ids.has(id))) throw new Error('Ukjend kjelde i notat');
  }
  for (const note of catalog.intro || []) {
    const intro = parsed.tokens.filter(item => item.kind === 'paragraph').map(item => plainText(item.text)).join('\n\n');
    if (!intro.includes(note.anchor)) throw new Error('Føreordnotat utan tekstanker: '+note.anchor);
    if (!note.sources?.length || note.sources.some(id => !ids.has(id))) throw new Error('Ukjend kjelde i føreordnotat');
  }
  return parsed;
}
