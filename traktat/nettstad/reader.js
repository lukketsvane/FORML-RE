(async function siteInit(){
  const response=await fetch("/traktat/document.json",{cache:"no-cache"});
  if(!response.ok)throw new Error("Kunne ikkje laste FORMLÆRE");
  const documentData=await response.json(),DATA=documentData.props,TOKENS=documentData.tokens;
  if(documentData.schemaVersion!==1||!DATA.length)throw new Error("Ufullstendig utgåve av FORMLÆRE");
  const expectedSource=document.querySelector('meta[name="formlaere-source"]').content;
  if(expectedSource!==documentData.sourceHash)throw new Error("Utgåva er oppdatert. Last sida på nytt.");
  const byNum=new Map(DATA.map(d=>[d.n,d]));
  for(const d of DATA){d.kids=[];let p=d.n.slice(0,-1);while(p&&!byNum.has(p))p=p.slice(0,-1);d.parent=p||null;}
  for(const d of DATA){if(d.parent)byNum.get(d.parent).kids.push(d);}
  function depthOf(d){return d.parent?1+depthOf(byNum.get(d.parent)):0;}
  for(const d of DATA)d.depth=depthOf(d);
  const roots=DATA.filter(d=>!d.parent),order=DATA.map(d=>d.n);
  const byRow=new Map(),read=document.getElementById("read"),stream=document.getElementById("stream"),svg=document.getElementById("tree"),NS="http://www.w3.org/2000/svg";
  let current=order[0],hashTimer=0,scrollFrame=0,navUntil=0;
  const reducedMotion=window.matchMedia("(prefers-reduced-motion: reduce)");
  const catalog={sources:documentData.sources};
  const sources=new Map(documentData.sources.map(s=>[String(s.id),s]));
  const allNotes=documentData.notes,noteById=new Map(allNotes.map(note=>[note.id,note]));
  function sourceButton(id){
    const number=sources.get(id).number;
    const link=make("a","xref",String(number));link.href="#referanse-"+id;
    link.setAttribute("aria-label","Til referanse "+number);
    bindPreview(link,()=>sourcePreview(id));
    return link;
  }
  function appendSources(el,ids){
    ids.forEach((id,index)=>{if(index)el.appendChild(document.createTextNode(", "));el.appendChild(sourceButton(String(id)));});
  }
  function appendGlossary(){
    if(!documentData.glossary?.length)return;
    const section=make("section","endmatter glossary");section.id="ordliste";
    const heading=make("h2","section-title","Ordliste");heading.id="ordliste-tittel";
    section.setAttribute("aria-labelledby",heading.id);section.appendChild(heading);
    const list=make("dl","glossary-list");
    for(const item of documentData.glossary){
      const entry=make("div","glossary-entry");entry.id="ord-"+item.id;
      const term=make("dt","glossary-term",item.term);
      if(item.symbol)term.appendChild(make("span","glossary-symbol",item.symbol));
      const definition=make("dd","glossary-definition");
      if(item.fields?.length)definition.appendChild(make("div","endnote-meta",item.fields.join(" · ")));
      definition.appendChild(make("p","",item.definition));
      if(item.connection)definition.appendChild(make("p","","I teksten: "+item.connection));
      if(item.propositions?.length||item.sources?.length){
        const refs=make("p","glossary-links");
        for(const [index,n] of (item.propositions||[]).entries()){
          if(index)refs.appendChild(document.createTextNode(", "));
          refs.appendChild(propositionLink(n,true));
        }
        if(item.sources?.length){
          refs.appendChild(document.createTextNode((item.propositions?.length?" · ":"")+"Kjelder: "));
          appendSources(refs,item.sources);
        }
        definition.appendChild(refs);
      }
      entry.append(term,definition);list.appendChild(entry);
    }
    section.appendChild(list);stream.appendChild(section);
  }
  function appendEndmatter(){
    for(const [kind,title,items] of [["notat","Notat",allNotes],["referansar","Referansar",[...sources.values()]]]){
      const section=make("section","endmatter");section.id=kind;
      const heading=make("h2","section-title",title);heading.id=kind+"-tittel";
      section.setAttribute("aria-labelledby",heading.id);section.appendChild(heading);
      const list=make("ol","endmatter-list");
      items.forEach((item,index)=>{
        const isNote=kind==="notat",number=item.number;
        const entry=make("li","endnote");entry.id=(isNote?"notat-":"referanse-")+(isNote?item.id:item.id);
        entry.appendChild(make("span","endnote-number",isNote?"n"+number:String(number)));
        const body=make("div","endnote-body");
        if(isNote){
          const meta=make("div","endnote-meta");
          const back=item.proposition?propositionLink(item.proposition,true):make("a","xref","Føreord");
          if(!item.proposition){back.href="#introduksjon";back.setAttribute("aria-label","Til føreordet");}
          meta.appendChild(back);
          if(item.relation)meta.appendChild(document.createTextNode(" · "+item.relation));
          body.appendChild(meta);body.appendChild(make("p","",item.note));
          if(item.sources?.length){
            const refs=make("p","source-links","[");appendSources(refs,item.sources);refs.appendChild(document.createTextNode("]"));body.appendChild(refs);
          }
        }else{
          body.appendChild(make("p","",item.citation));
          const url=item.url||(item.doi?"https://doi.org/"+item.doi:null);
          if(url){try{const parsedUrl=new URL(url);if(["https:","http:"].includes(parsedUrl.protocol)){
            const link=make("a","source-links",item.doi?"DOI: "+item.doi:"Opne kjelda");link.href=parsedUrl.href;link.target="_blank";link.rel="noopener noreferrer";body.appendChild(link);
          }}catch(e){}}
        }
        entry.appendChild(body);list.appendChild(entry);
      });
      section.appendChild(list);stream.appendChild(section);
    }
  }
  let addressWindow=window;
  try{if(window.parent!==window&&window.parent.location.hostname===window.location.hostname)addressWindow=window.parent;}catch(e){}
  function hashNumber(){
    try{
      const hash=decodeURIComponent(addressWindow.location.hash.slice(1));
      const source=hash.match(/^referanse-(\d+)$/);
      return source&&documentData.sourceAliases?.[source[1]]?"referanse-"+documentData.sourceAliases[source[1]]:hash;
    }catch(e){return "";}
  }
  // Every internal reference uses one preview and one interaction model.
  const preview=document.createElement("aside");
  preview.className="prop-preview";
  preview.id="prop-preview";
  preview.setAttribute("role","tooltip");
  preview.hidden=true;
  document.body.appendChild(preview);
  let previewAnchor=null,previewMode="";
  function closePreview(){
    if(previewAnchor){
      previewAnchor.classList.remove("previewing");
      previewAnchor.removeAttribute("aria-describedby");
      previewAnchor.removeAttribute("aria-expanded");
    }
    previewAnchor=null;previewMode="";preview.hidden=true;
  }
  function propositionPreview(n){
    const d=byNum.get(n);if(!d)return null;
    return {title:d.n+" · "+({d:"definisjon",a:"postulat/hypotese",t:"følgje under oppgjevne vilkår",o:"observasjon",i:"illustrasjon"}[d.status]||""),
      text:d.paragraphs.join("\n\n").replace(/\[\[kjelde:[\d,]+\]\]/g,"").replace(/\*{1,2}/g,"").trim()};
  }
  function notePreview(id){
    const note=noteById.get(id);if(!note)return null;
    const relation=note.relation?" · "+note.relation:"";
    const refs=note.sources?.length?"\n\nReferansar: "+note.sources.map(id=>sources.get(String(id)).number).join(", "):"";
    return {title:"Notat "+note.number+" · "+(note.proposition||"Føreord")+relation,text:note.note+refs};
  }
  function sourcePreview(id){
    const source=sources.get(String(id));if(!source)return null;
    const doi=source.doi&&!source.citation.includes(source.doi)?"\n\nDOI: "+source.doi:"";
    return {title:"Referanse "+source.number,text:source.citation+doi};
  }
  const mathRuns=new Map();let mathSerial=0;
  const superDigits=new Map([..."⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺"].map((char,index)=>[char,"0123456789-+"[index]]));
  const subDigits=new Map([..."₀₁₂₃₄₅₆₇₈₉₋₊₌₍₎ᵣ"].map((char,index)=>[char,"0123456789-+=()r"[index]]));
  const mathCharacter=char=>!!char&&(/[\p{Sm}\p{Script=Greek}]/u.test(char)||char.codePointAt(0)>=0x1d400&&char.codePointAt(0)<=0x1d7ff);
  function mathScript(text,start){
    if(text[start]==="{"){
      let depth=1;
      for(let i=start+1;i<text.length;i++){
        if(text[i]==="{")depth++;
        if(text[i]==="}"&&!--depth)return {text:text.slice(start+1,i),end:i+1};
      }
      return null;
    }
    const ascii=text.slice(start).match(/^[A-Za-z0-9]+/);
    const value=ascii?ascii[0]:String.fromCodePoint(text.codePointAt(start));
    return {text:value,end:start+value.length};
  }
  function appendMathText(el,text){
    const native=/⟦math:([a-f0-9]{24})⟧/g;
    if(native.test(text)){
      native.lastIndex=0;let cursor=0;
      for(const match of text.matchAll(native)){
        appendMathText(el,text.slice(cursor,match.index));
        const expression=documentData.mathematics?.[match[1]];
        if(!expression?.mathml)throw new Error("Manglande matematikk i utgåva");
        const node=make("span",expression.display?"native-math math-display":"native-math");
        const key=String(++mathSerial);
        node.setAttribute("data-source",expression.tex);node.setAttribute("data-math-id",key);
        node.setAttribute("data-display",expression.display?"block":"inline");mathRuns.set(key,node);
        if(expression.display){
          node.setAttribute("tabindex","0");node.setAttribute("role","region");
          node.setAttribute("aria-label","Matematisk uttrykk; rull vassrett ved behov");
        }
        // Build-time Pandoc output is restricted to validated MathML elements.
        node.innerHTML=expression.mathml;el.appendChild(node);
        cursor=match.index+match[0].length;
      }
      appendMathText(el,text.slice(cursor));return;
    }
    // Scripts are presentation only. Ordinary numbers, dates and citation IDs
    // remain plain text; source spelling is retained for copying a formula.
    let plain=0,index=0;
    while(index<text.length){
      const start=index,char=String.fromCodePoint(text.codePointAt(index));
      let end=index+char.length;
      if(/[A-Za-z0-9]/.test(char)){
        const ascii=text.slice(index).match(/^[A-Za-z0-9]+/)[0];end=index+ascii.length;
      }else if(!mathCharacter(char)){index=end;continue;}
      if(text[end]==="̂")end++;
      const baseEnd=end;
      const scripts=[];
      while(end<text.length){
        const operator=text[end];
        if((operator==="_"||operator==="^")&&end+1<text.length){
          const value=mathScript(text,end+1);if(!value)break;
          scripts.push({operator,text:value.text});end=value.end;
        }else if(superDigits.has(operator)||subDigits.has(operator)){
          const mapping=superDigits.has(operator)?superDigits:subDigits;
          let value="";while(end<text.length&&mapping.has(text[end]))value+=mapping.get(text[end++]);
          scripts.push({operator:mapping===superDigits?"^":"_",text:value});
        }else break;
      }
      if(!scripts.length){index=end;continue;}
      if(start>plain)el.appendChild(document.createTextNode(text.slice(plain,start)));
      const run=make("span","math-inline"),key=String(++mathSerial);
      run.setAttribute("data-source",text.slice(start,end));run.setAttribute("data-math-id",key);
      run.setAttribute("aria-label",text.slice(start,end));mathRuns.set(key,run);
      run.appendChild(make("span","math-base",text.slice(start,baseEnd)));
      const stack=make("span","math-scripts");
      for(const script of scripts){
        const node=make(script.operator==="^"?"sup":"sub","math-script");
        appendMathText(node,script.text);stack.appendChild(node);
      }
      run.appendChild(stack);el.appendChild(run);index=end;plain=end;
    }
    if(plain<text.length)el.appendChild(document.createTextNode(text.slice(plain)));
  }
  function childrenOf(node){return [...(node.childNodes||node.children||[])];}
  function hasMath(node){return node.classList?.contains("math-inline")||node.classList?.contains("native-math")||childrenOf(node).some(hasMath);}
  function forgetMath(node){
    if(node.classList?.contains("math-inline")||node.classList?.contains("native-math"))mathRuns.delete(node.getAttribute("data-math-id"));
    childrenOf(node).forEach(forgetMath);
  }
  function includesMathNode(selection,node){
    if(selection.containsNode(node,false))return true;
    // Chromium can report false for a fully selected MathML block. Compare
    // DOM range boundaries so a whole formula still copies as canonical TeX.
    if(!document.createRange||!selection.getRangeAt)return false;
    const selected=selection.getRangeAt(0),contents=document.createRange();
    if(!selected.compareBoundaryPoints)return false;
    contents.selectNodeContents(node);
    return selected.compareBoundaryPoints(0,contents)<=0&&selected.compareBoundaryPoints(2,contents)>=0;
  }
  function copiedMath(node,selection,inFormula=false){
    if(node.nodeType===3||node.tagName==="#TEXT")return node.textContent;
    if(["annotation","annotation-xml"].includes((node.localName||node.tagName||"").toLowerCase()))return "";
    if(node.classList?.contains("native-math")){
      const original=mathRuns.get(node.getAttribute("data-math-id"));
      if(original&&includesMathNode(selection,original)){
        const display=original.getAttribute("data-display")==="block";
        return (display?"\\[":"\\(")+original.getAttribute("data-source")+(display?"\\]":"\\)");
      }
      return childrenOf(node).map(child=>copiedMath(child,selection)).join("");
    }
    if(node.classList?.contains("math-inline")){
      const original=mathRuns.get(node.getAttribute("data-math-id"));
      if(original&&includesMathNode(selection,original))return original.getAttribute("data-source");
      const children=childrenOf(node);
      const hasBase=children.some(child=>child.classList?.contains("math-base")&&child.textContent);
      return children.map(child=>copiedMath(child,selection,hasBase)).join("");
    }
    const children=childrenOf(node);
    let value=children.length?children.map(child=>copiedMath(child,selection,inFormula)).join(""):node.textContent;
    if(inFormula&&node.classList?.contains("math-script")){
      const operator=node.tagName==="SUP"?"^":"_";
      return operator+([...value].length===1?value:"{"+value+"}");
    }
    if(node.tagName==="BR")return "\n";
    if(["P","ARTICLE","H2","LI","DT","DD","SECTION"].includes(node.tagName))value+="\n";
    return value;
  }
  document.addEventListener("copy",event=>{
    const selection=window.getSelection();
    if(!event.clipboardData||!selection||selection.isCollapsed||selection.rangeCount!==1)return;
    const within=container=>container.contains(selection.anchorNode)&&container.contains(selection.focusNode);
    if(!within(read)&&!within(preview))return;
    const fragment=selection.getRangeAt(0).cloneContents();
    if(!hasMath(fragment))return;
    event.clipboardData.setData("text/plain",copiedMath(fragment,selection).replace(/\n{3,}/g,"\n\n").trimEnd());
    event.preventDefault();
  });
  function showPreview(anchor,mode,content){
    if(!content)return;
    if(previewAnchor&&previewAnchor!==anchor)closePreview();
    previewAnchor=anchor;previewMode=mode;
    anchor.classList.add("previewing");
    anchor.setAttribute("aria-describedby","prop-preview");
    anchor.setAttribute("aria-expanded","true");
    const number=document.createElement("div");
    number.className="prop-preview-num";
    number.textContent=content.title;
    const body=document.createElement("div");
    body.className="prop-preview-body";
    const full=content.text.trim();
    let excerpt=full.length>335?full.slice(0,332).trimEnd():full;
    const partialMath=excerpt.lastIndexOf("⟦math:");
    if(partialMath>excerpt.lastIndexOf("⟧"))excerpt=excerpt.slice(0,partialMath).trimEnd();
    appendMathText(body,excerpt+(excerpt.length<full.length?"…":""));
    forgetMath(preview);preview.replaceChildren(number,body);
    preview.hidden=false;
    const rect=anchor.getBoundingClientRect();
    const width=preview.getBoundingClientRect().width;
    const left=Math.max(12,Math.min(window.innerWidth-width-12,rect.left+rect.width/2-width/2));
    const height=preview.getBoundingClientRect().height;
    const roomAbove=rect.top-12,roomBelow=window.innerHeight-rect.bottom-12;
    let top=roomAbove>=height?rect.top-height-9:rect.bottom+9;
    if(top+height>window.innerHeight-8&&roomAbove>roomBelow)top=rect.top-height-9;
    preview.style.left=left+"px";
    preview.style.top=Math.max(8,Math.min(top,window.innerHeight-height-8))+"px";
  }
  function bindPreview(link,content,navigate){
    let pointerType="mouse";
    link.addEventListener("pointerdown",e=>{pointerType=e.pointerType;});
    link.addEventListener("touchstart",()=>{pointerType="touch";},{passive:true});
    link.addEventListener("pointerenter",e=>{
      if(e.pointerType==="mouse"||e.pointerType==="pen")showPreview(link,"hover",content());
    });
    link.addEventListener("pointerleave",e=>{
      if((e.pointerType==="mouse"||e.pointerType==="pen")&&previewAnchor===link&&previewMode==="hover")closePreview();
    });
    link.addEventListener("focus",()=>{
      if(link.matches(":focus-visible"))showPreview(link,"focus",content());
    });
    link.addEventListener("blur",()=>{if(previewAnchor===link)closePreview();});
    link.addEventListener("click",e=>{
      e.stopPropagation();clearTimeout(hashTimer);
      const modified=e.metaKey||e.ctrlKey||e.shiftKey||e.altKey;
      const touch=pointerType==="touch"&&e.detail!==0&&!modified;
      pointerType="mouse";
      if(touch&&!(previewAnchor===link&&previewMode==="tap")){
        e.preventDefault();showPreview(link,"tap",content());return;
      }
      closePreview();
      // Native anchors retain keyboard, modifier-key and browser hash behavior.
      if(navigate&&!(link.tagName==="A"&&modified)){e.preventDefault();navigate();}
    });
  }
  function propositionLink(n,native=false){
    const link=make(native?"a":"button","xref",n);link.dataset.ref=n;
    if(native)link.href="#"+n;else link.type="button";
    link.setAttribute("aria-label","Vis proposisjon "+n);
    bindPreview(link,()=>propositionPreview(n),()=>go(n));
    return link;
  }
  function addLinkedText(el,text){
    // Only parenthesized proposition citations become links; numbers in
    // mathematical expressions, dates and note numbers stay untouched.
    const group=/\((\s*\d+(?:\.\d+)*(?:\s*[,;–—−-]\s*\d+(?:\.\d+)*)*\s*)\)/g;
    let start=0,m;
    while((m=group.exec(text))!==null){
      appendMathText(el,text.slice(start,m.index)+"(");
      const inner=m[1],numberPattern=/\d+(?:\.\d+)*/g;
      let last=0,match;
      while((match=numberPattern.exec(inner))!==null){
        appendMathText(el,inner.slice(last,match.index));
        const n=match[0];
        if(byNum.has(n)){
          el.appendChild(propositionLink(n));
        }else el.appendChild(document.createTextNode(n));
        last=match.index+n.length;
      }
      appendMathText(el,inner.slice(last)+")");
      start=group.lastIndex;
    }
    appendMathText(el,text.slice(start));
  }
  function richText(el,s){
    for(const part of s.split(/(\*\*[^*]+\*\*|\*[^*]+\*)/g)){
      if(!part)continue;
      if(part.startsWith("**")&&part.endsWith("**")){
        const b=document.createElement("strong");addLinkedText(b,part.slice(2,-2));el.appendChild(b);
      }else if(part.startsWith("*")&&part.endsWith("*")){
        const em=document.createElement("em");addLinkedText(em,part.slice(1,-1));el.appendChild(em);
      }else addLinkedText(el,part);
    }
  }
  function rich(el,s){
    const pattern=/\[\[kjelde:(\d+(?:,\d+)*)\]\]/g;let cursor=0;
    for(const match of s.matchAll(pattern)){
      richText(el,s.slice(cursor,match.index));
      const sup=make("sup","source-ref");appendSources(sup,match[1].split(","));el.appendChild(sup);
      cursor=match.index+match[0].length;
    }
    richText(el,s.slice(cursor));
  }
  function addNoteLinks(el,ids=[]){
    for(const id of ids){const note=noteById.get(id);if(!note)continue;
      const link=make("a","xref note-ref","n"+note.number);link.href="#notat-"+id;
      link.setAttribute("aria-label","Til notat "+note.number);
      bindPreview(link,()=>notePreview(id));el.appendChild(link);
    }
  }
  // Dismiss previews on scrolling, tapping elsewhere, rotating or Escape.
  read.addEventListener("scroll",closePreview,{passive:true});
  document.addEventListener("pointerdown",e=>{
    if(previewAnchor&&!previewAnchor.contains(e.target))closePreview();
  },{capture:true});
  document.addEventListener("keydown",e=>{if(e.key==="Escape")closePreview();});
  window.addEventListener("resize",closePreview,{passive:true});
  function make(tag,cls,text){
    const el=document.createElement(tag);if(cls)el.className=cls;if(text!==undefined)el.textContent=text;return el;
  }
  const FIGURES_AFTER={};
  for(const figure of documentData.figures)(FIGURES_AFTER[figure.after]??=[]).push(figure);
  // The reader begins at "Føreord". Title, subtitle and byline are
  // source metadata, not part of the reading stream.
  const bodyStart=TOKENS.findIndex(tok=>tok.kind==="heading"&&tok.text==="Føreord");
  if(bodyStart<0)throw new Error("Føreord manglar i FORMLÆRE");
  const readingStart=TOKENS.findIndex(tok=>tok.kind==="heading"&&tok.text==="Lesekode");
  if(readingStart<0)throw new Error("Lesekode manglar i FORMLÆRE");
  const visibleTokens=TOKENS.slice(bodyStart);
  // The tree belongs to the propositions, not the foreword or reading code.
  // Its sticky position is bounded by this section, so it leaves the screen
  // after the last proposition instead of covering the glossary and notes.
  const propositionStrip=document.querySelector(".strip");
  let propositionSection=null;
  for(const tok of visibleTokens){
    if(tok.kind==="heading"){const h=make("h2","section-title",tok.text);h.id=tok.text==="Føreord"?"introduksjon":"del-"+tok.text.toLowerCase().replace(/[^a-z0-9æøå]+/g,"-").replace(/^-|-$/g,"");stream.appendChild(h);}
    else if(tok.kind==="paragraph"){const p=make("p","plain-paragraph");rich(p,tok.text);addNoteLinks(p,tok.notes);stream.appendChild(p);}
    else if(tok.kind==="prop"){
      if(!propositionSection){
        propositionSection=make("section","proposition-section");
        propositionSection.setAttribute("aria-label","Proposisjonar og navigasjon");
        propositionSection.appendChild(propositionStrip);
        stream.appendChild(propositionSection);
      }
      const row=make("article","prop depth"+Math.min(byNum.get(tok.n).depth,4));row.dataset.n=tok.n;row.id=tok.n;
      const n=make("span","n",tok.n);const sup=make("sup","status",tok.status);n.appendChild(sup);
      const body=make("div","t");for(const para of tok.paragraphs){const p=make("p","prop-paragraph");rich(p,para);body.appendChild(p);}
      addNoteLinks(body.lastElementChild,tok.notes);
      row.append(n,body);row.addEventListener("click",()=>{if(!window.getSelection()?.toString())setCurrent(tok.n,true,false);});
      byRow.set(tok.n,row);propositionSection.appendChild(row);
      const figures=FIGURES_AFTER[tok.n];
      if(figures?.length){
        const group=make("div","figure-set");
        group.setAttribute("aria-label","Illustrasjonar knytte til proposisjon "+tok.n);
        for(const item of figures){
          const figure=make("figure","tractate-figure");
          const img=document.createElement("img");
          img.src="/traktat/illustrations/"+item.file;
          img.alt=item.alt;
          img.loading="lazy";
          img.decoding="async";
          figure.appendChild(img);
          group.appendChild(figure);
        }
        propositionSection.appendChild(group);
      }
    }
  }
  appendGlossary();appendEndmatter();
  const VW=358,PAD=5,SGAP=5,YROOT=17,YLAB=8,UNIT=75;
  const branches=roots.flatMap(r=>r.kids);
  const STEP=(VW-2*PAD-SGAP*(roots.length-1))/Math.max(1,branches.length);
  let x=PAD;
  for(const r of roots){r.x0=x;for(const b of r.kids){b.x=x+STEP/2;x+=STEP;}r.x1=x;x+=SGAP;}
  function ancestorBranch(d){
    if(!d||!d.parent)return null;
    while(d.parent&&byNum.get(d.parent)?.parent)d=byNum.get(d.parent);
    return d;
  }
  for(const b of branches)b.members=DATA.filter(d=>ancestorBranch(d)?.n===b.n);
  function branchHeight(b){return 12+Math.min(UNIT-14,6*Math.sqrt(b.members.length));}
  const VH=YROOT+Math.max(0,...branches.map(branchHeight))+5;
  function mk(tag,attrs){const e=document.createElementNS(NS,tag);for(const key in attrs)e.setAttribute(key,attrs[key]);return e;}
  function drawTree(){
    svg.setAttribute("viewBox",`0 0 ${VW} ${VH}`);svg.innerHTML="";
    const sec=byNum.get(current)?.n[0]||"1",group=ancestorBranch(byNum.get(current));const g=mk("g",{});
    for(const r of roots){
      const on=r.n===sec;
      g.appendChild(mk("path",{d:`M${r.x0} ${YROOT} H${r.x1}`,class:"rbar"+(on?" on":"")}));
      const lab=mk("text",{x:(r.x0+r.x1)/2,y:YLAB,class:"rlab"+(on?" on":"")});lab.textContent=r.n;g.appendChild(lab);
      for(const b of r.kids){
        const isBranch=group&&group.n===b.n;
        const ht=branchHeight(b);
        g.appendChild(mk("path",{d:`M${b.x} ${YROOT} V${YROOT+ht}`,class:"stem"+(isBranch?" on":on?" sec":"")}));
        if(isBranch){const i=b.members.findIndex(d=>d.n===current);if(i>=0){const cy=YROOT+5+(i+.5)/Math.max(1,b.members.length)*(ht-5);g.appendChild(mk("circle",{cx:b.x,cy,r:2.5,class:"dot"}));}}
      }
    }
    svg.appendChild(g);
    read.style.setProperty("--tree-height",propositionStrip.offsetHeight+"px");
  }
  function paint(){
    for(const [n,el] of byRow)el.classList.toggle("active",n===current);
    drawTree();
  }
  function hashWrite(){
    clearTimeout(hashTimer);
    hashTimer=setTimeout(()=>{try{addressWindow.history.replaceState(null,"","#"+current);}catch(e){}},220);
  }
  function setCurrent(n,write=true,scroll=false,behavior="smooth"){
    if(!byNum.has(n))return;
    current=n;paint();if(write)hashWrite();
    if(scroll){const motion=reducedMotion.matches?"auto":behavior;navUntil=performance.now()+(motion==="smooth"?520:80);byRow.get(n)?.scrollIntoView({block:"start",behavior:motion});}
  }
  function go(n,behavior="smooth"){setCurrent(n,true,true,behavior);}
  function currentFromScroll(){
    if(performance.now()<navUntil)return;
    if(read.scrollTop<=2){if(current!==order[0])setCurrent(order[0],false);return;}
    const scroller=read.getBoundingClientRect();
    const nav=propositionStrip.getBoundingClientRect();
    const navPinned=nav.top<=scroller.top+2&&nav.bottom>scroller.top+2;
    const line=scroller.top+(navPinned?propositionStrip.offsetHeight:0)+20;
    const endmatter=document.getElementById("ordliste")||document.getElementById("notat");
    if(endmatter?.getBoundingClientRect().top<=line)return;
    let candidate=null;
    for(const n of order){
      const r=byRow.get(n).getBoundingClientRect();
      if(r.top<=line&&r.bottom>=line){candidate=n;break;}
      if(r.top>line){candidate=n;break;}
    }
    if(!candidate)candidate=order[order.length-1];
    if(candidate!==current)setCurrent(candidate,false);
  }
  read.addEventListener("scroll",()=>{if(scrollFrame)return;scrollFrame=requestAnimationFrame(()=>{scrollFrame=0;currentFromScroll();});},{passive:true});
  for(const ev of ["wheel","touchstart","keydown"])read.addEventListener(ev,()=>{navUntil=0;},{passive:true});
  let scrubbing=false,pending=null,raf=0;
  function atPoint(cx,cy){
    const r=svg.getBoundingClientRect();if(!r.width)return null;
    const u=(cx-r.left)/r.width*VW,v=(cy-r.top)/r.height*VH;
    let b=branches[0],dist=Infinity;
    for(const c of branches){const d=Math.abs(c.x-u);if(d<dist){dist=d;b=c;}}
    if(!b)return null;
    if(v<YROOT)return b.parent;
    const t=Math.max(0,Math.min(1,(v-YROOT-5)/(branchHeight(b)-5)));
    return (b.members[Math.min(b.members.length-1,Math.floor(t*b.members.length))]||b).n;
  }
  function scrubTo(cx,cy){
    const n=atPoint(cx,cy);if(!n||n===current)return;
    pending=n;if(!raf)raf=requestAnimationFrame(()=>{raf=0;if(pending)go(pending,"auto");pending=null;});
  }
  svg.addEventListener("pointerdown",e=>{scrubbing=true;svg.setPointerCapture(e.pointerId);scrubTo(e.clientX,e.clientY);e.preventDefault();});
  svg.addEventListener("pointermove",e=>{if(scrubbing)scrubTo(e.clientX,e.clientY);});
  svg.addEventListener("pointerup",()=>{scrubbing=false;});
  svg.addEventListener("pointercancel",()=>{scrubbing=false;});
  const h=hashNumber();if(byNum.has(h))current=h;
  paint();
  if(byNum.has(h))requestAnimationFrame(()=>go(h,"auto"));
  else if(h)requestAnimationFrame(()=>document.getElementById(h)?.scrollIntoView({block:"start"}));
  addressWindow.addEventListener("hashchange",()=>{clearTimeout(hashTimer);const n=hashNumber();if(byNum.has(n))setCurrent(n,false,true,"auto");else document.getElementById(n)?.scrollIntoView({block:"start"});});
})().catch(err=>{const read=document.getElementById("read");if(read)read.textContent="Klarte ikkje laste FORMLÆRE.";console.error(err);});

if('serviceWorker' in navigator && window.isSecureContext){
  window.addEventListener('load',()=>navigator.serviceWorker.register('/service-worker.js',{scope:'/',updateViaCache:'none'}).catch(()=>{}),{once:true});
}
