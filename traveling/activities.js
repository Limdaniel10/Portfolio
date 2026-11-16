"use strict";
/* Static travel activity archive; update activities.json when new records are verified. */
(() => {
  const esc = value => String(value ?? "").replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
  const monthNames = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"];
  const formatDate = raw => {
    const match=String(raw||"").match(/^(\d{4})-(\d{2})(?:-(\d{2}))?$/);
    if(!match)return "Date not recorded";
    const m=Number(match[2]), day=match[3];
    return (day ? monthNames[m-1]+" "+Number(day)+", " : monthNames[m-1]+" ")+match[1];
  };
  const table = (headers, body) => '<div class="activity-table-wrap"><table class="activity-table"><thead><tr>'+
    headers.map(h=>'<th scope="col">'+esc(h)+'</th>').join("")+
    '</tr></thead><tbody>'+body+'</tbody></table></div>';
  const desc = text => '<p class="activity-pending">'+esc(text)+'</p>';
  fetch("./activities.json",{cache:"no-cache"}).then(r=>{
    if(!r.ok)throw Error("Activity archive unavailable");
    return r.json();
  }).then(data=>{
    const hikes=Array.isArray(data.trekking)?data.trekking:[];
    const dives=Array.isArray(data.scuba)?data.scuba:[];
    const surfs=Array.isArray(data.surfing)?data.surfing:[];
    document.getElementById("trekCount").textContent=hikes.length+" hikes";
    document.getElementById("scubaCount").textContent=dives.length?dives.length+" dives":"Dive logs pending";
    document.getElementById("surfCount").textContent=surfs.length+" sessions";
    const sortedHikes=[...hikes].sort((a,b)=>String(a.date).localeCompare(String(b.date)));
    document.getElementById("trekkingRecords").innerHTML=sortedHikes.length?table(
      ["Mountain / trail","Country","Date","Reached","Elevation"],
      sortedHikes.map(x=>{
        const recorded=Number.isFinite(x.elevationM);
        const elev=recorded ? Number(x.elevationM).toLocaleString("en-US")+" m" : "—";
        const basis=recorded ? (x.elevationBasis==="personal record"?"Personal record":"Summit reference") : "";
        return '<tr><td>'+esc(x.name)+'</td><td class="activity-nowrap">'+esc(x.country)+'</td>'+
          '<td class="activity-nowrap">'+esc(formatDate(x.date))+'</td><td>'+esc(x.reached||"Not recorded")+'</td>'+
          '<td class="activity-elev">'+esc(elev)+(basis?'<small>'+esc(basis)+'</small>':'')+'</td></tr>';
      }).join(""))
      :desc("No trekking records have been added.");
    document.getElementById("scubaRecords").innerHTML=dives.length?table(
      ["Date","Dive site","Country","Max depth","Duration"],
      [...dives].sort((a,b)=>String(a.date).localeCompare(String(b.date))).map(x=>
        '<tr><td class="activity-nowrap">'+esc(formatDate(x.date))+'</td><td>'+esc(x.site||"Not recorded")+'</td>'+
        '<td>'+esc(x.country||"—")+'</td><td class="activity-nowrap">'+
        (Number.isFinite(x.depthM)?esc(x.depthM)+" m":"—")+'</td><td class="activity-nowrap">'+
        (Number.isFinite(x.durationMin)?esc(x.durationMin)+" min":"—")+'</td></tr>'
      ).join(""))
      :desc("Dive-log details are pending. Once the log is provided, each dive will be listed by date, site, maximum depth and duration. No dive metrics have been invented.");
    document.getElementById("surfingRecords").innerHTML=surfs.length?table(
      ["Location","Country","Month"],
      [...surfs].sort((a,b)=>String(a.date).localeCompare(String(b.date))).map(x=>
        '<tr><td>'+esc(x.place)+'</td><td>'+esc(x.country)+'</td><td class="activity-nowrap">'+esc(formatDate(x.date))+'</td></tr>'
      ).join(""))
      :desc("No surfing records have been added.");
  }).catch(()=>{
    ["trekkingRecords","scubaRecords","surfingRecords"].forEach(id=>{
      document.getElementById(id).innerHTML=desc("This archive is temporarily unavailable.");
    });
  });
})();
