#!/usr/bin/env python3
"""Build an offline, local-only double-coder review interface for candidate citation lineages."""
import json
from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parent
OUT=ROOT/"results"

PAGE=r'''<!doctype html>
<html lang="nn">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="color-scheme" content="light">
<title>Formlære — siteringslinjer / blind vurdering</title>
<style>
:root { font-family:system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;color:#181818;background:#fff; }
body { margin:0 auto;max-width:1100px;padding:clamp(14px,4vw,44px);line-height:1.48 }
h1 { font-weight:550;letter-spacing:-.045em;font-size:clamp(30px,4vw,45px);line-height:1.08;margin:16px 0 8px }
small,.muted { color:#666 } 
a { color:#1444c9;text-decoration:none } a:hover { text-decoration:underline }
header { border-bottom:1px solid #ddd;padding-bottom:22px;margin-bottom:26px }
button,input,select,textarea { font:inherit;border:1px solid #bbb;border-radius:5px;padding:9px 11px;max-width:100%;box-sizing:border-box }
button { background:#fafafa;cursor:pointer } button:focus-visible { outline:3px solid #1458d4 }
button.primary { background:#171717;color:white;border-color:#171717 }
button:disabled { opacity:.4;cursor:default }
nav { display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin:15px 0 }
main { display:grid;grid-template-columns:1fr 1fr;gap:16px }
section.paper { border:1px solid #ddd;min-height:170px;border-radius:8px;padding:18px }
h2 { font-size:17px;margin:0 0 18px;font-weight:650 }
.paper h3 { font-size:clamp(18px,2.5vw,22px);line-height:1.25;font-weight:560;margin:0 0 10px }
fieldset { border:0;margin:16px 0 0;padding:0 } legend { font-weight:650;font-size:15px;margin:0 0 10px }
label.option { display:flex;gap:11px;padding:9px 12px;margin:5px 0;border:1px solid #ddd;border-radius:6px;cursor:pointer }
label.option:has(input:checked) {border-color:#222;background:#f0f0f0}
label.option input { margin:3px 0 0 }
label.block { display:block;font-weight:600;margin:16px 0 5px }
textarea { width:100%;min-height:80px;resize:vertical }
input[type=text] { width:100% } 
footer { border-top:1px solid #ddd;margin-top:22px;padding-top:15px }
.stat { padding:10px 15px;background:#f4f4f4;border-radius:6px }
@media(max-width:650px) { main { grid-template-columns:1fr } }
</style>
</head>
<body>
<header>
<small>FORM LÆRE / METAVITSKAP / ARBEIDSUTVAL</small>
<h1>Kva gjer denne siteringa?</h1>
<p>200 semantisk nærliggande siteringspar. Bruk fulltekstane til å vurdere om siteringa testar, replikerer, korrigerer eller berre omtalar eit eldre arbeid. Søkjeord og cosine er berre val av kandidatar, ikkje kodingsfasit.</p>
<p><strong>Ingen vurderingar vert sende nokon stad.</strong> Dei vert lagra lokalt i nettlesaren for valt kodar-ID. Eksporter JSON/CSV jamleg for å ta vare på arbeidet. To forskarar må kode uavhengig før ein samanliknar.</p>
<label class="block" for="reviewer">Kodar-ID (t.d. A eller B, ikkje personnamn)</label>
<input id="reviewer" type="text" value="A" maxlength="20" style="max-width:220px">
<nav>
  <button id="prev">Førre</button>
  <span id="counter" class="stat"></span>
  <button id="next" class="primary">Neste</button>
  <button id="jump">Neste ukoda</button>
</nav>
</header>
<main>
<section class="paper"><small>NYARE PUBLIKASJON — SITERANDE</small><h3 id="newTitle"></h3><p id="newMeta" class="muted"></p><a id="newLink" target="_blank" rel="noopener noreferrer">Opne DOI (eksternt)</a></section>
<section class="paper"><small>ELDRE PUBLIKASJON — SITERT</small><h3 id="oldTitle"></h3><p id="oldMeta" class="muted"></p><a id="oldLink" target="_blank" rel="noopener noreferrer">Opne DOI (eksternt)</a></section>
</main>
<fieldset id="choices">
<legend>Korleis brukar den nyare publikasjonen den eldre?</legend>
<label class="option"><input type="radio" name="relation" value="unread"> Kan ikkje avgjerast utan fulltekst</label>
<label class="option"><input type="radio" name="relation" value="background"> Bakgrunnsomtale / illustrasjon</label>
<label class="option"><input type="radio" name="relation" value="concept"> Låner omgrep eller konsept</label>
<label class="option"><input type="radio" name="relation" value="method"> Tek i bruk eller vidareutviklar metode</label>
<label class="option"><input type="radio" name="relation" value="extension"> Vidareutviklar ein bestemt teoretisk påstand</label>
<label class="option"><input type="radio" name="relation" value="test"> Testar ei spesifikk empirisk/falsifiserbar påstand</label>
<label class="option"><input type="radio" name="relation" value="replication"> Rapporterer eit uavhengig replikeringsforsøk</label>
<label class="option"><input type="radio" name="relation" value="contradiction"> Dokumenterer eksplisitt motfunn eller tilbakevising</label>
<label class="option"><input type="radio" name="relation" value="irrelevant"> Feilaktig fagtilfang eller ugyldig metadata</label>
</fieldset>
<label class="block" for="fulltext">Har du lest begge fulltekstane?</label>
<select id="fulltext"><option value="">Uvisst / ikkje svart</option><option value="yes">Ja, begge</option><option value="one">Berre éin</option><option value="no">Nei</option></select>
<label class="block" for="pages">Sidetal / presis dokumentasjon for tolkinga</label>
<input id="pages" type="text" placeholder="S. 8–9, avsnitt 2; DOI/figur">
<label class="block" for="notes">Grunngjeving og eventuelle motargument</label>
<textarea id="notes" placeholder="Kva konkret påstand vert referert, testa eller revidert? Noter avvik mellom tekst og mogleg tolkning."></textarea>
<nav>
 <button id="save" class="primary">Lagre denne vurderinga</button>
 <button id="exportJSON">Eksporter JSON</button>
 <button id="exportCSV">Eksporter CSV</button>
 <button id="clear">Tøm denne vurderinga</button>
</nav>
<p id="status" class="muted" aria-live="polite"></p>
<footer><small>Samanfall i tekstrommet er ikkje empirisk validering. Denne gjennomgangen erstattar ikkje eit tilfeldig trekt, representativt utval. Ingen ekstra brukardata eller fulltekst vert lasta inn frå serveren. Ved eksport vert berre eige kodingsarbeid og bibliografiske identifikatorar eksporterte.</small></footer>
<script id="paperData" type="application/json">__DATA__</script>
<script>
(()=>{"use strict";
const data=JSON.parse(document.querySelector("#paperData").textContent);
const byId=id=>document.getElementById(id);
const rv=byId("reviewer");
const key=(i)=>"formlaere-audit-v2:"+rv.value.trim()+":"+data[i].id;
let pos=0;
const read=i=>{ try { return JSON.parse(localStorage.getItem(key(i))||"null") } catch(e){return null} };
function setLink(anchor,raw){
  if(!raw || !/^https:\/\/doi\.org\/10\.[0-9]{4,9}\/[^ <>"']+$/i.test(raw)){
    anchor.removeAttribute("href");anchor.textContent="DOI ikkje tilgjengeleg";
  }else{anchor.href=raw;anchor.textContent="Opne DOI (eksternt)"}
}
function render(){
  const r=data[pos];
  byId("newTitle").textContent=r.citing_title;
  byId("oldTitle").textContent=r.cited_title;
  byId("newMeta").textContent=r.citing_year+" · arbeid "+r.citing_id;
  byId("oldMeta").textContent=r.cited_year+" · arbeid "+r.cited_id;
  setLink(byId("newLink"),r.citing_doi);
  setLink(byId("oldLink"),r.cited_doi);
  const saved=read(pos)||{};
  document.querySelectorAll('input[name="relation"]').forEach(x=>x.checked=x.value===saved.relation);
  byId("fulltext").value=saved.fulltext||"";
  byId("pages").value=saved.pages||"";
  byId("notes").value=saved.notes||"";
  const done=data.reduce((sum,x,j)=>sum+Number(Boolean(read(j)?.relation)),0);
  byId("counter").textContent=(pos+1)+"/"+data.length+" · "+done+" vurderte";
  byId("status").textContent= saved.relation ? "Lagra vurdering: "+(saved.saved||"") : "Ikkje koda enno";
  byId("prev").disabled=pos===0;
  byId("next").disabled=pos===data.length-1;
}
function save(){
  const relation=document.querySelector('input[name="relation"]:checked')?.value;
  if(!rv.value.trim()){byId("status").textContent="Skriv inn kodar-ID.";return}
  if(!relation){byId("status").textContent="Vel ei vurdering fyrst.";return}
  const record={relation,fulltext:byId("fulltext").value,pages:byId("pages").value,
     notes:byId("notes").value,saved:new Date().toISOString()};
  try{localStorage.setItem(key(pos),JSON.stringify(record));render()}
  catch(e){byId("status").textContent="Lokal lagring svikta. Eksporter vurderingane for sikkerheitskopi."}
}
function jump(){
  for(let j=pos+1;j<data.length;j++)if(!read(j)?.relation){pos=j;render();return}
  for(let j=0;j<pos;j++)if(!read(j)?.relation){pos=j;render();return}
  byId("status").textContent="Ingen ukoda postar att for denne kodar-ID-en.";
}
function exportRows(){
  return data.map((item,j)=>({...item,reviewer_id:rv.value.trim(),...(read(j)||{})}))
      .filter(x=>Boolean(x.relation));
}
function download(content,type,suffix){
  const blob=new Blob([content],{type});
  const url=URL.createObjectURL(blob);
  const a=document.createElement("a");a.href=url;
  a.download="formlaere-vurderingar-"+rv.value.trim()+"."+suffix;
  document.body.append(a);a.click();a.remove();
  setTimeout(()=>URL.revokeObjectURL(url),30000);
}
function csvField(s){return '"'+String(s??"").replaceAll('"','""')+'"'}
byId("prev").onclick=()=>{if(pos>0){pos--;render()}};
byId("next").onclick=()=>{if(pos<data.length-1){pos++;render()}};
byId("jump").onclick=jump;
byId("save").onclick=save;
rv.onchange=render;
byId("clear").onclick=()=>{
  if(confirm("Tøm denne vurderinga berre for "+rv.value+"?")){localStorage.removeItem(key(pos));render()}
};
byId("exportJSON").onclick=()=>download(JSON.stringify({
  schemaVersion:2,reviewerId:rv.value.trim(),exported:new Date().toISOString(),
  decisions:exportRows()},null,2),"application/json","json");
byId("exportCSV").onclick=()=>{
  const rows=exportRows();
  const columns=["id","citing_id","cited_id","reviewer_id","relation","fulltext","pages","notes","saved"];
  const body=[columns.join(","),...rows.map(x=>columns.map(c=>csvField(x[c])).join(","))].join("\r\n");
  download("\uFEFF"+body,"text/csv","csv");
};
render();
})();
</script>
</body>
</html>'''

