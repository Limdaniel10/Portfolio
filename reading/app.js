"use strict";
// Keep the established Reading Archive UI. Only data loading changed:
// book counts/list come from books.json; all page figures come from monthly-pages.json.
const $ = selector => document.querySelector(selector);
const fmt = n => Number(n).toLocaleString("en-US");
const MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
const bookUnit = n => n === 1 ? "book" : "books";
const NOTION_BY_YEAR = Object.freeze({
  "2020": "https://app.notion.com/p/130f8fb4581b80a1b86aeb048ddd2278",
  "2021": "https://app.notion.com/p/130f8fb4581b8026879cfe2ab98e48b8",
  "2022": "https://app.notion.com/p/130f8fb4581b803fb6a0e040d5fceacc",
  "2023": "https://app.notion.com/p/130f8fb4581b80a8816eee87307607c4",
  "2024": "https://app.notion.com/p/130f8fb4581b809e85c4e345f95dbba6",
  "2025": "https://app.notion.com/p/17ef8fb4581b80a2a968eee1550764b7"
});
let years = [];
let bookLookup = new Map();
let activeYear, activeMonth, showAllBooks = false, chartMetric = "books";

function groupArchive(books, monthlyPages) {
  if (!Array.isArray(books) || !Array.isArray(monthlyPages)) {
    throw new Error("Invalid JSON schema: expected book and monthly-pages arrays.");
  }
  const pageMap = new Map();
  const yearSet = new Set();
  for (const record of monthlyPages) {
    const year = Number(record.year), month = Number(record.month), pages = Number(record.pages_read);
    if (!Number.isInteger(year) || !Number.isInteger(month) || month < 1 || month > 12 || !Number.isInteger(pages) || pages < 0) {
      throw new Error("Invalid monthly page record.");
    }
    const key = `${year}-${month}`;
    if (pageMap.has(key)) throw new Error(`Duplicate month: ${key}`);
    pageMap.set(key, pages);
    yearSet.add(year);
  }
  bookLookup = new Map();
  const seenIds = new Set();
  for (const book of books) {
    const year = Number(book.year), month = Number(book.month);
    if (!book.id || seenIds.has(book.id) || !book.title || !book.author || !Number.isInteger(year) || !Number.isInteger(month) || month < 1 || month > 12 || book.status !== "Completed") {
      throw new Error("Invalid or duplicate completed-book record.");
    }
    seenIds.add(book.id);
    yearSet.add(year);
    const key = `${year}-${month}`;
    if (!bookLookup.has(key)) bookLookup.set(key, []);
    bookLookup.get(key).push(book);
  }
  for (const entries of bookLookup.values()) entries.sort((a, b) => Number(a.month_order) - Number(b.month_order) || a.id.localeCompare(b.id));
  return [...yearSet].sort((a, b) => a - b).map(year => {
    const months = MONTHS.map((_, i) => {
      const month = i + 1;
      const count = (bookLookup.get(`${year}-${month}`) || []).length;
      return { month, books: count, pages: pageMap.get(`${year}-${month}`) ?? 0 };
    });
    return { year, books: months.reduce((a, m) => a + m.books, 0), pages: months.reduce((a, m) => a + m.pages, 0), months, notion: NOTION_BY_YEAR[String(year)] };
  });
}

function drawBars() {
  const max = Math.max(1, ...years.map(y => y[chartMetric]));
  $("#bars").replaceChildren(...years.map(y => {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "barrow" + (y.year === activeYear ? " active" : "");
    btn.setAttribute("aria-pressed", String(y.year === activeYear));
    btn.setAttribute("aria-label", `${y.year}: ${y.books} ${bookUnit(y.books)}, ${fmt(y.pages)} pages recorded`);
    const label = document.createElement("span"); label.className = "yearlabel"; label.textContent = y.year;
    const track = document.createElement("span"); track.className = "track";
    const fill = document.createElement("span"); fill.className = "fill";
    fill.style.width = (100 * y[chartMetric] / max) + "%";
    track.append(fill);
    const qty = document.createElement("span"); qty.className = "qty"; qty.textContent = fmt(y[chartMetric]);
    btn.append(label, track, qty);
    btn.onclick = () => {
      activeYear = y.year;
      activeMonth = y.months.find(m => m.books > 0)?.month || 1;
      showAllBooks = false;
      draw();
    };
    return btn;
  }));
}

