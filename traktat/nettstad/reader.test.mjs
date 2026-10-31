import test from 'node:test';
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {splitCitations,parseSource,plainText,validateEdition} from './content.mjs';

test('citations are explicit; powers, dates and proposition numbers remain ordinary text',()=>{
  const math='ρ ∼ 10⁷, året 2026 og (5.232).';
  assert.deepEqual(splitCitations(math),[{kind:'text',text:math}]);
  assert.deepEqual(splitCitations('Form.[[kjelde:3,8,58]] Vidare.'),[
    {kind:'text',text:'Form.'},{kind:'citation',ids:['3','8','58']},{kind:'text',text:' Vidare.'}
  ]);
  assert.equal(plainText('**Form**.[[kjelde:8]] 10⁷'),'Form. 10⁷');
});

test('parser retains separate paragraphs, formatting and source marks',()=>{
  const {props,tokens}=parseSource('# FORMLÆRE\n\n## Føreord\nTekst.\n\n**1d** *Form*.[[kjelde:1]]\n\nNeste avsnitt.\n\n**1.01t** Seinare.');
  assert.equal(tokens[0].kind,'title');
  assert.deepEqual(props.map(prop=>prop.n),['1','1.01']);
  assert.deepEqual(props[0].paragraphs,['*Form*.[[kjelde:1]]','Neste avsnitt.']);
});

test('current edition has 375 unique propositions and every citation resolves',async()=>{
  const text=await readFile(new URL('../tekst/formlaere.txt',import.meta.url),'utf8');
  const catalog=JSON.parse(await readFile(new URL('../kjelder.json',import.meta.url),'utf8'));
  assert.equal(validateEdition(text,catalog).props.length,375);
  assert.ok(catalog.sources.length>=107);
  const changed=text.replace(/\[\[kjelde:[\d,]+\]\]/,'[[kjelde:999999]]');
  assert.throws(()=>validateEdition(changed,catalog),/Ukjend kjeldetilvising/);
  assert.throws(()=>validateEdition(text.replace('**7.4t**','**7.3t**'),catalog),/utgåve|Dupliserte/);
});