def main():
    tab=pd.read_csv(OUT/"lineage_review_queue.csv",dtype=str).fillna("")
    # No source abstracts in browser; filenames and DOI only.
    vals=[]
    for i,row in tab.iterrows():
        source=str(row.citing_doi)
        target=str(row.cited_doi)
        def doi(x):
            return x if x.startswith("https://doi.org/10.") else ""
        vals.append({
          "id":f"{i+1:03d}-{row.citing_year}-{row.cited_year}",
          "citing_id":str(row.citing_id),
          "cited_id":str(row.cited_id),
          "citing_title":str(row.citing_title),
          "cited_title":str(row.cited_title),
          "citing_doi":doi(source),"cited_doi":doi(target),
          "citing_year":str(row.citing_year),"cited_year":str(row.cited_year)
        })
    # Include stable OpenAlex identifiers from actual citation links where possible.
    # Stable pair IDs preserve review state when the ranking changes in a later run.
    import hashlib
    for r in vals:
        stable=r["citing_id"]+"|"+r["cited_id"]
        r["id"]=hashlib.sha256(stable.encode("utf-8")).hexdigest()[:20]
    data=json.dumps(vals,ensure_ascii=False,separators=(",",":")).replace("</","<\\/")
    (OUT/"review.html").write_text(PAGE.replace("__DATA__",data),encoding="utf-8")
    (OUT/"review_setup.md").write_text(
      "# Blindpar-gransking\n\nÅpne review.html lokalt i nettlesar eller start:\n\n"
      "    python -m http.server 8765\n\n"
      "frå research/nordisk-designforsking og gå til "
      "http://localhost:8765/results/review.html.\n\n"
      "Bruk ei eiga kodar-ID for kvar forskar, kod uavhengig og eksporter JSON/CSV.\n"
      "Grunngje vurderingar med sidetal i begge fulltekstar. "
      "Eit markert svar utan fulltekst er ikkje vitskapleg dokumentasjon.\n"
      "Ingen data vert sendt til tredjepart. Berre DOI-lenkjer vert opna etter klikk.\n\n"
      "Merk: Utvalet er semantisk målretta, ikkje representativt. "
      "Resultata kan nyttast til instrumentvalidering, ikkje estimat over heile faget.\n",encoding="utf-8")
    print(f"Built local audit tool with {len(vals)} pairs; embedded titles and DOI only.")
if __name__=="__main__":main()