function draw() {
  drawBars();
  const y = years.find(x => x.year === activeYear);
  $("#selectedYear").textContent = String(y.year);
  $("#selectedBooks").textContent = fmt(y.books) + " " + bookUnit(y.books);
  $("#selectedPages").textContent = fmt(y.pages) + " pages";
  $("#monthgrid").replaceChildren(...y.months.map(m => {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "month" + (m.month === activeMonth ? " active" : "");
    btn.setAttribute("aria-pressed", String(m.month === activeMonth));
    const heading = document.createElement("small"); heading.textContent = MONTHS[m.month - 1].slice(0, 3);
    const count = document.createElement("b"); count.textContent = fmt(m.books) + " " + bookUnit(m.books);
    const pages = document.createElement("em"); pages.className="month-pages"; pages.textContent=fmt(m.pages)+" pages"; btn.append(heading, count, pages);
    btn.onclick = () => { activeMonth = m.month; showAllBooks = false; drawMonth(); };
    return btn;
  }));
  drawMonth();
  $("#notionlink").replaceChildren();
  if (y.notion) {
    const link = document.createElement("a");
    link.href = y.notion;
    link.target = "_blank";
    link.rel = "noopener noreferrer";
    link.textContent = `View ${y.year} reading notes on Notion`;
    $("#notionlink").append(link);
  }
}

function renderBooks(target, books) {
  target.replaceChildren(...books.map((b, i) => {
    const item = document.createElement("li"); item.className = "bookitem";
    const number = document.createElement("span"); number.className = "bookindex"; number.textContent = String(i + 1).padStart(2, "0");
    const info = document.createElement("span"); info.className = "bookinfo";
    const title = document.createElement("span"); title.className = "booktitle"; title.textContent = b.title;
    const author = document.createElement("span"); author.className = "bookauthor"; author.textContent = b.author;
    info.append(title, author); item.append(number, info);
    return item;
  }));
}

function drawBookList() {
  const completed = bookLookup.get(`${activeYear}-${activeMonth}`) || [];
  const hasMore = completed.length > 12;
  const visible = hasMore && !showAllBooks ? completed.slice(0, 12) : completed;
  $("#booksHeading").textContent = `${MONTHS[activeMonth - 1]} ${activeYear} · Books read`;
  $("#bookCount").textContent = `${fmt(completed.length)} ${bookUnit(completed.length)} · Titles and authors`;
  renderBooks($("#booklist"), visible);
  $("#bookempty").hidden = completed.length > 0;
  $("#bookempty").textContent = "No books recorded for this month.";
  const more = $("#showmore");
  more.hidden = !hasMore;
  more.textContent = showAllBooks ? "Show fewer" : `Show all ${fmt(completed.length)} books`;
}

function drawMonth() {
  const y = years.find(x => x.year === activeYear);
  const m = y.months.find(x => x.month === activeMonth);
  document.querySelectorAll(".month").forEach((el, i) => {
    el.classList.toggle("active", i + 1 === activeMonth);
    el.setAttribute("aria-pressed", String(i + 1 === activeMonth));
  });
  const detail = $("#monthdetail");
  const heading = document.createElement("strong"); heading.textContent = `${MONTHS[activeMonth - 1]} ${activeYear}`;
  const line = document.createElement("div");
  const value = document.createElement("span");
  value.textContent = `${fmt(m.books)} ${bookUnit(m.books)} · ${fmt(m.pages)} pages recorded`;
  line.append(value);
  detail.replaceChildren(heading, line);
  drawBookList();
}

$("#showmore").onclick = () => { showAllBooks = !showAllBooks; drawBookList(); };
for (const metric of ["books","pages"]) { const button = $(metric === "books" ? "#metricBooks" : "#metricPages"); button.onclick=()=> {chartMetric=metric; $("#metricBooks").classList.toggle("active",metric==="books");$("#metricPages").classList.toggle("active",metric==="pages");$("#metricBooks").setAttribute("aria-pressed",String(metric==="books"));$("#metricPages").setAttribute("aria-pressed",String(metric==="pages"));drawBars();}; }

