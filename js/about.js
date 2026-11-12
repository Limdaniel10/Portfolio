"use strict";
fetch("../data/countries.json",{cache:"no-cache"}).then(r=>{if(!r.ok)throw Error("No statistics");return r.json()}).then(d=>{
const vals={aboutCountries:d.totalCountries,aboutBooks:d.totalBooks,aboutNights:d.airportNights};
for(const [id,value] of Object.entries(vals)){const e=document.getElementById(id);if(e&&Number.isFinite(Number(value)))e.textContent=Number(value).toLocaleString("en-US")}
}).catch(()=>{/* Use documented fallback values if offline. */});
