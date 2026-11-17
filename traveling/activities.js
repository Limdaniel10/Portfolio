"use strict";
/* Localized activity controls; original personal place names remain in their source language. */
(() => {
  const esc = value => String(value ?? "").replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
  const locales = {
    "en":{
      trek:["Mountain / trail","Country","Date","Summit / landmark elevation"],
      dive:["Date","Dive site / country","Max depth","Duration"],
      surf:["Location","Country","Month"],
      counts:["hikes","logged dives","sessions"],
      basis:{viewpoint:"Viewpoint","highest lake":"Highest lake","approximate summit":"Approx. summit","highest massif peak (Tsetsee Gun)":"Tsetsee Gun summit"},
      record:"Personal Record",truncated:"Name truncated in the original logbook",
      empty:["No trekking records have been added.","Dive-log details are pending.","No surfing records have been added."],
      unavailable:"This archive is temporarily unavailable.",pending:"Dive logs pending"
    },
    "ko":{
      trek:["산 / 트레일","국가","날짜","산 정상 / 명소 고도"],
      dive:["날짜","다이빙 사이트 / 국가","최대 수심","다이빙 시간"],
      surf:["장소","국가","월"],
      counts:["회 트레킹","회 다이빙 기록","회 서핑 기록"],
      basis:{viewpoint:"전망대","highest lake":"최고 고도 호수","approximate summit":"정상 고도 약","highest massif peak (Tsetsee Gun)":"체체군산 정상"},
      record:"개인 최고 기록",truncated:"원본 로그북에서 이름 일부가 잘림",
      empty:["트레킹 기록이 없습니다.","다이빙 로그 세부 정보가 아직 없습니다.","서핑 기록이 없습니다."],
      unavailable:"현재 활동 기록을 불러올 수 없습니다.",pending:"다이빙 로그 입력 대기"
    },
    "zh-Hans":{
      trek:["山峰 / 徒步路线","国家","日期","山峰 / 景点海拔"],
      dive:["日期","潜点 / 国家","最大深度","潜水时长"],
      surf:["地点","国家","月份"],
      counts:["次徒步","次潜水记录","次冲浪记录"],
      basis:{viewpoint:"观景台","highest lake":"最高湖泊","approximate summit":"约海拔","highest massif peak (Tsetsee Gun)":"策策贡峰顶"},
      record:"个人最高纪录",truncated:"原始潜水日志中的名称未完整显示",
      empty:["暂无徒步记录。","潜水日志详情尚待录入。","暂无冲浪记录。"],
      unavailable:"暂时无法加载活动档案。",pending:"待录入潜水日志"
    },
    "es":{
      trek:["Montaña / sendero","País","Fecha","Altitud de cima / lugar"],
      dive:["Fecha","Sitio de buceo / país","Profundidad máxima","Duración"],
      surf:["Lugar","País","Mes"],
      counts:["caminatas","inmersiones registradas","sesiones de surf"],
      basis:{viewpoint:"Mirador","highest lake":"Lago más alto","approximate summit":"Cima aprox.","highest massif peak (Tsetsee Gun)":"Cima Tsetsee Gun"},
      record:"Récord personal",truncated:"Nombre recortado en el registro original",
      empty:["Todavía no hay caminatas registradas.","Faltan los detalles del registro de buceo.","Todavía no hay sesiones de surf."],
      unavailable:"Este archivo no está disponible temporalmente.",pending:"Registros de buceo pendientes"
    },
    "zh-Hant":{
      trek:["山峰 / 健行路線","國家","日期","山峰 / 景點海拔"],
      dive:["日期","潛點 / 國家","最大深度","潛水時間"],
      surf:["地點","國家","月份"],
      counts:["次健行","次潛水紀錄","次衝浪紀錄"],
      basis:{viewpoint:"觀景臺","highest lake":"最高湖泊","approximate summit":"約海拔","highest massif peak (Tsetsee Gun)":"策策貢峰頂"},
      record:"個人最高紀錄",truncated:"原始潛水日誌中的名稱未完整顯示",
      empty:["尚無健行紀錄。","潛水日誌詳細資料尚待輸入。","尚無衝浪紀錄。"],
      unavailable:"目前無法載入活動紀錄。",pending:"潛水日誌待輸入"
    },
    "fr":{
      trek:["Montagne / sentier","Pays","Date","Altitude du sommet / site"],
      dive:["Date","Site de plongée / pays","Profondeur maximale","Durée"],
      surf:["Lieu","Pays","Mois"],
      counts:["randonnées","plongées enregistrées","sessions de surf"],
      basis:{viewpoint:"Belvédère","highest lake":"Lac le plus élevé","approximate summit":"Sommet env.","highest massif peak (Tsetsee Gun)":"Sommet Tsetsee Gun"},
      record:"Record personnel",truncated:"Nom tronqué dans le carnet de plongée d'origine",
      empty:["Aucune randonnée enregistrée.","Les détails des plongées restent à ajouter.","Aucune séance de surf enregistrée."],
      unavailable:"Les archives sont temporairement indisponibles.",pending:"Carnet de plongée à compléter"
    },
    "de":{
      trek:["Berg / Wanderweg","Land","Datum","Gipfel- / Ortshöhe"],
      dive:["Datum","Tauchplatz / Land","Maximale Tiefe","Dauer"],
      surf:["Ort","Land","Monat"],
      counts:["Wanderungen","protokollierte Tauchgänge","Surf-Sessions"],
      basis:{viewpoint:"Aussichtspunkt","highest lake":"Höchster See","approximate summit":"Gipfel ca.","highest massif peak (Tsetsee Gun)":"Tsetsee-Gun-Gipfel"},
      record:"Persönlicher Rekord",truncated:"Name im ursprünglichen Logbuch abgeschnitten",
      empty:["Noch keine Wanderungen eingetragen.","Tauchprotokolle stehen noch aus.","Noch keine Surf-Sessions eingetragen."],
      unavailable:"Dieses Archiv ist vorübergehend nicht verfügbar.",pending:"Tauchprotokolle ausstehend"
    }
  };
  const lang = () => {
    const value=window.PortfolioI18n?.getLanguage?.() || document.documentElement.lang || "en";
    return locales[value] ? value : "en";
  };
  const fmtDate = (raw, currentLang) => {
    const match=String(raw||"").match(/^(\d{4})-(\d{2})(?:-(\d{2}))?$/);
    if(!match) return "—";
    const locale=currentLang==="zh-Hans"?"zh-CN":currentLang==="zh-Hant"?"zh-TW":currentLang;
    return new Intl.DateTimeFormat(locale,{year:"numeric",month:"short",...(match[3]?{day:"numeric"}:{}),timeZone:"UTC"})
      .format(new Date(Date.UTC(Number(match[1]),Number(match[2])-1,Number(match[3]||"1"))));
  };
  const table = (headers,body) => '<div class="activity-table-wrap"><table class="activity-table"><thead><tr>'+
    headers.map(h=>'<th scope="col">'+esc(h)+'</th>').join("")+
    '</tr></thead><tbody>'+body+'</tbody></table></div>';
  const pending = text => '<p class="activity-pending">'+esc(text)+'</p>';
  let archive=null,failed=false;
  function render() {
    const currentLang=lang(),t=locales[currentLang];
    if (!archive) {
      if(failed)["trekkingRecords","scubaRecords","surfingRecords"].forEach(id=>{
        document.getElementById(id).innerHTML=pending(t.unavailable);
      });
      return;
    }
    const hikes=Array.isArray(archive.trekking)?archive.trekking:[];
    const dives=Array.isArray(archive.scuba)?archive.scuba:[];
    const surfs=Array.isArray(archive.surfing)?archive.surfing:[];
    document.getElementById("trekCount").textContent=currentLang==="ko"?hikes.length+t.counts[0]:hikes.length+" "+t.counts[0];
    document.getElementById("scubaCount").textContent=dives.length?(currentLang==="ko"?dives.length+t.counts[1]:dives.length+" "+t.counts[1]):t.pending;
    document.getElementById("surfCount").textContent=currentLang==="ko"?surfs.length+t.counts[2]:surfs.length+" "+t.counts[2];
    document.getElementById("trekkingRecords").innerHTML=hikes.length?table(t.trek,
      [...hikes].sort((a,b)=>String(a.date).localeCompare(String(b.date))).map(x=>{
        const height=Number.isFinite(x.elevationM)?Number(x.elevationM).toLocaleString(currentLang)+" m":"—";
        const personal=Boolean(x.personalRecord);
        const basis=personal?t.record:(t.basis[x.elevationBasis]||"");
        return '<tr'+(personal?' class="activity-record"':'')+'><td>'+esc(x.name)+'</td><td class="activity-nowrap">'+esc(x.country)+'</td>'+
          '<td class="activity-nowrap">'+esc(fmtDate(x.date,currentLang))+'</td>'+
          '<td class="activity-elev">'+esc(height)+(basis?'<small>'+esc(basis)+'</small>':'')+'</td></tr>';
      }).join("")):pending(t.empty[0]);
    document.getElementById("scubaRecords").innerHTML=dives.length?table(t.dive,
      [...dives].sort((a,b)=>String(a.date).localeCompare(String(b.date))).map(x=>
        '<tr><td class="activity-nowrap">'+esc(fmtDate(x.date,currentLang))+'</td><td>'+esc(x.site||"—")+
        ' <span class="activity-muted">· '+esc(x.country||"—")+'</span>'+
        (x.siteNameTruncated?'<small class="activity-truncated">'+esc(t.truncated)+'</small>':'')+'</td>'+
        '<td class="activity-nowrap">'+(Number.isFinite(x.depthM)?esc(x.depthM)+" m":"—")+'</td>'+
        '<td class="activity-nowrap">'+(Number.isFinite(x.durationMin)?esc(x.durationMin)+" min":"—")+'</td></tr>'
      ).join("")):pending(t.empty[1]);
    document.getElementById("surfingRecords").innerHTML=surfs.length?table(t.surf,
      [...surfs].sort((a,b)=>String(a.date).localeCompare(String(b.date))).map(x=>
        '<tr><td>'+esc(x.place)+'</td><td>'+esc(x.country)+'</td>'+
        '<td class="activity-nowrap">'+esc(fmtDate(x.date,currentLang))+'</td></tr>'
      ).join("")):pending(t.empty[2]);
  }
  document.addEventListener("portfolio:language",render);
  fetch("./activities.json",{cache:"no-cache"}).then(r=>{
    if(!r.ok)throw Error("Activity archive unavailable");
    return r.json();
  }).then(data=>{archive=data;render();}).catch(()=>{failed=true;render();});
})();
