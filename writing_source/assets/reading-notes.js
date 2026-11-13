"use strict";
// A book-reflection collection in Writing. The Reading page keeps completion statistics only.
(async function(){
 const host=document.getElementById("wr-archive"),search=document.getElementById("wr-search"),filter=document.getElementById("wr-filter"),empty=document.getElementById("wr-empty");
 if(!host||!search||!filter||!empty)return;
 const make=(tag,cls,value)=>{const el=document.createElement(tag);if(cls)el.className=cls;if(value!==undefined)el.textContent=value;return el;};
 try{
  const res=await fetch("../assets/reading-notes.json",{cache:"no-cache"});
  if(!res.ok)throw new Error("Readings HTTP "+res.status);
  const data=await res.json();
  if(!Array.isArray(data.notes))throw new Error("Invalid Readings data");
  const notes=data.notes.filter(x=>x&&x.id&&x.title&&x.author&&x.date&&x.brunch_url);
  const monthName=month=>{
   const d=new Date(month+"-01T12:00:00");
   return isNaN(d.getTime())?month:d.toLocaleDateString("en-US",{year:"numeric",month:"long"});
  };
  const draw=()=>{
   const q=search.value.trim().toLocaleLowerCase(),mode=filter.value;
   const selected=notes.filter(n=>(mode!=="quoted"||!!n.quote)&&(mode!=="pending"||!n.reflection)&&(!q||[n.title,n.author,n.reflection,n.quote].join(" ").toLocaleLowerCase().includes(q)));
   const groups=new Map();
   for(const n of selected){const key=n.date.slice(0,7);if(!groups.has(key))groups.set(key,[]);groups.get(key).push(n);}
   const fragment=document.createDocumentFragment();
   [...groups].sort((a,b)=>b[0].localeCompare(a[0])).forEach(([month,entries],i)=>{
    const section=make("details","wr-month");section.open=!!q||i===0;
    const heading=make("summary");
    heading.append(make("span","wr-month-name",monthName(month)),make("span","wr-month-count",entries.length+" "+(entries.length===1?"entry":"entries")),make("span","wr-month-plus","+"));section.append(heading);
    const body=make("div","wr-month-body");
    entries.sort((a,b)=>b.date.localeCompare(a.date)||b.id.localeCompare(a.id)).forEach(n=>{
     const card=make("details","wr-note");card.open=!!q;
     const title=make("summary");
     const titlePart=make("span","wr-note-head");
     titlePart.append(make("span","wr-note-title",n.title),make("span","wr-note-author",n.author));
     title.append(titlePart,make("time","wr-note-date",n.date));card.append(title);
     const content=make("div","wr-note-content");
     if(n.quote){
       content.append(make("blockquote","wr-quote",n.quote));
       content.append(make("p","wr-source-label",n.verification==="Notion exact match"?"NOTION HIGHLIGHT · MATCHED":"SELECTED PASSAGE"));
     }
     content.append(n.reflection?make("p","wr-reflection",n.reflection):make("p","wr-pending","Reflection not yet transcribed. Read the original Brunch post."));
     if(n.brunch_url.startsWith("https://brunch.co.kr/")){
       const link=make("a","wr-link","Read original on Brunch ↗");
       link.href=n.brunch_url;link.target="_blank";link.rel="noopener noreferrer";content.append(link);
     }
     card.append(content);body.append(card);
    });
    section.append(body);fragment.append(section);
   });
   host.replaceChildren(fragment);empty.hidden=selected.length!==0;
  };
  search.addEventListener("input",draw);filter.addEventListener("change",draw);draw();
 }catch(e){
  console.error("Writing Readings unavailable",e);
  host.replaceChildren(make("p","wr-status","The reflections archive is temporarily unavailable."));
 }
})();
