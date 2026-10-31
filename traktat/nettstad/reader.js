import {splitCitations, plainText, validateEdition} from "./content.mjs";

// WebKit can ignore user-scalable=no on iPhone. Suppress pinch gestures,
// but keep single-finger scrolling and reader controls entirely native.
(function preventPagePinch(){
  const stopIfMultitouch = event => {
    if (event.touches && event.touches.length > 1 && event.cancelable) {
      event.preventDefault();
    }
  };
  document.addEventListener('touchstart', stopIfMultitouch, {passive:false, capture:true});
  document.addEventListener('touchmove', stopIfMultitouch, {passive:false, capture:true});
  for (const name of ['gesturestart','gesturechange']) {
    document.addEventListener(name, event => {
      if (event.cancelable) event.preventDefault();
    }, {passive:false, capture:true});
  }
})();
(async function siteInit(){
  const [response, sourceResponse] = await Promise.all([
    fetch("/data/formlaere.txt", {cache:"no-store"}),
    fetch("/data/kjelder.json", {cache:"no-store"})
  ]);
  if(!response.ok || !sourceResponse.ok) throw new Error("Kunne ikkje laste FORMLÆRE");
  const [sourceText, catalog] = await Promise.all([response.text(), sourceResponse.json()]);
  const parsed=validateEdition(sourceText,catalog), DATA=parsed.props, TOKENS=parsed.tokens;
  const sources = new Map(catalog.sources.map(source=>[source.id,source]));
  const byNum=new Map(DATA.map(d=>[d.n,d]));
  for(const d of DATA){d.kids=[];let p=d.n.slice(0,-1);while(p&&!byNum.has(p))p=p.slice(0,-1);d.parent=p||null;}
  for(const d of DATA){if(d.parent)byNum.get(d.parent).kids.push(d);}
  function depthOf(d){return d.parent?1+depthOf(byNum.get(d.parent)):0;}
  for(const d of DATA)d.depth=depthOf(d);
  const roots=DATA.filter(d=>!d.parent),order=DATA.map(d=>d.n);
  const byRow=new Map(),read=document.getElementById("read"),stream=document.getElementById("stream"),pos=document.getElementById("pos"),svg=document.getElementById("tree"),NS="http://www.w3.org/2000/svg";
  let current=order[0],hashTimer=0,scrollFrame=0,navUntil=0;
  const reducedMotion=window.matchMedia("(prefers-reduced-motion: reduce)");
  let addressWindow=window;
  try{if(window.parent!==window&&window.parent.location.hostname===window.location.hostname)addressWindow=window.parent;}catch(e){}
  function hashNumber(){try{return decodeURIComponent(addressWindow.location.hash.slice(1));}catch(e){return "";}}
  // One quiet overlay serves both proposition and source previews.
  const preview=document.createElement("aside");
  preview.className="prop-preview";
  preview.id="reference-preview";
  preview.setAttribute("role","tooltip");
  preview.hidden=true;
  document.body.appendChild(preview);
  const anchorNotes=new WeakMap();
  let previewAnchor=null,previewMode="",closeTimer=0;
  function closePreview(){
    clearTimeout(closeTimer);
    if(previewAnchor){
      previewAnchor.classList.remove("previewing");
      previewAnchor.removeAttribute("aria-describedby");
    }
    previewAnchor=null;previewMode="";preview.hidden=true;
  }
  function scheduleClose(){
    clearTimeout(closeTimer);
    closeTimer=setTimeout(()=>{
      if(previewMode==="hover"&&!preview.matches(":hover")&&!previewAnchor?.matches(":hover"))closePreview();
    },160);
  }
  function positionPreview(anchor){
    const rect=anchor.getBoundingClientRect();
    const view=window.visualViewport;
    const vw=view?.width||window.innerWidth,vh=view?.height||window.innerHeight;
    const width=preview.getBoundingClientRect().width;
    const left=Math.max(12,Math.min(vw-width-12,rect.left+rect.width/2-width/2));
    const height=preview.getBoundingClientRect().height;
    const roomAbove=rect.top-12,roomBelow=vh-rect.bottom-12;
    let top=roomAbove>=height?rect.top-height-7:rect.bottom+7;
    if(top+height>vh-8&&roomAbove>roomBelow)top=rect.top-height-7;
    preview.style.left=left+"px";
    preview.style.top=Math.max(8,Math.min(top,vh-height-8))+"px";
  }
  function showPreview(anchor,mode){
    clearTimeout(closeTimer);
    if(previewAnchor&&previewAnchor!==anchor)closePreview();
    const note=anchorNotes.get(anchor),d=byNum.get(anchor.dataset.ref);
    if(!note&&!d)return;
    previewAnchor=anchor;previewMode=mode;
    anchor.classList.add("previewing");
    anchor.setAttribute("aria-describedby",preview.id);
    const number=make("div","prop-preview-num");
    const body=make("div","prop-preview-body");
    if(note){
      preview.classList.add("source-preview");
      number.textContent=note.relation|| (note.sources.length===1?"Kjelde":"Kjelder");
      if(note.note)body.appendChild(make("p","source-note",note.note));
      for(const id of note.sources){
        const source=sources.get(id);
        if(!source)continue;
        body.appendChild(make("p","source-citation","["+id+"] "+source.citation));
      }
    }else{
      preview.classList.remove("source-preview");
      number.textContent=d.n+" · "+({d:"definisjon",a:"postulat",t:"modellvilkårsvis følgje",o:"observasjon",i:"illustrasjon"}[d.status]||"");
      const full=plainText(d.paragraphs.join("\n\n")).trim();
      body.textContent=full.length>450?full.slice(0,447).trimEnd()+"…":full;
    }
    preview.replaceChildren(number,body);
    preview.hidden=false;
    positionPreview(anchor);
  }
  preview.addEventListener("pointerenter",()=>clearTimeout(closeTimer));
  preview.addEventListener("pointerleave",scheduleClose);
  function bindPreview(anchor,activate){
    let pointerType="mouse";
    anchor.addEventListener("pointerdown",event=>{pointerType=event.pointerType;});
    anchor.addEventListener("pointerenter",event=>{
      if(event.pointerType==="mouse"||event.pointerType==="pen")showPreview(anchor,"hover");
    });
    anchor.addEventListener("pointerleave",()=>{
      if(previewAnchor===anchor&&previewMode==="hover")scheduleClose();
    });
    anchor.addEventListener("focus",()=>{
      if(anchor.matches(":focus-visible"))showPreview(anchor,"focus");
    });
    anchor.addEventListener("blur",()=>{
      if(previewAnchor===anchor)closePreview();
    });
    anchor.addEventListener("keydown",event=>{
      pointerType="keyboard";
      if(previewAnchor===anchor&&["ArrowDown","ArrowUp","PageDown","PageUp"].includes(event.key)){
        event.preventDefault();
        const body=preview.querySelector(".prop-preview-body");
        const amount=event.key.startsWith("Page")?body.clientHeight:40;
        body.scrollTop+=(event.key.endsWith("Down")?1:-1)*amount;
      }
    });
    anchor.addEventListener("click",event=>{
      event.stopPropagation();event.preventDefault();
      if(activate){
        if(pointerType==="touch"&&!(previewAnchor===anchor&&previewMode==="tap"))showPreview(anchor,"tap");
        else{closePreview();activate();}
      }else if(previewAnchor===anchor&&previewMode==="tap")closePreview();
      else showPreview(anchor,"tap");
    });
  }
  function addLinkedText(el,text){
    // Parenthesized proposition citations alone become navigation links.
    const group=/\((\s*\d+(?:\.\d+)*(?:\s*[,;–—−-]\s*\d+(?:\.\d+)*)*\s*)\)/g;
    let start=0,m;
    while((m=group.exec(text))!==null){
      el.appendChild(document.createTextNode(text.slice(start,m.index)+"("));
      const inner=m[1],numberPattern=/\d+(?:\.\d+)*/g;
      let last=0,match;
      while((match=numberPattern.exec(inner))!==null){
        el.appendChild(document.createTextNode(inner.slice(last,match.index)));
        const n=match[0];
        if(byNum.has(n)){
          const link=make("button","xref",n);
          link.type="button";link.dataset.ref=n;
          link.setAttribute("aria-label","Vis proposisjon "+n);
          bindPreview(link,()=>go(n));
          el.appendChild(link);
        }else el.appendChild(document.createTextNode(n));
        last=match.index+n.length;
      }
      el.appendChild(document.createTextNode(inner.slice(last)+")"));
      start=group.lastIndex;
    }
    el.appendChild(document.createTextNode(text.slice(start)));
  }
  function addSourceText(el,text){
    for(const part of splitCitations(text)){
      if(part.kind==="text")addLinkedText(el,part.text);
      else{
        const button=make("button","source-ref",part.ids.join(","));
        button.type="button";
        button.dataset.sources=part.ids.join(",");
        button.setAttribute("aria-label",(part.ids.length===1?"Vis kjelde ":"Vis kjelder ")+part.ids.join(", "));
        anchorNotes.set(button,{sources:part.ids});
        bindPreview(button);
        el.appendChild(button);
      }
    }
  }
  function addAnnotations(el,notes){
    for(const note of notes){
      const walker=document.createTreeWalker(el,NodeFilter.SHOW_TEXT);
      let node;
      while((node=walker.nextNode())){
        if(node.parentElement.closest("button"))continue;
        const index=node.data.indexOf(note.anchor);
        if(index<0)continue;
        const before=node.data.slice(0,index),after=node.data.slice(index+note.anchor.length);
        const button=make("button","source-term",note.anchor);
        button.type="button";
        button.dataset.sources=note.sources.join(",");
        button.setAttribute("aria-label",note.anchor+", vis kjeldegrunnlag");
        anchorNotes.set(button,note);bindPreview(button);
        node.replaceWith(document.createTextNode(before),button,document.createTextNode(after));
        break;
      }
    }
  }
  function rich(el,s,notes=[]){
    for(const part of s.split(/(\*\*[^*]+\*\*|\*[^*]+\*)/g)){
      if(!part)continue;
      if(part.startsWith("**")&&part.endsWith("**")){
        const b=document.createElement("strong");addSourceText(b,part.slice(2,-2));el.appendChild(b);
      }else if(part.startsWith("*")&&part.endsWith("*")){
        const em=document.createElement("em");addSourceText(em,part.slice(1,-1));el.appendChild(em);
      }else addSourceText(el,part);
    }
    addAnnotations(el,notes);
  }
  // Scrolling the text dismisses the overlay; scrolling a source itself does not.
  read.addEventListener("scroll",closePreview,{passive:true});
  document.addEventListener("pointerdown",event=>{
    if(previewAnchor&&!event.target.closest(".xref,.source-ref,.source-term,.prop-preview"))closePreview();
  },{capture:true});
  document.addEventListener("keydown",event=>{
    if(event.key==="Escape"&&previewAnchor){event.preventDefault();closePreview();}
  });
  window.addEventListener("resize",closePreview,{passive:true});
  window.visualViewport?.addEventListener("resize",closePreview,{passive:true});
  function make(tag,cls,text){
    const el=document.createElement(tag);if(cls)el.className=cls;if(text!==undefined)el.textContent=text;return el;
  }
  const FIGURES_AFTER={"1.54":[{"file":"scan-20261031-p13-c-k-operator-tabell-og-rorsle.png","alt":"C–K-operasjonane: retning og lyskjegleoperasjonar"}],"2.212":[{"file":"scan-20261031-p16-royrstol-utvikling.png","alt":"Frå sykkelramme til røyrstol"}],"5.125":[{"file":"scan-20261031-p21-agentrang.png","alt":"Agens frå termostat til designar"}],"6.66":[{"file":"scan-20261031-p35-d-modell-diagram.png","alt":"Formrom, partisjon, grammatikk, landskap og agenthierarki"}],"7.142":[{"file":"scan-20261031-p41-sommarfugl-livslop.png","alt":"Larve, puppe og sommarfugl"}],"1.4":[{"file":"scan-20261031-p11-busette-opne-forbodne.png","alt":"Busette, opne og forbodne regionar"}]};
  for(const tok of TOKENS){
    if(tok.kind==="title"){const h=make("h1","doc-title",tok.text);stream.appendChild(h);}
    else if(tok.kind==="heading"){const h=make("h2","section-title",tok.text);h.id="del-"+tok.text.toLowerCase().replace(/[^a-z0-9æøå]+/g,"-").replace(/^-|-$/g,"");stream.appendChild(h);}
    else if(tok.kind==="paragraph"){const p=make("p","plain-paragraph");rich(p,tok.text,catalog.intro||[]);stream.appendChild(p);}
    else if(tok.kind==="prop"){
      const row=make("article","prop depth"+Math.min(tok.depth,4));row.dataset.n=tok.n;row.id=tok.n;
      const n=make("span","n",tok.n);const sup=make("sup","status",tok.status);n.appendChild(sup);
      const body=make("div","t");for(const para of tok.paragraphs){const p=make("p","prop-paragraph");rich(p,para,(catalog.annotations||[]).filter(note=>note.proposition===tok.n));body.appendChild(p);}
      row.append(n,body);row.addEventListener("click",()=>{if(!window.getSelection()?.toString())setCurrent(tok.n,true,false);});
      byRow.set(tok.n,row);stream.appendChild(row);
      const figures=FIGURES_AFTER[tok.n];
      if(figures?.length){
        const group=make("div","figure-set");
        group.setAttribute("aria-label","Illustrasjonar knytte til proposisjon "+tok.n);
        for(const item of figures){
          const figure=make("figure","tractate-figure");
          const img=document.createElement("img");
          img.src="/illustrations/"+item.file;
          img.alt=item.alt;
          img.loading="lazy";
          img.decoding="async";
          figure.appendChild(img);
          group.appendChild(figure);
        }
        stream.appendChild(group);
      }
    }
  }
  stream.appendChild(make("div","endmark",order[order.length-1]+" · SLUTT"));
  const bibliography=make("details","bibliography");
  bibliography.id="kjelder";
  bibliography.appendChild(make("summary","", "Kjelder · "+catalog.sources.length));
  const referenceList=make("ol","source-list");
  for(const source of catalog.sources){
    const item=make("li","source-record");
    item.id="kjelde-"+source.id;item.value=Number(source.id);
    item.appendChild(document.createTextNode(source.citation));
    if(source.url && /^https?:\/\//.test(source.url)){
      const link=make("a","source-url","Les kjelda");
      link.href=source.url;link.target="_blank";link.rel="noopener noreferrer";
      item.appendChild(link);
    }
    referenceList.appendChild(item);
  }
  bibliography.appendChild(referenceList);stream.appendChild(bibliography);
  const VW=358,PAD=5,SGAP=5,YROOT=17,YLAB=8,UNIT=75;
  const branches=roots.flatMap(r=>r.kids);
  const STEP=(VW-2*PAD-SGAP*(roots.length-1))/Math.max(1,branches.length);
  let x=PAD;
  for(const r of roots){r.x0=x;for(const b of r.kids){b.x=x+STEP/2;x+=STEP;}r.x1=x;x+=SGAP;}
  const VH=YROOT+UNIT+7;
  function ancestorBranch(d){
    if(!d||!d.parent)return null;
    while(d.parent&&byNum.get(d.parent)?.parent)d=byNum.get(d.parent);
    return d;
  }
  for(const b of branches)b.members=DATA.filter(d=>ancestorBranch(d)?.n===b.n);
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
        const ht=12+Math.min(UNIT-14,6*Math.sqrt(b.members.length));
        g.appendChild(mk("path",{d:`M${b.x} ${YROOT} V${YROOT+ht}`,class:"stem"+(isBranch?" on":on?" sec":"")}));
        if(isBranch){const i=b.members.findIndex(d=>d.n===current);if(i>=0){const cy=YROOT+5+(i+.5)/Math.max(1,b.members.length)*(ht-5);g.appendChild(mk("circle",{cx:b.x,cy,r:2.5,class:"dot"}));}}
      }
    }
    svg.appendChild(g);
  }
  function paint(){
    for(const [n,el] of byRow)el.classList.toggle("active",n===current);
    const i=order.indexOf(current);pos.textContent=current+" · "+(i+1)+"/"+order.length;
    document.getElementById("prev").disabled=i===0;
    document.getElementById("next").disabled=i===order.length-1;
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
  function step(k){const i=order.indexOf(current)+k;if(i>=0&&i<order.length)go(order[i]);}
  document.getElementById("prev").addEventListener("click",()=>step(-1));
  document.getElementById("next").addEventListener("click",()=>step(1));
  function currentFromScroll(){
    if(performance.now()<navUntil)return;
    if(read.scrollTop<=2){if(current!==order[0])setCurrent(order[0]);return;}
    const line=read.getBoundingClientRect().top+32;
    let candidate=null;
    for(const n of order){
      const r=byRow.get(n).getBoundingClientRect();
      if(r.top<=line&&r.bottom>=line){candidate=n;break;}
      if(r.top>line){candidate=n;break;}
    }
    if(!candidate)candidate=order[order.length-1];
    if(candidate!==current)setCurrent(candidate);
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
    const t=Math.max(0,Math.min(1,(v-YROOT)/UNIT));
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
  let sx=0,sy=0,tracking=false;
  read.addEventListener("touchstart",e=>{if(e.touches.length===1){sx=e.touches[0].clientX;sy=e.touches[0].clientY;tracking=true;}},{passive:true});
  read.addEventListener("touchend",e=>{if(!tracking)return;tracking=false;const t=e.changedTouches[0],dx=t.clientX-sx,dy=t.clientY-sy;if(Math.abs(dx)>64&&Math.abs(dy)<44)step(dx<0?1:-1);},{passive:true});
  const h=hashNumber();if(byNum.has(h))current=h;
  paint();if(byNum.has(h))requestAnimationFrame(()=>go(h,"auto"));
  addressWindow.addEventListener("hashchange",()=>{const n=hashNumber();if(byNum.has(n))setCurrent(n,false,true,"auto");});
})().catch(err=>{const read=document.getElementById("read");if(read)read.textContent="Klarte ikkje laste FORMLÆRE.";console.error(err);});