async function initialize() {
  try {
    const [bookRes, pageRes] = await Promise.all([
      fetch("./data/books.json", { cache: "no-cache" }),
      fetch("./data/monthly-pages.json", { cache: "no-cache" })
    ]);
    if (!bookRes.ok || !pageRes.ok) throw new Error(`Data unavailable (books: ${bookRes.status}, pages: ${pageRes.status}).`);
    const [bookData, pageData] = await Promise.all([bookRes.json(), pageRes.json()]);
    years = groupArchive(bookData.books, pageData.months);
    if (!years.length) throw new Error("No reading years found.");
    const totalBooks = years.reduce((n, y) => n + y.books, 0);
    const totalPages = years.reduce((n, y) => n + y.pages, 0);
    $("#totBooks").textContent = fmt(totalBooks);
    $("#totPages").textContent = fmt(totalPages);
    activeYear = years[years.length - 1].year;
    const recentMonths = years[years.length - 1].months.filter(m => m.books > 0);
    activeMonth = recentMonths.length ? recentMonths[recentMonths.length - 1].month : 1;
    $("#archiveStatus").hidden = true;
    draw();
  } catch (error) {
    console.error("Reading Archive could not load:", error);
    $("#archiveStatus").textContent = "Reading records are temporarily unavailable. Please refresh the page or try again later.";
    $("#archiveStatus").hidden = false;
  }
}
initialize();


