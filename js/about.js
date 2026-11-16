"use strict";
fetch("../data/countries.json",{cache:"no-cache"}).then(r=>{if(!r.ok)throw Error("No statistics");return r.json()}).then(d=>{
const vals={aboutCountries:d.totalCountries,aboutBooks:d.totalBooks,aboutNights:d.airportNights};
for(const [id,value] of Object.entries(vals)){const e=document.getElementById(id);if(e&&Number.isFinite(Number(value)))e.textContent=Number(value).toLocaleString("en-US")}
}).catch(()=>{/* Use documented fallback values if offline. */});

/* The source lists are checked into About/goals.json. Update there to change the board. */
(() => {
  const target = document.getElementById("goalBoards");
  if (!target) return;
  const esc = value => String(value ?? "").replace(/[&<>"']/g, char => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[char]));
  const labels = {todo:"To do", in_progress:"In progress",completed:"Completed"};
  const statuses = ["todo","in_progress","completed"];
  function renderSet(set) {
    const items = Array.isArray(set.items) ? set.items.filter(x=>x.title && statuses.includes(x.status)) : [];
    const done = items.filter(x=>x.status==="completed").length;
    const percentage = items.length ? Math.round(done/items.length*100) : 0;
    const columns = statuses.map(status => {
      const group=items.filter(x=>x.status===status);
      return `<section class="goal-column" data-status="${status}" aria-label="${labels[status]} goals"><header><strong>${labels[status]}</strong><span>${group.length}</span></header><div class="goal-column-body">${group.length ? group.map(x=>`<div class="goal-item">${esc(x.title)}</div>`).join("") : '<p class="goal-empty">Nothing here yet.</p>'}</div></section>`;
    }).join("");
    return `<details class="goal-set"><summary><span><strong class="goal-set-title">${esc(set.name)}</strong><small class="goal-set-desc">${esc(set.description)}</small></span><span class="goal-set-tally"><b>${percentage}%</b><small>${done} of ${items.length} completed</small><span class="goal-meter" aria-hidden="true"><span style="width:${percentage}%"></span></span></span><span class="goal-toggle" aria-hidden="true">+</span></summary><div class="goal-board">${columns}</div></details>`;
  }
  fetch("./goals.json",{cache:"no-cache"}).then(response=>{
    if(!response.ok) throw Error("Goals archive unavailable");
    return response.json();
  }).then(data=>{
    if(!Array.isArray(data.sets)) throw Error("Invalid goals archive");
    target.innerHTML=data.sets.map(renderSet).join("");
  }).catch(()=>{target.innerHTML='<p class="goal-loading">The goals archive could not be loaded.</p>';});
})();
