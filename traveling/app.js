'use strict';
const D=window.TRAVEL,$=s=>document.querySelector(s),esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
let year=null,month=null,cumulative=true,tab='abroad',listAll=true;const enabled=new Set(['Plane','Train','Car','Bus','Ferry']);
const regionName=new Intl.DisplayNames(['en'],{type:'region'});const cname=iso=>{try{return regionName.of(iso)||iso}catch{return iso}};const flag=iso=>/^[A-Z]{2}$/.test(iso)?String.fromCodePoint(...[...iso].map(c=>127397+c.charCodeAt(0))):'◦';
const years=[...new Set([...D.visits.map(x=>x.year),...D.flights.map(x=>x.year)])].filter(Boolean).sort((a,b)=>a-b);
const monthName=m=>new Date(2020,m-1,1).toLocaleString('en',{month:'long'});const byPlace=new Map();D.visits.forEach(v=>{if(!byPlace.has(v.place_id))byPlace.set(v.place_id,[]);byPlace.get(v.place_id).push(v)});
const map=L.map('map',{minZoom:1,maxZoom:12,zoomSnap:.25,scrollWheelZoom:false,preferCanvas:true,worldCopyJump:true}).setView([20,10],1.5);L.geoJSON(WORLD,{style:{color:'#bdcfdc',weight:.65,fillColor:'#f4f8fb',fillOpacity:1},interactive:false}).addTo(map);map.attributionControl.setPrefix(false);map.attributionControl.addAttribution('GeoNames · OurAirports · Natural Earth · OSM contributors');const layers=L.layerGroup().addTo(map);const pinIndex=new Map();
function match(y,ms=[],cum=cumulative){
  if(!year)return true;
  if(!y && !ms.length)return false;
  // A trip starting in December may continue into January: use each recorded
  // YYYY-MM month instead of requiring v.year to match the selected year.
  if(month){
    const key=`${year}-${String(month).padStart(2,'0')}`;
    if(ms.length)return cum?ms.some(m=>m<=key):ms.includes(key);
    return false;
  }
  if(cum)return y<=year || ms.some(m=>Number(m.slice(0,4))<=year);
  return y===year || ms.some(m=>Number(m.slice(0,4))===year);
}
function current(y,ms=[]){return year?match(y,ms,false):true}
function visiblePlaces(cum=cumulative){return D.places.filter(p=>!year||(byPlace.get(p.id)||[]).some(v=>match(v.year,v.months||[],cum))||(!month&&p.first_visit_year&&(cum?p.first_visit_year<=year:p.first_visit_year===year)))}
function select(y,m=null){year=y;month=m;tab='abroad';if($('#korea').open){$('#korea').open=false;$('#abroad').open=true;}$('#abroadBody').append($('#placeExplorer'));renderTimeline();render();}
function renderTimeline(){const target=$('#years');const scroll=target.scrollTop;target.innerHTML=years.map(y=>{const ms=[...new Set([...D.visits,...D.flights].filter(v=>v.year===y&&(v.months||[]).length===1).map(v=>+v.months[0].slice(5)))].sort((a,b)=>a-b);return `<details class="year ${year===y?'selected':''}" ${year===y?'open':''}><summary data-year="${y}"><span>${y}</span><small>${year===y?'−':'+'}</small></summary><div class="months"><button data-year="${y}" class="${year===y&&!month?'active':''}">Full year</button>${ms.map(m=>`<button data-year="${y}" data-month="${m}" class="${year===y&&month===m?'active':''}">${String(m).padStart(2,'0')} · ${monthName(m).slice(0,3)}</button>`).join('')}</div></details>`}).join('');target.scrollTop=scroll;target.querySelectorAll('[data-year]').forEach(el=>el.onclick=e=>{e.preventDefault();select(+el.dataset.year,el.dataset.month?+el.dataset.month:null)});}
function renderMap(){layers.clearLayers();pinIndex.clear();const korea=tab==='korea';const points=korea?D.domestic_places:visiblePlaces();let routes=0;const colors={Plane:'#377fb3',Train:'#12496c',Car:'#7c94aa',Bus:'#956d35',Ferry:'#2397af'};
if(!korea)D.geometry.features.filter(f=>['flight','surface_route'].includes(f.properties.kind)).forEach(f=>{const p=f.properties;if(!enabled.has(p.mode)||!match(p.year,p.months||[]))return;const active=current(p.year,p.months||[]);L.geoJSON(f,{style:{color:colors[p.mode],weight:active?(p.mode==='Train'?2.8:1.6):.65,opacity:active?(p.mode==='Train'?.9:.6):.13,dashArray:p.mode==='Ferry'?'3 5':p.mode==='Car'||p.mode==='Bus'?'2 3':null}}).bindPopup(`<strong>${esc(p.from||p.from_name)} → ${esc(p.to||p.to_name)}</strong><p>${esc(p.mode)} · ${p.year||'Year not recorded'}${(p.months||[]).length===1?' · '+p.months[0]:''}<br>Schematic connection</p>`).addTo(layers);routes++});
points.forEach(p=>{const active=korea||!year||(byPlace.get(p.id)||[]).some(v=>current(v.year,v.months||[]));const visits=byPlace.get(p.id)||[];const dates=korea?'Visited · no date filter':[...new Set(visits.map(v=>v.months?.length===1?v.months[0]:v.year||'Date not recorded'))].join(' / ')||'Date not recorded';const marker=L.circleMarker([p.latitude,p.longitude],{radius:active?3.2:2,color:active?'#1a5f94':'#82a7c4',weight:.8,fillColor:active?'#2b75ac':'#9ab9d0',fillOpacity:active?.9:.5}).bindPopup(`<strong>${esc(p.name)}</strong><p>${esc(cname(p.country_iso2))} · ${esc(p.type.replaceAll('_',' '))}<br>${esc(dates)}</p>`).addTo(layers);pinIndex.set(p.id,marker)});
if($('#nights').checked&&!korea)D.airport_overnights.filter(n=>match(n.year,[n.date.slice(0,7)])).forEach(n=>L.circleMarker([n.latitude,n.longitude],{radius:6,color:'#aa773d',weight:1,fillColor:'#ffe4ba',fillOpacity:.9}).bindPopup(`<strong>${esc(n.airport_iata)} · Airport night</strong><p>${esc(n.place)}<br>${n.date} · 1 night</p>`).addTo(layers));
$('#mapCount').textContent=`${points.length} places${korea?'':' · '+routes+' routes'}`;}
function focusPlace(id){if(!pinIndex.has(id) && year)select(null);const marker=pinIndex.get(id);if(marker){map.flyTo(marker.getLatLng(),6,{duration:.8});marker.openPopup();$('#atlas').scrollIntoView({behavior:'smooth'})}}
function renderList(){const korea=tab==='korea';const query=$('#search').value.trim().toLowerCase();const points=korea?D.domestic_places:(listAll?D.places:visiblePlaces(false));const groups=new Map();
if(!korea){let codes=(listAll||!year)?D.countries.filter(c=>c.iso2!=='KR').map(c=>c.iso2):D.stays.filter(s=>{if(!s.start_date)return false;const start=month?`${year}-${String(month).padStart(2,'0')}`:String(year);const cut=month?7:4;return s.start_date.slice(0,cut)<=start&&(!s.end_date||s.end_date.slice(0,cut)>=start)}).map(s=>s.country_iso2).filter(c=>c!=='KR');codes.forEach(c=>groups.set(c,[]));}
points.forEach(p=>{let key=korea?(p.region||'Other places'):p.country_iso2;if(!groups.has(key))groups.set(key,[]);groups.get(key).push(p)});
const sorted=[...groups].sort((a,b)=>(korea?a[0]:cname(a[0])).localeCompare(korea?b[0]:cname(b[0])));let html='';sorted.forEach(([key,ps])=>{const name=korea?key:cname(key);const matches=name.toLowerCase().includes(query)?ps:ps.filter(p=>p.name.toLowerCase().includes(query));if(query&&!name.toLowerCase().includes(query)&&!matches.length)return;const territory=!korea&&D.countries.find(c=>c.iso2===key)?.category==='region_or_territory';html+=`<details class="country" ${query?'open':''}><summary><span class="flag">${korea?'◦':flag(key)}</span><b>${esc(name)}${territory?' <small>territory / region</small>':''}</b><small>${matches.length?`${matches.length} ${matches.length===1?'place':'places'}`:'Visit recorded'}</small><em>+</em></summary><div class="placebuttons">${matches.length?matches.sort((a,b)=>a.name.localeCompare(b.name)).map(p=>`<button data-place="${p.id}">${esc(p.name)}</button>`).join(''):'<span class="small">Country visit recorded; no place resolved for this period.</span>'}</div></details>`});$('#countryList').innerHTML=html||'<p class="empty">No matching places in this period.</p>';$('#countryList').querySelectorAll('[data-place]').forEach(b=>b.onclick=()=>focusPlace(b.dataset.place));$('#listPeriod').textContent=korea?'Undated · all visits':(listAll||!year)?`All years · ${D.countries.filter(x=>x.count_in_195).length} countries`:(month?monthName(month)+' ':'')+year;$('#listHint').textContent=korea?`${D.domestic_places.length} visited places in Korea · independent of the timeline`:(listAll||!year)?`${groups.size} countries and territories abroad · ${D.countries.filter(x=>x.count_in_195).length} countries counted in total including Korea · expand to explore places`:`${groups.size} countries and territories in this period · expand to explore places`;
$('#listAll').classList.toggle('active',listAll);$('#listYear').classList.toggle('active',!listAll);$('#listAll').setAttribute('aria-pressed',String(listAll));$('#listYear').setAttribute('aria-pressed',String(!listAll));$('#listYear').disabled=!year;$('#listYear').textContent=year?`${year} only`:'Selected year';$('#abroadCount').textContent=(listAll||!year)?`${D.countries.filter(x=>x.count_in_195).length} countries + territories · all visits`:`${groups.size} destinations · ${year}`;}
function render(){const title=year?(month?monthName(month)+' ':'')+year:'All years';$('#period').textContent=tab==='korea'?'Korea':title;$('#scope').textContent=tab==='korea'?`${D.domestic_places.length} places · beyond the timeline`:!year?'The complete journey':cumulative?'Journeys accumulated through this chapter':'Only this chapter';renderMap();renderList();}
$('#allYears').onclick=()=>select(null);$('#cumulative').onclick=()=>setMode(true);$('#periodOnly').onclick=()=>setMode(false);function setMode(value){cumulative=value;$('#cumulative').classList.toggle('active',value);$('#periodOnly').classList.toggle('active',!value);$('#cumulative').setAttribute('aria-pressed',value);$('#periodOnly').setAttribute('aria-pressed',!value);render()}
function setTab(t){tab=t;$('#search').value='';$('#'+t+'Body').append($('#placeExplorer'));render();map.flyTo(t==='korea'?[36.2,127.7]:[20,10],t==='korea'?6:1.5,{duration:.7});}
['abroad','korea'].forEach(t=>$('#'+t).addEventListener('toggle',()=>{if(!$('#'+t).open)return;$('#'+(t==='abroad'?'korea':'abroad')).open=false;setTab(t);}));
$('#listAll').onclick=()=>{listAll=true;renderList()};$('#listYear').onclick=()=>{if(!year)return;listAll=false;renderList()};$('#search').oninput=renderList;$('#resetMap').onclick=()=>map.flyTo(tab==='korea'?[36.2,127.7]:[20,10],tab==='korea'?6:1.5);document.querySelectorAll('[data-mode]').forEach(e=>e.onchange=()=>{e.checked?enabled.add(e.dataset.mode):enabled.delete(e.dataset.mode);renderMap()});$('#nights').onchange=renderMap;
function focusSiberianRail(){select(2026);if(!enabled.has('Train')){enabled.add('Train');const b=document.querySelector('[data-mode="Train"]');if(b)b.checked=true;renderMap()}map.fitBounds([[43,29],[60,133]],{padding:[24,24],maxZoom:5});$('#atlas').scrollIntoView({behavior:'smooth'})}
const stories=[
  [
    "50 countries in one year.",
    "One year, fifty countries.",
    "I visited 50 countries in a single year—a chapter of travel that took me across borders again and again.",
    null
  ],
  [
    "45 nights at airports.",
    "Quito, London, Istanbul and beyond.",
    "Between 2022 and 2026, I spent 45 nights at airports. Together they form another itinerary, recorded alongside the journeys. Turn on Airport nights in the map to explore them.",
    null
  ],
  [
    "Across Siberia, by rail.",
    "Saint Petersburg to Irkutsk, then Vladivostok.",
    "I travelled from Saint Petersburg to Irkutsk by train, then continued by rail to Vladivostok. The round trip to Khuzhir was overland.",
    2026
  ],
  [
    "Three days. Ninety kilometres.",
    "On foot in El Chaltén, Patagonia.",
    "I walked 90 kilometres over three days in El Chaltén, along the mountain paths around Fitz Roy. The journey became part of my travel writing.",
    2025
  ],
  [
    "22 hours. Three countries.",
    "A border crossing that took nearly a day.",
    "One journey took 22 hours and crossed three countries. The time spent getting from one place to another became a story of its own.",
    null
  ],
  [
    "Fossil hunting in the Arctic.",
    "A different kind of search in the far north.",
    "In the Arctic, I went looking for fossils—an encounter with a much older world during a journey to the far north.",
    null
  ],
  [
    "Down a volcano.",
    "Volcano boarding.",
    "I went volcano boarding, riding down the slope of a volcano. Alongside two climbs on an active volcano, it became one of the more unusual experiences in my travel record.",
    null
  ],
  [
    "Three islands in the Galápagos.",
    "San Cristóbal, Santa Cruz and Isabela.",
    "I travelled between San Cristóbal, Santa Cruz and Isabela by boat. Among the memories of that journey is an unexpected encounter: stepping on a shark while my feet were bleeding.",
    2022
  ],
  [
    "A week with sight in one eye.",
    "An unexpected week in South America.",
    "For a week while travelling in South America, I could see out of only one eye. It became one of the most difficult episodes in my travel record.",
    null
  ],
  [
    "445 days on the road.",
    "A graduation-era snapshot.",
    "By the time of my graduation post, I had counted 445 days on the road, more than 80 countries and more than 200 cities—and still graduated. These figures preserve that moment; the totals at the top of this page reflect the current archive.",
    null
  ]
];$('#stories').innerHTML=stories.map((s,i)=>`<details class="story"><summary><span class="num">${String(i+1).padStart(2,'0')}</span><div><h3>${s[0]}</h3><p>${s[1]}</p></div><span class="plus">+</span></summary><div class="storybody"><p>${s[2]}</p>${s[3]?`<button data-story-year="${s[3]}">Explore ${s[3]} in the atlas ↗</button>`:''}</div></details>`).join('');document.querySelectorAll('[data-story-year]').forEach(b=>b.onclick=()=>{if(+b.dataset.storyYear===2026)focusSiberianRail();else{select(+b.dataset.storyYear);$('#atlas').scrollIntoView({behavior:'smooth'})}});renderTimeline();render();

// Stats that can be derived safely when the travel sheet is updated.
document.getElementById("travelCountriesTotal").textContent = D.countries.filter(x=>x.count_in_195).length;
document.getElementById("travelFlightsTotal").textContent = D.flights.filter(x=>x.count_status==="recorded_flown").length;
document.getElementById("travelNightsTotal").textContent = D.airport_overnights.length;
document.getElementById('koreaPlaceCount').textContent = `${D.domestic_places.length} places · undated`;
document.getElementById('countryBasisText').textContent = `${D.countries.filter(x => x.count_in_195).length} countries visited, including Taiwan · ${D.countries.filter(x => !x.count_in_195 && x.category === 'region_or_territory' && !['GB','MD'].includes(x.iso2)).length} additional overseas territories tracked separately`;
