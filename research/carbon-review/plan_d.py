import collections, csv, json, re
from pathlib import Path

root=Path(__file__).resolve().parents[2]
out=Path(__file__).resolve().parent
src=(root/"traktat"/"tekst"/"formlaere.tex").read_text(encoding="utf-8")
oldnames=("6.02","6.0201","6.021","6.0211","6.022","6.023","6.0231","6.024","6.025","6.026","6.027")
newnames=("6.8","6.801","6.81","6.811","6.82","6.83","6.831","6.84","6.85","6.86","6.87")
mapping=dict(zip(oldnames,newnames))
pattern=r"\\begin\{formproposition\}\{([\d.]+)\}\{([datio])\}([\s\S]*?)\\end\{formproposition\}"
matches=list(re.finditer(pattern,src))
original={m.group(1):m for m in matches}
assert len(original)==len(matches)==491
assert all(x in original for x in mapping)
assert not (set(newnames)&set(original))
blocks=[]
for old,new in mapping.items():
    m=original[old]
    oldprefix=r"\begin{formproposition}{"+old+"}"
    newprefix=r"\begin{formproposition}{"+new+"}"
    assert m.group(0).startswith(oldprefix)
    blocks.append(m.group(0).replace(oldprefix,newprefix,1))
body=src
for old in oldnames:
    m=original[old]
    assert body.count(m.group(0))==1
    body=body.replace(m.group(0),"",1)
anchor=original["6.76"].group(0)
assert body.count(anchor)==1
body=body.replace(anchor,anchor+"\n\n"+"\n\n".join(blocks),1)
newmatches=list(re.finditer(pattern,body))
ids=[m.group(1) for m in newmatches]
assert len(ids)==len(set(ids))==491
assert "6.8" in ids and "6.02" not in ids
assert ids.index("6.01")+1==ids.index("6.1")
assert ids.index("6.76")+1==ids.index("6.8")
assert ids.index("6.87")+1==ids.index("7")
assert all(original[x].group(2)==next(m.group(2) for m in newmatches if m.group(1)==mapping[x]) for x in mapping)
formulas=lambda x:collections.Counter(re.findall(r"\\\[[\s\S]*?\\\]|\\\([\s\S]*?\\\)",x))
marks=lambda x:collections.Counter(re.findall(r"\\(?:kjelder|notat)\{[^}]*\}",x))
assert formulas(body)==formulas(src)
assert marks(body)==marks(src)
assert re.findall(r"\\section\{[^}]*\}",body)==re.findall(r"\\section\{[^}]*\}",src)
(out/"PLAN_D_ARBEIDSKOPI_491.tex.txt").write_text(body,encoding="utf-8")

refs=[]
files=[
root/"traktat"/"tekst"/"formlaere.tex",
root/"traktat"/"kjelder.json",
root/"traktat"/"ordliste.json",
root/"traktat"/"figurar.json",
root/"traktat"/"nettstad"/"kort.html",
root/"traktat"/"nettstad"/"kortversjon.tex",
root/"traktat"/"tests"/"test_autoresearch_004.py",
root/"traktat"/"tests"/"test_claim_consistency.py",
]
r=re.compile(r"(?<![\d.])(?:"+"|".join(re.escape(x) for x in sorted(mapping,key=len,reverse=True))+r")(?![\d])")
for p in files:
    if not p.exists():continue
    for n,line in enumerate(p.read_text(encoding="utf-8").splitlines(),1):
        for m in r.finditer(line):
            refs.append((str(p.relative_to(root)).replace("\\","/"),n,m.group(),mapping[m.group()],line[max(0,m.start()-65):m.end()+65].strip()[:150]))
with (out/"PLAN_D_REFERANSEKART.tsv").open("w",encoding="utf-8",newline="") as f:
    w=csv.writer(f,delimiter="\t");w.writerow(("file","line","old","new","context"));w.writerows(refs)

md=[
"# Plan D: designaren som konklusjon, ikkje premiss",
"",
"**Status:** Kontrafaktisk arbeidskopi, ikkje publiseringsklar. Ingen endringar i kanonisk LaTeX.",
"",
"Fable-rapporten for 43815960203 foreslår å flytte elleve definisjons- og følgjeproposisjonar (6.02 til 6.027) frå opninga av del 6 til plassen etter 6.76. Då kan argumentet fyrst leggje fram fleire agentar, val, omsorg og konsekvensar, og først deretter definere designaren som den formgjevaren som tek omsyn til den andre. Carbon-arbeidsmåten støttar behovet for ein samanhengande alternativ komposisjon, men dette konkrete grepet kjem frå Fable-rapporten.",
"",
"## Maskinelt verifisert prototype",
"",
"- 491 unike proposisjonsadresser både før og etter flytting.",
"- Elleve gamle adresser har fått elleve nye; ingen kollisjon.",
"- Proposisjonstypar uendra, matematiske uttrykk og kjeldemarkørar identiske som mengder.",
"- Føreord, etterord og andre seksjonsgrenser står.",
"- 6.01 går vidare til 6.1; 6.76 går vidare til 6.8, og 6.87 går vidare til 7.",
"- Arbeidskopien inneheld enno gamle kryssreferansar i prose/metadata. Han skal ikkje byggjast til publisering som han står.",
"",
"## Renummerering",
"",
"| Før | Etter |",
"|---|---|",
]
md.extend("| "+x+" | "+mapping[x]+" |" for x in oldnames)
md+=["",f"## Referansearbeid: {len(refs)} tekstlege treff i relevante kjeldefiler","",
"Det maskinelle referansekartet er i PLAN_D_REFERANSEKART.tsv. Treff kan òg vere omtalar av proposisjonar eller gamle prøvenummer og må klassifiserast før endring. Særleg føreord, notar, ordlista, figurkoplingar, tl;dr og tester må oppdaterast samstundes.",
"",
"## Verknad og risiko",
"",
"- Styrke: Det du kallar designaren, kan bli den endelege konsekvensen av argumentet om omsorg i del 6, i staden for ein definisjon før dei verkelege vilkåra er etablerte.",
"- Styrke: 6.0201 sitt krav om eit arbeid som kan rettast av den andre sitt svar kjem etter dei faktiske modellane av svar og tilbakeføring.",
"- Tap: Lesaren møter ikkje omgrepet designar tidleg i del 6. Ordet er brukt andre stader før den nye definisjonen og må anten fjernast eller motiverast.",
"- Risiko: Flyttinga kan gjere del 6 tyngre eller lukke det opne i slutten for sterkt. Ho er ein konkret hypotese som må vurderast i ei fullstendig lesing.",
"- Samspel med Fable-plan C: kan kombinerast, men krev då ei meir omfattande omnummerering; bør ikkje gjerast før Plan D er prøvd aleine.",
"- Fable-plan E om å byte ordlyden i 6 og 6.13 er ikkje lagt inn: den føreslåtte todelinga mellom agent og landskap er ikkje strengt sann dersom landskapet omfattar agentane sine eigne val.",
"",
"**Konklusjon:** Eit reelt komposisjonsforsøk med maskinelt validert intern struktur. Ingen påstand om at det nye verket er betre før referansar, matematisk tolking og heilskapslesing er prøvde.",
]
(out/"PLAN_D_VURDERING.md").write_text("\n".join(md)+"\n",encoding="utf-8")
print(json.dumps({"propositions":len(ids),"moved":len(mapping),"references":len(refs),"by_file":dict(collections.Counter(x[0] for x in refs))},ensure_ascii=False))