/* Reading > Notion Highlights: dates come from Books, never from Notion pages. */
async function initializeHighlights(){
 const root=document.getElementById("highlightArchive"), search=document.getElementById("highlightSearch");
 const filter=document.getElementById("highlightSource"), count=document.getElementById("highlightCount");
 const total=document.getElementById("highlightTotal"), linked=document.getElementById("highlightLinked");
 const empty=document.getElementById("highlightEmpty");
 if(!root||!search||!filter||!count||!total||!linked||!empty)return;
 const el=(tag,cls,txt)=>{const e=document.createElement(tag);if(cls)e.className=cls;if(txt!==undefined)e.textContent=txt;return e;};
 const norm=s=>String(s||"").normalize("NFKC").toLocaleLowerCase().replace(/[\s\p{P}\p{S}]/gu,"");
 try{
  const [r1,r2]=await Promise.all([fetch("./data/highlights.json",{cache:"no-cache"}),fetch("./data/books.json",{cache:"no-cache"})]);
  if(!r1.ok||!r2.ok)throw Error("Highlight or book records unavailable");
  const [data,ledger]=await Promise.all([r1.json(),r2.json()]);
  if(!Array.isArray(data.entries)||!Array.isArray(ledger.books))throw Error("Invalid highlight data");
  const byID=new Map(),byTitle=new Map();
  for(const b of ledger.books){
   byID.set(b.id,b);
   const key=norm(b.title);
   if(!byTitle.has(key))byTitle.set(key,[]);
   byTitle.get(key).push(b);
  }
  const notes=data.entries.map(n=>{
   let b=n.book_id?byID.get(n.book_id):null;
   if(b&&norm(b.title)!==norm(n.title))b=null;
   if(!b){
    const candidates=byTitle.get(norm(n.title))||[];
    if(candidates.length===1&&norm(candidates[0].author)===norm(n.author))b=candidates[0];
   }
   if(b&&!Number.isInteger(Number(b.month)))b=null;
   return {...n,book:b||null,year:b?Number(b.year):null,month:b?Number(b.month):null};
  });
  total.textContent=fmt(notes.length);
  linked.textContent=fmt(notes.filter(n=>n.book).length);
  function noteCard(note,show){
   const card=el("details","highlight-book");card.open=show;
   const title=el("summary","highlight-book-heading");
   const left=el("span","highlight-book-left");
   left.append(el("strong","highlight-book-title",note.title),
               el("span","highlight-book-author",note.author||""),
               el("span","highlight-book-preview",note.preview||""));
   title.append(left,el("span","highlight-book-source","HIGHLIGHT "+note.source+" · "+String(note.ordinal).padStart(2,"0")));
   card.append(title);
   const body=el("div","highlight-book-content");
   const paragraphs=String(note.text||"").split(/\n{2,}/).map(s=>s.trim()).filter(Boolean);
   if(paragraphs.length){
    paragraphs.forEach((p,i)=>body.append(el("p",i===0?"highlight-first-passage":"highlight-passage",p)));
   }else{
    body.append(el("p","highlight-missing-passage","This Notion entry has no text passage. Open the source notebook for more context."));
   }
   const links=el("div","highlight-book-actions");
   if(note.notion_url.startsWith("https://app.notion.com/")){
    const a=el("a","highlight-original-link","View original on Notion ↗");
    a.href=note.notion_url;a.target="_blank";a.rel="noopener noreferrer";links.append(a);
   }
   if(note.book){
    const btn=el("button","highlight-find-book","Find completed month ↗");
    btn.type="button";
    btn.addEventListener("click",()=>{
      if(!years.some(y=>y.year===note.year))return;
      activeYear=note.year;activeMonth=note.month;showAllBooks=false;
      draw();
      document.getElementById("reading-years")?.scrollIntoView({behavior:"smooth",block:"start"});
    });
    links.append(btn);
   }
   body.append(links);card.append(body);return card;
  }
  function group(cls,label,arr,open){
   const d=el("details",cls);d.open=open;
   const header=el("summary","highlight-group-heading");
   header.append(el("strong","highlight-group-name",label),
                 el("span","highlight-group-count",fmt(arr.length)+" "+(arr.length===1?"highlight":"highlights")),
                 el("span","highlight-group-plus","+"));
   d.append(header);return d;
  }
  function render(){
   const q=search.value.trim().toLocaleLowerCase(),src=filter.value;
   const selection=notes.filter(n=>(src==="all"||n.source===src)&&(!q||[n.title,n.author,n.preview,n.text].join(" ").toLocaleLowerCase().includes(q)));
   const byYear=new Map(),orphan=new Map();
   for(const n of selection){
    if(n.book){
     if(!byYear.has(n.year))byYear.set(n.year,new Map());
     const months=byYear.get(n.year);
     if(!months.has(n.month))months.set(n.month,[]);
     months.get(n.month).push(n);
    }else{
     if(!orphan.has(n.source))orphan.set(n.source,[]);
     orphan.get(n.source).push(n);
    }
   }
   const frag=document.createDocumentFragment();
   const yKeys=[...byYear.keys()].sort((a,b)=>b-a);
   yKeys.forEach((y,yi)=>{
    const months=byYear.get(y),all=[...months.values()].flat();
    const year=group("highlight-year",String(y),all,!!q||yi===0);
    const content=el("div","highlight-year-body");
    [...months.keys()].sort((a,b)=>b-a).forEach((m,mi)=>{
     const arr=months.get(m).slice().sort((a,b)=>Number(a.book.month_order||0)-Number(b.book.month_order||0)||a.title.localeCompare(b.title,"ko"));
     const month=group("highlight-month",MONTHS[m-1]+" "+y,arr,!!q||(yi===0&&mi===0));
     const list=el("div","highlight-book-list");
     arr.forEach(n=>list.append(noteCard(n,!!q)));
     month.append(list);content.append(month);
    });
    year.append(content);frag.append(year);
   });
   if(orphan.size){
    const all=[...orphan.values()].flat();
    const other=group("highlight-year","Completion date not linked",all,!!q||!yKeys.length);
    const content=el("div","highlight-year-body");
    content.append(el("p","highlight-unlinked-caption","These original passages have no unambiguous matching book or reread in the ledger. No date has been assigned."));
    ["I","II","III","IV"].filter(s=>orphan.has(s)).forEach(s=>{
      const arr=orphan.get(s).slice().sort((a,b)=>a.ordinal-b.ordinal);
      const sourceGroup=group("highlight-month","Highlight "+s,arr,!!q||!yKeys.length);
      const list=el("div","highlight-book-list");
      arr.forEach(n=>list.append(noteCard(n,!!q)));
      sourceGroup.append(list);content.append(sourceGroup);
    });
    other.append(content);frag.append(other);
   }
   root.replaceChildren(frag);
   count.textContent=fmt(selection.length)+" of "+fmt(notes.length)+" collected highlights";
   empty.hidden=selection.length!==0;
  }
  search.addEventListener("input",render);
  filter.addEventListener("change",render);
  render();
 }catch(e){
  console.error("Reading Notion Highlights unavailable",e);
  root.replaceChildren(el("p","highlight-error","Notion highlights are temporarily unavailable."));
  count.textContent="Archive unavailable";
 }
}
initializeHighlights();
