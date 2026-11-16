"use strict";
fetch("../data/countries.json",{cache:"no-cache"}).then(r=>{if(!r.ok)throw Error("No statistics");return r.json()}).then(d=>{
const vals={aboutCountries:d.totalCountries,aboutBooks:d.totalBooks,aboutNights:d.airportNights};
for(const [id,value] of Object.entries(vals)){const e=document.getElementById(id);if(e&&Number.isFinite(Number(value)))e.textContent=Number(value).toLocaleString("en-US")}
}).catch(()=>{/* Use documented fallback values if offline. */});

/* Goal item titles remain in the original archive language; interactive UI is localized. */
(() => {
  const target = document.getElementById("goalBoards");
  if (!target) return;
  const escapeHtml = value => String(value ?? "").replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
  const statuses = ["todo","in_progress","completed"];
  const translations = {
    "en": {
      names: ["University Years","Before 30"],
      descriptions: ["Goals set during my university years","Milestones I want to reach before thirty"],
      states: ["To do","In progress","Completed"],
      count: (done,total) => done+" of "+total+" completed",
      empty: "Nothing here yet.", loading:"Loading the goals archive…", error:"The goals archive could not be loaded."
    },
    "ko": {
      names: ["대학 시절 목표","서른 전 목표"],
      descriptions: ["대학 시절에 세운 목표","서른 살이 되기 전 이루고 싶은 목표"],
      states: ["할 일","진행 중","완료"],
      count: (done,total) => total+"개 중 "+done+"개 완료",
      empty: "아직 항목이 없습니다.", loading:"목표 목록을 불러오는 중…", error:"목표 목록을 불러올 수 없습니다."
    },
    "zh-Hans": {
      names: ["大学时期的目标","三十岁前的目标"],
      descriptions: ["大学时期制定的目标","希望在三十岁前实现的目标"],
      states: ["待完成","进行中","已完成"],
      count: (done,total) => "已完成 "+done+" / "+total,
      empty: "暂无项目。", loading:"正在加载目标清单…", error:"无法加载目标清单。"
    },
    "es": {
      names: ["Años universitarios","Antes de los 30"],
      descriptions: ["Objetivos fijados durante la universidad","Metas que quiero cumplir antes de los treinta"],
      states: ["Pendiente","En curso","Completado"],
      count: (done,total) => done+" de "+total+" completados",
      empty: "Todavía no hay objetivos.", loading:"Cargando objetivos…", error:"No se pudo cargar la lista de objetivos."
    },
    "zh-Hant": {
      names: ["大學時期的目標","三十歲前的目標"],
      descriptions: ["大學時期訂下的目標","希望在三十歲前實現的目標"],
      states: ["待完成","進行中","已完成"],
      count: (done,total) => "已完成 "+done+" / "+total,
      empty: "目前沒有項目。", loading:"正在載入目標清單…", error:"無法載入目標清單。"
    },
    "fr": {
      names: ["Années universitaires","Avant 30 ans"],
      descriptions: ["Objectifs fixés pendant mes études","Étapes que je souhaite franchir avant trente ans"],
      states: ["À faire","En cours","Terminé"],
      count: (done,total) => done+" sur "+total+" terminés",
      empty: "Aucun objectif pour le moment.", loading:"Chargement des objectifs…", error:"Impossible de charger les objectifs."
    },
    "de": {
      names: ["Studienzeit","Vor dem 30. Geburtstag"],
      descriptions: ["Ziele aus meiner Studienzeit","Meilensteine, die ich vor dreißig erreichen möchte"],
      states: ["Offen","In Arbeit","Erledigt"],
      count: (done,total) => done+" von "+total+" erledigt",
      empty: "Noch keine Einträge.", loading:"Ziele werden geladen…", error:"Die Zielliste konnte nicht geladen werden."
    }
  };
  let sets = null;
  let failed = false;
  const language = () => {
    const lang = window.PortfolioI18n?.getLanguage?.() || document.documentElement.lang || "en";
    return translations[lang] ? lang : "en";
  };
  function render() {
    const t=translations[language()];
    if (!sets) {
      target.innerHTML='<p class="goal-loading">'+escapeHtml(failed?t.error:t.loading)+'</p>';
      return;
    }
    const openSets=new Set(Array.from(target.querySelectorAll("details.goal-set[open]"), node=>node.dataset.goalSet));
    target.innerHTML=sets.map((set,index)=>{
      const items=Array.isArray(set.items)?set.items.filter(x=>x.title&&statuses.includes(x.status)):[];
      const done=items.filter(x=>x.status==="completed").length;
      const pct=items.length?Math.round(done/items.length*100):0;
      const title=t.names[index] || set.name;
      const description=t.descriptions[index] || set.description;
      const columns=statuses.map((status,statusIndex)=>{
        const group=items.filter(x=>x.status===status);
        const label=t.states[statusIndex];
        const cards=group.length ? group.map(x=>'<div class="goal-item">'+escapeHtml(x.title)+'</div>').join("") :
          '<p class="goal-empty">'+escapeHtml(t.empty)+'</p>';
        return '<section class="goal-column" data-status="'+status+'" aria-label="'+escapeHtml(label)+'">'+
          '<header><strong>'+escapeHtml(label)+'</strong><span>'+group.length+'</span></header>'+
          '<div class="goal-column-body">'+cards+'</div></section>';
      }).join("");
      return '<details class="goal-set" data-goal-set="'+escapeHtml(set.id)+'"'+(openSets.has(set.id)?' open':'')+'>'+
        '<summary><span><strong class="goal-set-title">'+escapeHtml(title)+'</strong>'+
        '<small class="goal-set-desc">'+escapeHtml(description)+'</small></span>'+
        '<span class="goal-set-tally"><b>'+pct+'%</b><small>'+escapeHtml(t.count(done,items.length))+'</small>'+
        '<span class="goal-meter" aria-hidden="true"><span style="width:'+pct+'%"></span></span></span>'+
        '<span class="goal-toggle" aria-hidden="true">+</span></summary>'+
        '<div class="goal-board">'+columns+'</div></details>';
    }).join("");
  }
  document.addEventListener("portfolio:language", render);
  fetch("./goals.json",{cache:"no-cache"}).then(response=>{
    if(!response.ok)throw Error("Goals archive unavailable");
    return response.json();
  }).then(data=>{
    if(!Array.isArray(data.sets))throw Error("Invalid goals archive");
    sets=data.sets;
    render();
  }).catch(()=>{failed=true;render();});
})();
