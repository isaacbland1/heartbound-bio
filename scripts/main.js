async function loadJSON(p){const r=await fetch(p,{cache:"no-store"});if(!r.ok)throw new Error(`Failed ${p}: ${r.status}`);return r.json()}
function el(t,a={},c=[]){const n=document.createElement(t);Object.entries(a).forEach(([k,v])=>{if(k==="class")n.className=v;else if(k==="text")n.textContent=v;else n.setAttribute(k,v)});c.forEach(x=>n.appendChild(x));return n}
function resolvePath(p){try{return new URL(p,document.baseURI).toString()}catch(e){return p||""}}
function imgEl(src,alt){
  const i=document.createElement("img");
  const s=resolvePath(src||"assets/placeholder.svg");
  const v=Date.now();
  i.src=s+(s.includes("?")?"&":"?")+"v="+v;
  i.alt=alt||"Item";
  i.onerror=()=>{const f=resolvePath("assets/placeholder.svg");i.src=f+(f.includes("?")?"&":"?")+"v="+v};
  return i
}
function card({image,name,desc,url,cta="Open"}){
  const link=el("a",{href:url,target:"_blank",rel:"noopener",class:"btn btn-primary",text:cta});
  const img=imgEl(image,name);
  const a=el("a",{href:resolvePath(image||"assets/placeholder.svg"),target:"_blank",rel:"noopener",class:"img-src",text:"Image link"});
  return el("div",{class:"card"},[
    img,
    el("div",{class:"meta"},[
      el("h3",{text:name||"Untitled"}),
      el("p",{text:desc||""}),
      a
    ]),
    el("div",{class:"actions"},[link])
  ])
}
(async()=>{try{
  const [cfg,aff,svc]=await Promise.all([loadJSON("config.json"),loadJSON("affiliates.json"),loadJSON("services.json")]);
  const brand=document.getElementById("brand"),tag=document.getElementById("tagline"),logo=document.getElementById("logo"),link=document.getElementById("main-site-link"),disc=document.getElementById("disclaimer");
  brand.textContent=cfg.brandName||"Heartbound Journeys";tag.textContent=cfg.brandTagline||"";disc.textContent=cfg.disclaimer||"";
  if(cfg.logo){logo.src=resolvePath(cfg.logo);logo.style.display="block"}
  if(cfg.themeColor){document.documentElement.style.setProperty("--brand",cfg.themeColor)}
  link.href=cfg.mainSiteUrl||"#";
  const af=document.getElementById("affiliates");aff.forEach(i=>af.appendChild(card({image:i.image,name:i.name,desc:i.desc,url:i.url,cta:"View"})));
  const sv=document.getElementById("services");svc.forEach(s=>sv.appendChild(card({image:s.image,name:s.name,desc:s.desc,url:s.url,cta:"Book / Learn More"})));
}catch(e){console.error(e);alert("Error loading content. Reload.")}})();
